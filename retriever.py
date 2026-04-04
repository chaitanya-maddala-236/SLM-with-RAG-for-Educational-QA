"""
retriever.py
------------
Builds and manages the Chroma vector store.
Provides retrieval functions for:

  - retrieve_top_k()          — baseline vector (semantic) retrieval
  - hybrid_search()           — BM25 + vector combined retrieval
  - rerank_documents()        — re-score a candidate pool and return top-K
  - hierarchical_retrieve()   — topic-route first, then chunk-level retrieval
  - build_bm25_index()        — build / rebuild the BM25 index from the corpus
"""

import os
import re
import hashlib
from collections import defaultdict

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# Embedding support: use flexible get_embeddings factory
from embeddings import get_embeddings
from data_loader import get_texts_and_metadatas
from research_config import DEFAULT_EMBEDDING, CHROMA_DIR_TEMPLATE, COLLECTION_NAME_TEMPLATE
from glossary_mapper import expand_query_with_topic, get_chunk_size

# ── Chunking constants (used by the scalable retriever) ───────────────────────
CHUNK_SIZE = 400
CHUNK_OVERLAP = 50

# ── Reranking constants ───────────────────────────────────────────────────────
# Bonus added to the token-overlap score when a document's metadata topic
# matches the query's resolved topic.  Chosen to be meaningful relative to
# typical token-overlap scores (0–1 range) while not overwhelming the signal.
TOPIC_MATCH_BONUS: float = 0.3

# Minimum character length for a chunk to receive a full relevance score.
# Chunks shorter than this are likely incomplete sentence fragments and rarely
# contain a complete answer; they are down-weighted (× 0.5) during reranking.
MIN_CHUNK_LENGTH: int = 40

# Candidate pool size multiplier: during hybrid search we collect
# k × CANDIDATE_POOL_MULTIPLIER candidates before reranking to k.
# A 4× pool gives the reranker enough diversity to surface the best results.
CANDIDATE_POOL_MULTIPLIER: int = 4

# ── BM25 retrieval constants ──────────────────────────────────────────────────
_BM25_AVAILABLE = False
try:
    from rank_bm25 import BM25Okapi as _BM25Okapi
    _BM25_AVAILABLE = True
except ImportError:
    pass

# ── Stop-words filtered out before BM25 tokenisation ─────────────────────────
_BM25_STOPWORDS = frozenset({
    "the", "a", "an", "is", "it", "in", "of", "to", "and", "or",
    "that", "this", "with", "for", "are", "was", "be", "by", "as",
    "how", "what", "does", "do", "can", "explain", "about", "at",
})


# ── Helpers ───────────────────────────────────────────────────────────────────

def _doc_key(doc: Document) -> str:
    """Return a stable hash key for deduplication in hybrid search."""
    return hashlib.md5(doc.page_content.encode()).hexdigest()


def _tokenise(text: str) -> list[str]:
    """Return a filtered list of lowercase word tokens suitable for BM25."""
    tokens = re.findall(r"\b[a-z0-9]+\b", text.lower())
    return [t for t in tokens if t not in _BM25_STOPWORDS and len(t) > 1]


def _token_overlap_score(query: str, doc_text: str) -> float:
    """
    Compute a simple token-overlap relevance score in [0, 1].
    Used by the fallback reranker when a cross-encoder is not available.
    """
    q_tokens = set(_tokenise(query))
    d_tokens = set(_tokenise(doc_text))
    if not q_tokens or not d_tokens:
        return 0.0
    return len(q_tokens & d_tokens) / len(q_tokens)


# ── Chroma vector store ───────────────────────────────────────────────────────

