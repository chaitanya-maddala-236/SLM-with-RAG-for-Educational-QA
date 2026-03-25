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
from contextual_query_builder import ContextualQueryBuilder
from query_classifier import classify_query, detect_topic_shift
from glossary_mapper import (
    get_ambiguous_terms,
    disambiguate_with_signals,
    expand_query,
    AMBIGUOUS_TERMS,
)
from retriever import (
    build_bm25_index,
    hybrid_search,
    hierarchical_retrieve,
    BM25Index,
)
from evaluation import compute_all_metrics
from data_loader import get_texts_and_metadatas

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

TOP_K = 5          # number of documents to return after reranking
RETRIEVAL_CANDIDATES = 20   # wider pool fetched before reranking
# Similarity threshold: scores at or above this use RAG mode; below → LLM Fallback
RAG_SIMILARITY_THRESHOLD: float = 0.6
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

# ── Conjunction pattern for compound-query detection ─────────────────────────
_COMPOUND_RE = re.compile(
    r"\b(and|also|additionally|furthermore|as well as|plus)\b", re.IGNORECASE
)


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

    def log(self, step: int, message: str) -> None:
        entry = f"[Step {step:>2}] {message}"
        self.step_log.append(entry)
        print(entry)

    def tag_log(self, tag: str, message: str) -> None:
        """Emit a labelled console log line and record it in step_log."""
        entry = f"[{tag}] {message}"
        self.step_log.append(entry)
        print(entry)


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
    ) -> None:
        self.vector_store = vector_store
        self.top_k = top_k
        self.llm = OllamaLLM(model=model_name, temperature=0.1)
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
    ) -> PipelineResult:
        """
        Execute the full contextual RAG pipeline for one user query.

        Args:
            user_query:     Raw text typed by the user.
            memory:         Current conversation memory (mutated in-place).
            topic_manager:  Optional topic memory manager (mutated in-place).
                            Pass ``None`` to skip topic-manager tracking.

        Returns:
            PipelineResult with answer, metrics, and step log.
        """
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
        # Compare the current query to the last conversation turn.  If the
        # similarity is below the threshold the user has shifted to an
        # unrelated topic: clear context and answer directly from the LLM.
        if memory.history:
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
                result.answer = answer.strip()
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

                # Record the turn so future turns have a reference point
                memory.add_turn(
                    user_query=user_query,
                    resolved_topic=None,
                    answer_snippet=result.answer[:120],
                )
                return result

        # ── Step 3: Contextual Query Builder ──────────────────────────────────
        ctx_result = self._ctx_builder.build(user_query, memory)
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

        # ── Step 7: Hierarchical retrieval (topic-route → hybrid BM25+vector) ──
        result.log(
            7,
            f"Hierarchical retrieval (top-{RETRIEVAL_CANDIDATES} candidates, "
            f"hybrid BM25+vector) on: '{retrieval_query}' "
            f"| topic route: '{final_topic or 'none'}'",
        )
        retrieved = hierarchical_retrieve(
            vector_store=self.vector_store,
            bm25_index=self._bm25_index,
            query=retrieval_query,
            topic=final_topic,
            k=self.top_k,
        )
        result.log(7, f"Retrieved {len(retrieved)} document(s) after reranking.")

        # ── Determine retrieval similarity score and pipeline mode ────────────
        try:
            score_hits = self.vector_store.similarity_search_with_relevance_scores(
                retrieval_query, k=1
            )
            top_score = score_hits[0][1] if score_hits else 0.0
        except Exception:
            top_score = 0.0

        result.retrieval_score = top_score
        result.mode = "RAG" if top_score >= RAG_SIMILARITY_THRESHOLD else "LLM Fallback"
        result.tag_log("Retrieval Score", f"{top_score:.4f} (threshold: {RAG_SIMILARITY_THRESHOLD})")
        result.tag_log("Mode", result.mode)

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
            context = "\n\n".join(
                f"[Doc {i+1}] {doc.page_content}"
                for i, doc in enumerate(result.retrieved_docs)
            )
            prompt_text = RAG_PROMPT.format(context=context, question=user_query)
            result.log(9, "Mode RAG: sending context + question to Phi-3 via Ollama …")
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

        result.answer = answer.strip()
        result.log(10, f"Answer generated ({len(result.answer)} chars).")

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
        if _MLFLOW_AVAILABLE:
            try:
                with _mlflow.start_run(nested=True):
                    _mlflow.log_param("model_name", self.llm.model)
                    _mlflow.log_param("top_k", self.top_k)
                    _mlflow.log_param(
                        "retrieval_mode",
                        "hybrid" if self._bm25_index is not None else "vector",
                    )
                    for metric_name, metric_val in result.metrics.items():
                        # MLflow metric names must not contain '@'; replace with '_at_'
                        _mlflow.log_metric(metric_name.replace("@", "_at_"), metric_val)
                    _mlflow.set_tag("query_topic", str(final_topic or "unknown"))
                    _mlflow.set_tag("pipeline_mode", result.mode)
            except Exception:
                pass  # MLflow errors must never crash the pipeline

        # ── Update pipeline stats and log ─────────────────────────────────────
        _pipeline_stats["total_queries"] += 1
        result.tag_log(
            "Pipeline Stats",
            f"total={_pipeline_stats['total_queries']}, "
            f"fallbacks={_pipeline_stats['fallback_triggers']}, "
            f"clarifications={_pipeline_stats['clarifications_requested']}",
        )

        # ── Update memory and topic manager ───────────────────────────────────
        memory.add_turn(
            user_query=user_query,
            resolved_topic=final_topic,
            answer_snippet=result.answer[:120],
        )
        if topic_manager is not None:
            topic_manager.update(final_topic)

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
