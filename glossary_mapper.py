"""
glossary_mapper.py
------------------
Maps ambiguous terms and synonyms to canonical topic names.
Also provides term expansion for better retrieval.
"""

import re

# ── Canonical topic names (must match metadata in data_loader.py) ────────────
TOPICS = ["water cycle", "carbon cycle", "bicycle", "photosynthesis"]

# ── Ambiguous terms: each key maps to possible topics ────────────────────────
# Used by the ambiguity detector.  Order matters: first entry = default
# when context clues are insufficient.
AMBIGUOUS_TERMS: dict[str, list[str]] = {
    "cycle": ["water cycle", "carbon cycle", "bicycle"],
    "pump": ["water cycle", "bicycle"],   # water pump vs bike pump
    "chain": ["bicycle", "carbon cycle"], # bike chain vs carbon chain
    "green": ["photosynthesis", "bicycle"],
    "light": ["photosynthesis"],
    "gas": ["carbon cycle", "photosynthesis"],
    "energy": ["photosynthesis", "bicycle"],
    "wheel": ["bicycle"],
    "flow": ["water cycle", "carbon cycle"],
}

# ── Synonym / concept expansion map ─────────────────────────────────────────
# Expands a query term to its canonical topic name.
GLOSSARY: dict[str, str] = {
    # water cycle
    "hydrological cycle": "water cycle",
    "hydrologic cycle": "water cycle",
    "water circulation": "water cycle",
    "evaporation": "water cycle",
    "condensation": "water cycle",
    "precipitation": "water cycle",
    "transpiration": "water cycle",
    "groundwater": "water cycle",
    "rain": "water cycle",
    "snow": "water cycle",
    "clouds": "water cycle",

    # carbon cycle
    "co2": "carbon cycle",
    "carbon dioxide": "carbon cycle",
    "greenhouse gas": "carbon cycle",
    "fossil fuel": "carbon cycle",
    "decomposition": "carbon cycle",
    "carbon sink": "carbon cycle",
    "carbon emission": "carbon cycle",
    "climate change": "carbon cycle",

    # bicycle
    "bike": "bicycle",
    "cycling": "bicycle",
    "pedal": "bicycle",
    "gear": "bicycle",
    "brake": "bicycle",
    "handlebar": "bicycle",
    "sprocket": "bicycle",
    "derailleur": "bicycle",
    "two-wheel": "bicycle",
    "ride": "bicycle",
    "rider": "bicycle",

    # photosynthesis
    "chlorophyll": "photosynthesis",
    "chloroplast": "photosynthesis",
    "glucose": "photosynthesis",
    "sunlight": "photosynthesis",
    "oxygen": "photosynthesis",
    "calvin cycle": "photosynthesis",
    "light reaction": "photosynthesis",
    "rubisco": "photosynthesis",
    "plant food": "photosynthesis",
    "stomata": "photosynthesis",
}

# ── Context signals that help disambiguate ────────────────────────────────────
# When the term 'cycle' appears, these words in the query shift the meaning.
DISAMBIGUATION_SIGNALS: dict[str, dict[str, str]] = {
    "cycle": {
        # words in the query that signal a specific meaning
        "water": "water cycle",
        "rain": "water cycle",
        "cloud": "water cycle",
        "evaporation": "water cycle",
        "carbon": "carbon cycle",
        "co2": "carbon cycle",
        "fossil": "carbon cycle",
        "move": "bicycle",
        "ride": "bicycle",
        "wheel": "bicycle",
        "pedal": "bicycle",
        "fast": "bicycle",
        "speed": "bicycle",
    },
}


def map_term(term: str) -> str | None:
    """
    Look up a term in the glossary and return its canonical topic name,
    or None if not found.
    """
    return GLOSSARY.get(term.lower().strip())


def expand_query(query: str) -> tuple[str, str | None]:
    """
    Scan the query for glossary terms and return:
      - enriched_query: query with any matched canonical topic appended
      - detected_topic: the first matched topic, or None
    """
    tokens = query.lower().split()
    detected_topic = None

    # Check multi-word phrases first (up to 3 tokens)
    for n in (3, 2, 1):
        for i in range(len(tokens) - n + 1):
            phrase = " ".join(tokens[i: i + n])
            if phrase in GLOSSARY:
                detected_topic = GLOSSARY[phrase]
                break
        if detected_topic:
            break

    if detected_topic and detected_topic.lower() not in query.lower():
        enriched = f"{query} ({detected_topic})"
    else:
        enriched = query

    return enriched, detected_topic


def get_ambiguous_terms(query: str) -> list[str]:
    """
    Return a list of ambiguous terms found in the query.

    If a complete canonical topic name (e.g. "water cycle") is already
    present in the query the topic is unambiguous, so no terms are flagged.
    This prevents false positives such as treating "water cycle" as
    ambiguous because the word "cycle" appears in it.

    Word tokens are extracted with a word-boundary regex so that trailing
    punctuation (e.g. "cycle?") does not prevent a match.
    """
    query_lower = query.lower()
    # If a full known topic is explicitly present, nothing is ambiguous.
    for topic in TOPICS:
        if topic in query_lower:
            return []
    tokens = re.findall(r"\b[a-z0-9]+\b", query_lower)
    return [tok for tok in tokens if tok in AMBIGUOUS_TERMS]


def disambiguate_with_signals(ambiguous_term: str, query: str) -> str | None:
    """
    Try to resolve an ambiguous term using other words present in the query.
    Returns the resolved topic, or None if still ambiguous.
    """
    signals = DISAMBIGUATION_SIGNALS.get(ambiguous_term.lower(), {})
    query_lower = query.lower()
    for signal_word, resolved_topic in signals.items():
        if signal_word in query_lower:
            return resolved_topic
    return None