def build_vector_store(
    persist: bool = True,
    embedding_name: str = DEFAULT_EMBEDDING,
) -> Chroma:
    """
    Create (or reload from disk) the Chroma vector store for a given embedding.

    Each embedding model uses its own persist directory and collection name to
    avoid dimension-mismatch errors between different embedding spaces.

    On first run for a new embedding: embeds all documents and persists to disk.
    On later runs: loads the persisted store (much faster).

    Args:
        persist:        If True, persist the store to disk.
        embedding_name: Embedding key from EMBEDDING_MODELS (e.g. "bge-small").

    Returns:
        Initialised Chroma vector store.
    """
    # Embedding support: each embedding uses its own directory and collection
    persist_dir = CHROMA_DIR_TEMPLATE.format(embedding_name=embedding_name)
    collection = COLLECTION_NAME_TEMPLATE.format(embedding_name=embedding_name)

    print(f"  [Chroma] Using embedding: {embedding_name}")
    embeddings = get_embeddings(embedding_name)

    if persist and os.path.exists(persist_dir):
        print("  [Chroma] Loading existing vector store from disk...")
        store = Chroma(
            collection_name=collection,
            embedding_function=embeddings,
            persist_directory=persist_dir,
        )
        # Sanity check: make sure the collection is non-empty
        if store._collection.count() > 0:
            return store
        print("  [Chroma] Store empty – rebuilding...")

    print("  [Chroma] Building vector store (embedding documents)...")
    texts, metadatas = get_texts_and_metadatas()

    docs = [
        Document(page_content=text, metadata=meta)
        for text, meta in zip(texts, metadatas)
    ]

    store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=collection,
        persist_directory=persist_dir if persist else None,
    )

    return store


# ── BM25 index ────────────────────────────────────────────────────────────────

def build_bm25_index(docs: list[Document]) -> "BM25Index | None":
    """
    Build a BM25 index from a list of LangChain Documents.

    Returns ``None`` if the ``rank_bm25`` package is not installed.

    Args:
        docs: Corpus of documents to index.

    Returns:
        A ``BM25Index`` wrapper, or ``None`` if BM25 is unavailable.
    """
    if not _BM25_AVAILABLE:
        return None
    return BM25Index(docs)


class BM25Index:
    """
    Thin wrapper around rank_bm25.BM25Okapi.

    Stores the document corpus alongside the index so that search results can
    be returned as LangChain Document objects.
    """

    def __init__(self, docs: list[Document]) -> None:
        self.docs = docs
        tokenised = [_tokenise(d.page_content) for d in docs]
        self._index = _BM25Okapi(tokenised)

    def search(self, query: str, k: int = 20) -> list[tuple[Document, float]]:
        """
        Return the top-*k* documents ranked by BM25 score.

        Args:
            query: The search query string.
            k:     Maximum number of results to return.

        Returns:
            List of (Document, score) tuples ordered by descending BM25 score.
        """
        q_tokens = _tokenise(query)
        if not q_tokens:
            return []
        scores = self._index.get_scores(q_tokens)
        ranked = sorted(
            enumerate(scores), key=lambda x: x[1], reverse=True
        )[:k]
        return [(self.docs[i], float(s)) for i, s in ranked if s > 0]


# ── Reranking ─────────────────────────────────────────────────────────────────

def mmr_rerank(
    query: str,
    candidates: list[Document],
    top_k: int = 5,
    lambda_param: float = 0.5,
    topic_filter: str | None = None,
) -> list[Document]:
    """
    Maximum Marginal Relevance reranking for diversity + relevance balance.

    # RAG Improvement 9: MMR reranking
    MMR selects documents that are both relevant to the query AND diverse
    from already-selected documents, reducing redundant results.

    Args:
        query: The user query string.
        candidates: Pool of candidate documents.
        top_k: Number of documents to return.
        lambda_param: Trade-off between relevance (1.0) and diversity (0.0).
        topic_filter: If set, give bonus to topic-matching documents.

    Returns:
        Reranked list of at most top_k documents.
    """
    if not candidates:
        return []

    def _relevance(doc: Document) -> float:
        score = _token_overlap_score(query, doc.page_content)
        if (
            topic_filter
            and doc.metadata.get("topic", "").lower() == topic_filter.lower()
        ):
            score += TOPIC_MATCH_BONUS
        if len(doc.page_content) < MIN_CHUNK_LENGTH:
            score *= 0.5
        return score

    relevance_scores = [_relevance(doc) for doc in candidates]
    selected: list[Document] = []
    remaining = list(range(len(candidates)))

    while remaining and len(selected) < top_k:
        best_idx = None
        best_score = float("-inf")
        for i in remaining:
            rel = relevance_scores[i]
            if selected:
                max_sim = max(
                    _token_overlap_score(candidates[i].page_content, s.page_content)
                    for s in selected
                )
            else:
                max_sim = 0.0
            mmr_score = lambda_param * rel - (1 - lambda_param) * max_sim
            if mmr_score > best_score:
                best_score = mmr_score
                best_idx = i
        if best_idx is not None:
            selected.append(candidates[best_idx])
            remaining.remove(best_idx)

    return selected


