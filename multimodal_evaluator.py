"""
multimodal_evaluator.py
-----------------------
Evaluation harness for the multimodal (text + image) RAG pipeline.

All reported metric values are derived entirely from live pipeline results.
No hardcoded scores, accuracy labels, or counts appear in any comparison
table.  Every number in the output comes from a MultimodalQueryResult field
that was populated by running the actual RAGPipeline.run() call.

Supported query types
---------------------
  text_only   - plain text query, no image supplied;
                tests whether the CLIP text encoder enriches retrieval.
  image_only  - raw image bytes supplied, minimal text query;
                tests whether CLIP image vectors retrieve relevant context.
  text+image  - both text and image provided;
                tests the full multimodal fusion path.

Usage
-----
  # List available embedding models:
  python multimodal_evaluator.py --list-embeddings

  # Single run (default model + default embedding):
  python multimodal_evaluator.py --mode single

  # Compare all models on multimodal queries:
  python multimodal_evaluator.py --mode model_comparison

  # Full matrix (all models x all embeddings):
  python multimodal_evaluator.py --mode full_matrix

  # Point at a directory of PNG/JPEG images for image queries:
  python multimodal_evaluator.py --mode single --image-dir ./test_images

  # Override output file:
  python multimodal_evaluator.py --mode single --output my_mm_results.txt

Results are appended to multimodal_results.txt (one section per run).
"""

from __future__ import annotations

import argparse
import io
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from research_config import (
    MODELS_TO_EVALUATE,
    RETRIEVAL_MODES,
    MULTIMODAL_RESULTS_FILE,
    EMBEDDING_MODELS,
    DEFAULT_EMBEDDING,
    get_model_config,
)
from retriever import build_vector_store
from rag_pipeline import RAGPipeline
from context_memory import ConversationMemory
from topic_memory_manager import TopicMemoryManager


# ---------------------------------------------------------------------------
# Optional multimodal dependencies
# ---------------------------------------------------------------------------

_MM_AVAILABLE = False
_load_or_build_image_index = None  # set below when available

try:
    from multimodal_processor import (  # type: ignore[import]
        load_or_build_image_index as _load_fn,
        multimodal_available,
    )
    _MM_AVAILABLE = multimodal_available()
    _load_or_build_image_index = _load_fn
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Multimodal test-query corpus
#
# Each entry is a dict with:
#   id                  - unique string identifier
#   category            - query category (used for per-category breakdowns)
#   query_type          - "text_only" | "image_only" | "text+image"
#   query               - text of the question
#   expected_topic      - topic the pipeline should detect (None = no topic)
#   expected_mode       - "RAG" | "Partial RAG" | "LLM Fallback"
#   expected_keywords   - keywords that should appear in a correct answer
#   image_label         - label used to pick a test image from --image-dir,
#                         or to generate a synthetic one (None = no image)
#   conversation_reset  - True to start a fresh memory context before this
#   note                - optional annotation string
# ---------------------------------------------------------------------------

MM_TEST_QUERIES: list[dict] = [
    # TEXT-ONLY (exercises CLIP text-encoder path)
    {
        "id": "MT01", "category": "text_only", "query_type": "text_only",
        "query": "explain the water cycle",
        "expected_topic": "water cycle", "expected_mode": "RAG",
        "expected_keywords": ["evaporation", "condensation", "precipitation"],
        "image_label": None, "conversation_reset": True,
    },
    {
        "id": "MT02", "category": "text_only", "query_type": "text_only",
        "query": "how does photosynthesis produce glucose",
        "expected_topic": "photosynthesis", "expected_mode": "RAG",
        "expected_keywords": ["chlorophyll", "glucose", "sunlight"],
        "image_label": None, "conversation_reset": True,
    },
    {
        "id": "MT03", "category": "text_only", "query_type": "text_only",
        "query": "describe the nitrogen cycle stages",
        "expected_topic": "nitrogen cycle", "expected_mode": "RAG",
        "expected_keywords": ["nitrification", "fixation", "bacteria"],
        "image_label": None, "conversation_reset": True,
    },
    {
        "id": "MT04", "category": "text_only", "query_type": "text_only",
        "query": "what are newtons laws of motion",
        "expected_topic": "newton's laws", "expected_mode": "RAG",
        "expected_keywords": ["force", "mass", "acceleration"],
        "image_label": None, "conversation_reset": True,
    },
    {
        "id": "MT05", "category": "text_only", "query_type": "text_only",
        "query": "explain atomic structure",
        "expected_topic": "atomic structure", "expected_mode": "RAG",
        "expected_keywords": ["proton", "electron", "neutron"],
        "image_label": None, "conversation_reset": True,
    },
    {
        "id": "MT06", "category": "text_only", "query_type": "text_only",
        "query": "what is chemical bonding",
        "expected_topic": "chemical bonding", "expected_mode": "RAG",
        "expected_keywords": ["ionic", "covalent", "electron"],
        "image_label": None, "conversation_reset": True,
    },

    # IMAGE-ONLY (exercises CLIP image-encoder path)
    {
        "id": "MI01", "category": "image_only", "query_type": "image_only",
        "query": "what does this diagram show",
        "expected_topic": None, "expected_mode": "RAG",
        "expected_keywords": [],
        "image_label": "diagram", "conversation_reset": True,
        "note": "Generic diagram - any retrieved context is acceptable",
    },
    {
        "id": "MI02", "category": "image_only", "query_type": "image_only",
        "query": "explain this scientific image",
        "expected_topic": None, "expected_mode": "RAG",
        "expected_keywords": [],
        "image_label": "science", "conversation_reset": True,
    },
    {
        "id": "MI03", "category": "image_only", "query_type": "image_only",
        "query": "describe what is illustrated here",
        "expected_topic": None, "expected_mode": "RAG",
        "expected_keywords": [],
        "image_label": "biology", "conversation_reset": True,
    },

    # TEXT + IMAGE (exercises full multimodal fusion path)
    {
        "id": "MM01", "category": "text_image", "query_type": "text+image",
        "query": "explain what is shown in this diagram of the water cycle",
        "expected_topic": "water cycle", "expected_mode": "RAG",
        "expected_keywords": ["evaporation", "condensation"],
        "image_label": "water_cycle", "conversation_reset": True,
    },
    {
        "id": "MM02", "category": "text_image", "query_type": "text+image",
        "query": "describe the process illustrated in this biology diagram",
        "expected_topic": "photosynthesis", "expected_mode": "RAG",
        "expected_keywords": ["chlorophyll", "glucose"],
        "image_label": "photosynthesis", "conversation_reset": True,
    },
    {
        "id": "MM03", "category": "text_image", "query_type": "text+image",
        "query": "what scientific concept does this figure represent",
        "expected_topic": None, "expected_mode": "RAG",
        "expected_keywords": [],
        "image_label": "generic_science", "conversation_reset": True,
        "note": "No specific topic expected - tests fusion retrieval quality",
    },
    {
        "id": "MM04", "category": "text_image", "query_type": "text+image",
        "query": "explain the forces shown in this physics diagram",
        "expected_topic": "newton's laws", "expected_mode": "RAG",
        "expected_keywords": ["force", "mass"],
        "image_label": "physics", "conversation_reset": True,
    },

    # FOLLOWUP AFTER MULTIMODAL
    {
        "id": "MF01", "category": "mm_followup", "query_type": "text_only",
        "query": "give more details about that",
        "expected_topic": "water cycle", "expected_mode": "RAG",
        "expected_keywords": ["evaporation", "water"],
        "image_label": None, "conversation_reset": False,
        "depends_on": "MM01",
        "note": "Followup after text+image query - tests memory context",
    },
    {
        "id": "MF02", "category": "mm_followup", "query_type": "text_only",
        "query": "what are its main stages",
        "expected_topic": "water cycle", "expected_mode": "RAG",
        "expected_keywords": ["condensation", "precipitation"],
        "image_label": None, "conversation_reset": False,
        "depends_on": "MM01",
    },

    # OUT-OF-SCOPE
    {
        "id": "MO01", "category": "mm_out_of_scope", "query_type": "text_only",
        "query": "describe a stock market candlestick chart",
        "expected_topic": None, "expected_mode": "LLM Fallback",
        "expected_keywords": [],
        "image_label": None, "conversation_reset": True,
        "note": "Out-of-scope text query - validates fallback path",
    },
    {
        "id": "MO02", "category": "mm_out_of_scope", "query_type": "image_only",
        "query": "what is in this picture",
        "expected_topic": None, "expected_mode": "RAG",
        "expected_keywords": [],
        "image_label": "random", "conversation_reset": True,
        "note": "Image with no domain overlap - tests graceful degradation",
    },

    # VAGUE / EDGE-CASE
    {
        "id": "MV01", "category": "mm_vague", "query_type": "text_only",
        "query": "   ",
        "expected_topic": None, "expected_mode": "LLM Fallback",
        "expected_keywords": [],
        "image_label": None, "conversation_reset": True,
        "note": "Whitespace-only query - EMPTY QUERY error path",
    },
]


