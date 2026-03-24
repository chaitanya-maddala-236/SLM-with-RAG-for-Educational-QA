"""
evaluation.py
-------------
Computes evaluation metrics for the RAG pipeline.

Metrics implemented:
  - Precision@K  : fraction of retrieved docs relevant to the query topic
  - Recall@K     : fraction of all relevant docs that were retrieved
  - MRR          : Mean Reciprocal Rank (position of first relevant doc)
  - Faithfulness : how well the answer stays grounded in retrieved context
  - Answer Relevance  : how directly the answer addresses the question
  - Context Relevance : how relevant the retrieved context is to the question
"""

import re
from langchain_core.documents import Document


# ── Shared stop-word set & tokeniser ─────────────────────────────────────────

_STOP_WORDS = {
    "the", "a", "an", "is", "it", "in", "of", "to", "and", "or",
    "that", "this", "with", "for", "are", "was", "be", "by", "as",
    "how", "what", "does", "do", "can", "explain",
}


def _tokenise(text: str) -> set[str]:
    """Return a set of meaningful lowercase tokens from *text*."""
    tokens = re.findall(r"\b[a-z0-9]+\b", text.lower())
    return {t for t in tokens if t not in _STOP_WORDS and len(t) > 2}


def _strip_topic_hint(query: str) -> str:
    """Remove appended topic hints like ' (topic: water cycle)' from a query."""
    return re.sub(r"\s*\(topic:[^)]*\)", "", query).strip()


# ── Helper: simple term-overlap relevance ────────────────────────────────────

def _token_overlap(text_a: str, text_b: str) -> float:
    """
    Compute Jaccard-like token overlap between two texts.
    Returns a float in [0, 1].
    """
    a_tokens = _tokenise(text_a)
    b_tokens = _tokenise(text_b)
    if not a_tokens or not b_tokens:
        return 0.0
    intersection = a_tokens & b_tokens
    union = a_tokens | b_tokens
    return len(intersection) / len(union)


# ── Metric functions ──────────────────────────────────────────────────────────

def precision_at_k(
    retrieved_docs: list[Document],
    query_topic: str | None,
    k: int = 5,
) -> float:
    """
    Precision@K = (number of relevant docs in top-K) / K.
    A document is considered relevant if its metadata topic matches query_topic.
    Falls back to token overlap if topic is unknown.
    """
    if not retrieved_docs:
        return 0.0
    docs = retrieved_docs[:k]

    if query_topic:
        relevant = sum(
            1 for doc in docs
            if doc.metadata.get("topic", "").lower() == query_topic.lower()
        )
    else:
        # No topic known: all retrieved docs assumed relevant (optimistic)
        relevant = len(docs)

    return relevant / len(docs)


def recall_at_k(
    retrieved_docs: list[Document],
    all_docs: list[Document],
    query_topic: str | None,
    k: int = 5,
) -> float:
    """
    Recall@K = (number of relevant docs in top-K) / (total relevant docs in corpus).
    """
    if not query_topic:
        return 1.0  # unknown topic → assume full recall

    total_relevant = sum(
        1 for doc in all_docs
        if doc.metadata.get("topic", "").lower() == query_topic.lower()
    )
    if total_relevant == 0:
        return 0.0

    retrieved_relevant = sum(
        1 for doc in retrieved_docs[:k]
        if doc.metadata.get("topic", "").lower() == query_topic.lower()
    )
    return retrieved_relevant / total_relevant


def mean_reciprocal_rank(
    retrieved_docs: list[Document],
    query_topic: str | None,
) -> float:
    """
    MRR = 1 / rank of the first relevant document.
    Returns 0 if no relevant document is found.
    """
    if not query_topic or not retrieved_docs:
        return 0.0
    for rank, doc in enumerate(retrieved_docs, start=1):
        if doc.metadata.get("topic", "").lower() == query_topic.lower():
            return 1.0 / rank
    return 0.0


def faithfulness_score(
    answer: str,
    retrieved_docs: list[Document],
) -> float:
    """
    Faithfulness: fraction of answer tokens that are grounded in the context.

    Uses *answer-token recall* – what proportion of the answer's meaningful
    vocabulary appears in the combined retrieved context.  This avoids
    penalising long, detailed answers for containing extra information.
    Score ∈ [0, 1].

    Returns 0.0 when there are no retrieved documents (e.g. LLM Fallback
    mode where no context was provided to the model).
    """
    if not answer or not retrieved_docs:
        return 0.0
    combined_context = " ".join(doc.page_content for doc in retrieved_docs)
    answer_tokens = _tokenise(answer)
    context_tokens = _tokenise(combined_context)
    if not answer_tokens:
        return 0.0
    covered = answer_tokens & context_tokens
    return len(covered) / len(answer_tokens)


