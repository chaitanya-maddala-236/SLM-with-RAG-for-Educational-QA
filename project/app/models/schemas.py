from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class QuestionType(str, Enum):
    factual = "factual"
    conceptual = "conceptual"
    procedural = "procedural"
    conversational = "conversational"


@dataclass(slots=True)
class UserInput:
    question: str
    chat_history: list[dict[str, str]] = field(default_factory=list)
    metadata_filters: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class QueryFeatures:
    is_follow_up: bool
    has_reference: bool
    question_type: QuestionType
    normalized_query: str


@dataclass(slots=True)
class RetrievedDoc:
    doc_id: str
    content: str
    score: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class PipelineDiagnostics:
    retrieval_confidence: float
    fallback_level: int
    ambiguity_detected: bool
    citations: list[str] = field(default_factory=list)


@dataclass(slots=True)
class PipelineResponse:
    answer: str
    context: str
    retrieved_docs: list[RetrievedDoc]
    diagnostics: PipelineDiagnostics