# ---------------------------------------------------------------------------
# Synthetic image helper
# ---------------------------------------------------------------------------

def _make_synthetic_image(width: int = 224, height: int = 224) -> bytes:
    """Return minimal valid PNG bytes (224x224 grey square when Pillow is
    available; a spec-compliant 1x1 white PNG otherwise).

    The image has no semantic content.  Its sole purpose is to exercise the
    CLIP image-encoder code path when no real test images are provided.
    """
    try:
        from PIL import Image as _PILImage  # type: ignore[import]
        img = _PILImage.new("RGB", (width, height), color=(220, 220, 220))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    except ImportError:
        # Minimal spec-compliant 1x1 white PNG (no external dependencies)
        return (
            b"\x89PNG\r\n\x1a\n"
            b"\x00\x00\x00\rIHDR"
            b"\x00\x00\x00\x01\x00\x00\x00\x01"
            b"\x08\x02\x00\x00\x00"
            b"\x90wS\xde"
            b"\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00"
            b"\x00\x01\x01\x00\x05\x18\xd8N"
            b"\x00\x00\x00\x00IEND\xaeB`\x82"
        )


def _load_image_bytes(
    image_dir: Optional[str],
    label: Optional[str],
) -> Optional[bytes]:
    """Return raw image bytes for the given label.

    Resolution order:
      1. If image_dir is provided, scan for a file whose stem contains label
         (case-insensitive) with a common image extension.  Return first match.
      2. If no file matches (or image_dir is None), generate a synthetic image.
      3. If label is None, return None (text-only query path).

    Args:
        image_dir: Directory to search for real image files, or None.
        label:     Descriptive label for the desired image (e.g. "water_cycle").

    Returns:
        Raw image bytes, or None when no image is needed.
    """
    if label is None:
        return None

    if image_dir:
        search_root = Path(image_dir)
        for pattern in ("*.png", "*.jpg", "*.jpeg", "*.PNG", "*.JPG", "*.JPEG"):
            for path in search_root.glob(pattern):
                if label.lower() in path.stem.lower():
                    return path.read_bytes()

    # No file found - return a synthetic image so the CLIP path is still tested
    return _make_synthetic_image()


# ---------------------------------------------------------------------------
# MultimodalQueryResult dataclass
# ---------------------------------------------------------------------------

@dataclass
class MultimodalQueryResult:
    """Result of running the pipeline on one multimodal test query.

    Every numeric field is populated directly from the live pipeline response
    or derived arithmetically from those values.  There are no hardcoded
    initialisation values that could appear in summary tables.
    """

    # Query identity
    query_id: str
    category: str
    query_type: str         # "text_only" | "image_only" | "text+image"
    query: str
    model: str
    retrieval_mode: str
    embedding_name: str

    # Correctness signals
    expected_topic: Optional[str]
    actual_topic: Optional[str]
    topic_correct: bool
    expected_mode: str
    actual_mode: str
    mode_correct: bool

    # Answer quality
    answer: str
    answer_length: int
    keyword_hits: int
    keyword_total: int
    keyword_coverage: float     # hits / total; 1.0 when total == 0

    # Latency and tokens - all from live pipeline result
    latency_ms: float
    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost_usd: float

    # Multimodal fields - all from live pipeline result
    image_supplied: bool          # True when image bytes were passed in
    has_image_context: bool       # result.has_image_context from PipelineResult
    image_captions_found: int     # len(result.image_captions)
    image_caption_text: str       # " | ".join(result.image_captions)

    note: str = ""
    error: str = ""


# ---------------------------------------------------------------------------
# MultimodalResearchEvaluator
# ---------------------------------------------------------------------------

