from __future__ import annotations

import re
from difflib import get_close_matches

ABBREVIATIONS = {
    "bio": "biology",
    "chem": "chemistry",
    "phy": "physics",
    "math": "mathematics",
}

COMMON_TERMS = [
    "biology",
    "chemistry",
    "physics",
    "mathematics",
    "photosynthesis",
    "mitosis",
    "ecosystem",
    "gravity",
]


def normalize_query(query: str) -> str:
    return re.sub(r"\s+", " ", query.strip().lower())


def expand_abbreviations(query: str) -> str:
    words = query.split()
    return " ".join(ABBREVIATIONS.get(w, w) for w in words)


def correct_typos(query: str) -> str:
    corrected: list[str] = []
    for token in query.split():
        if token in COMMON_TERMS:
            corrected.append(token)
            continue
        match = get_close_matches(token, COMMON_TERMS, n=1, cutoff=0.85)
        corrected.append(match[0] if match else token)
    return " ".join(corrected)


def preprocess_query(query: str) -> str:
    normalized = normalize_query(query)
    expanded = expand_abbreviations(normalized)
    return correct_typos(expanded)
