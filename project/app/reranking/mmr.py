from __future__ import annotations

import logging
from dataclasses import dataclass

from project.app.retrieval.hybrid import ScoredDocument

logger = logging.getLogger(__name__)


def _token_set(text: str) -> set[str]:
    return set(text.lower().split())


def _sim(a: str, b: str) -> float:
    a_tokens = _token_set(a)
    b_tokens = _token_set(b)
    if not a_tokens or not b_tokens:
        return 0.0
    return len(a_tokens & b_tokens) / len(a_tokens | b_tokens)


def mmr_rerank(
    query: str,
    docs: list[ScoredDocument],
    top_k: int,
    lambda_mult: float = 0.7,
) -> list[ScoredDocument]:
    if not docs:
        return []

    selected: list[ScoredDocument] = []
    remaining = docs[:]

    while remaining and len(selected) < top_k:
        best = None
        best_score = float("-inf")
        for candidate in remaining:
            relevance = _sim(query, candidate.doc.page_content)
            diversity_penalty = 0.0
            if selected:
                diversity_penalty = max(
                    _sim(candidate.doc.page_content, item.doc.page_content)
                    for item in selected
                )
            mmr_score = lambda_mult * relevance - (1 - lambda_mult) * diversity_penalty
            if mmr_score > best_score:
                best_score = mmr_score
                best = candidate
        if best is None:
            break
        selected.append(best)
        remaining.remove(best)

    logger.info("MMR reranked %d docs to %d", len(docs), len(selected))
    return selected


def compress_context(docs: list[ScoredDocument], max_chars_per_doc: int = 900) -> list[ScoredDocument]:
    compressed: list[ScoredDocument] = []
    for item in docs:
        content = item.doc.page_content.strip()
        if len(content) > max_chars_per_doc:
            item.doc.page_content = content[:max_chars_per_doc].rsplit(" ", 1)[0] + " ..."
        compressed.append(item)
    return compressed
