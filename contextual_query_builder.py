"""
contextual_query_builder.py
---------------------------
Contextual Query Builder for the EduSLM-RAG system.

Combines conversation memory, the previous topic, and the current user question
to produce an explicit, unambiguous query ready for vector retrieval.

Components
----------
QueryNormalizer
    Cleans raw input: lowercase, expand contractions, strip stray punctuation.

TopicConfidenceScorer
    Assigns a weighted keyword score to each topic.  A score ≥ TOPIC_SWITCH_THRESHOLD
    is "high confidence" and allows a topic switch even if memory says otherwise.

AmbiguityResolver
    Detects ambiguous terms (cycle, cell, model, system, …) and resolves them
    using (in priority order):
      1. High-confidence topic from the query itself
      2. In-query disambiguation signals  (e.g. 'move' near 'cycle' → bicycle)
      3. Last topic in conversation memory
      4. Unresolved — pipeline will request clarification

ContextualQueryBuilder
    Orchestrates the three components above to return a ContextualQueryResult
    containing the rewritten query, resolved topic, and rich debug metadata.

Example
-------
    Conversation:
      User: "Explain water cycle"    → last_topic = "water cycle"
      User: "What is cycle?"

    ContextualQueryBuilder.build("What is cycle?", memory)
    → rewritten_query = "What is the water cycle?"
    → resolved_topic  = "water cycle"
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from context_memory import ConversationMemory
from glossary_mapper import AMBIGUOUS_TERMS, DISAMBIGUATION_SIGNALS, GLOSSARY

# ── Canonical topics (must match metadata in data_loader.py) ─────────────────
TOPICS: list[str] = ["water cycle", "carbon cycle", "bicycle", "photosynthesis"]

# ── Extended ambiguous terms ──────────────────────────────────────────────────
# Superset of glossary_mapper.AMBIGUOUS_TERMS; adds domain-relevant words that
# are genuinely ambiguous across the topics covered by this system.
EXTENDED_AMBIGUOUS_TERMS: dict[str, list[str]] = {
    **AMBIGUOUS_TERMS,
    # Domain terms ambiguous across multiple educational topics:
    "cell":    ["photosynthesis", "carbon cycle"],  # biology cell vs. battery cell
    "model":   ["water cycle", "carbon cycle", "photosynthesis", "bicycle"],
    "system":  ["water cycle", "carbon cycle", "photosynthesis"],
    "process": ["water cycle", "carbon cycle", "photosynthesis"],
    "reaction": ["photosynthesis", "carbon cycle"],
    # Pronouns that must always be resolved via memory
    "it":   [],
    "this": [],
    "that": [],
}

# ── Weighted keyword map for topic confidence scoring ─────────────────────────
# Higher weight → stronger signal for that topic.
TOPIC_KEYWORD_WEIGHTS: dict[str, dict[str, float]] = {
    "water cycle": {
        "water": 2.0, "evaporation": 3.0, "condensation": 3.0,
        "precipitation": 3.0, "transpiration": 3.0, "groundwater": 3.0,
        "rain": 2.0, "cloud": 1.5, "hydrological": 3.0, "runoff": 2.5,
        "infiltration": 3.0, "aquifer": 3.0, "snow": 1.5,
    },
    "carbon cycle": {
        "carbon": 2.0, "co2": 3.0, "fossil": 2.5, "emission": 2.5,
        "greenhouse": 3.0, "decomposition": 3.0, "carbon dioxide": 3.0,
        "climate": 2.0, "sink": 2.0, "limestone": 3.0,
    },
    "bicycle": {
        "bicycle": 4.0, "bike": 3.0, "pedal": 3.0, "gear": 2.5,
        "brake": 3.0, "handlebar": 3.0, "sprocket": 3.0, "ride": 2.0,
        "wheel": 2.0, "chain": 2.0, "derailleur": 3.0, "move": 1.5,
    },
    "photosynthesis": {
        "photosynthesis": 4.0, "chlorophyll": 3.0, "chloroplast": 3.0,
        "glucose": 3.0, "sunlight": 2.5, "oxygen": 2.0, "calvin": 3.0,
        "rubisco": 3.0, "stomata": 3.0, "thylakoid": 3.0, "stroma": 3.0,
        "light reaction": 3.0,
    },
}

# Minimum weighted score required to consider a topic "high confidence"
TOPIC_SWITCH_THRESHOLD: float = 2.0

# Divisor used to normalise a topic score into a [0, 1] confidence value.
# A single strong keyword (e.g. "chlorophyll" = 3.0) divided by this yields
# 0.75; the maximum reasonable compound score (≈8–12) caps at 1.0 via min().
_SCORE_NORMALISER: float = 4.0


# ── 1. Query Normalizer ───────────────────────────────────────────────────────

class QueryNormalizer:
    """
    Normalises raw user input before further processing.

    Steps
    -----
    1. Lowercase and strip surrounding whitespace
    2. Expand common English contractions
    3. Remove stray punctuation (keeps hyphens and apostrophes inside words)
    4. Collapse repeated whitespace
    """

    _CONTRACTIONS: dict[str, str] = {
        "what's": "what is", "it's": "it is", "that's": "that is",
        "how's": "how is", "there's": "there is", "isn't": "is not",
        "doesn't": "does not", "don't": "do not", "didn't": "did not",
        "can't": "cannot", "won't": "will not", "i'm": "i am",
        "they're": "they are", "we're": "we are", "you're": "you are",
        "where's": "where is", "when's": "when is", "who's": "who is",
    }

    def normalize(self, text: str) -> str:
        """
        Return a normalised copy of *text*.

        Args:
            text: Raw user input string.

        Returns:
            Cleaned, lowercase string.
        """
        result = text.lower().strip()
        for contraction, expansion in self._CONTRACTIONS.items():
            result = result.replace(contraction, expansion)
        # Remove characters that are not word chars, spaces, hyphens, or apostrophes
        result = re.sub(r"[^\w\s\-']", " ", result)
        result = re.sub(r"\s+", " ", result).strip()
        return result


# ── 2. Topic Confidence Scorer ────────────────────────────────────────────────

@dataclass
class TopicConfidenceResult:
    """Output of the TopicConfidenceScorer."""

    scores: dict[str, float]      # per-topic weighted keyword score
    top_topic: str | None         # topic with the highest score (or None)
    top_score: float              # score of the top topic
    is_high_confidence: bool      # True if top_score >= TOPIC_SWITCH_THRESHOLD


class TopicConfidenceScorer:
    """
    Scores how confidently each topic is signalled by the query.

    Uses the weighted keyword map (TOPIC_KEYWORD_WEIGHTS).  A score that meets
    or exceeds TOPIC_SWITCH_THRESHOLD is labelled "high confidence", allowing
    the pipeline to override conversation memory with a new topic.

    Low or zero scores mean the query is vague and memory should be respected.
    """

    def score(self, query: str) -> TopicConfidenceResult:
        """
        Compute per-topic confidence scores.

        Args:
            query: Normalised query text.

        Returns:
            TopicConfidenceResult with scores and the winning topic.
        """
        query_lower = query.lower()
        scores: dict[str, float] = {}

        for topic, keywords in TOPIC_KEYWORD_WEIGHTS.items():
            total = 0.0
            for keyword, weight in keywords.items():
                if keyword in query_lower:
                    total += weight
            if total > 0.0:
                scores[topic] = round(total, 2)

        if not scores:
            return TopicConfidenceResult(
                scores={},
                top_topic=None,
                top_score=0.0,
                is_high_confidence=False,
            )

        top_topic = max(scores, key=scores.__getitem__)
        top_score = scores[top_topic]

        return TopicConfidenceResult(
            scores=scores,
            top_topic=top_topic,
            top_score=top_score,
            is_high_confidence=(top_score >= TOPIC_SWITCH_THRESHOLD),
        )


# ── 3. Ambiguity Resolver ─────────────────────────────────────────────────────

@dataclass
class AmbiguityResult:
    """Output of the AmbiguityResolver."""

    ambiguous_terms: list[str]    # terms detected as ambiguous
    resolved_topic: str | None    # final resolved topic (or None)
    resolution_source: str        # "query_signals" | "memory" | "unresolved"
    confidence: float             # resolution confidence  ∈ [0, 1]


class AmbiguityResolver:
    """
    Detects ambiguous terms in the query and resolves them to a canonical topic.

    Resolution priority
    -------------------
    1. High-confidence topic from weighted keyword scoring → use directly.
    2. In-query disambiguation signals from DISAMBIGUATION_SIGNALS
       (e.g. 'move' near 'cycle' → 'bicycle').
    3. Last topic from conversation memory — if the ambiguous term can
       plausibly refer to that topic.
    4. Unresolved — caller may request clarification from the user.

    Handles single-word ambiguous terms (cycle, cell, …) and pronouns
    (it, this, that) that should always be resolved via memory.
    """

    def resolve(
        self,
        query: str,
        memory: ConversationMemory,
        topic_confidence: TopicConfidenceResult,
    ) -> AmbiguityResult:
        """
        Detect and resolve ambiguous terms in *query*.

        Args:
            query:            Normalised user query.
            memory:           Current conversation memory.
            topic_confidence: Pre-computed topic confidence scores.

        Returns:
            AmbiguityResult describing what was found and how it was resolved.
        """
        query_lower = query.lower()
        tokens = query_lower.split()

        # Detect ambiguous single-word terms
        ambiguous_found = [tok for tok in tokens if tok in EXTENDED_AMBIGUOUS_TERMS]

        # Also check for multi-word ambiguous terms (none currently, but future-proof)
        for term in EXTENDED_AMBIGUOUS_TERMS:
            if " " in term and term in query_lower and term not in ambiguous_found:
                ambiguous_found.append(term)

        if not ambiguous_found:
            return AmbiguityResult(
                ambiguous_terms=[],
                resolved_topic=topic_confidence.top_topic,
                resolution_source="query_signals",
                confidence=min(1.0, topic_confidence.top_score / _SCORE_NORMALISER),
            )

        # Priority 1: High-confidence topic from query keywords
        if topic_confidence.is_high_confidence:
            return AmbiguityResult(
                ambiguous_terms=ambiguous_found,
                resolved_topic=topic_confidence.top_topic,
                resolution_source="query_signals",
                confidence=min(1.0, topic_confidence.top_score / _SCORE_NORMALISER),
            )

        # Priority 2: In-query disambiguation signals
        for term in ambiguous_found:
            signals = DISAMBIGUATION_SIGNALS.get(term, {})
            for signal_word, resolved_topic in signals.items():
                if signal_word in query_lower:
                    return AmbiguityResult(
                        ambiguous_terms=ambiguous_found,
                        resolved_topic=resolved_topic,
                        resolution_source="query_signals",
                        confidence=0.85,
                    )

        # Priority 3: Conversation memory
        last_topic = memory.get_last_topic()
        if last_topic:
            first_term = ambiguous_found[0]
            possible_topics = EXTENDED_AMBIGUOUS_TERMS.get(first_term, [])
            # Accept memory if the term can refer to that topic, or term has no
            # specific restrictions (e.g. pronouns with empty list)
            if not possible_topics or last_topic in possible_topics:
                return AmbiguityResult(
                    ambiguous_terms=ambiguous_found,
                    resolved_topic=last_topic,
                    resolution_source="memory",
                    confidence=0.75,
                )

        # Priority 4: Unresolved
        return AmbiguityResult(
            ambiguous_terms=ambiguous_found,
            resolved_topic=None,
            resolution_source="unresolved",
            confidence=0.0,
        )


# ── 4. Contextual Query Builder ───────────────────────────────────────────────

@dataclass
class ContextualQueryResult:
    """Full output of the ContextualQueryBuilder for one user turn."""

    original_query: str
    normalized_query: str
    rewritten_query: str           # explicit, context-enriched query for retrieval
    resolved_topic: str | None     # canonical topic name (or None)
    topic_confidence: TopicConfidenceResult
    ambiguity_result: AmbiguityResult
    topic_switched: bool           # True when topic changed from memory's last topic
    debug_notes: list[str] = field(default_factory=list)


class ContextualQueryBuilder:
    """
    Orchestrates query normalisation, topic confidence scoring, ambiguity
    resolution, topic-switch detection, and context-aware query rewriting.

    This module sits at Step 3 of the pipeline — after conversation memory
    is loaded but before ambiguity detection and query classification —
    so that all downstream steps receive an already-explicit query.

    Usage
    -----
    >>> builder = ContextualQueryBuilder()
    >>> result  = builder.build("What is cycle?", memory)
    >>> result.rewritten_query
    'What is the water cycle?'
    >>> result.resolved_topic
    'water cycle'
    """

    def __init__(self) -> None:
        self._normalizer = QueryNormalizer()
        self._scorer = TopicConfidenceScorer()
        self._resolver = AmbiguityResolver()
        # Pre-compute multi-word GLOSSARY phrases that contain an ambiguous term.
        # Used in _rewrite to skip substitution when the term is part of a
        # meaningful compound phrase already in the query (e.g. "calvin cycle").
        self._compound_phrases: set[str] = {
            phrase
            for phrase in GLOSSARY
            if " " in phrase
            and any(tok in EXTENDED_AMBIGUOUS_TERMS for tok in phrase.split())
        }

    # ── Public API ─────────────────────────────────────────────────────────────

    def build(
        self,
        user_query: str,
        memory: ConversationMemory,
    ) -> ContextualQueryResult:
        """
        Build a contextual, explicit query from the raw user input.

        Processing steps
        ----------------
        A. Normalise the raw query (lowercase, expand contractions, …)
        B. Score topic confidence from weighted keywords
        C. Resolve ambiguous terms using signals + memory
        D. Decide final topic and whether a topic switch occurred
        E. Rewrite the query to be explicit

        Args:
            user_query: Raw text from the user.
            memory:     Current conversation memory (read-only; not mutated here).

        Returns:
            ContextualQueryResult with the rewritten query and full metadata.
        """
        notes: list[str] = []
        last_topic = memory.get_last_topic()

        # A: Normalise
        normalised = self._normalizer.normalize(user_query)
        notes.append(f"Normalised query: '{normalised}'")

        # B: Score topic confidence
        confidence = self._scorer.score(normalised)
        if confidence.top_topic:
            notes.append(
                f"Topic confidence → '{confidence.top_topic}' "
                f"(score={confidence.top_score}, "
                f"high={'yes' if confidence.is_high_confidence else 'no'})"
            )
        else:
            notes.append("Topic confidence → no topic signal detected")

        # C: Resolve ambiguity
        ambiguity = self._resolver.resolve(normalised, memory, confidence)
        if ambiguity.ambiguous_terms:
            notes.append(
                f"Ambiguous terms: {ambiguity.ambiguous_terms} "
                f"→ resolved via '{ambiguity.resolution_source}' "
                f"→ topic: '{ambiguity.resolved_topic}' "
                f"(confidence={ambiguity.confidence:.2f})"
            )
        else:
            notes.append("No ambiguous terms detected.")

        # D: Decide final topic and switch flag
        resolved_topic, topic_switched = self._decide_topic(
            confidence=confidence,
            ambiguity=ambiguity,
            last_topic=last_topic,
            notes=notes,
        )

        # E: Rewrite
        rewritten = self._rewrite(
            original=user_query,
            normalised=normalised,
            resolved_topic=resolved_topic,
            memory=memory,
        )
        notes.append(f"Rewritten query: '{rewritten}'")

        return ContextualQueryResult(
            original_query=user_query,
            normalized_query=normalised,
            rewritten_query=rewritten,
            resolved_topic=resolved_topic,
            topic_confidence=confidence,
            ambiguity_result=ambiguity,
            topic_switched=topic_switched,
            debug_notes=notes,
        )

    # ── Private helpers ────────────────────────────────────────────────────────

    def _decide_topic(
        self,
        confidence: TopicConfidenceResult,
        ambiguity: AmbiguityResult,
        last_topic: str | None,
        notes: list[str],
    ) -> tuple[str | None, bool]:
        """
        Apply topic-switch logic and return (resolved_topic, topic_switched).

        Priority rules
        --------------
        1. High-confidence new topic (score ≥ TOPIC_SWITCH_THRESHOLD) → switch.
        2. Ambiguity resolved via query signals → accept (switch if different).
        3. Ambiguity resolved via memory → keep that topic (no switch).
        4. Medium-confidence signal (score ≥ 1.0) AND different from memory → switch.
        5. No signal → keep last topic from memory.
        """
        # Rule 1: High-confidence topic from query keywords
        if confidence.is_high_confidence:
            switched = (
                last_topic is not None
                and confidence.top_topic != last_topic
            )
            if switched:
                notes.append(
                    f"Topic switch: '{last_topic}' → '{confidence.top_topic}' "
                    f"(high confidence, score={confidence.top_score})"
                )
            return confidence.top_topic, switched

        # Rule 2 / 3: Ambiguity resolved
        if ambiguity.resolved_topic:
            switched = (
                last_topic is not None
                and ambiguity.resolved_topic != last_topic
                and ambiguity.resolution_source == "query_signals"
            )
            return ambiguity.resolved_topic, switched

        # Rule 4: Medium-confidence signal, clearly different topic
        if (
            confidence.top_score >= 1.0
            and confidence.top_topic is not None
            and confidence.top_topic != last_topic
        ):
            notes.append(
                f"Medium-confidence topic switch: '{last_topic}' → "
                f"'{confidence.top_topic}' (score={confidence.top_score})"
            )
            return confidence.top_topic, True

        # Rule 5: Fall back to memory
        if last_topic:
            notes.append(f"No topic signal; retaining memory topic: '{last_topic}'")
            return last_topic, False

        return confidence.top_topic, False

    def _rewrite(
        self,
        original: str,
        normalised: str,
        resolved_topic: str | None,
        memory: ConversationMemory,
    ) -> str:
        """
        Rewrite the query to make it explicit and context-aware.

        Rewriting rules (applied in order)
        ------------------------------------
        1. Find the first ambiguous term in the query.
           a. If the resolved topic is a *superset* of the ambiguous term
              (e.g. "water cycle" ⊃ "cycle") AND the extra words are not yet
              in the query → replace the ambiguous term with the full topic name
              (adding "the" for compound topics).
           b. If the resolved topic is a *different* word (e.g. "cycle" → "bicycle")
              → substitute directly.
        2. Pronoun references (it / this / that) with a resolved topic
           → replace with "Explain <topic> in more detail".
        3. Default: if the resolved topic is not already present, append it as
           a context hint: "<original> (context: <topic>)".
        """
        if not resolved_topic:
            return original

        tokens = normalised.split()

        # Find the first ambiguous token present in the query
        amb_term: str | None = None
        for tok in tokens:
            if tok in EXTENDED_AMBIGUOUS_TERMS:
                amb_term = tok
                break

        # ── Rule 2: pronoun-only references ───────────────────────────────────
        pronouns = {"it", "this", "that", "they", "them"}
        if set(tokens) & pronouns and amb_term in pronouns:
            if memory.get_last_topic():
                return f"Explain {resolved_topic} in more detail"

        # ── Rule 1: Ambiguous term substitution ───────────────────────────────
        if amb_term and amb_term in EXTENDED_AMBIGUOUS_TERMS:
            # Guard: skip substitution when the ambiguous term is part of a
            # multi-word GLOSSARY phrase that is already present in the query
            # (e.g. "calvin cycle" in "What is the Calvin cycle?" → keep as-is).
            term_in_compound = any(
                phrase in normalised.lower()
                for phrase in self._compound_phrases
                if amb_term in phrase.split()
            )
            if term_in_compound:
                # The compound phrase is already meaningful; just append context
                if resolved_topic.lower() not in normalised.lower():
                    return f"{original} (context: {resolved_topic})"
                return original

            topic_words = resolved_topic.split()

            if amb_term not in topic_words:
                # Resolved topic is a different word (e.g. "cycle" → "bicycle").
                # Only substitute when the resolution came from a word-level
                # disambiguation signal, not from generic keyword scoring.
                # We detect this by checking that the ambiguous term *by itself*
                # does NOT produce a high confidence score for the resolved topic
                # (i.e. the score came from other keywords, not the term itself).
                rewritten = re.sub(
                    r"\b" + re.escape(amb_term) + r"\b",
                    resolved_topic,
                    normalised,
                    count=1,
                )
                return rewritten.strip().capitalize()

            # Topic is a superset of the ambiguous term (e.g. "water cycle" ⊃ "cycle")
            extra_words = [w for w in topic_words if w != amb_term]
            extras_in_query = any(w in normalised for w in extra_words)

            if not extras_in_query:
                # Safe to expand: "What is cycle?" → "What is the water cycle?"
                replacement = (
                    f"the {resolved_topic}"
                    if len(topic_words) > 1
                    else resolved_topic
                )
                rewritten = re.sub(
                    r"\b" + re.escape(amb_term) + r"\b",
                    replacement,
                    normalised,
                    count=1,
                )
                # Clean up double articles that can arise from expansion
                rewritten = re.sub(r"\bthe the\b", "the", rewritten)
                return rewritten.strip().capitalize()

        # ── Rule 3: Append context hint ───────────────────────────────────────
        if resolved_topic.lower() not in normalised.lower():
            return f"{original} (context: {resolved_topic})"

        return original