class MultimodalResearchEvaluator:
    """Orchestrates one (model, retrieval_mode, embedding_name) experiment
    using MM_TEST_QUERIES, including image-augmented queries.

    If the multimodal stack (CLIP / FAISS / Pillow) is available and an image
    index exists on disk, it is loaded and passed to the pipeline.  Otherwise
    the pipeline runs in text-only mode for every query.
    """

    def __init__(
        self,
        model: str,
        retrieval_mode: str,
        embedding_name: str = DEFAULT_EMBEDDING,
        image_dir: Optional[str] = None,
        index_path: str = "image_index.faiss",
        meta_path: str = "image_meta.json",
    ) -> None:
        # Build text vector store for this embedding
        vector_store = build_vector_store(embedding_name=embedding_name)

        # Try to load the persisted FAISS image index
        image_index = None
        if _MM_AVAILABLE and _load_or_build_image_index is not None:
            try:
                image_index = _load_or_build_image_index(
                    pdf_paths=None,
                    index_path=index_path,
                    meta_path=meta_path,
                )
                if image_index is not None:
                    print(f"  [MM] Image index loaded ({image_index.count} image(s))")
                else:
                    print("  [MM] No image index on disk; image retrieval disabled.")
            except Exception as exc:
                print(f"  [MM] Could not load image index: {exc}")

        self.pipeline = RAGPipeline(
            vector_store,
            model_name=model,
            retrieval_mode=retrieval_mode,
            image_index=image_index,
        )
        self.model = model
        self.retrieval_mode = retrieval_mode
        self.embedding_name = embedding_name
        self.image_dir = image_dir
        self.results: list[MultimodalQueryResult] = []

    # -- Static helpers -------------------------------------------------------

    @staticmethod
    def _check_keywords(answer: str, keywords: list[str]) -> tuple[int, int, float]:
        """Case-insensitive keyword coverage check."""
        if not keywords:
            return 0, 0, 1.0
        if not answer:
            return 0, len(keywords), 0.0
        lower = answer.lower()
        hits = sum(1 for kw in keywords if kw.lower() in lower)
        return hits, len(keywords), hits / len(keywords)

    @staticmethod
    def _is_model_available(model_name: str) -> bool:
        """Return True if model_name is reachable (API key present or Ollama)."""
        cfg = get_model_config(model_name) or {}
        provider = cfg.get("provider", "ollama")
        env_map = {
            "groq":      "GROQ_API_KEY",
            "openai":    "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "google":    "GOOGLE_API_KEY",
        }
        if provider in env_map:
            return bool(os.environ.get(env_map[provider], ""))
        # Ollama - check `ollama list`
        try:
            proc = subprocess.run(
                ["ollama", "list"], capture_output=True, text=True, timeout=10
            )
            return model_name in proc.stdout
        except Exception:
            return False

    # -- Single query runner --------------------------------------------------

    def run_single_query(
        self,
        query_config: dict,
        memory: ConversationMemory,
        topic_manager: TopicMemoryManager,
    ) -> MultimodalQueryResult:
        """Run the pipeline for one MM_TEST_QUERIES entry and return a result.

        Image bytes are resolved via _load_image_bytes() - from disk when
        --image-dir is provided, otherwise as a synthetic PNG.  Every metric
        value in the returned object is computed from the live pipeline response.
        """
        qid = query_config["id"]
        category = query_config["category"]
        query_type = query_config["query_type"]
        query = query_config["query"]
        expected_topic: Optional[str] = query_config.get("expected_topic")
        expected_mode: str = query_config.get("expected_mode", "RAG")
        expected_keywords: list[str] = query_config.get("expected_keywords", [])
        image_label: Optional[str] = query_config.get("image_label")
        note: str = query_config.get("note", "")

        # Resolve image bytes based on declared query_type
        image_bytes: Optional[bytes] = None
        if query_type in ("image_only", "text+image"):
            image_bytes = _load_image_bytes(self.image_dir, image_label)

        image_supplied = image_bytes is not None
        print(
            f"  [{qid}] {category} ({query_type}): '{query[:50]}'",
            end="", flush=True,
        )

        # Edge case: completely empty input (no text, no image)
        if not query.strip() and not image_supplied:
            print(" -> LLM Fallback | topic=None | 0ms | img=0 caption(s)")
            return MultimodalQueryResult(
                query_id=qid, category=category, query_type=query_type,
                query=query, model=self.model,
                retrieval_mode=self.retrieval_mode,
                embedding_name=self.embedding_name,
                expected_topic=expected_topic, actual_topic=None,
                topic_correct=(expected_topic is None),
                expected_mode=expected_mode, actual_mode="LLM Fallback",
                mode_correct=(expected_mode == "LLM Fallback"),
                answer="", answer_length=0,
                keyword_hits=0, keyword_total=len(expected_keywords),
                keyword_coverage=0.0,
                latency_ms=0.0,
                input_tokens=0, output_tokens=0, total_tokens=0,
                estimated_cost_usd=0.0,
                image_supplied=False, has_image_context=False,
                image_captions_found=0, image_caption_text="",
                note=note, error="EMPTY QUERY",
            )

        # Run pipeline
        try:
            result = self.pipeline.run(
                user_query=query,
                memory=memory,
                topic_manager=topic_manager,
                image_input=image_bytes,
            )
        except ConnectionRefusedError:
            print(" -> ERROR | topic=None | 0ms | img=0 caption(s)")
            return MultimodalQueryResult(
                query_id=qid, category=category, query_type=query_type,
                query=query, model=self.model,
                retrieval_mode=self.retrieval_mode,
                embedding_name=self.embedding_name,
                expected_topic=expected_topic, actual_topic=None,
                topic_correct=False,
                expected_mode=expected_mode, actual_mode="ERROR",
                mode_correct=False,
                answer="PIPELINE ERROR", answer_length=14,
                keyword_hits=0, keyword_total=len(expected_keywords),
                keyword_coverage=0.0,
                latency_ms=0.0,
                input_tokens=0, output_tokens=0, total_tokens=0,
                estimated_cost_usd=0.0,
                image_supplied=image_supplied, has_image_context=False,
                image_captions_found=0, image_caption_text="",
                note=note, error="OLLAMA NOT RUNNING",
            )
        except Exception as exc:
            print(" -> ERROR | topic=None | 0ms | img=0 caption(s)")
            return MultimodalQueryResult(
                query_id=qid, category=category, query_type=query_type,
                query=query, model=self.model,
                retrieval_mode=self.retrieval_mode,
                embedding_name=self.embedding_name,
                expected_topic=expected_topic, actual_topic=None,
                topic_correct=False,
                expected_mode=expected_mode, actual_mode="ERROR",
                mode_correct=False,
                answer="PIPELINE ERROR", answer_length=14,
                keyword_hits=0, keyword_total=len(expected_keywords),
                keyword_coverage=0.0,
                latency_ms=0.0,
                input_tokens=0, output_tokens=0, total_tokens=0,
                estimated_cost_usd=0.0,
                image_supplied=image_supplied, has_image_context=False,
                image_captions_found=0, image_caption_text="",
                note=note, error=str(exc),
            )

        # Extract all values from live pipeline result
        actual_topic: Optional[str] = result.detected_topic
        actual_mode: str = result.mode
        latency_ms: float = result.latency_ms
        answer: str = result.answer

        # Topic correctness
        if expected_topic is None and actual_topic is None:
            topic_correct = True
        elif expected_topic is None:
            topic_correct = False  # expected None but pipeline detected a topic
        else:
            topic_correct = (
                actual_topic is not None
                and (
                    expected_topic.lower() in actual_topic.lower()
                    or actual_topic.lower() in expected_topic.lower()
                )
            )

        # Mode normalisation - "Out of Scope" is an alias for "LLM Fallback"
        normalised_mode = "LLM Fallback" if actual_mode == "Out of Scope" else actual_mode
        mode_correct = (normalised_mode == expected_mode)

        # Keyword analysis
        hits, total, coverage = self._check_keywords(answer, expected_keywords)

        # Token counts - all from live pipeline result
        tc = result.token_counts
        input_tokens: int = tc.get("input_tokens", 0)
        output_tokens: int = tc.get("output_tokens", 0)
        total_tokens: int = tc.get("total_tokens", input_tokens + output_tokens)

        # Estimated cost derived from registry rates (0.0 for local SLMs)
        cfg = get_model_config(self.model) or {}
        estimated_cost_usd: float = (
            input_tokens  * cfg.get("cost_per_1k_input_tokens",  0.0) / 1000.0
            + output_tokens * cfg.get("cost_per_1k_output_tokens", 0.0) / 1000.0
        )

        # Multimodal fields - all from live pipeline result
        image_captions: list[str] = result.image_captions
        has_image_context: bool = result.has_image_context
        image_captions_found: int = len(image_captions)
        image_caption_text: str = " | ".join(image_captions)

        print(
            f" -> {actual_mode} | topic={actual_topic} | "
            f"{latency_ms:.0f}ms | img={image_captions_found} caption(s)"
        )

        return MultimodalQueryResult(
            query_id=qid, category=category, query_type=query_type,
            query=query, model=self.model,
            retrieval_mode=self.retrieval_mode,
            embedding_name=self.embedding_name,
            expected_topic=expected_topic, actual_topic=actual_topic,
            topic_correct=topic_correct,
            expected_mode=expected_mode, actual_mode=actual_mode,
            mode_correct=mode_correct,
            answer=answer, answer_length=len(answer),
            keyword_hits=hits, keyword_total=total,
            keyword_coverage=coverage,
            latency_ms=latency_ms,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            estimated_cost_usd=estimated_cost_usd,
            image_supplied=image_supplied,
            has_image_context=has_image_context,
            image_captions_found=image_captions_found,
            image_caption_text=image_caption_text,
            note=note, error="",
        )

    # -- Experiment runner ----------------------------------------------------

    def run_experiment(self) -> list[MultimodalQueryResult]:
        """Run all MM_TEST_QUERIES and return the list of results.

        Conversation memory and topic manager are reset for each query that
        has conversation_reset=True.
        """
        self.results = []
        memory: Optional[ConversationMemory] = None
        topic_manager: Optional[TopicMemoryManager] = None
        last_category: Optional[str] = None

        for q in MM_TEST_QUERIES:
            if q.get("conversation_reset", True) or memory is None:
                memory = ConversationMemory(max_turns=5)
                topic_manager = TopicMemoryManager()

            cat = q["category"]
            if cat != last_category:
                print(f"\n-- {cat.upper()} ------------------")
                last_category = cat

            res = self.run_single_query(q, memory, topic_manager)  # type: ignore[arg-type]
            self.results.append(res)

        return self.results

    # -- Summary computation - ALL values from live results -------------------

    def compute_summary(self) -> dict:
        """Compute aggregate metrics over self.results.

        Every value in the returned dict is derived arithmetically from the
        actual MultimodalQueryResult objects.  There are no hardcoded values.
        Errored results are excluded from accuracy/latency averages but
        counted in failed_queries.
        """
        if not self.results:
            return _empty_mm_summary()

        total = len(self.results)
        ok = [r for r in self.results if not r.error]
        errored = [r for r in self.results if r.error]

        def _acc(subset: list[MultimodalQueryResult], attr: str) -> float:
            if not subset:
                return 0.0
            return round(sum(1 for r in subset if getattr(r, attr)) / len(subset), 4)

        def _avg(subset: list[MultimodalQueryResult], attr: str) -> float:
            if not subset:
                return 0.0
            return round(sum(getattr(r, attr) for r in subset) / len(subset), 4)

        # Core accuracy metrics
        topic_accuracy       = _acc(ok, "topic_correct")
        mode_accuracy        = _acc(ok, "mode_correct")
        avg_keyword_coverage = _avg(ok, "keyword_coverage")
        avg_latency_ms       = round(_avg(ok, "latency_ms"), 1)

        # Multimodal-specific metrics
        image_queries = [r for r in ok if r.image_supplied]
        image_context_rate = (
            round(
                sum(1 for r in image_queries if r.has_image_context) / len(image_queries), 4
            ) if image_queries else 0.0
        )
        avg_captions_per_image_query = (
            round(sum(r.image_captions_found for r in image_queries) / len(image_queries), 2)
            if image_queries else 0.0
        )

        # Per-query-type topic accuracy
        def _type_acc(qtype: str) -> float:
            subset = [r for r in ok if r.query_type == qtype]
            return _acc(subset, "topic_correct")

        # Token statistics
        avg_input_tokens  = _avg(ok, "input_tokens")
        avg_output_tokens = _avg(ok, "output_tokens")
        avg_total_tokens  = _avg(ok, "total_tokens")
        avg_cost_usd = (
            round(sum(r.estimated_cost_usd for r in ok) / len(ok), 6) if ok else 0.0
        )

        # Mode counts (across ALL results including errors)
        rag_count = sum(1 for r in self.results if r.actual_mode == "RAG")
        partial_rag_count = sum(
            1 for r in self.results if r.actual_mode == "Partial RAG"
        )
        fallback_count = sum(
            1 for r in self.results
            if r.actual_mode in ("LLM Fallback", "Out of Scope")
        )

        # Per-category breakdown
        cats: dict[str, list[MultimodalQueryResult]] = {}
        for r in self.results:
            cats.setdefault(r.category, []).append(r)

        per_category: dict[str, dict] = {}
        for cat, rows in cats.items():
            cat_ok = [r for r in rows if not r.error]
            img_sub = [r for r in cat_ok if r.image_supplied]
            per_category[cat] = {
                "count":              len(rows),
                "topic_accuracy":     _acc(cat_ok, "topic_correct"),
                "mode_accuracy":      _acc(cat_ok, "mode_correct"),
                "avg_kw_coverage":    _avg(cat_ok, "keyword_coverage"),
                "avg_latency_ms":     round(_avg(cat_ok, "latency_ms"), 1),
                "avg_total_tokens":   _avg(cat_ok, "total_tokens"),
                "image_context_rate": (
                    round(
                        sum(1 for r in img_sub if r.has_image_context) / len(img_sub), 4
                    ) if img_sub else 0.0
                ),
            }

        # Per-query-type breakdown
        per_query_type: dict[str, dict] = {}
        for qtype in ("text_only", "image_only", "text+image"):
            subset = [r for r in ok if r.query_type == qtype]
            img_sub = [r for r in subset if r.image_supplied]
            per_query_type[qtype] = {
                "count":            len(subset),
                "topic_accuracy":   _acc(subset, "topic_correct"),
                "mode_accuracy":    _acc(subset, "mode_correct"),
                "avg_latency_ms":   round(_avg(subset, "latency_ms"), 1),
                "avg_total_tokens": _avg(subset, "total_tokens"),
                "image_context_rate": (
                    round(
                        sum(1 for r in img_sub if r.has_image_context) / len(img_sub), 4
                    ) if img_sub else 0.0
                ),
            }

        return {
            "total_queries":               total,
            "successful_queries":          len(ok),
            "failed_queries":              len(errored),
            "topic_accuracy":              topic_accuracy,
            "mode_accuracy":               mode_accuracy,
            "avg_keyword_coverage":        avg_keyword_coverage,
            "avg_latency_ms":              avg_latency_ms,
            "rag_count":                   rag_count,
            "partial_rag_count":           partial_rag_count,
            "fallback_count":              fallback_count,
            # Multimodal
            "image_queries_count":                len(image_queries),
            "image_context_rate":                 image_context_rate,
            "avg_captions_per_image_query":       avg_captions_per_image_query,
            "text_only_topic_accuracy":           _type_acc("text_only"),
            "image_only_topic_accuracy":          _type_acc("image_only"),
            "text_image_topic_accuracy":          _type_acc("text+image"),
            # Tokens
            "avg_input_tokens":  avg_input_tokens,
            "avg_output_tokens": avg_output_tokens,
            "avg_total_tokens":  avg_total_tokens,
            "avg_cost_usd":      avg_cost_usd,
            # Breakdowns
            "per_category":   per_category,
            "per_query_type": per_query_type,
        }


