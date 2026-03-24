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
from embeddings import get_bge_embeddings
from data_loader import get_texts_and_metadatas

CHROMA_PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "educational_rag"

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

def build_vector_store(persist: bool = True) -> Chroma:
    """
    Create (or reload from disk) the Chroma vector store with all educational documents.

    On first run:  embeds documents and saves to CHROMA_PERSIST_DIR.
    On later runs: loads the persisted store (much faster).

    Args:
        persist: If True, persist the store to disk.

    Returns:
        Initialised Chroma vector store.
    """
    embeddings = get_bge_embeddings()

    if persist and os.path.exists(CHROMA_PERSIST_DIR):
        print("  [Chroma] Loading existing vector store from disk...")
        store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=CHROMA_PERSIST_DIR,
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
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PERSIST_DIR if persist else None,
    )

    if persist:
        store.persist()
        print(f"  [Chroma] Persisted {len(docs)} documents to {CHROMA_PERSIST_DIR}")

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

def rerank_documents(
    query: str,
    candidates: list[Document],
    top_k: int = 5,
    topic_filter: str | None = None,
) -> list[Document]:
    """
    Re-score a pool of candidate documents and return the top-*top_k*.

    Uses a lightweight token-overlap scoring model so the system stays fast
    on CPU / SLM hardware.  A topic-match bonus is applied when *topic_filter*
    is provided so that topically relevant documents rank higher.

    Retrieve top-20 candidates from the upstream retrieval step, then pass
    them here to get the best top-5.

    Args:
        query:        The user query (used for relevance scoring).
        candidates:   Pool of candidate documents (e.g. top-20 from retrieval).
        top_k:        Number of documents to keep after reranking.
        topic_filter: If set, give a bonus to documents whose metadata topic
                      matches this value.

    Returns:
        Re-ranked list of at most *top_k* documents.
    """
    if not candidates:
        return []

    scored: list[tuple[Document, float]] = []
    for doc in candidates:
        score = _token_overlap_score(query, doc.page_content)

        # Topic-match bonus (encourages topically correct documents)
        if (
            topic_filter
            and doc.metadata.get("topic", "").lower() == topic_filter.lower()
        ):
            score += TOPIC_MATCH_BONUS

        # Penalise very short chunks that rarely contain full answers
        if len(doc.page_content) < MIN_CHUNK_LENGTH:
            score *= 0.5

        scored.append((doc, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in scored[:top_k]]


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

    Returns:
        List of LangChain Document objects ordered by combined relevance.
    """
    # ── 1. BM25 retrieval ─────────────────────────────────────────────────────
    bm25_results: dict[str, tuple[Document, float]] = {}
    if bm25_index is not None:
        raw = bm25_index.search(query, k=bm25_candidates)
        max_bm25 = max((s for _, s in raw), default=1.0) or 1.0
        for doc, score in raw:
            bm25_results[_doc_key(doc)] = (doc, score / max_bm25)

    # ── 2. Vector retrieval ───────────────────────────────────────────────────
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
            vec_raw = vector_store.similarity_search_with_relevance_scores(
                query, k=vector_candidates, filter=where_clause
            )
            if len(vec_raw) < 2:
                vec_raw = vector_store.similarity_search_with_relevance_scores(
                    query, k=vector_candidates
                )
        else:
            vec_raw = vector_store.similarity_search_with_relevance_scores(
                query, k=vector_candidates
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
