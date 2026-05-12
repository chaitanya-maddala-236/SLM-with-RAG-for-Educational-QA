from __future__ import annotations

import logging
from dataclasses import dataclass

from project.app.prompts.templates import HYDE_PROMPT

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class HyDEResult:
    rewritten_query: str
    hypothetical_answer: str


def apply_hyde(
    query: str,
    llm_generate: callable,
    hyde_enabled: bool,
) -> HyDEResult:
    if not hyde_enabled:
        return HyDEResult(rewritten_query=query, hypothetical_answer="")

    prompt = f"{HYDE_PROMPT}\nQuestion: {query}\nPassage:"
    hypo = llm_generate(prompt, max_tokens=40).strip()
    logger.info("Generated HyDE hypothetical passage (%d chars)", len(hypo))
    rewritten = hypo if hypo else query
    return HyDEResult(rewritten_query=rewritten, hypothetical_answer=hypo)