# ---------------------------------------------------------------------------
# Token summary helper
# ---------------------------------------------------------------------------

def compute_mm_token_summary(results: list[MultimodalQueryResult]) -> dict:
    """Compute token-usage statistics from a list of MultimodalQueryResult
    objects.

    Only non-errored results are included in averages.  Every returned number
    is computed from actual result fields - there are no hardcoded values.
    """
    ok = [r for r in results if not r.error]
    if not ok:
        return {
            "total_input_tokens": 0, "total_output_tokens": 0, "total_tokens": 0,
            "avg_input_per_query": 0.0, "avg_output_per_query": 0.0,
            "avg_total_per_query": 0.0, "total_cost_usd": 0.0,
            "avg_cost_per_query": 0.0, "tokens_per_ms": 0.0,
            "min_tokens_query": 0, "max_tokens_query": 0,
            "by_query_type": {}, "by_category": {},
        }

    n = len(ok)
    total_input  = sum(r.input_tokens         for r in ok)
    total_output = sum(r.output_tokens        for r in ok)
    total_all    = sum(r.total_tokens         for r in ok)
    total_cost   = sum(r.estimated_cost_usd   for r in ok)
    total_lat    = sum(r.latency_ms           for r in ok)

    avg_input  = round(total_input  / n, 1)
    avg_output = round(total_output / n, 1)
    avg_total  = round(total_all    / n, 1)
    avg_cost   = round(total_cost   / n, 6)
    tokens_per_ms = round(
        (avg_total / (total_lat / n)) if (n > 0 and total_lat > 0) else 0.0, 4
    )

    min_tok = min(r.total_tokens for r in ok)
    max_tok = max(r.total_tokens for r in ok)

    # Per-query-type breakdown
    by_query_type: dict[str, float] = {}
    for qtype in ("text_only", "image_only", "text+image"):
        sub = [r for r in ok if r.query_type == qtype]
        by_query_type[qtype] = (
            round(sum(r.total_tokens for r in sub) / len(sub), 1) if sub else 0.0
        )

    # Per-category breakdown
    cat_groups: dict[str, list[int]] = {}
    for r in ok:
        cat_groups.setdefault(r.category, []).append(r.total_tokens)
    by_category = {
        cat: round(sum(vals) / len(vals), 1)
        for cat, vals in cat_groups.items()
    }

    return {
        "total_input_tokens":   total_input,
        "total_output_tokens":  total_output,
        "total_tokens":         total_all,
        "avg_input_per_query":  avg_input,
        "avg_output_per_query": avg_output,
        "avg_total_per_query":  avg_total,
        "total_cost_usd":       round(total_cost, 6),
        "avg_cost_per_query":   avg_cost,
        "tokens_per_ms":        tokens_per_ms,
        "min_tokens_query":     min_tok,
        "max_tokens_query":     max_tok,
        "by_query_type":        by_query_type,
        "by_category":          by_category,
    }


