from __future__ import annotations

import logging

from project.app.config.schema import ModelsConfig
from project.app.retrieval.hybrid import ScoredDocument
from project.app.utils.text import simple_token_count

logger = logging.getLogger(__name__)


def pack_context(
    docs: list[ScoredDocument],
    model_key: str,
    models_config: ModelsConfig,
) -> tuple[str, list[ScoredDocument]]:
    profile = models_config.registry[model_key]
    max_docs = profile.max_context_docs
    budget = profile.safe_context_budget

    packed: list[str] = []
    selected: list[ScoredDocument] = []
    used_tokens = 0

    ordered = sorted(docs, key=lambda d: d.score, reverse=True)
    for item in ordered:
        if len(selected) >= max_docs:
            break
        block = f"[source={item.doc.metadata.get('source', 'unknown')}]\n{item.doc.page_content}"
        block_tokens = simple_token_count(block)
        if used_tokens + block_tokens > budget:
            continue
        packed.append(block)
        selected.append(item)
        used_tokens += block_tokens

    logger.info("Packed %d docs (%d tokens) for model=%s", len(selected), used_tokens, model_key)
    return "\n\n".join(packed), selected