# Backward-compatible alias
rerank_documents = mmr_rerank


# ── Hybrid search (BM25 + vector) ─────────────────────────────────────────────

def hybrid_search(
    vector_store: Chroma,
    bm25_index: "BM25Index | None",
    query: str,
    k: int = 5,
    bm25_candidates: int = 20,
    vector_candidates: int = 20,
    alpha: float = 0.5,
    topic_filter: str | None = None,
    subject_filter: str | None = None,
    grade_filter: str | None = None,
) -> list[Document]:
    """
    Combine BM25 keyword search with semantic vector search.

    Pipeline
    --------
    1. BM25 retrieval  → top ``bm25_candidates`` documents.
    2. Vector retrieval → top ``vector_candidates`` documents.
    3. Merge: deduplicate and compute a weighted combined score.
    4. Rerank the merged pool and return the best ``k`` documents.

    Args:
        vector_store:      Initialised Chroma store.
        bm25_index:        Pre-built BM25 index (or None to skip BM25).
        query:             The search query string.
        k:                 Final number of documents to return.
        bm25_candidates:   How many BM25 results to collect before merging.
        vector_candidates: How many vector results to collect before merging.
        alpha:             Weight assigned to vector scores (BM25 weight = 1−alpha).
                           0.5 gives equal weight to both.
        topic_filter:      Optional Chroma metadata filter on 'topic'.
        subject_filter:    Optional Chroma metadata filter on 'subject'.
        grade_filter:      Optional Chroma metadata filter on 'grade'.

    Returns:
        List of LangChain Document objects ordered by combined relevance.
    """
    # RAG Improvement 10: Query expansion
    # Expand query with topic-specific terminology before retrieval
    if topic_filter:
        expanded_query = expand_query_with_topic(query, topic_filter)
    else:
        expanded_query = query

    # ── 1. BM25 retrieval ─────────────────────────────────────────────────────
    bm25_results: dict[str, tuple[Document, float]] = {}
    if bm25_index is not None:
        raw = bm25_index.search(expanded_query, k=bm25_candidates)
        max_bm25 = max((s for _, s in raw), default=1.0) or 1.0
        for doc, score in raw:
            bm25_results[_doc_key(doc)] = (doc, score / max_bm25)

    # ── 2. Vector retrieval ───────────────────────────────────────────────────
    # RAG Improvement 8: Grade-aware filtering
    where_filters: list[dict] = []
    if topic_filter:
        where_filters.append({"topic": {"$eq": topic_filter}})
    if subject_filter:
        where_filters.append({"subject": {"$eq": subject_filter}})
    if grade_filter:
        where_filters.append({"grade": {"$eq": grade_filter}})

    if len(where_filters) > 1:
        where_clause: dict | None = {"$and": where_filters}
    elif len(where_filters) == 1:
        where_clause = where_filters[0]
    else:
        where_clause = None

    try:
        if where_clause:
            vec_raw = vector_store.similarity_search_with_relevance_scores(
                expanded_query, k=vector_candidates, filter=where_clause
            )
            if len(vec_raw) < 2:
                vec_raw = vector_store.similarity_search_with_relevance_scores(
                    expanded_query, k=vector_candidates
                )
        else:
            vec_raw = vector_store.similarity_search_with_relevance_scores(
                expanded_query, k=vector_candidates
            )
    except Exception as e:
        print(f"  [HybridSearch] Vector retrieval error: {e}. Falling back to BM25 only.")
        vec_raw = []

    vec_results: dict[str, tuple[Document, float]] = {}
    if vec_raw:
        max_vec = max((s for _, s in vec_raw), default=1.0) or 1.0
        for doc, score in vec_raw:
            vec_results[_doc_key(doc)] = (doc, score / max_vec)

    # ── 3. Merge scores ────────────────────────────────────────────────────────
    all_keys: set[str] = set(bm25_results) | set(vec_results)
    merged: list[tuple[Document, float]] = []
    for key in all_keys:
        bm25_score = bm25_results[key][1] if key in bm25_results else 0.0
        vec_score = vec_results[key][1] if key in vec_results else 0.0
        combined = (1 - alpha) * bm25_score + alpha * vec_score
        doc = (bm25_results.get(key) or vec_results.get(key))[0]
        merged.append((doc, combined))

    merged.sort(key=lambda x: x[1], reverse=True)
    candidates = [doc for doc, _ in merged[:max(k * CANDIDATE_POOL_MULTIPLIER, bm25_candidates)]]

    # ── 4. Rerank ─────────────────────────────────────────────────────────────
    return rerank_documents(query, candidates, top_k=k, topic_filter=topic_filter)