def _empty_mm_summary() -> dict:
    """Return an all-zero summary dict for when results list is empty."""
    return {
        "total_queries": 0, "successful_queries": 0, "failed_queries": 0,
        "topic_accuracy": 0.0, "mode_accuracy": 0.0,
        "avg_keyword_coverage": 0.0, "avg_latency_ms": 0.0,
        "rag_count": 0, "partial_rag_count": 0, "fallback_count": 0,
        "image_queries_count": 0, "image_context_rate": 0.0,
        "avg_captions_per_image_query": 0.0,
        "text_only_topic_accuracy": 0.0,
        "image_only_topic_accuracy": 0.0,
        "text_image_topic_accuracy": 0.0,
        "avg_input_tokens": 0.0, "avg_output_tokens": 0.0,
        "avg_total_tokens": 0.0, "avg_cost_usd": 0.0,
        "per_category": {}, "per_query_type": {},
    }


# ---------------------------------------------------------------------------
# Results writer
# ---------------------------------------------------------------------------

class MultimodalResultsWriter:
    """Appends multimodal experiment results to a plain-text log file."""

    BLOCK_MARKER = "<<"

    def __init__(self, filepath: str = MULTIMODAL_RESULTS_FILE) -> None:
        self.filepath = Path(filepath)

    def _line(self, f, text: str = "") -> None:
        f.write(text + "\n")

    def _section(self, f, title: str) -> None:
        self._line(f, f"\n{self.BLOCK_MARKER} {title}")

    def write_experiment(
        self,
        model: str,
        retrieval_mode: str,
        embedding_name: str,
        results: list[MultimodalQueryResult],
        summary: dict,
        token_summary: dict,
    ) -> None:
        """Append per-query rows and aggregate summary for one experiment."""
        with open(self.filepath, "a", encoding="utf-8") as f:
            self._line(f)
            self._line(f, "=" * 90)
            self._section(
                f,
                f"MULTIMODAL EXPERIMENT  model={model}  retrieval={retrieval_mode}"
                f"  embedding={embedding_name}"
                f"  started={datetime.now().isoformat(timespec='seconds')}",
            )
            self._line(f, "=" * 90)
            self._line(f, f"  MODEL     : {model}")
            self._line(f, f"  EMBEDDING : {embedding_name}")
            self._line(f, f"  RETRIEVAL : {retrieval_mode}")
            self._line(f, f"  MM STACK  : {'available' if _MM_AVAILABLE else 'unavailable'}")
            self._line(f)

            # Per-query results table
            self._section(f, "QUERY RESULTS")
            self._line(f,
                f"  {'ID':<6} {'Type':<12} {'TopicOK':<8} {'ModeOK':<7} "
                f"{'KwCov':>6} {'Lat':>8} {'InTok':>6} {'OutTok':>7} "
                f"{'TotTok':>7} {'ImgCtx':<7} {'Caps':>4}")
            self._line(f, "  " + "-" * 84)
            for r in results:
                self._line(
                    f,
                    f"  {r.query_id:<6} {r.query_type:<12} "
                    f"{'Y' if r.topic_correct else 'N':<8} "
                    f"{'Y' if r.mode_correct  else 'N':<7} "
                    f"{r.keyword_coverage:>6.3f} {r.latency_ms:>6.0f}ms "
                    f"{r.input_tokens:>6} {r.output_tokens:>7} {r.total_tokens:>7} "
                    f"{'Y' if r.has_image_context else 'N':<7} "
                    f"{r.image_captions_found:>4}"
                    + (f"  [{r.error}]" if r.error else ""),
                )
            self._line(f, "  " + "=" * 84)

            # Overall summary
            self._section(f, "SUMMARY")
            self._line(f, f"  total={summary['total_queries']}  "
                       f"successful={summary['successful_queries']}  "
                       f"failed={summary['failed_queries']}")
            self._line(f, f"  topic_accuracy={summary['topic_accuracy']*100:.2f}%  "
                       f"mode_accuracy={summary['mode_accuracy']*100:.2f}%  "
                       f"avg_kw_coverage={summary['avg_keyword_coverage']:.3f}  "
                       f"avg_latency={summary['avg_latency_ms']}ms")
            self._line(f, f"  rag={summary['rag_count']}  "
                       f"partial_rag={summary['partial_rag_count']}  "
                       f"fallback={summary['fallback_count']}")

            # Multimodal summary
            self._section(f, "MULTIMODAL METRICS")
            self._line(f, f"  image_queries={summary['image_queries_count']}  "
                       f"image_context_rate={summary['image_context_rate']*100:.1f}%  "
                       f"avg_captions/img={summary['avg_captions_per_image_query']:.2f}")
            self._line(f, f"  text_only_acc={summary['text_only_topic_accuracy']*100:.1f}%  "
                       f"image_only_acc={summary['image_only_topic_accuracy']*100:.1f}%  "
                       f"text+image_acc={summary['text_image_topic_accuracy']*100:.1f}%")

            # Token statistics
            self._section(f, "TOKEN STATISTICS")
            self._line(f, f"  total_input_tokens  : {token_summary['total_input_tokens']}")
            self._line(f, f"  total_output_tokens : {token_summary['total_output_tokens']}")
            self._line(f, f"  total_tokens        : {token_summary['total_tokens']}")
            self._line(f, f"  avg_input/query     : {token_summary['avg_input_per_query']:.1f}")
            self._line(f, f"  avg_output/query    : {token_summary['avg_output_per_query']:.1f}")
            self._line(f, f"  avg_total/query     : {token_summary['avg_total_per_query']:.1f}")
            self._line(f, f"  total_cost_usd      : ${token_summary['total_cost_usd']:.6f}")
            self._line(f, f"  avg_cost/query      : ${token_summary['avg_cost_per_query']:.6f}")
            self._line(f, f"  tokens/ms           : {token_summary['tokens_per_ms']:.4f}")
            self._line(f, f"  min/max tokens      : {token_summary['min_tokens_query']} / "
                       f"{token_summary['max_tokens_query']}")

            # Per-query-type breakdown
            self._section(f, "PER QUERY-TYPE BREAKDOWN")
            self._line(f,
                f"  {'Type':<12} {'Count':>5} {'TopicAcc':>9} "
                f"{'ModeAcc':>8} {'AvgLat':>8} {'ImgCtxRate':>11} "
                f"{'AvgTok':>7} {'Tok/type':>8}")
            self._line(f, "  " + "-" * 74)
            for qtype, stats in summary["per_query_type"].items():
                tok_for_type = token_summary["by_query_type"].get(qtype, 0.0)
                self._line(
                    f,
                    f"  {qtype:<12} {stats['count']:>5} "
                    f"{stats['topic_accuracy']*100:>8.1f}% "
                    f"{stats['mode_accuracy']*100:>7.1f}% "
                    f"{stats['avg_latency_ms']:>6.0f}ms "
                    f"{stats['image_context_rate']*100:>10.1f}% "
                    f"{stats['avg_total_tokens']:>7.0f} "
                    f"{tok_for_type:>8.1f}",
                )
            self._line(f, "  " + "=" * 74)

            # Per-category breakdown
            self._section(f, "PER CATEGORY BREAKDOWN")
            self._line(f,
                f"  {'Category':<20} {'N':>4} {'TopicAcc':>9} "
                f"{'ModeAcc':>8} {'KwCov':>6} {'AvgLat':>8} "
                f"{'ImgCtxRate':>11} {'AvgTok':>7}")
            self._line(f, "  " + "-" * 80)
            for cat, stats in summary["per_category"].items():
                self._line(
                    f,
                    f"  {cat:<20} {stats['count']:>4} "
                    f"{stats['topic_accuracy']*100:>8.1f}% "
                    f"{stats['mode_accuracy']*100:>7.1f}% "
                    f"{stats['avg_kw_coverage']:>6.3f} "
                    f"{stats['avg_latency_ms']:>6.0f}ms "
                    f"{stats['image_context_rate']*100:>10.1f}% "
                    f"{stats['avg_total_tokens']:>7.0f}",
                )
            self._line(f, "  " + "=" * 80)

    def write_comparison_table(
        self,
        title: str,
        headers: list[str],
        rows: list[list[str]],
        footer_lines: Optional[list[str]] = None,
    ) -> None:
        """Append a formatted comparison table to the results file."""
        with open(self.filepath, "a", encoding="utf-8") as f:
            self._section(f, title)
            self._line(f, "  " + " | ".join(headers))
            self._line(f, "  " + "-" * 96)
            for row in rows:
                self._line(f, "  " + " | ".join(row))
            self._line(f, "  " + "=" * 96)
            if footer_lines:
                for line in footer_lines:
                    self._line(f, f"  {line}")


