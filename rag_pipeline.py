"""
rag_pipeline.py
---------------
Orchestrates the full 10-step RAG pipeline:

  Step 1  – Receive user question
  Step 2  – Check conversation memory
  Step 3  – Detect ambiguous terms
  Step 4  – Classify query (subject + topic)
  Step 5  – Apply glossary mapping
  Step 6  – Rewrite query with context
  Step 7  – Vector retrieval (BGE + Chroma)
  Step 8  – Select top-K documents
  Step 9  – Generate answer with SLM (Phi-3 via Ollama)
  Step 10 – Return answer + evaluation metrics

Each step logs a clearly formatted message so the pipeline is transparent.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from langchain.schema import Document
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma

from context_memory import ConversationMemory
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
    Full conversational RAG pipeline.
    Stateless except for the vector store; conversation memory is passed in.
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
        # Collect all corpus docs for recall computation
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
    ) -> PipelineResult:
        """
        Execute the full pipeline for one user query.

        Args:
            user_query: Raw text typed by the user.
            memory:     Current conversation memory (mutated in-place on success).

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

        # ── Step 2: Check conversation memory ────────────────────────────────
        last_topic = memory.get_last_topic()
        recent_topics = memory.get_recent_topics()
        result.log(
            2,
            f"Conversation memory → last topic: '{last_topic}' | "
            f"recent topics: {recent_topics}",
        )

        # ── Step 3: Detect ambiguous terms ────────────────────────────────────
        ambiguous = get_ambiguous_terms(user_query)
        result.ambiguous_terms = ambiguous
        result.log(3, f"Ambiguous terms detected: {ambiguous or 'none'}")

        # Try to resolve each ambiguous term
        resolved_from_ambiguity: str | None = None
        for term in ambiguous:
            # First, try signals within the query itself
            resolved = disambiguate_with_signals(term, user_query)
            if resolved:
                result.log(3, f"  → '{term}' resolved via query signals → '{resolved}'")
                resolved_from_ambiguity = resolved
                break

            # Next, check conversation context
            if last_topic and last_topic in AMBIGUOUS_TERMS.get(term, []):
                # Decide: is there a shift signal (e.g. 'move', 'ride') in the query?
                options = AMBIGUOUS_TERMS[term]
                # Look for any non-last-topic signal in the query
                shift_resolved = None
                for option in options:
                    if option != last_topic:
                        # Check if any word that strongly signals this option is present
                        option_tokens = set(option.split())
                        query_tokens = set(user_query.lower().split())
                        if option_tokens & query_tokens:
                            shift_resolved = option
                            break

                if shift_resolved:
                    result.log(
                        3,
                        f"  → '{term}' → intent shift detected → '{shift_resolved}' "
                        f"(was '{last_topic}')",
                    )
                    resolved_from_ambiguity = shift_resolved
                else:
                    result.log(
                        3,
                        f"  → '{term}' → no shift; continuing with context topic '{last_topic}'",
                    )
                    resolved_from_ambiguity = last_topic
                break

            # Cannot resolve: ask for clarification
            options_str = ", ".join(AMBIGUOUS_TERMS.get(term, []))
            result.clarification_needed = True
            result.clarification_message = CLARIFICATION_MSG.format(
                term=term, options=options_str
            )
            result.log(
                3,
                f"  → '{term}' is ambiguous (options: {options_str}). "
                "Requesting clarification.",
            )
            # Store partial turn and return early
            memory.add_turn(user_query=user_query, resolved_topic=None)
            return result

        # ── Step 4: Query classification ──────────────────────────────────────
        classification = classify_query(user_query)
        topic_from_classifier = classification["topic"]
        subject_from_classifier = classification["subject"]
        result.log(
            4,
            f"Query classification → subject: '{subject_from_classifier}' "
            f"(score={classification['subject_score']}), "
            f"topic: '{topic_from_classifier}' "
            f"(score={classification['topic_score']})",
        )

        # ── Step 5: Glossary mapping / expand query ───────────────────────────
        enriched_query, topic_from_glossary = expand_query(user_query)
        result.log(
            5,
            f"Glossary mapping → topic from glossary: '{topic_from_glossary}' | "
            f"enriched query: '{enriched_query}'",
        )

        # ── Determine final topic (priority: ambiguity resolution > classifier > glossary > memory)
        final_topic = (
            resolved_from_ambiguity
            or topic_from_classifier
            or topic_from_glossary
            or last_topic
        )
        final_subject = subject_from_classifier

        # Detect topic shift: if classifier fires confidently, prefer it over memory
        if (topic_from_classifier
                and classification["topic_score"] >= 2
                and detect_topic_shift(topic_from_classifier, last_topic)):
            final_topic = topic_from_classifier
            result.log(4, f"  → Topic shift detected; overriding memory with '{final_topic}'")

        result.detected_topic = final_topic
        result.detected_subject = final_subject

        # ── Step 6: Rewrite query ─────────────────────────────────────────────
        rewritten = _rewrite_query(user_query, final_topic, memory)
        result.rewritten_query = rewritten
        result.log(6, f"Rewritten query: '{rewritten}'")

        # ── Step 7: Vector retrieval ──────────────────────────────────────────
        result.log(7, f"Performing semantic retrieval (top-{self.top_k}) …")
        retrieved = retrieve_top_k(
            self.vector_store,
            rewritten,
            k=self.top_k,
            topic_filter=final_topic,
        )
        result.log(
            7,
            f"Retrieved {len(retrieved)} document(s) from Chroma.",
        )

        # ── Step 8: Top-K selection ───────────────────────────────────────────
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

        # ── Evaluation metrics ────────────────────────────────────────────────
        result.metrics = compute_all_metrics(
            query=rewritten,
            answer=result.answer,
            retrieved_docs=result.retrieved_docs,
            all_docs=self.all_docs,
            query_topic=final_topic,
            k=self.top_k,
        )

        # ── Update memory ─────────────────────────────────────────────────────
        memory.add_turn(
            user_query=user_query,
            resolved_topic=final_topic,
            answer_snippet=result.answer[:120],
        )

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
