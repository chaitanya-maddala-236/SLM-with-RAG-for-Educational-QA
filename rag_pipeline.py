"""
rag_pipeline.py
---------------
Orchestrates the upgraded 10-step Contextual Retrieval RAG pipeline:

  Step 1  – Receive user question
  Step 2  – Check conversation memory
  Step 3  – Contextual Query Builder (normalise + confidence score + ambiguity
            resolve + context-aware rewrite)
  Step 4  – Ambiguity detection (final check on rewritten query)
  Step 5  – Query classification (subject + topic)
  Step 6  – Glossary mapping (synonym / concept expansion)
  Step 7  – Vector retrieval (BGE embeddings + Chroma)
  Step 8  – Top-K document selection
  Step 9  – Answer generation (Phi-3 via Ollama)
  Step 10 – Evaluation metrics + memory update

Each step prints a clearly labelled debug line so the pipeline is fully
transparent from the command line and the Streamlit sidebar.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

import numpy as np

# Research addition: optional MLflow integration (pip install mlflow)
try:
    import mlflow as _mlflow
    _MLFLOW_AVAILABLE = True
except ImportError:
    _mlflow = None  # type: ignore[assignment]
    _MLFLOW_AVAILABLE = False
# from langchain.schema import Document
from langchain_core.documents import Document
from langchain_ollama import OllamaLLM
# from langchain.prompts import PromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma

# ── API LLM availability flags ────────────────────────────────────────────────
_GROQ_AVAILABLE = False
try:
    from langchain_groq import ChatGroq as _ChatGroq  # type: ignore[import]
    _GROQ_AVAILABLE = True
except ImportError:
    pass

# ── Token counting (tiktoken with graceful fallback) ──────────────────────────
try:
    import tiktoken as _tiktoken
    _TOKENIZER = _tiktoken.get_encoding("cl100k_base")

    def _count_tokens(text: str) -> int:
        """Count tokens using tiktoken cl100k_base encoding (approximate for Phi-3)."""
        return len(_TOKENIZER.encode(text))

except Exception:  # ImportError, ConnectionError, or any other init failure
    def _count_tokens(text: str) -> int:  # type: ignore[misc]
        """Approximate token count by word splitting (tiktoken unavailable).

        Note: word-split counts typically underestimate actual token counts
        (English text averages ~1.3–1.5 tokens per word).
        """
        return len(text.split())

from context_memory import ConversationMemory
from topic_memory_manager import TopicMemoryManager
from contextual_query_builder import ContextualQueryBuilder, TOPIC_KEYWORD_WEIGHTS
from query_classifier import classify_query, detect_topic_shift
from glossary_mapper import (
    get_ambiguous_terms,
    disambiguate_with_signals,
    expand_query,
    AMBIGUOUS_TERMS,
    OUT_OF_SCOPE_SIGNALS,
    get_rag_threshold,    # RAG Improvement 16
    get_context_budget,   # RAG Improvement 15
    expand_query_with_topic,  # RAG Improvement 10
)
from retriever import (
    build_bm25_index,
    hybrid_search,
    hierarchical_retrieve,
    retrieve_top_k,
    BM25Index,
)
from evaluation import compute_all_metrics
from data_loader import get_texts_and_metadatas
from research_config import MODEL_REGISTRY

# ── Multimodal extension (optional; degrades gracefully when deps are absent) ─
try:
    from multimodal_processor import (
        CLIPEmbedder as _CLIPEmbedder,
        ImageCaptioner as _ImageCaptioner,
        ImageFAISSIndex as _ImageFAISSIndex,
        fuse_multimodal_context as _fuse_multimodal_context,
    )
    _MULTIMODAL_AVAILABLE = True
except ImportError:
    _MULTIMODAL_AVAILABLE = False

# ── Prompt template for the SLM ──────────────────────────────────────────────
RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a helpful educational assistant for students.
Use ONLY the context below to answer the question.
If the context does not contain enough information, say so clearly.
Keep your answer concise and suitable for the student's level.

Context:
{context}

Question: {question}

Answer:""",
)

# ── Prompt template for LLM fallback (no retrieved context) ──────────────────
LLM_FALLBACK_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are an educational assistant.

The user asked a question: "{question}".

No external documents are available. Answer based on your own knowledge.

- If the question is ambiguous, provide possible interpretations.
- Explain clearly and simply for students.
- If unsure, indicate uncertainty rather than making up facts.

Answer:""",
)

# ── Prompt template for partial context (low-confidence retrieval) ────────────
PARTIAL_CONTEXT_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a helpful educational assistant.
The following context may be partially relevant to the question.
Use it if helpful, but also draw on your own knowledge if needed.
Be honest if the context is not directly relevant.

Partial Context:
{context}

Question: {question}

Answer:""",
)

# ── Prompt template for vague / one-word queries ──────────────────────────────
VAGUE_QUERY_PROMPT = PromptTemplate(
    input_variables=["query"],
    template="""You are an educational assistant.

The user asked a vague question: "{query}".

Provide possible interpretations and a brief explanation for each.
If context exists, prioritize it, but do not assume unrelated topics.

List at least 2-3 possible interpretations clearly and concisely for students.

Answer:""",
)

# RAG Improvement 17: Conversation-aware prompting
RAG_PROMPT_WITH_HISTORY = PromptTemplate(
    input_variables=["context", "question", "history"],
    template="""You are a helpful educational assistant for students.
Use ONLY the context below to answer the question.
Consider the recent conversation history for context.
If the context does not contain enough information, say so clearly.
Keep your answer concise and suitable for the student's level.

Recent conversation:
{history}

Context:
{context}

Question: {question}

Answer:""",
)

# ── Prompt template for multimodal (text + image captions) context ────────────
# Used in place of RAG_PROMPT / PARTIAL_CONTEXT_PROMPT when image captions are
# present in the context (i.e. result.has_image_context is True).  The context
# passed here is built by fuse_multimodal_context() which prepends a
# "=== Text Context ===" section followed by a
# "=== Visual Context (from diagrams/images) ===" section containing BLIP
# captions.  Downstream grounding and evaluation logic work identically.
MULTIMODAL_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a helpful educational assistant for students.
Use ONLY the context below (which includes both text and descriptions of relevant
diagrams or images) to answer the question.
If the context does not contain enough information, say so clearly.
Keep your answer concise and suitable for the student's level.

Context:
{context}

Question: {question}