# ---------------------------------------------------------------------------
# High-level experiment runners
# ---------------------------------------------------------------------------

def run_multimodal_single(
    model: str = "phi3",
    retrieval_mode: str = "hybrid",
    embedding_name: str = DEFAULT_EMBEDDING,
    image_dir: Optional[str] = None,
    output: str = MULTIMODAL_RESULTS_FILE,
) -> dict:
    """Run MM_TEST_QUERIES for one (model, retrieval_mode, embedding_name).

    All values in the printed summary and output file are derived from live
    pipeline results.

    Args:
        model:          Model name (Ollama local or Groq/OpenAI/etc. API).
        retrieval_mode: Retrieval mode ("hybrid", "vector_only", "bm25_only").
        embedding_name: Embedding model key (e.g. "bge-small").
        image_dir:      Directory of test images (None -> synthetic images).
        output:         Path to results file (default: multimodal_results.txt).

    Returns:
        Summary dict from compute_summary().
    """
    print(f"\n{'=' * 60}")
    print(f"  MULTIMODAL EVALUATION")
    print(f"  Model: {model} | Retrieval: {retrieval_mode} | Embedding: {embedding_name}")
    print(f"  Multimodal stack: {'available' if _MM_AVAILABLE else 'unavailable'}")
    print(f"  Image source: {image_dir or 'synthetic'}")
    print(f"{'=' * 60}")

    evaluator = MultimodalResearchEvaluator(
        model=model,
        retrieval_mode=retrieval_mode,
        embedding_name=embedding_name,
        image_dir=image_dir,
    )
    results = evaluator.run_experiment()
    summary = evaluator.compute_summary()
    token_summary = compute_mm_token_summary(results)

    writer = MultimodalResultsWriter(filepath=output)
    writer.write_experiment(
        model, retrieval_mode, embedding_name, results, summary, token_summary
    )

    _print_summary(summary, token_summary)
    print(f"  Results appended to: {output}")
    return summary