# ── Hierarchical retrieval ────────────────────────────────────────────────────

def hierarchical_retrieve(
    vector_store: Chroma,
    bm25_index: "BM25Index | None",
    query: str,
    topic: str | None,
    k: int = 5,
) -> list[Document]:
    """
    Two-stage hierarchical retrieval.

    Stage 1 — Topic routing:
        If *topic* is known, restrict the search space to documents whose
        metadata ``topic`` field matches.  This avoids irrelevant chunks from
        other subjects polluting the results.

    Stage 2 — Chunk-level retrieval:
        Run hybrid search within the routed topic scope and rerank the results.

    Falls back to full-corpus hybrid search when topic routing yields too few
    results (< 2 documents).

    Args:
        vector_store: Initialised Chroma store.
        bm25_index:   Pre-built BM25 index (or None to skip BM25 stage).
        query:        The search query string.
        topic:        Resolved topic for routing (or None for no routing).
        k:            Number of documents to return.

    Returns:
        List of LangChain Document objects ordered by relevance.
    """
    # Stage 1: topic-filtered hybrid search
    if topic:
        results = hybrid_search(
            vector_store=vector_store,
            bm25_index=bm25_index,
            query=query,
            k=k,
            topic_filter=topic,
        )
        if len(results) >= 2:
            return results
        print(
            f"  [HierarchicalRetriever] Topic '{topic}' returned only "
            f"{len(results)} doc(s); expanding to full corpus."
        )

    # Stage 2: full-corpus fallback
    return hybrid_search(
        vector_store=vector_store,
        bm25_index=bm25_index,
        query=query,
        k=k,
    )


# ── Baseline vector-only retrieval (kept for backward compatibility) ──────────

def retrieve_top_k(
    vector_store: Chroma,
    query: str,
    k: int = 5,
    topic_filter: str | None = None,
    subject_filter: str | None = None,
) -> list[Document]:
    """
    Retrieve the top-K documents most semantically similar to the query.

    Optionally filter by topic and/or subject via Chroma metadata filtering.
    Falls back to unfiltered retrieval if no documents match the filter.

    Args:
        vector_store:   Initialised Chroma store.
        query:          The (possibly rewritten) query string.
        k:              Number of documents to return (3–5 recommended).
        topic_filter:   If set, restrict to documents with this topic.
        subject_filter: If set, restrict to documents with this subject.

    Returns:
        List of LangChain Document objects, ordered by relevance (most relevant first).
    """
    where_clause: dict | None = None

    if topic_filter and subject_filter:
        where_clause = {
            "$and": [
                {"topic": {"$eq": topic_filter}},
                {"subject": {"$eq": subject_filter}},
            ]
        }
    elif topic_filter:
        where_clause = {"topic": {"$eq": topic_filter}}
    elif subject_filter:
        where_clause = {"subject": {"$eq": subject_filter}}

    try:
        if where_clause:
            docs = vector_store.similarity_search(query, k=k, filter=where_clause)
        else:
            docs = vector_store.similarity_search(query, k=k)

        # If filtered search returns too few results, fall back to unfiltered
        if where_clause and len(docs) < 2:
            print(f"  [Retriever] Filter returned only {len(docs)} doc(s); "
                  "falling back to unfiltered retrieval.")
            docs = vector_store.similarity_search(query, k=k)

    except Exception as e:
        print(f"  [Retriever] Error during retrieval: {e}. Falling back to unfiltered.")
        docs = vector_store.similarity_search(query, k=k)

    return docs
