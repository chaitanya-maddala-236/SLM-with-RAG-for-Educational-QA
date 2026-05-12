from __future__ import annotations

import re

from project.app.models.schemas import QuestionType

AMBIGUOUS_TERMS = {"it", "they", "this", "that", "thing", "process"}


def detect_follow_up(question: str) -> bool:
    return bool(re.search(r"\b(also|what about|and|then|next)\b", question.lower()))


def detect_references(question: str) -> bool:
    words = set(re.findall(r"\b\w+\b", question.lower()))
    return bool(words & AMBIGUOUS_TERMS)


def classify_question_type(question: str) -> QuestionType:
    q = question.lower()
    if any(k in q for k in ["how to", "steps", "procedure", "solve"]):
        return QuestionType.procedural
    if any(k in q for k in ["why", "explain", "concept", "difference"]):
        return QuestionType.conceptual
    if any(k in q for k in ["hi", "hello", "thanks", "who are you"]):
        return QuestionType.conversational
    return QuestionType.factual


def detect_ambiguity(question: str) -> bool:
    short = len(question.split()) < 4
    pronoun_heavy = detect_references(question)
    return short or pronoun_heavy
