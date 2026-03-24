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

from dataclasses import dataclass, field
from langchain.schema import Document
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma

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
from retriever import retrieve_top_k
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

TOP_K = 5          # number of documents to retrieve
CLARIFICATION_MSG = (
    "I found the term '{term}' in your question, which could mean: {options}. "
    "Could you clarify which one you meant?"
)


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

    def log(self, step: int, message: str) -> None:
        entry = f"[Step {step:>2}] {message}"
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
        self.llm = Ollama(model=model_name, temperature=0.1)
        self._ctx_builder = ContextualQueryBuilder()
        # Collect all corpus docs once (for recall denominator)
        texts, metadatas = get_texts_and_metadatas()
        self.all_docs = [
            Document(page_content=t, metadata=m)
            for t, m in zip(texts, metadatas)
        ]

    # ── Public entry point ────────────────────────────────────────────────────

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
        )

        # ── Step 1: Receive question ──────────────────────────────────────────
        result.log(1, f"User question received: '{user_query}'")

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

        # ── Step 3: Contextual Query Builder ──────────────────────────────────
        ctx_result = self._ctx_builder.build(user_query, memory)
        result.log(
            3,
            f"Contextual Query Builder → "
            f"normalised: '{ctx_result.normalized_query}' | "
            f"topic confidence: {ctx_result.topic_confidence.top_topic!r} "
            f"(score={ctx_result.topic_confidence.top_score}) | "
            f"topic switched: {ctx_result.topic_switched}",
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
            memory.add_turn(user_query=user_query, resolved_topic=None)
            return result

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

        # ── Step 7: Vector retrieval ──────────────────────────────────────────
        result.log(7, f"Vector retrieval (top-{self.top_k}) on: '{retrieval_query}'")
        retrieved = retrieve_top_k(
            self.vector_store,
            retrieval_query,
            k=self.top_k,
            topic_filter=final_topic,
        )
        result.log(7, f"Retrieved {len(retrieved)} document(s) from Chroma.")

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
        context = "\n\n".join(
            f"[Doc {i+1}] {doc.page_content}"
            for i, doc in enumerate(result.retrieved_docs)
        )
        prompt_text = RAG_PROMPT.format(context=context, question=user_query)
        result.log(9, "Sending context + question to Phi-3 via Ollama …")

        try:
            answer = self.llm.invoke(prompt_text)
        except Exception as e:
            answer = f"[Error generating answer: {e}]"

        result.answer = answer.strip()
        result.log(10, f"Answer generated ({len(result.answer)} chars).")

        # ── Step 10: Evaluation metrics ───────────────────────────────────────
        result.metrics = compute_all_metrics(
            query=retrieval_query,
            answer=result.answer,
            retrieved_docs=result.retrieved_docs,
            all_docs=self.all_docs,
            query_topic=final_topic,
            k=self.top_k,
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


# ── Helper: query rewriting ───────────────────────────────────────────────────

def _rewrite_query(
    original_query: str,
    resolved_topic: str | None,
    memory: ConversationMemory,
) -> str:
    """
    Rewrite the user query by:
    1. Appending the resolved topic (if any) to make retrieval more precise.
    2. Replacing very short queries ('what is it?', 'explain it') with a
       topic-anchored version using conversation memory.
    """
    query_lower = original_query.lower().strip()

    # Short / underspecified queries: replace with topic-aware version
    vague_prefixes = ("what is it", "explain it", "tell me more", "how does it",
                      "what about it", "and what")
    if any(query_lower.startswith(p) for p in vague_prefixes) and resolved_topic:
        return f"Explain {resolved_topic} in detail"

    # For 'what is cycle?' type queries, replace 'cycle' with resolved topic.
    # Guard: only perform the replacement when the resolved topic is NOT already
    # present in the query – this prevents "water cycle" → "water water cycle".
    if resolved_topic and "cycle" in query_lower and resolved_topic != "bicycle":
        if resolved_topic.lower() not in query_lower:
            rewritten = query_lower.replace("cycle", resolved_topic, 1)
            return rewritten.capitalize()

    # Default: append topic as context hint
    if resolved_topic and resolved_topic.lower() not in query_lower:
        return f"{original_query} (topic: {resolved_topic})"

    return original_query
