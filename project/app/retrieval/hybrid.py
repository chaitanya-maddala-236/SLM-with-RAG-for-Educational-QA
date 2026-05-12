from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from retriever import BM25Index

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ScoredDocument:
    doc: Document
    score: float


def dense_retrieve(
    vector_store: Chroma,
    query: str,
    top_k: int,
    metadata_filter: dict[str, str] | None = None,
) -> list[ScoredDocument]:
    docs_scores = vector_store.similarity_search_with_relevance_scores(
        query,
        k=top_k,
        filter=metadata_filter or None,
    )
    return [ScoredDocument(doc=d, score=float(s)) for d, s in docs_scores]


def sparse_retrieve(
    bm25_index: BM25Index | None,
    query: str,
    top_k: int,
) -> list[ScoredDocument]:
    if bm25_index is None:
        return []
    pairs = bm25_index.search(query, k=top_k)
    return [ScoredDocument(doc=d, score=float(s)) for d, s in pairs]


def reciprocal_rank_fusion(
    dense_docs: list[ScoredDocument],
    sparse_docs: list[ScoredDocument],
    rrf_k: int,
    dense_weight: float,
    sparse_weight: float,
    pool_size: int,
) -> list[ScoredDocument]:
    scores: dict[str, float] = defaultdict(float)
    docs: dict[str, Document] = {}

    for rank, item in enumerate(dense_docs, start=1):
        key = item.doc.page_content
        docs[key] = item.doc
        scores[key] += dense_weight * (1.0 / (rrf_k + rank))

    for rank, item in enumerate(sparse_docs, start=1):
        key = item.doc.page_content
        docs[key] = item.doc
        scores[key] += sparse_weight * (1.0 / (rrf_k + rank))

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:pool_size]
    logger.info("RRF fused %d dense + %d sparse docs", len(dense_docs), len(sparse_docs))
    return [ScoredDocument(doc=docs[k], score=v) for k, v in ranked]
