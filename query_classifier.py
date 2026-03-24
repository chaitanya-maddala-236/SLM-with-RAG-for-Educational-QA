"""
query_classifier.py
--------------------
Classifies an incoming query into a subject area and detects the
most likely topic.  Uses keyword heuristics (fast, no model needed)
so the pipeline stays lightweight.
"""

from glossary_mapper import TOPICS, GLOSSARY, AMBIGUOUS_TERMS

# ── Subject keyword map ───────────────────────────────────────────────────────
SUBJECT_KEYWORDS: dict[str, list[str]] = {
    "geography": [
        "water", "rain", "cloud", "ocean", "river", "lake", "sea", "snow",
        "groundwater", "atmosphere", "precipitation", "evaporation", "condensation",
        "run-off", "aquifer", "infiltration",
    ],
    "biology": [
        "plant", "cell", "organism", "chlorophyll", "photosynthesis", "leaf",
        "stomata", "chloroplast", "glucose", "oxygen", "co2", "carbon dioxide",
        "decompose", "food", "green", "algae", "bacteria", "enzyme", "calvin",
        "rubisco", "atp",
    ],
    "environmental science": [
        "carbon", "fossil fuel", "climate", "greenhouse", "emission", "sink",
        "ocean", "limestone", "coral",
    ],
    "physics": [
        "gear", "sprocket", "brake", "friction", "gyroscope", "force", "energy",
        "balance", "wheel", "momentum", "mass", "speed",
    ],
    "transportation": [
        "bicycle", "bike", "ride", "pedal", "handlebar", "cycle", "transport",
        "vehicle", "wheel", "chain", "road",
    ],
}

# ── Topic keyword map ─────────────────────────────────────────────────────────
TOPIC_KEYWORDS: dict[str, list[str]] = {
    "water cycle": [
        "water cycle", "hydrological", "evaporation", "condensation",
        "precipitation", "transpiration", "groundwater", "rain", "cloud",
        "run-off", "infiltration", "aquifer",
    ],
    "carbon cycle": [
        "carbon cycle", "carbon dioxide", "co2", "fossil fuel", "decomposition",
        "carbon sink", "greenhouse", "emission", "limestone", "coral",
    ],
    "bicycle": [
        "bicycle", "bike", "pedal", "gear", "brake", "handlebar", "chain",
        "sprocket", "derailleur", "ride", "rider", "wheel", "gyroscope",
    ],
    "photosynthesis": [
        "photosynthesis", "chlorophyll", "chloroplast", "glucose", "sunlight",
        "light reaction", "calvin cycle", "rubisco", "oxygen", "stomata",
        "thylakoid", "stroma",
    ],
}


def classify_query(query: str) -> dict:
    """
    Analyse the query and return a classification dict:
    {
        "subject": str | None,
        "topic": str | None,
        "subject_score": int,
        "topic_score": int,
        "all_topic_scores": dict[str, int],
    }
    """
    query_lower = query.lower()
    tokens = set(query_lower.split())

    # ── Score each subject ────────────────────────────────────────────────────
    subject_scores: dict[str, int] = {}
    for subject, keywords in SUBJECT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in query_lower)
        if score:
            subject_scores[subject] = score

    top_subject = max(subject_scores, key=subject_scores.get) if subject_scores else None
    top_subject_score = subject_scores.get(top_subject, 0) if top_subject else 0

    # ── Score each topic ──────────────────────────────────────────────────────
    topic_scores: dict[str, int] = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in query_lower)
        if score:
            topic_scores[topic] = score

    top_topic = max(topic_scores, key=topic_scores.get) if topic_scores else None
    top_topic_score = topic_scores.get(top_topic, 0) if top_topic else 0

    return {
        "subject": top_subject,
        "topic": top_topic,
        "subject_score": top_subject_score,
        "topic_score": top_topic_score,
        "all_topic_scores": topic_scores,
    }


def detect_topic_shift(new_topic: str | None, last_topic: str | None) -> bool:
    """
    Return True if the new topic is clearly different from the last resolved topic.
    Used to decide whether to override conversation context.
    """
    if new_topic is None or last_topic is None:
        return False
    return new_topic != last_topic