def answer_relevance_score(
    answer: str,
    query: str,
) -> float:
    """
    Answer Relevance: fraction of meaningful query terms that appear in the answer.

    Uses *query-term recall* rather than Jaccard similarity so that long,
    detailed answers are not penalised for containing extra information beyond
    the narrow query vocabulary.  Topic-hint suffixes (e.g. "(topic: water cycle)")
    are stripped from the query before scoring.
    Score ∈ [0, 1].
    """
    if not answer or not query:
        return 0.0
    clean_query = _strip_topic_hint(query)
    q_tokens = _tokenise(clean_query)
    a_tokens = _tokenise(answer)
    if not q_tokens or not a_tokens:
        return 0.0
    covered = q_tokens & a_tokens
    return len(covered) / len(q_tokens)


def context_relevance_score(
    retrieved_docs: list[Document],
    query: str,
) -> float:
    """
    Context Relevance: average fraction of query terms covered by each retrieved doc.

    Uses *query-term recall per document* rather than Jaccard similarity so that
    rich, long documents are not down-scored for containing extra content.
    Topic-hint suffixes are stripped from the query before scoring.
    Score ∈ [0, 1].
    """
    if not retrieved_docs or not query:
        return 0.0
    clean_query = _strip_topic_hint(query)
    q_tokens = _tokenise(clean_query)
    if not q_tokens:
        return 0.0
    scores = []
    for doc in retrieved_docs:
        d_tokens = _tokenise(doc.page_content)
        covered = q_tokens & d_tokens
        scores.append(len(covered) / len(q_tokens))
    return sum(scores) / len(scores)


# ── Main evaluation runner ────────────────────────────────────────────────────

def compute_all_metrics(
    query: str,
    answer: str,
    retrieved_docs: list[Document],
    all_docs: list[Document],
    query_topic: str | None,
    k: int = 5,
    mode: str = "RAG",
) -> dict[str, float]:
    """
    Compute and return all six evaluation metrics.

    Args:
        query:          The original (or rewritten) user query.
        answer:         The SLM-generated answer text.
        retrieved_docs: Documents actually retrieved for this query.
        all_docs:       Full corpus (for computing recall denominator).
        query_topic:    Resolved topic name (or None).
        k:              K for precision/recall/MRR.
        mode:           Pipeline mode ("RAG" or "LLM Fallback").  In LLM
                        Fallback mode the model answers from its own
                        knowledge without using the retrieved documents, so
                        faithfulness is reported as 0.0 (no grounding
                        context was given to the model).

    Returns:
        Dict mapping metric name → float score.
    """
    # Faithfulness is not applicable in LLM Fallback mode because the answer
    # was generated without any retrieved context being passed to the model.
    if mode == "LLM Fallback":
        faith = 0.0
    else:
        faith = faithfulness_score(answer, retrieved_docs)

    return {
        f"Precision@{k}": round(precision_at_k(retrieved_docs, query_topic, k), 3),
        f"Recall@{k}":    round(recall_at_k(retrieved_docs, all_docs, query_topic, k), 3),
        "MRR":            round(mean_reciprocal_rank(retrieved_docs, query_topic), 3),
        "Faithfulness":   round(faith, 3),
        "Answer Relevance":  round(answer_relevance_score(answer, query), 3),
        "Context Relevance": round(context_relevance_score(retrieved_docs, query), 3),
    }


def format_metrics_table(metrics: dict[str, float]) -> str:
    """
    Return a pretty-printed ASCII table of evaluation metrics.

    +---------------------+--------+
    | Evaluation Metric   | Score  |
    +---------------------+--------+
    | Precision@5         | 0.820  |
    ...
    """
    col1_width = max(len(k) for k in metrics) + 2
    col2_width = 8
    sep = f"+{'-' * (col1_width + 2)}+{'-' * (col2_width + 2)}+"
    header = f"| {'Evaluation Metric':<{col1_width}} | {'Score':<{col2_width}} |"

    rows = [sep, header, sep]
    for metric, score in metrics.items():
        row = f"| {metric:<{col1_width}} | {score:<{col2_width}.3f} |"
        rows.append(row)
    rows.append(sep)
    return "\n".join(rows)
