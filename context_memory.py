"""
context_memory.py
-----------------
Manages conversation history and extracts context signals.
Tracks the last N turns to help resolve ambiguous queries.
"""

from collections import deque
from dataclasses import dataclass, field


@dataclass
class Turn:
    """A single conversation turn."""
    user_query: str
    resolved_topic: str | None = None   # what topic was determined for this turn
    answer_snippet: str | None = None   # first 120 chars of the answer, for context


class ConversationMemory:
    """
    Stores recent conversation turns and provides helpers
    to extract the most recently discussed topics.
    """

    def __init__(self, max_turns: int = 5):
        self.history: deque[Turn] = deque(maxlen=max_turns)

    # ── Public API ───────────────────────────────────────────────────────────

    def add_turn(self, user_query: str, resolved_topic: str | None = None,
                 answer_snippet: str | None = None) -> None:
        """Record a completed conversation turn."""
        self.history.append(
            Turn(user_query=user_query,
                 resolved_topic=resolved_topic,
                 answer_snippet=answer_snippet)
        )

    def get_recent_topics(self, n: int = 3) -> list[str]:
        """Return the resolved topics from the last n turns (most recent first)."""
        topics = [
            t.resolved_topic for t in reversed(self.history)
            if t.resolved_topic
        ]
        return topics[:n]

    def get_last_topic(self) -> str | None:
        """Convenience: return the single most recently resolved topic."""
        topics = self.get_recent_topics(1)
        return topics[0] if topics else None

    def get_context_string(self) -> str:
        """Return a human-readable summary of recent turns for prompt injection."""
        if not self.history:
            return "No prior conversation."
        lines = []
        for i, turn in enumerate(self.history, 1):
            lines.append(f"Turn {i}: User asked '{turn.user_query}' "
                         f"→ topic resolved as '{turn.resolved_topic or 'unknown'}'")
        return "\n".join(lines)

    def clear(self) -> None:
        """Reset conversation state (e.g., when user starts a new session)."""
        self.history.clear()

    def to_list(self) -> list[dict]:
        """Serialise history to a list of dicts (useful for Streamlit session state)."""
        return [
            {
                "user_query": t.user_query,
                "resolved_topic": t.resolved_topic,
                "answer_snippet": t.answer_snippet,
            }
            for t in self.history
        ]

    @classmethod
    def from_list(cls, data: list[dict], max_turns: int = 5) -> "ConversationMemory":
        """Rebuild a ConversationMemory from serialised list (from Streamlit session)."""
        mem = cls(max_turns=max_turns)
        for item in data:
            mem.add_turn(
                user_query=item["user_query"],
                resolved_topic=item.get("resolved_topic"),
                answer_snippet=item.get("answer_snippet"),
            )
        return mem