def run_multimodal_model_comparison(
    retrieval_mode: str = "hybrid",
    embedding_name: str = DEFAULT_EMBEDDING,
    image_dir: Optional[str] = None,
    output: str = MULTIMODAL_RESULTS_FILE,
) -> None:
    """Compare all available models on MM_TEST_QUERIES.

    Every number in the printed table comes from a live pipeline result.
    Models that are not reachable are skipped with a log message.

    Args:
        retrieval_mode: Retrieval mode used for all models.
        embedding_name: Embedding model key.
        image_dir:      Directory of test images (None -> synthetic images).
        output:         Path to results file.
    """
    print(f"\n{'=' * 60}")
    print(f"  MULTIMODAL MODEL COMPARISON")
    print(f"  Retrieval: {retrieval_mode} | Embedding: {embedding_name}")
    print(f"  Models: {MODELS_TO_EVALUATE}")
    print(f"{'=' * 60}")

    writer = MultimodalResultsWriter(filepath=output)
    summaries: dict[str, dict] = {}
    token_sums: dict[str, dict] = {}
    ran: list[str] = []

    for model in MODELS_TO_EVALUATE:
        if not MultimodalResearchEvaluator._is_model_available(model):
            print(f"\n  [Skip] '{model}' not available.")
            continue
        evaluator = MultimodalResearchEvaluator(
            model=model,
            retrieval_mode=retrieval_mode,
            embedding_name=embedding_name,
            image_dir=image_dir,
        )
        results = evaluator.run_experiment()
        summaries[model] = evaluator.compute_summary()
        token_sums[model] = compute_mm_token_summary(results)
        writer.write_experiment(
            model, retrieval_mode, embedding_name,
            results, summaries[model], token_sums[model],
        )
        ran.append(model)

    if not ran:
        print("  No models were available - exiting.")
        return

    # Winners derived from live computed summaries
    best_topic    = max(ran, key=lambda m: summaries[m]["topic_accuracy"])
    best_img_ctx  = max(ran, key=lambda m: summaries[m]["image_context_rate"])
    fastest       = min(ran, key=lambda m: summaries[m]["avg_latency_ms"])
    most_eff_tok  = min(ran, key=lambda m: token_sums[m]["avg_total_per_query"])
    lowest_cost   = min(ran, key=lambda m: token_sums[m]["avg_cost_per_query"])

    # Comparison table rows - no hardcoded values
    col_headers = [
        f"{'Model':<16}", f"{'TopicAcc':>8}", f"{'ModeAcc':>7}",
        f"{'KwCov':>6}", f"{'Lat':>8}", f"{'ImgCtxRate':>11}",
        f"{'Caps/Img':>8}", f"{'InTok':>6}", f"{'OutTok':>7}",
        f"{'TotTok':>7}", f"{'AvgCost':>12}",
    ]
    table_rows: list[list[str]] = []
    for model in ran:
        s = summaries[model]
        t = token_sums[model]
        table_rows.append([
            f"{model:<16}",
            f"{s['topic_accuracy']*100:>7.1f}%",
            f"{s['mode_accuracy']*100:>6.1f}%",
            f"{s['avg_keyword_coverage']:>6.3f}",
            f"{s['avg_latency_ms']:>6.0f}ms",
            f"{s['image_context_rate']*100:>10.1f}%",
            f"{s['avg_captions_per_image_query']:>8.2f}",
            f"{t['avg_input_per_query']:>6.0f}",
            f"{t['avg_output_per_query']:>7.0f}",
            f"{t['avg_total_per_query']:>7.0f}",
            f"${t['avg_cost_per_query']:>11.6f}",
        ])

    # Per-query-type breakdown table
    type_headers = [
        f"{'Model':<16}", f"{'Type':<12}", f"{'TopicAcc':>9}",
        f"{'ModeAcc':>8}", f"{'AvgLat':>8}", f"{'ImgCtxRate':>11}",
        f"{'AvgTok':>7}",
    ]
    type_rows: list[list[str]] = []
    for model in ran:
        s = summaries[model]
        for qtype in ("text_only", "image_only", "text+image"):
            qt = s["per_query_type"].get(qtype, {})
            if not qt or qt["count"] == 0:
                continue
            type_rows.append([
                f"{model:<16}",
                f"{qtype:<12}",
                f"{qt['topic_accuracy']*100:>8.1f}%",
                f"{qt['mode_accuracy']*100:>7.1f}%",
                f"{qt['avg_latency_ms']:>6.0f}ms",
                f"{qt['image_context_rate']*100:>10.1f}%",
                f"{qt['avg_total_tokens']:>7.0f}",
            ])

    footer = [
        f"Best topic accuracy    : {best_topic} "
        f"({summaries[best_topic]['topic_accuracy']*100:.1f}%)",
        f"Best image context rate: {best_img_ctx} "
        f"({summaries[best_img_ctx]['image_context_rate']*100:.1f}%)",
        f"Fastest                : {fastest} "
        f"({summaries[fastest]['avg_latency_ms']:.0f}ms avg)",
        f"Most token-efficient   : {most_eff_tok} "
        f"({token_sums[most_eff_tok]['avg_total_per_query']:.0f} avg tokens/query)",
        f"Lowest cost            : {lowest_cost} "
        f"(${token_sums[lowest_cost]['avg_cost_per_query']:.6f}/query)",
        f"Results saved to       : {output}",
    ]

    # Print to stdout
    print(f"\n{'=' * 60} MODEL COMPARISON {'=' * 3}")
    print("  " + " | ".join(col_headers))
    print("  " + "-" * 96)
    for row in table_rows:
        print("  " + " | ".join(row))
    print("  " + "=" * 96)
    for line in footer:
        print(f"  {line}")

    # Write to file
    writer.write_comparison_table(
        title=f"MULTIMODAL MODEL COMPARISON  retrieval={retrieval_mode}  embedding={embedding_name}",
        headers=col_headers,
        rows=table_rows,
        footer_lines=footer,
    )
    writer.write_comparison_table(
        title="MULTIMODAL PER-QUERY-TYPE BREAKDOWN",
        headers=type_headers,
        rows=type_rows,
    )


