"""
topic_memory_manager.py
-----------------------
Manages topic history across conversation turns with confidence decay.

Complements ConversationMemory by tracking:
  - Topic frequency  (how many turns each topic has appeared in)
  - Topic recency    (turn number of the last mention)
  - Topic confidence (starts at 1.0; decays by DECAY_RATE each turn without mention)

The decay model prevents stale topics from dominating context resolution when
the user has clearly moved on to a new subject.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TopicRecord:
    """Statistics for a single topic across the conversation."""

    topic: str
    frequency: int = 0       # total turns this topic appeared
    last_turn: int = 0       # turn index of the most recent mention
    confidence: float = 0.0  # current confidence score  ∈ [0, 1]
    subject: str = ""        # subject area associated with this topic
    grade_context: str = ""  # grade level context for this topic


class TopicMemoryManager:
    """
    Maintains a registry of topics seen across conversation turns.

    Key behaviours
    --------------
    - When a topic is resolved for a turn, its confidence resets to 1.0
      and its frequency counter increments.
    - All *other* topics lose DECAY_RATE confidence per turn (floor 0.0).
    - ``get_active_topic()`` returns the topic with the highest confidence
      above ACTIVE_THRESHOLD, tie-broken by frequency.
    - The manager can be serialised / deserialised for Streamlit session state.

    Typical usage
    -------------
    >>> mgr = TopicMemoryManager()
    >>> mgr.update("water cycle")   # turn 1
    >>> mgr.update("water cycle")   # turn 2
    >>> mgr.update(None)            # turn 3 – no new topic; confidence decays
    >>> mgr.get_active_topic()
    'water cycle'
    """

    DECAY_RATE = 0.25        # confidence subtracted per missed turn
    ACTIVE_THRESHOLD = 0.3   # minimum confidence to consider a topic "active"

    def __init__(self) -> None:
        self._registry: dict[str, TopicRecord] = {}
        self._turn: int = 0

    # ── Public API ─────────────────────────────────────────────────────────────

    def update(self, resolved_topic: str | None, subject: str = "", grade: str = "") -> None:
        """
        Record the outcome of one conversation turn.

        Args:
            resolved_topic: Topic resolved for this turn, or ``None`` if unknown.
            subject:        Optional subject area for the resolved topic.
            grade:          Optional grade level context for the resolved topic.
        """
        self._turn += 1

        # Decay all topics that were NOT discussed in this turn
        for record in self._registry.values():
            if record.topic != resolved_topic:
                record.confidence = max(0.0, record.confidence - self.DECAY_RATE)

        # Reinforce (or create) the resolved topic
        if resolved_topic:
            if resolved_topic not in self._registry:
                self._registry[resolved_topic] = TopicRecord(
                    topic=resolved_topic,
                    frequency=1,
                    last_turn=self._turn,
                    confidence=1.0,
                    subject=subject,
                    grade_context=grade,
                )
            else:
                rec = self._registry[resolved_topic]
                rec.frequency += 1
                rec.last_turn = self._turn
                rec.confidence = 1.0  # reset to full on re-mention
                if subject:
                    rec.subject = subject
                if grade:
                    rec.grade_context = grade

    def get_active_topic(self) -> str | None:
        """
        Return the topic with the highest current confidence above
        ACTIVE_THRESHOLD, or ``None`` if all topics have decayed.

        Tie-breaking: when two topics share the same confidence, the one that
        has been discussed more frequently (higher ``frequency`` count) wins.
        This is implemented by comparing ``(confidence, frequency)`` tuples.
        """
        active = [
            rec
            for rec in self._registry.values()
            if rec.confidence >= self.ACTIVE_THRESHOLD
        ]
        if not active:
            return None
        best = max(active, key=lambda r: (r.confidence, r.frequency))
        return best.topic

    def get_active_subject(self) -> str | None:
        """Return subject of the highest-confidence active topic, or None."""
        active = [
            rec
            for rec in self._registry.values()
            if rec.confidence >= self.ACTIVE_THRESHOLD
        ]
        if not active:
            return None
        best = max(active, key=lambda r: (r.confidence, r.frequency))
        return best.subject or None

    def get_topic_subject_pairs(self) -> list[tuple[str, str]]:
        """Return list of (topic, subject) for all active topics, sorted by descending confidence."""
        return [
            (rec.topic, rec.subject)
            for rec in sorted(
                self._registry.values(), key=lambda r: r.confidence, reverse=True
            )
            if rec.confidence >= self.ACTIVE_THRESHOLD
        ]

    def get_grade_context(self) -> str | None:
        """Return grade_context of the highest-confidence active topic, or None."""
        active = [
            rec
            for rec in self._registry.values()
            if rec.confidence >= self.ACTIVE_THRESHOLD
        ]
        if not active:
            return None
        best = max(active, key=lambda r: (r.confidence, r.frequency))
        return best.grade_context or None

    def get_conversation_subjects(self) -> list[str]:
        """Return unique subjects seen across all topic records (non-empty only)."""
        seen: list[str] = []
        for rec in self._registry.values():
            if rec.subject and rec.subject not in seen:
                seen.append(rec.subject)
        return seen

    def detect_subject_change(self, new_subject: str) -> bool:
        """Return True if new_subject differs from the currently active subject."""
        current = self.get_active_subject()
        if current is None:
            return False
        return current.lower() != new_subject.lower()

    def get_topic_confidence(self, topic: str) -> float:
        """Return the current confidence for a specific topic (0.0 if unseen)."""
        rec = self._registry.get(topic)
        return rec.confidence if rec else 0.0

    def get_all_active_topics(self) -> list[tuple[str, float]]:
        """
        Return all active (confidence >= ACTIVE_THRESHOLD) topics sorted by
        descending confidence.

        Returns:
            List of (topic_name, confidence) tuples.
        """
        active = [
            (rec.topic, rec.confidence)
            for rec in self._registry.values()
            if rec.confidence >= self.ACTIVE_THRESHOLD
        ]
        return sorted(active, key=lambda x: x[1], reverse=True)

    def current_turn(self) -> int:
        """Return the current turn counter."""
        return self._turn

    def reset(self) -> None:
        """Clear all topic history and reset the turn counter."""
        self._registry.clear()
        self._turn = 0

    # ── Serialisation ──────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Serialise to a plain dict (for Streamlit session state storage)."""
        return {
            "turn": self._turn,
            "registry": {
                topic: {
                    "frequency": rec.frequency,
                    "last_turn": rec.last_turn,
                    "confidence": rec.confidence,
                    "subject": rec.subject,
                    "grade_context": rec.grade_context,
                }
                for topic, rec in self._registry.items()
            },
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TopicMemoryManager":
        """Rebuild a TopicMemoryManager from a serialised dict."""
        mgr = cls()
        mgr._turn = data.get("turn", 0)
        for topic, rec_data in data.get("registry", {}).items():
            mgr._registry[topic] = TopicRecord(
                topic=topic,
                frequency=rec_data.get("frequency", 0),
                last_turn=rec_data.get("last_turn", 0),
                confidence=rec_data.get("confidence", 0.0),
                subject=rec_data.get("subject", ""),
                grade_context=rec_data.get("grade_context", ""),
            )
        return mgr
