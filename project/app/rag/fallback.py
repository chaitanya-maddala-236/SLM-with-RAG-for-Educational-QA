from __future__ import annotations

from enum import IntEnum


class FallbackLevel(IntEnum):
    full_rag = 1
    partial_rag = 2
    llm_fallback = 3


def select_fallback_level(confidence: float, high: float, low: float) -> FallbackLevel:
    if confidence >= high:
        return FallbackLevel.full_rag
    if confidence >= low:
        return FallbackLevel.partial_rag
    return FallbackLevel.llm_fallback