def run_multimodal_full_matrix(
    retrieval_mode: str = "hybrid",
    image_dir: Optional[str] = None,
    output: str = MULTIMODAL_RESULTS_FILE,
) -> None:
    """Run all available models x all embedding models on MM_TEST_QUERIES.

    Every number in the output is derived from live pipeline results.
    Interrupted runs can be resumed because per-(model,embedding) results
    are written incrementally.

    Args:
        retrieval_mode: Retrieval mode used for all combinations.
        image_dir:      Directory of test images (None -> synthetic images).
        output:         Path to results file.
    """
    emb_names = [e["name"] for e in EMBEDDING_MODELS]
    total_runs = len(MODELS_TO_EVALUATE) * len(EMBEDDING_MODELS)
    print(f"\n{'=' * 56} FULL MATRIX {'=' * 4}")
    print(f"  Models     : {MODELS_TO_EVALUATE}")
    print(f"  Embeddings : {emb_names}")
    print(f"  Retrieval  : {retrieval_mode}")
    print(f"  Total runs : up to {total_runs}")
    print(f"{'=' * 80}")

    writer = MultimodalResultsWriter(filepath=output)
    matrix_rows: list[dict] = []
    run_idx = 0

    for model in MODELS_TO_EVALUATE:
        if not MultimodalResearchEvaluator._is_model_available(model):
            print(f"\n  [Skip] Model '{model}' not available.")
            continue

        for emb in EMBEDDING_MODELS:
            emb_name = emb["name"]
            run_idx += 1
            print(f"\n[{run_idx}/{total_runs}] {model} + {emb_name} + {retrieval_mode}")

            try:
                evaluator = MultimodalResearchEvaluator(
                    model=model,
                    retrieval_mode=retrieval_mode,
                    embedding_name=emb_name,
                    image_dir=image_dir,
                )
            except (OSError, ConnectionError) as exc:
                print(f"  Failed to init {emb_name}: {exc}. Skipping.")
                continue

            results = evaluator.run_experiment()
            summary = evaluator.compute_summary()
            tok = compute_mm_token_summary(results)

            writer.write_experiment(model, retrieval_mode, emb_name,
                                    results, summary, tok)

            matrix_rows.append({
                "model":           model,
                "embedding":       emb_name,
                "topic_acc":       summary["topic_accuracy"],
                "mode_acc":        summary["mode_accuracy"],
                "kw_cov":          summary["avg_keyword_coverage"],
                "lat":             summary["avg_latency_ms"],
                "img_ctx_rate":    summary["image_context_rate"],
                "avg_caps":        summary["avg_captions_per_image_query"],
                "avg_in_tok":      tok["avg_input_per_query"],
                "avg_out_tok":     tok["avg_output_per_query"],
                "avg_total_tok":   tok["avg_total_per_query"],
                "avg_cost":        tok["avg_cost_per_query"],
            })

    if not matrix_rows:
        return

    # Compute winners from real data
    best_overall = max(matrix_rows, key=lambda r: r["topic_acc"] + r["mode_acc"])
    fastest = min(matrix_rows, key=lambda r: r["lat"])
    best_img_ctx = max(matrix_rows, key=lambda r: r["img_ctx_rate"])
    value_rows = [r for r in matrix_rows if r["avg_total_tok"] > 0]
    best_value = (
        max(value_rows, key=lambda r: (r["topic_acc"] + r["mode_acc"]) / r["avg_total_tok"])
        if value_rows else best_overall
    )

    col_headers = [
        f"{'Model':<14}", f"{'Embedding':<20}",
        f"{'TopicAcc':>8}", f"{'ModeAcc':>7}", f"{'KwCov':>6}",
        f"{'Lat':>8}", f"{'ImgCtx':>7}", f"{'InTok':>6}",
        f"{'OutTok':>7}", f"{'TotTok':>7}", f"{'AvgCost':>12}",
    ]
    table_rows = [
        [
            f"{r['model']:<14}", f"{r['embedding']:<20}",
            f"{r['topic_acc']*100:>7.1f}%", f"{r['mode_acc']*100:>6.1f}%",
            f"{r['kw_cov']:>6.3f}", f"{r['lat']:>6.0f}ms",
            f"{r['img_ctx_rate']*100:>6.1f}%",
            f"{r['avg_in_tok']:>6.0f}", f"{r['avg_out_tok']:>7.0f}",
            f"{r['avg_total_tok']:>7.0f}", f"${r['avg_cost']:>11.6f}",
        ]
        for r in matrix_rows
    ]

    footer = [
        f"Best overall   : {best_overall['model']} + {best_overall['embedding']}"
        f" ({best_overall['topic_acc']*100:.1f}% topic acc)",
        f"Fastest        : {fastest['model']} + {fastest['embedding']}"
        f" ({fastest['lat']:.0f}ms)",
        f"Best img ctx   : {best_img_ctx['model']} + {best_img_ctx['embedding']}"
        f" ({best_img_ctx['img_ctx_rate']*100:.1f}%)",
        f"Best value     : {best_value['model']} + {best_value['embedding']}",
        f"Results saved  : {output}",
    ]

    print(f"\n{'=' * 56} FULL MATRIX RESULTS {'=' * 4}")
    print("  " + " | ".join(col_headers))
    print("  " + "-" * 80)
    for row in table_rows:
        print("  " + " | ".join(row))
    print("  " + "=" * 80)
    for line in footer:
        print(f"  {line}")

    writer.write_comparison_table(
        title=f"MULTIMODAL FULL MATRIX  retrieval={retrieval_mode}",
        headers=col_headers,
        rows=table_rows,
        footer_lines=footer,
    )


# ---------------------------------------------------------------------------
# Stdout helpers
# ---------------------------------------------------------------------------

def _print_summary(summary: dict, token_summary: dict) -> None:
    """Print a compact single-experiment summary to stdout."""
    print(f"\n  topic_accuracy={summary['topic_accuracy']*100:.2f}%"
          f"  mode_accuracy={summary['mode_accuracy']*100:.2f}%"
          f"  avg_latency={summary['avg_latency_ms']}ms")
    print(f"  image_context_rate={summary['image_context_rate']*100:.1f}%"
          f"  avg_captions/img={summary['avg_captions_per_image_query']:.2f}")
    print(f"  text_only_acc={summary['text_only_topic_accuracy']*100:.1f}%"
          f"  image_only_acc={summary['image_only_topic_accuracy']*100:.1f}%"
          f"  text+image_acc={summary['text_image_topic_accuracy']*100:.1f}%")
    print(f"  avg_in_tok={token_summary['avg_input_per_query']:.0f}"
          f"  avg_out_tok={token_summary['avg_output_per_query']:.0f}"
          f"  avg_total_tok={token_summary['avg_total_per_query']:.0f}"
          f"  avg_cost=${token_summary['avg_cost_per_query']:.6f}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

_MODES = ["single", "model_comparison", "full_matrix"]


def _parse_args() -> argparse.Namespace:
    emb_names = [e["name"] for e in EMBEDDING_MODELS]
    parser = argparse.ArgumentParser(
        description="Multimodal evaluation harness for the SLM-with-RAG pipeline."
    )
    parser.add_argument(
        "--mode", choices=_MODES, default="single",
        help="Experiment mode: single | model_comparison | full_matrix  (default: single).",
    )
    parser.add_argument(
        "--model", choices=MODELS_TO_EVALUATE, default="phi3",
        help="Model to evaluate (default: phi3). Used only in --mode single.",
    )
    parser.add_argument(
        "--retrieval", choices=RETRIEVAL_MODES, default="hybrid",
        help="Retrieval mode to use (default: hybrid).",
    )
    parser.add_argument(
        "--embedding", choices=emb_names, default=DEFAULT_EMBEDDING,
        help=f"Embedding model to use (default: {DEFAULT_EMBEDDING}).",
    )
    parser.add_argument(
        "--image-dir", default=None,
        help=(
            "Directory containing PNG/JPEG test images.  Files are matched "
            "to queries by label substring.  If omitted, synthetic images are "
            "generated automatically."
        ),
    )
    parser.add_argument(
        "--output", default=None,
        help=(
            "Override results file path.  If omitted, results go to "
            f"{MULTIMODAL_RESULTS_FILE}."
        ),
    )
    parser.add_argument(
        "--list-embeddings", action="store_true",
        help="Print all available embedding models and exit.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    if args.list_embeddings:
        print("Available embeddings:")
        for emb in EMBEDDING_MODELS:
            print(f"  {emb['name']:<12} | {emb['dimension']}d | {emb['description']}")
        sys.exit(0)

    _out: dict = {} if args.output is None else {"output": args.output}
    image_dir = args.image_dir

    if args.mode == "single":
        run_multimodal_single(
            model=args.model,
            retrieval_mode=args.retrieval,
            embedding_name=args.embedding,
            image_dir=image_dir,
            **_out,
        )
    elif args.mode == "model_comparison":
        run_multimodal_model_comparison(
            retrieval_mode=args.retrieval,
            embedding_name=args.embedding,
            image_dir=image_dir,
            **_out,
        )
    elif args.mode == "full_matrix":
        run_multimodal_full_matrix(
            retrieval_mode=args.retrieval,
            image_dir=image_dir,
            **_out,
        )


if __name__ == "__main__":
    main()