Answer:""",
)

TOP_K = 5          # number of documents to return after reranking
RETRIEVAL_CANDIDATES = 20   # wider pool fetched before reranking
# Similarity threshold: scores at or above this use RAG mode; below → LLM Fallback
RAG_SIMILARITY_THRESHOLD: float = 0.6
# Bugfix: Partial RAG threshold — scores between this and RAG_SIMILARITY_THRESHOLD
# use PARTIAL_CONTEXT_PROMPT with retrieved docs as partial context instead of
# discarding them entirely.
PARTIAL_RAG_THRESHOLD: float = 0.3
# RAG Improvement 14: minimum grounding score before a warning is emitted
MIN_GROUNDING_THRESHOLD: float = 0.3
# Context drift threshold: cosine similarity between the current query and the
# last conversation context below this value indicates an out-of-context query.
CONTEXT_SIMILARITY_THRESHOLD: float = 0.30
CLARIFICATION_MSG = (
    "I found the term '{term}' in your question, which could mean: {options}. "
    "Could you clarify which one you meant?"
)

# Research addition: list of SLMs available via Ollama for multi-model evaluation
MODELS_TO_EVALUATE = ["tinyllama", "phi3", "llama3.2", "mistral"]

# ── Pipeline-level statistics (module-level, survives across pipeline calls) ──
_pipeline_stats: dict[str, int] = {
    "total_queries": 0,
    "fallback_triggers": 0,
    "clarifications_requested": 0,
}

# ── Filler words excluded from vague-query word count ────────────────────────
_FILLER_WORDS: frozenset[str] = frozenset({
    "what", "is", "are", "how", "does", "do", "can", "explain", "tell",
    "me", "about", "the", "a", "an", "of", "in", "for", "it", "its",
    "that", "this", "please", "just", "give", "show", "describe",
})

# ── Pure follow-up patterns (Bug 3 fix) ──────────────────────────────────────
# Queries that start with (or exactly match) these phrases are pure follow-ups
# that should never trigger context-drift detection.
_PURE_FOLLOWUP_PATTERNS: frozenset[str] = frozenset({
    "advantages", "disadvantages", "limitations", "examples",
    "applications", "uses", "difference", "compare", "elaborate",
    "summarize", "explain more", "tell me more", "pros and cons",
    "what are its", "what are the", "how does it", "why does it",
    "give example", "real world", "where is it used",
})

# ── Stop-words used by _extract_query_topic ───────────────────────────────────
_TOPIC_QUESTION_WORDS: frozenset[str] = frozenset({
    "what", "is", "are", "how", "does", "explain", "tell",
    "describe", "define", "why", "where", "when", "do", "can",
    # aspect/modifier words that are not themselves a topic
    "advantages", "disadvantages", "limitations", "examples",
    "applications", "uses",
})
_TOPIC_FILLER_WORDS: frozenset[str] = frozenset({
    "me", "about", "the", "a", "an", "of", "in", "for",
})

# ── Conjunction pattern for compound-query detection ─────────────────────────
_COMPOUND_RE = re.compile(
    r"\b(and|also|additionally|furthermore|as well as|plus)\b", re.IGNORECASE
)


def _extract_answer_text(response) -> str:
    """Extract plain text from an LLM response.

    OllamaLLM.invoke() returns a plain ``str``; ChatGroq (and other
    LangChain ChatModel subclasses) return an ``AIMessage`` whose text
    lives in ``.content``.  This helper normalises both so the rest of
    the pipeline always works with a plain string.
    """
    if hasattr(response, "content"):
        return str(response.content)
    return str(response)


def _cosine_similarity(v1: list[float], v2: list[float]) -> float:
    """Return cosine similarity between two embedding vectors.

    Since BGE embeddings are L2-normalised, this is equivalent to the dot
    product.  A safe fallback of 0.0 is returned for zero-length vectors.
    """
    a = np.asarray(v1, dtype=float)
    b = np.asarray(v2, dtype=float)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / denom) if denom > 0 else 0.0


def _is_vague_query(query: str) -> bool:
    """Return True if *query* is too short or contains only filler words.

    A query with at most one meaningful (non-filler, >2-char) token is
    considered vague (e.g. "cycle", "system", "it").
    """
    meaningful = [
        t for t in re.findall(r"\b[a-z0-9]+\b", query.lower())
        if t not in _FILLER_WORDS and len(t) > 2
    ]
    return len(meaningful) <= 1


def _is_compound_query(query: str) -> bool:
    """Return True if *query* contains a conjunction suggesting multiple parts."""
    return bool(_COMPOUND_RE.search(query))


def _extract_query_topic(query: str) -> str | None:
    """Extract the main noun/topic from a query for memory storage.

    Used when no knowledge base topic is matched (LLM Fallback mode) so that
    follow-up questions can still resolve pronouns and topic references.

    Strategy:
    1. Remove common question words: what, is, are, how, does, explain, tell,
       describe, define, why, where, when.
    2. Remove filler words: me, about, the, a, an, of, in, for.
    3. Remove aspect/modifier words: advantages, disadvantages, limitations,
       examples, applications, uses.
    4. Return the remaining meaningful phrase (first 3 words max).
    5. If nothing remains, return None.

    Examples:
        "what is agriculture"           → "agriculture"
        "explain the water cycle"       → "water cycle"
        "how does photosynthesis work"  → "photosynthesis work"
        "tell me about soil degradation" → "soil degradation"
        "advantages of farming"         → "farming"
    """
    tokens = re.findall(r"\b[a-z0-9]+\b", query.lower())
    meaningful = [
        t for t in tokens
        if t not in _TOPIC_QUESTION_WORDS and t not in _TOPIC_FILLER_WORDS
    ]
    if not meaningful:
        return None
    return " ".join(meaningful[:3])


# RAG Improvement 14: Grounding score
def _compute_grounding_score(answer: str, docs: list[Document]) -> float:
    """
    Compute sentence-level grounding score: fraction of answer sentences
    that share at least one content token with retrieved documents.

    A score below MIN_GROUNDING_THRESHOLD (0.3) indicates the answer may not be well-grounded in the retrieved docs.

    Args:
        answer: The generated answer string.
        docs: Retrieved documents used for context.

    Returns:
        Float in [0, 1] indicating the proportion of grounded answer sentences.
    """
    if not docs or not answer.strip():
        return 0.0
    doc_tokens: set[str] = set()
    for doc in docs:
        tokens = re.findall(r"\b[a-z0-9]+\b", doc.page_content.lower())
        doc_tokens.update(t for t in tokens if len(t) > 2)
    sentences = [s.strip() for s in re.split(r"[.!?]+", answer) if s.strip()]
    if not sentences:
        return 0.0
    grounded = 0
    for sentence in sentences:
        s_tokens = set(re.findall(r"\b[a-z0-9]+\b", sentence.lower()))
        if s_tokens & doc_tokens:
            grounded += 1
    return grounded / len(sentences)


# RAG Improvement 15: Context budget manager
def _build_context_with_budget(docs: list[Document], model_name: str) -> str:
    """
    Build context string from retrieved docs respecting the model's token budget.

    Uses get_context_budget() to avoid exceeding context limits for small models.

    Args:
        docs: Retrieved documents.
        model_name: The model being used (determines budget).

    Returns:
        Concatenated context string within token budget.
    """
    budget = get_context_budget(model_name)
    parts: list[str] = []
    used = 0
    for doc in docs:
        doc_tokens = _count_tokens(doc.page_content)
        if used + doc_tokens > budget:
            break
        parts.append(doc.page_content)
        used += doc_tokens
    return "\n\n".join(parts) if parts else (docs[0].page_content if docs else "")


def _build_multimodal_context_with_budget(
    docs: list[Document],
    image_hits: list,
    model_name: str,
    additional_captions: list[str] | None = None,
) -> str:
    """
    Build a multimodal context string (text chunks + image captions) respecting
    the model's token budget.

    Strategy:
      1. Allocate the full context budget to text chunks via
         ``_build_context_with_budget()``.
      2. Count tokens consumed by the text portion.
      3. Fill the remaining budget with image captions (one at a time, in
         relevance order), truncating a caption if it alone would overflow.

    Args:
        docs:        Retrieved LangChain Document objects.
        image_hits:  List of (ImageRecord, score) from the image index.
        model_name:  Model identifier — determines the budget ceiling.

    Returns:
        Unified context string within token budget.
    """
    budget = get_context_budget(model_name)

    # ── Text portion ──────────────────────────────────────────────────────────
    text_context = _build_context_with_budget(docs, model_name)
    used = _count_tokens(text_context)

    # ── Caption portion (remaining budget) ────────────────────────────────────
    caption_parts: list[str] = []
    caption_candidates = [
        *(additional_captions or []),
        *[
            rec.caption
            for rec, _ in image_hits
            if rec.caption
        ],
    ]

    seen_captions: set[str] = set()
    for raw_caption in caption_candidates:
        caption_text = (raw_caption or "").strip()
        if not caption_text:
            continue
        key = caption_text.lower()
        if key in seen_captions:
            continue
        seen_captions.add(key)
        caption_line = f"[Image Context]: {caption_text}"
        # Tokenize the full caption once to avoid per-word re-encoding overhead.
        cap_tokens = _count_tokens(caption_line)
        remaining = budget - used
        if remaining <= 0:
            break
        if cap_tokens > remaining:
            # Truncate: use a binary search over word boundaries (O(log n) encodes
            # instead of O(n)) to find the longest prefix that fits the budget.
            words = caption_line.split()
            lo, hi = 0, len(words)
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if _count_tokens(" ".join(words[:mid])) <= remaining:
                    lo = mid
                else:
                    hi = mid - 1
            if lo == 0:
                break
            caption_line = " ".join(words[:lo])
            cap_tokens = _count_tokens(caption_line)
        caption_parts.append(caption_line)
        used += cap_tokens

    # ── Assemble ──────────────────────────────────────────────────────────────
    parts: list[str] = []
    if text_context:
        parts.append("=== Text Context ===")
        parts.append(text_context)
    if caption_parts:
        parts.append("=== Visual Context (from diagrams/images) ===")
        parts.extend(caption_parts)
    return "\n\n".join(parts)


@dataclass
class PipelineResult:
    """Container for all outputs produced by one pipeline run."""

    query: str
    rewritten_query: str
    detected_topic: str | None
    detected_subject: str | None
    ambiguous_terms: list[str]
    clarification_needed: bool
    clarification_message: str | None
    retrieved_docs: list[Document]
    answer: str
    metrics: dict[str, float]
    step_log: list[str] = field(default_factory=list)
    retrieval_score: float = 0.0
    mode: str = "RAG"
    token_counts: dict[str, int] = field(default_factory=dict)
    context_similarity: float | None = None
    latency_ms: float = 0.0
    grounding_score: float = 0.0       # RAG Improvement 14
    estimated_cost_usd: float = 0.0    # RAG Improvement 18
    image_captions: list[str] = field(default_factory=list)   # Multimodal
    has_image_context: bool = False                            # Multimodal

    def log(self, step: int, message: str) -> None:
        entry = f"[Step {step:>2}] {message}"
        self.step_log.append(entry)
        print(entry)

    def tag_log(self, tag: str, message: str) -> None:
        """Emit a labelled console log line and record it in step_log."""
        entry = f"[{tag}] {message}"
        self.step_log.append(entry)
        print(entry)


# ── LLM factory: supports Ollama SLMs and OpenAI/Anthropic/Google API LLMs ───

def _build_llm(model_name: str, temperature: float = 0.1):
    """
    Return a LangChain LLM / ChatModel for the given *model_name*.

    Looks up the model in MODEL_REGISTRY to determine the provider:
      - ``ollama``    → OllamaLLM (local, no API key needed)
      - ``groq``      → ChatGroq (requires GROQ_API_KEY)

    Falls back to OllamaLLM for any unknown provider.

    Args:
        model_name:  Name as listed in MODEL_REGISTRY (e.g. "gpt-4.1",
                     "groq-llama3-8b").
        temperature: Sampling temperature passed to the model.

    Returns:
        A LangChain Runnable that can be invoked with a prompt string.

    Raises:
        ImportError:  If the required langchain_* package is not installed.
        ValueError:   If the required API key env var is not set.
    """
    import os as _os

    def _is_configured_secret(value: str | None) -> bool:
        v = (value or "").strip()
        if not v:
            return False
        lowered = v.lower()
        placeholder_markers = ("replace_with", "your_", "example", "placeholder")
        return not any(marker in lowered for marker in placeholder_markers)

    cfg = next((m for m in MODEL_REGISTRY if m["name"] == model_name), None)
    provider = cfg["provider"] if cfg else "ollama"
    model_id = cfg["model_id"] if cfg else model_name

    if provider == "groq":
        if not _GROQ_AVAILABLE:
            raise ImportError(
                "langchain-groq is not installed. "
                "Run: pip install langchain-groq"
            )
        api_key = _os.environ.get("GROQ_API_KEY", "")
        if not _is_configured_secret(api_key):
            raise ValueError("GROQ_API_KEY environment variable is not set.")
        return _ChatGroq(
            model=model_id,
            temperature=temperature,
            api_key=api_key,
        )

    # Default: Ollama (local)
    return OllamaLLM(model=model_id, temperature=temperature)


class RAGPipeline:
    """
    Full conversational Contextual Retrieval RAG pipeline.

    Stateless except for the vector store and the ContextualQueryBuilder;
    per-session state (ConversationMemory, TopicMemoryManager) is passed in.
    """

    def __init__(
        self,
        vector_store: Chroma,
        model_name: str = "phi3",
        top_k: int = TOP_K,
        retrieval_mode: str = "hybrid",
        image_index: "_ImageFAISSIndex | None" = None,
        use_cross_encoder: bool = False,
    ) -> None:
        self.vector_store = vector_store
        self.top_k = top_k
        self.model_name = model_name  # Bugfix: store for MLflow logging
        self.retrieval_mode = retrieval_mode
        self.use_cross_encoder = use_cross_encoder
        # Build the LLM: API models (GPT-4.1, Claude, Gemini) or local Ollama
        try:
            self.llm = _build_llm(model_name, temperature=0.1)
            print(f"[Init] LLM loaded: {model_name}")
        except Exception as exc:
            fallback_model = "phi3"
            print(
                f"[Init] LLM load failed for '{model_name}': {exc}. "
                f"Falling back to {fallback_model}."
            )
            try:
                self.llm = _build_llm(fallback_model, temperature=0.1)
                print(f"[Init] LLM loaded: {fallback_model}")
            except Exception as fallback_exc:
                raise RuntimeError(
                    f"Unable to initialize LLM '{model_name}' or fallback "
                    f"'{fallback_model}'. Make sure Ollama is running and "
                    f"'{fallback_model}' is pulled (`ollama pull {fallback_model}`). "
                    f"Original error: {exc}. "
                    f"Fallback error: {fallback_exc}"
                ) from fallback_exc
        self._ctx_builder = ContextualQueryBuilder()
        # Embedding function reused for context-similarity checks
        self._embed_fn = vector_store._embedding_function
        # Collect all corpus docs once (for recall denominator and BM25 index)
        texts, metadatas = get_texts_and_metadatas()
        self.all_docs = [
            Document(page_content=t, metadata=m)
            for t, m in zip(texts, metadatas)
        ]
        # Build BM25 index for hybrid search (gracefully skipped if rank_bm25
        # is not installed)
        self._bm25_index: BM25Index | None = build_bm25_index(self.all_docs)
        if self._bm25_index is not None:
            print("[Init] BM25 index built for hybrid search.")
        else:
            print("[Init] rank_bm25 not installed; using vector-only retrieval.")

        # Multimodal extension: optional FAISS image index + CLIP embedder
        self._image_index = image_index
        self._clip_embedder: "_CLIPEmbedder | None" = None
        self._image_captioner: "_ImageCaptioner | None" = None
        if self._image_index is not None and _MULTIMODAL_AVAILABLE:
            try:
                self._clip_embedder = _CLIPEmbedder()
                print("[Init] CLIP embedder loaded for multimodal retrieval.")
            except Exception as exc:
                print(f"[Init] CLIP embedder unavailable: {exc}")
                self._clip_embedder = None

    # ── Public entry point ────────────────────────────────────────────────────

    def _context_similarity(self, query: str, context_text: str) -> float:
        """Compute cosine similarity between *query* and *context_text*.

        Uses the same BGE embedding model that powers the vector store so that
        similarity scores are consistent with the retrieval pipeline.  Returns
        1.0 (assume in-context) on any embedding failure so that errors never
        silently block normal retrieval.
        """
        try:
            q_vec = self._embed_fn.embed_query(query)
            c_vec = self._embed_fn.embed_query(context_text)
            return _cosine_similarity(q_vec, c_vec)
        except Exception:
            return 1.0

    def run(
        self,
        user_query: str,
        memory: ConversationMemory,
        topic_manager: TopicMemoryManager | None = None,
        image_input: bytes | None = None,
    ) -> PipelineResult:
        """
        Execute the full contextual RAG pipeline for one user query.

        Args:
            user_query:    Raw text typed by the user.
            memory:        Current conversation memory (mutated in-place).
            topic_manager: Optional topic memory manager (mutated in-place).
                           Pass ``None`` to skip topic-manager tracking.
            image_input:   Optional raw image bytes (PNG/JPEG).  When provided,
                           the image is encoded with CLIP and used to retrieve
                           relevant images from the image index.  The resulting
                           captions are fused into the SLM context.

        Returns:
            PipelineResult with answer, metrics, and step log.
        """
        import time as _time
        _run_start = _time.time()

        result = PipelineResult(
            query=user_query,
            rewritten_query=user_query,
            detected_topic=None,
            detected_subject=None,
            ambiguous_terms=[],
            clarification_needed=False,
            clarification_message=None,
            retrieved_docs=[],
            answer="",
            metrics={},
            retrieval_score=0.0,
            mode="RAG",
            token_counts={},
        )

        # ── Step 1: Receive question ──────────────────────────────────────────
        result.log(1, f"User question received: '{user_query}'")
        result.tag_log("Query", user_query)

        # ── Step 2: Conversation memory ───────────────────────────────────────
        last_topic = memory.get_last_topic()
        recent_topics = memory.get_recent_topics()
        active_topic = (
            topic_manager.get_active_topic() if topic_manager else last_topic
        )
        result.log(
            2,
            f"Conversation memory → last topic: '{last_topic}' | "
            f"recent: {recent_topics} | "
            f"active (with decay): '{active_topic}'",
        )

        # ── Context Drift Detection ───────────────────────────────────────────
        # Bugfix: if the query contains a pronoun and we have a last topic,
        # skip the drift check entirely and force-resolve to the last topic.
        # This prevents "what are its components" from clearing nitrogen-cycle memory.
        _PRONOUNS = frozenset({"it", "its", "they", "their", "this", "that", "these", "those"})
        query_tokens_lower = set(re.findall(r"\b[a-z]+\b", user_query.lower()))
        has_pronoun = bool(query_tokens_lower & _PRONOUNS)

        if has_pronoun and last_topic:
            result.log(
                2,
                f"Pronoun detected — skipping drift check, "
                f"resolving to last topic: '{last_topic}'",
            )
            # Rewrite the query to make the topic explicit for retrieval.
            # Replace only the first pronoun occurrence to avoid over-substitution
            # (e.g. "what are its components and their functions" keeps "their").
            pronoun_rewritten = re.sub(
                r"\b(it|its|they|their|this|that|these|those)\b",
                last_topic,
                user_query,
                count=1,
                flags=re.IGNORECASE,
            ).strip()
            result.rewritten_query = pronoun_rewritten

        # Check for follow-up BEFORE drift detection
        # Follow-up queries must never trigger drift detection; they always
        # continue the last topic regardless of low cosine similarity.
        _FOLLOWUP_SKIP_WORDS: set[str] = {
            "it", "its", "this", "that", "these", "those",
            "they", "their", "advantages", "disadvantages",
            "limitations", "example", "examples", "explain",
            "why", "how", "what", "applications", "uses",
            "difference", "compare", "summarize", "elaborate",
        }
        query_tokens_set = set(user_query.lower().split())
        is_likely_followup = (
            len(query_tokens_set) <= 5
            and bool(query_tokens_set & _FOLLOWUP_SKIP_WORDS)
            and memory.get_last_topic() is not None
        )

        if is_likely_followup:
            result.log(2, "Follow-up query detected — skipping drift check")

        # Bugfix (Bug 3): detect pure follow-up patterns (e.g. "advantages",
        # "examples") that carry no topic by themselves.  These must never
        # trigger drift detection; the last memory topic will be reused.
        query_stripped = user_query.lower().strip().rstrip("?")
        is_pure_followup = any(
            query_stripped == pattern or query_stripped.startswith(pattern)
            for pattern in _PURE_FOLLOWUP_PATTERNS
        )
        if is_pure_followup and memory.get_last_topic():
            result.log(
                2,
                f"Pure follow-up detected — skipping ALL drift checks, "
                f"using last topic: '{memory.get_last_topic()}'",
            )

        # Compare the current query to the last conversation turn.  If the
        # similarity is below the threshold the user has shifted to an
        # unrelated topic: clear context and answer directly from the LLM.
        if memory.history and not (is_likely_followup or (is_pure_followup and memory.get_last_topic())):
            last_turn = list(memory.history)[-1]
            last_context_text = last_turn.user_query
            if last_turn.resolved_topic:
                last_context_text += f" {last_turn.resolved_topic}"

            ctx_sim = self._context_similarity(user_query, last_context_text)
            result.context_similarity = ctx_sim
            result.log(
                2,
                f"Context similarity to last turn: {ctx_sim:.4f} "
                f"(threshold: {CONTEXT_SIMILARITY_THRESHOLD})",
            )
            result.tag_log("Context Similarity", f"{ctx_sim:.4f}")

            if ctx_sim < CONTEXT_SIMILARITY_THRESHOLD:
                result.log(
                    2,
                    "Context drift detected — clearing conversation context "
                    "and switching to LLM fallback.",
                )
                memory.clear()
                if topic_manager is not None:
                    topic_manager.update(None)

                result.mode = "LLM Fallback"
                _pipeline_stats["fallback_triggers"] += 1

                # ── Step 9 (fast-path): answer from LLM only ─────────────────
                prompt_text = LLM_FALLBACK_PROMPT.format(question=user_query)
                result.log(
                    9,
                    "Mode LLM Fallback (context drift): answering from "
                    "Phi-3 knowledge only (no retrieved context) …",
                )
                result.tag_log("Mode", result.mode)
                try:
                    answer = self.llm.invoke(prompt_text)
                except Exception as e:
                    answer = f"[Error generating answer: {e}]"
                result.answer = _extract_answer_text(answer).strip()
                result.log(10, f"Answer generated ({len(result.answer)} chars).")

                # ── Token counting ────────────────────────────────────────────
                input_tokens = _count_tokens(prompt_text)
                output_tokens = _count_tokens(result.answer)
                total_tokens = input_tokens + output_tokens
                result.token_counts = {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": total_tokens,
                }
                result.tag_log(
                    "Tokens Used",
                    f"input={input_tokens}, output={output_tokens}, "
                    f"total={total_tokens}",
                )

                # ── Update pipeline stats ─────────────────────────────────────
                _pipeline_stats["total_queries"] += 1
                result.tag_log(
                    "Pipeline Stats",
                    f"total={_pipeline_stats['total_queries']}, "
                    f"fallbacks={_pipeline_stats['fallback_triggers']}, "
                    f"clarifications={_pipeline_stats['clarifications_requested']}",
                )

                # Bugfix (Bug 2): extract topic from query even for out-of-scope
                # questions so follow-up turns can resolve pronoun/topic references.
                fallback_topic = _extract_query_topic(user_query)
                memory.add_turn(
                    user_query=user_query,
                    resolved_topic=fallback_topic,
                    answer_snippet=result.answer[:120],
                )
                if topic_manager is not None:
                    topic_manager.update(fallback_topic)
                result.detected_topic = fallback_topic
                result.latency_ms = (_time.time() - _run_start) * 1000
                return result

        # ── Step 2b: Out-of-scope pre-validation ──────────────────────────────
        # Check if query is outside the knowledge base BEFORE calling the LLM.
        # Bugfix: pre-score topic confidence here so the out-of-scope check can
        # respect a strong in-scope signal (edge case: "car battery" → electricity).
        _pre_confidence = self._ctx_builder._scorer.score(user_query.lower())
        oos_detected, oos_word = self._ctx_builder._is_out_of_scope(
            user_query, _pre_confidence
        )
        if oos_detected:
            result.log(
                2,
                f"[Step 2b] Out-of-scope detected: '{oos_word}' not in knowledge base",
            )
            result.mode = "Out of Scope"
            result.answer = (
                f"This question appears to be outside my knowledge base which "
                f"covers educational science and mathematics topics. "
                f"I found '{oos_word}' in your query which is not a topic I cover. "
                f"Could you ask about: water cycle, photosynthesis, nitrogen cycle, "
                f"genetics, electricity, or any other science/maths topic?"
            )
            _pipeline_stats["total_queries"] += 1
            result.tag_log(
                "Pipeline Stats",
                f"total={_pipeline_stats['total_queries']}, "
                f"fallbacks={_pipeline_stats['fallback_triggers']}, "
                f"clarifications={_pipeline_stats['clarifications_requested']}",
            )
            memory.add_turn(
                user_query=user_query,
                resolved_topic=None,
                answer_snippet=result.answer[:120],
            )
            result.latency_ms = (_time.time() - _run_start) * 1000
            return result

        # ── Step 3: Contextual Query Builder ──────────────────────────────────
        ctx_result = self._ctx_builder.build(user_query, memory)

        # Followup handling — log and tag when the builder resolved via memory
        if ctx_result.ambiguity_result.resolution_source == "followup_memory":
            result.log(
                3,
                f"Follow-up query detected → resolved to last topic "
                f"'{ctx_result.resolved_topic}' | "
                f"rewritten: '{ctx_result.rewritten_query}'",
            )
            result.tag_log("Query", f"[Follow-up] {ctx_result.rewritten_query}")

        shift_info = (
            f" ({ctx_result.ambiguity_result.shift_reason})"
            if ctx_result.ambiguity_result.shift_detected
            else ""
        )
        result.log(
            3,
            f"Contextual Query Builder → "
            f"normalised: '{ctx_result.normalized_query}' | "
            f"topic confidence: {ctx_result.topic_confidence.top_topic!r} "
            f"(score={ctx_result.topic_confidence.top_score}) | "
            f"topic switched: {ctx_result.topic_switched} | "
            f"shift detected: {ctx_result.ambiguity_result.shift_detected}"
            + shift_info,
        )
        for note in ctx_result.debug_notes:
            result.log(3, f"  → {note}")

        # The contextually rewritten query is used for all downstream steps
        ctx_rewritten = ctx_result.rewritten_query
        ctx_topic = ctx_result.resolved_topic

        # ── Step 3b: Post-rewrite sanity check ────────────────────────────────
        # Bugfix: reject rewrites that contradict strong content words in the
        # original query (e.g. original="how car moves", rewritten contains
        # "bicycle" but "car" is an out-of-scope word unrelated to bicycle).
        _rewrite_rejected = False
        if ctx_topic is not None:
            original_tokens = set(re.findall(r"\b[a-z]+\b", user_query.lower()))
            # Check if any original word belongs to a DIFFERENT topic's keywords
            # than the resolved topic, or is an out-of-scope signal word
            ctx_topic_kw_tokens: set[str] = {
                tok
                for kw in TOPIC_KEYWORD_WEIGHTS.get(ctx_topic, {})
                for tok in kw.split()
            }
            for orig_word in original_tokens:
                if orig_word in OUT_OF_SCOPE_SIGNALS:
                    # Contradiction: original query has an out-of-scope word
                    # but rewriter picked an in-scope topic — reject
                    result.log(
                        3,
                        f"[Step 3b] Rewrite rejected — contradiction detected "
                        f"('{orig_word}' is out-of-scope but rewrite resolved to "
                        f"'{ctx_topic}'), reverting to original query",
                    )
                    ctx_rewritten = user_query
                    ctx_topic = None
                    _rewrite_rejected = True
                    break
        if not _rewrite_rejected:
            result.log(3, f"[Step 3b] Rewrite validated: '{ctx_rewritten}'")

        # ── Step 4: Ambiguity detection (on the rewritten query) ──────────────
        # After the ContextualQueryBuilder the query is usually already resolved;
        # this step handles any remaining ambiguity that slipped through.
        ambiguous = get_ambiguous_terms(ctx_rewritten)
        result.ambiguous_terms = ambiguous
        result.log(4, f"Ambiguity detection → terms: {ambiguous or 'none'}")

        resolved_from_ambiguity: str | None = ctx_topic
        needs_clarification = False

        if ambiguous and not ctx_topic:
            for term in ambiguous:
                resolved = disambiguate_with_signals(term, ctx_rewritten)
                if resolved:
                    result.log(
                        4, f"  → '{term}' resolved via signals → '{resolved}'"
                    )
                    resolved_from_ambiguity = resolved
                    break

                if last_topic and last_topic in AMBIGUOUS_TERMS.get(term, []):
                    resolved_from_ambiguity = last_topic
                    result.log(
                        4,
                        f"  → '{term}' resolved via memory → '{last_topic}'",
                    )
                    break

                # Still unresolved → request clarification
                options_str = ", ".join(AMBIGUOUS_TERMS.get(term, []))
                result.clarification_needed = True
                result.clarification_message = CLARIFICATION_MSG.format(
                    term=term, options=options_str
                )
                result.log(
                    4,
                    f"  → '{term}' still ambiguous (options: {options_str}). "
                    "Requesting clarification.",
                )
                needs_clarification = True
                break

        if needs_clarification:
            _pipeline_stats["clarifications_requested"] += 1
            memory.add_turn(user_query=user_query, resolved_topic=None)
            result.latency_ms = (_time.time() - _run_start) * 1000
            return result

        # ── Compound-query detection (log only; LLM handles both parts) ────────
        if _is_compound_query(ctx_rewritten):
            result.log(
                4,
                "Compound query detected (contains conjunction). "
                "The model will address all parts together.",
            )

        # ── Step 5: Query classification ──────────────────────────────────────
        classification = classify_query(ctx_rewritten)
        topic_from_classifier = classification["topic"]
        subject_from_classifier = classification["subject"]
        result.log(
            5,
            f"Query classification → subject: '{subject_from_classifier}' "
            f"(score={classification['subject_score']}), "
            f"topic: '{topic_from_classifier}' "
            f"(score={classification['topic_score']})",
        )

        # ── Step 6: Glossary mapping ───────────────────────────────────────────
        enriched_query, topic_from_glossary = expand_query(ctx_rewritten)
        result.log(
            6,
            f"Glossary mapping → topic from glossary: '{topic_from_glossary}' | "
            f"enriched query: '{enriched_query}'",
        )

        # ── Determine final topic ─────────────────────────────────────────────
        # Priority: contextual builder > classifier (high confidence) > glossary > memory
        final_topic = resolved_from_ambiguity or topic_from_glossary or last_topic
        final_subject = subject_from_classifier

        if (
            topic_from_classifier
            and classification["topic_score"] >= 2
            and detect_topic_shift(topic_from_classifier, final_topic)
        ):
            final_topic = topic_from_classifier
            result.log(
                5, f"  → High-confidence classifier topic overrides: '{final_topic}'"
            )

        result.detected_topic = final_topic
        result.detected_subject = final_subject

        # Choose best query for retrieval: prefer the enriched glossary query
        retrieval_query = enriched_query
        result.rewritten_query = retrieval_query

        # ── Step 7: Retrieval (mode: hybrid / vector_only / bm25_only) ──────────
        result.log(
            7,
            f"Retrieval mode={self.retrieval_mode} "
            f"(top-{RETRIEVAL_CANDIDATES} candidates) on: '{retrieval_query}' "
            f"| topic route: '{final_topic or 'none'}'",
        )
        if self.retrieval_mode == "vector_only":
            retrieved = retrieve_top_k(
                self.vector_store,
                retrieval_query,
                k=self.top_k,
                topic_filter=final_topic,
            )
        elif self.retrieval_mode == "bm25_only" and self._bm25_index is not None:
            bm25_hits = self._bm25_index.search(retrieval_query, k=self.top_k)
            retrieved = [doc for doc, _ in bm25_hits]
        else:  # "hybrid" (default) or bm25_only fallback when index unavailable
            retrieved = hierarchical_retrieve(
                vector_store=self.vector_store,
                bm25_index=self._bm25_index,
                query=retrieval_query,
                topic=final_topic,
                k=self.top_k,
                use_cross_encoder=self.use_cross_encoder,
            )
        result.log(7, f"Retrieved {len(retrieved)} document(s) after reranking.")

        # ── Step 7b: Multimodal image retrieval ───────────────────────────────
        # Uses the CLIP image index when available.  For image queries the
        # uploaded image is encoded with CLIP; for text queries the query itself
        # is encoded with the CLIP text encoder so that relevant images can still
        # be surfaced.  Captions from matching images are later fused into the
        # SLM context.
        _image_hits: list = []
        uploaded_image_caption: str | None = None
        uploaded_image_captions: list[str] = []
        if image_input is not None and _MULTIMODAL_AVAILABLE:
            try:
                import io as _io
                from PIL import Image as _PILImg  # type: ignore[import]
                if self._image_captioner is None:
                    self._image_captioner = _ImageCaptioner()
                pil_img_for_caption = _PILImg.open(_io.BytesIO(image_input)).convert("RGB")
                uploaded_image_caption = self._image_captioner.caption(pil_img_for_caption)
                if uploaded_image_caption:
                    result.log(7, "Step 7b: Generated caption from uploaded image")
            except Exception as exc:
                result.log(7, f"Step 7b: Uploaded-image captioning error — {exc}")

        if self._image_index is not None and self._clip_embedder is not None:
            try:
                if image_input is not None:
                    # Image query path: encode the uploaded image with CLIP
                    import io as _io
                    from PIL import Image as _PILImg  # type: ignore[import]
                    pil_img = _PILImg.open(_io.BytesIO(image_input)).convert("RGB")
                    query_vec = self._clip_embedder.embed_image(pil_img)
                    result.log(
                        7,
                        "Step 7b: Image input — encoded with CLIP image encoder",
                    )
                else:
                    # Text query path: encode query text with CLIP text encoder
                    query_vec = self._clip_embedder.embed_text(retrieval_query)
                    result.log(
                        7,
                        "Step 7b: Text query — searching image index with CLIP "
                        "text encoder",
                    )
                _image_hits = self._image_index.search(query_vec, k=3)
                caption_count = sum(1 for rec, _ in _image_hits if rec.caption)
                result.log(
                    7,
                    f"Step 7b: Retrieved {len(_image_hits)} image(s), "
                    f"{caption_count} with caption(s)",
                )
                result.image_captions = [
                    rec.caption for rec, _ in _image_hits if rec.caption
                ]
            except Exception as exc:
                result.log(7, f"Step 7b: Image retrieval error — {exc}")
        if uploaded_image_caption:
            if uploaded_image_caption not in result.image_captions:
                result.image_captions.insert(0, uploaded_image_caption)
            uploaded_image_captions.append(uploaded_image_caption)
        result.has_image_context = bool(result.image_captions)

        # ── Determine retrieval similarity score and pipeline mode ────────────
        try:
            score_hits = self.vector_store.similarity_search_with_relevance_scores(
                retrieval_query, k=1
            )
            top_score = score_hits[0][1] if score_hits else 0.0
        except Exception:
            top_score = 0.0

        result.retrieval_score = top_score
        # Bugfix (Bug 1): Three-mode decision instead of two.
        # Partial RAG uses retrieved docs even when score is below the full
        # RAG threshold, rather than discarding them entirely.
        if top_score >= RAG_SIMILARITY_THRESHOLD:
            result.mode = "RAG"
        elif top_score >= PARTIAL_RAG_THRESHOLD and retrieved:
            result.mode = "Partial RAG"
        else:
            result.mode = "LLM Fallback"
        result.tag_log("Retrieval Score", f"{top_score:.4f} (threshold: {RAG_SIMILARITY_THRESHOLD})")
        result.tag_log("Mode", f"{result.mode} (score={top_score:.3f})")

        # ── Step 8: Top-K document selection ──────────────────────────────────
        result.retrieved_docs = retrieved[: self.top_k]
        result.log(8, f"Selected {len(result.retrieved_docs)} top-K documents:")
        for i, doc in enumerate(result.retrieved_docs, 1):
            meta = doc.metadata
            snippet = doc.page_content[:80].replace("\n", " ")
            result.log(
                8,
                f"  [{i}] topic={meta.get('topic')} | grade={meta.get('grade')} "
                f"| '{snippet}…'",
            )

        # ── Step 9: SLM generation ────────────────────────────────────────────
        if result.mode == "RAG":
            # RAG Improvement 15: use context budget manager
            # Multimodal: fuse image captions within remaining token budget
            if result.has_image_context and _MULTIMODAL_AVAILABLE:
                context = _build_multimodal_context_with_budget(
                    result.retrieved_docs,
                    _image_hits,
                    self.model_name,
                    additional_captions=uploaded_image_captions,
                )
                prompt_text = MULTIMODAL_PROMPT.format(context=context, question=user_query)
                result.log(
                    9,
                    "Mode RAG (multimodal): fused text + image captions "
                    "(budget-capped) sent to SLM …",
                )
            else:
                context = _build_context_with_budget(result.retrieved_docs, self.model_name)
                prompt_text = RAG_PROMPT.format(context=context, question=user_query)
                result.log(9, "Mode RAG: sending context + question to Phi-3 via Ollama …")
        elif result.mode == "Partial RAG":
            # Bugfix (Bug 1): use retrieved docs even when score is below the
            # full RAG threshold instead of discarding them entirely.
            # RAG Improvement 15: use context budget manager
            # Multimodal: fuse image captions within remaining token budget
            if result.has_image_context and _MULTIMODAL_AVAILABLE:
                context = _build_multimodal_context_with_budget(
                    result.retrieved_docs,
                    _image_hits,
                    self.model_name,
                    additional_captions=uploaded_image_captions,
                )
                prompt_text = MULTIMODAL_PROMPT.format(context=context, question=user_query)
                result.log(
                    9,
                    "Mode Partial RAG (multimodal): fused text + image captions "
                    "(budget-capped) …",
                )
            else:
                context = _build_context_with_budget(result.retrieved_docs, self.model_name)
                prompt_text = PARTIAL_CONTEXT_PROMPT.format(context=context, question=user_query)
            result.log(
                9,
                "Mode Partial RAG: partial context sent to Phi-3 "
                "(score below RAG threshold but above partial threshold) …",
            )
        else:
            _pipeline_stats["fallback_triggers"] += 1
            if _is_vague_query(user_query):
                prompt_text = VAGUE_QUERY_PROMPT.format(query=user_query)
                result.log(
                    9,
                    "Mode LLM Fallback (vague query): requesting multiple "
                    "interpretations from Phi-3 …",
                )
            else:
                prompt_text = LLM_FALLBACK_PROMPT.format(question=user_query)
                result.log(
                    9,
                    "Mode LLM Fallback: low retrieval score — answering directly "
                    "from Phi-3 knowledge (no retrieved context) …",
                )

        try:
            answer = self.llm.invoke(prompt_text)
        except Exception as e:
            answer = f"[Error generating answer: {e}]"

        result.answer = _extract_answer_text(answer).strip()
        result.log(10, f"Answer generated ({len(result.answer)} chars).")

        # RAG Improvement 14: Compute grounding score
        grounding_score = _compute_grounding_score(result.answer, result.retrieved_docs)
        result.grounding_score = grounding_score
        if grounding_score < MIN_GROUNDING_THRESHOLD and result.mode == "RAG":
            print(f"  [Grounding] ⚠ Low grounding score: {grounding_score:.3f}")

        # ── Token counting ────────────────────────────────────────────────────
        input_tokens = _count_tokens(prompt_text)
        output_tokens = _count_tokens(result.answer)
        total_tokens = input_tokens + output_tokens
        result.token_counts = {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
        }
        result.tag_log(
            "Tokens Used",
            f"input={input_tokens}, output={output_tokens}, total={total_tokens}",
        )

        # ── Step 10: Evaluation metrics ───────────────────────────────────────
        result.metrics = compute_all_metrics(
            query=retrieval_query,
            answer=result.answer,
            retrieved_docs=result.retrieved_docs,
            all_docs=self.all_docs,
            query_topic=final_topic,
            k=self.top_k,
            mode=result.mode,
        )

        # Research addition: optional MLflow logging (no-op when mlflow is not installed)
        # Bugfix: end any existing run first to avoid nested run errors, then open a
        # fresh named run so metrics are always recorded correctly.
        if _MLFLOW_AVAILABLE:
            try:
                try:
                    _mlflow.end_run()
                except Exception:
                    pass
                with _mlflow.start_run(run_name=f"{self.model_name}_top{self.top_k}"):
                    _mlflow.log_param("model", self.model_name)
                    _mlflow.log_param("top_k", self.top_k)
                    _mlflow.log_param("retrieval_mode", self.retrieval_mode)
                    _mlflow.log_param("pipeline_mode", result.mode)
                    _mlflow.log_param("query_topic", str(final_topic))
                    for metric_name, metric_value in result.metrics.items():
                        safe_name = metric_name.replace("@", "_at_").replace(" ", "_")
                        _mlflow.log_metric(safe_name, metric_value)
            except Exception as mlflow_error:
                print(f"[MLflow] Logging skipped: {mlflow_error}")

        # ── Update pipeline stats and log ─────────────────────────────────────
        _pipeline_stats["total_queries"] += 1
        result.tag_log(
            "Pipeline Stats",
            f"total={_pipeline_stats['total_queries']}, "
            f"fallbacks={_pipeline_stats['fallback_triggers']}, "
            f"clarifications={_pipeline_stats['clarifications_requested']}",
        )

        # ── Update memory and topic manager ───────────────────────────────────
        # Bugfix (Bug 2): for LLM Fallback, extract a topic from the raw query
        # so follow-up turns can resolve "it"/"advantages of it" etc. correctly.
        if result.mode == "LLM Fallback":
            fallback_topic = _extract_query_topic(user_query) or final_topic
            memory.add_turn(
                user_query=user_query,
                resolved_topic=fallback_topic,
                answer_snippet=result.answer[:120],
            )
            if topic_manager is not None:
                topic_manager.update(fallback_topic, subject=final_subject or "", grade="")
            result.detected_topic = fallback_topic
        else:
            memory.add_turn(
                user_query=user_query,
                resolved_topic=final_topic,
                answer_snippet=result.answer[:120],
            )
            if topic_manager is not None:
                topic_manager.update(final_topic, subject=final_subject or "", grade="")

        result.latency_ms = (_time.time() - _run_start) * 1000
        return result


# Research addition: multi-model comparison helper
def run_model_comparison(
    queries: list[str],
    models: list[str] | None = None,
    vector_store: "Chroma | None" = None,
    top_k: int = TOP_K,
) -> dict[str, dict]:
    """
    Run the same list of queries through multiple Ollama models and return
    averaged evaluation metrics per model for comparison.

    Args:
        queries:      List of plain-text queries to evaluate.
        models:       List of Ollama model names.  Defaults to MODELS_TO_EVALUATE.
        vector_store: A pre-built Chroma vector store.  If None the store is
                      built fresh (slow — provide one when calling repeatedly).
        top_k:        Number of documents to retrieve per query.

    Returns:
        Dict mapping model_name → {"avg_metrics": {...}, "per_query": [...]}
    """
    from retriever import build_vector_store as _build_vs
    from context_memory import ConversationMemory
    from topic_memory_manager import TopicMemoryManager

    if models is None:
        models = MODELS_TO_EVALUATE

    if vector_store is None:
        vector_store = _build_vs(persist=True)

    comparison: dict[str, dict] = {}

    for model_name in models:
        print(f"\n[Model Comparison] Running model: {model_name} …")
        try:
            pipeline = RAGPipeline(
                vector_store=vector_store,
                model_name=model_name,
                top_k=top_k,
            )
        except Exception as exc:
            comparison[model_name] = {"error": str(exc), "avg_metrics": {}, "per_query": []}
            print(f"  [Model Comparison] Failed to load {model_name}: {exc}")
            continue

        per_query: list[dict] = []
        all_metrics: list[dict] = []

        for query in queries:
            memory = ConversationMemory(max_turns=5)
            topic_manager = TopicMemoryManager()
            try:
                result = pipeline.run(
                    user_query=query,
                    memory=memory,
                    topic_manager=topic_manager,
                )
                per_query.append({"query": query, "metrics": result.metrics})
                if result.metrics:
                    all_metrics.append(result.metrics)
            except Exception as exc:
                per_query.append({"query": query, "error": str(exc), "metrics": {}})

        avg_metrics: dict[str, float] = {}
        if all_metrics:
            for key in all_metrics[0]:
                avg_metrics[key] = round(
                    sum(m[key] for m in all_metrics) / len(all_metrics), 3
                )

        comparison[model_name] = {"avg_metrics": avg_metrics, "per_query": per_query}
        print(f"  [Model Comparison] {model_name} done. Avg metrics: {avg_metrics}")

    return comparison
