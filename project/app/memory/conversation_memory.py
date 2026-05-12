from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class MemoryTurn:
    question: str
    answer: str
    topic: str
    importance: float
    age: int = 0


@dataclass(slots=True)
class TopicState:
    topic: str
    score: float


class ConversationMemory:
    def __init__(self, short_term_limit: int, decay_rate: float = 0.25) -> None:
        self.short_term_limit = short_term_limit
        self.decay_rate = decay_rate
        self.turns: list[MemoryTurn] = []
        self.topic_scores: dict[str, float] = {}
        self.summary: str = ""

    def add_turn(self, question: str, answer: str, topic: str) -> None:
        importance = self._importance_score(question, answer)
        for turn in self.turns:
            turn.age += 1
        self.turns.append(MemoryTurn(question, answer, topic, importance))
        self.topic_scores[topic] = self.topic_scores.get(topic, 0.0) + importance
        self._prune()

    def _importance_score(self, question: str, answer: str) -> float:
        return min(1.0, (len(question.split()) + len(answer.split())) / 80.0)

    def _decayed_score(self, turn: MemoryTurn) -> float:
        return turn.importance * math.exp(-self.decay_rate * turn.age)

    def _prune(self) -> None:
        if len(self.turns) <= self.short_term_limit:
            return
        ranked = sorted(self.turns, key=self._decayed_score, reverse=True)
        kept = sorted(ranked[: self.short_term_limit], key=lambda t: t.age)
        dropped = [t for t in self.turns if t not in kept]
        if dropped:
            self.summary = self.summarize(self.summary, dropped)
        self.turns = kept

    def summarize(self, existing_summary: str, dropped_turns: list[MemoryTurn]) -> str:
        snippets = [f"Q:{t.question} A:{t.answer}" for t in dropped_turns[:3]]
        fragment = " | ".join(snippets)
        merged = f"{existing_summary} {fragment}".strip()
        logger.info("Memory summarized with %d dropped turns", len(dropped_turns))
        return merged[:1200]

    def semantic_retrieval(self, query: str, top_k: int = 3) -> list[MemoryTurn]:
        tokens = set(query.lower().split())
        scored = []
        for turn in self.turns:
            turn_tokens = set((turn.question + " " + turn.answer).lower().split())
            overlap = len(tokens & turn_tokens) / max(len(tokens), 1)
            scored.append((overlap + self._decayed_score(turn), turn))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [turn for _, turn in scored[:top_k] if _ > 0]

    def current_topic(self) -> TopicState | None:
        if not self.topic_scores:
            return None
        topic = max(self.topic_scores, key=lambda t: self.topic_scores[t])
        return TopicState(topic=topic, score=self.topic_scores[topic])
