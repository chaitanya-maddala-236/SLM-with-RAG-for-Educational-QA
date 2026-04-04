"""
glossary_mapper.py
------------------
Maps ambiguous terms and synonyms to canonical topic names.
Also provides term expansion for better retrieval.
"""

import re

# ── Canonical topic names (must match metadata in data_loader.py) ────────────
TOPICS = [
    "water cycle", "carbon cycle", "bicycle", "photosynthesis",
    "trigonometry", "genetics", "machine learning", "electricity",
    "magnetism", "nervous system", "evolution", "cell structure",
    "cellular respiration", "nitrogen cycle", "digestion", "immune system",
    "sound waves", "cybersecurity",
]

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
# Bugfix: removed "move", "fast", "speed" — too generic; kept only unambiguous
# bicycle-specific signals.
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
        # Bugfix: only strong unambiguous bicycle signals kept here
        "ride": "bicycle",
        "pedal": "bicycle",
        "wheel": "bicycle",
        "brake": "bicycle",
        "gear": "bicycle",
        "sprocket": "bicycle",
        "handlebar": "bicycle",
    },
}

# ── Out-of-scope signals ──────────────────────────────────────────────────────
# Words that indicate a query is outside this knowledge base.
# Declared as a frozenset for O(1) membership testing in hot code paths.
# Edge case handled: OUT_OF_SCOPE detection is bypassed when topic confidence >= 2.0
OUT_OF_SCOPE_SIGNALS: frozenset[str] = frozenset({
    "car", "truck", "airplane", "plane", "ship", "boat",
    "train", "rocket", "helicopter", "drone", "submarine",
    "animal", "dog", "cat", "horse", "bird", "fish",
    "history", "war", "politics", "economy", "religion",
    "country", "city", "person", "celebrity", "sport",
    "football", "cricket", "movie", "music", "food",
    "recipe", "cooking", "fashion", "weather",
})


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


GLOSSARY.update({
    # trigonometry
    "trig": "trigonometry",
    "sine": "trigonometry",
    "cosine": "trigonometry",
    "tangent": "trigonometry",
    "sin": "trigonometry",
    "cos": "trigonometry",
    "tan": "trigonometry",
    "hypotenuse": "trigonometry",
    "pythagorean theorem": "trigonometry",
    "unit circle": "trigonometry",
    "radian": "trigonometry",
    "right triangle": "trigonometry",
    "trigonometric": "trigonometry",

    # genetics
    "dna": "genetics",
    "gene": "genetics",
    "allele": "genetics",
    "chromosome": "genetics",
    "heredity": "genetics",
    "inheritance": "genetics",
    "genotype": "genetics",
    "phenotype": "genetics",
    "dominant trait": "genetics",
    "recessive trait": "genetics",
    "punnett square": "genetics",
    "mendelian genetics": "genetics",
    "mutation": "genetics",
    "genome": "genetics",

    # machine learning
    "neural network": "machine learning",
    "deep learning": "machine learning",
    "artificial intelligence": "machine learning",
    "supervised learning": "machine learning",
    "unsupervised learning": "machine learning",
    "training data": "machine learning",
    "gradient descent": "machine learning",
    "overfitting": "machine learning",
    "classification algorithm": "machine learning",
    "regression model": "machine learning",

    # electricity
    "voltage": "electricity",
    "current": "electricity",
    "resistance": "electricity",
    "ohm's law": "electricity",
    "electric circuit": "electricity",
    "series circuit": "electricity",
    "parallel circuit": "electricity",
    "conductor": "electricity",
    "insulator": "electricity",
    "ampere": "electricity",
    "watt": "electricity",
    "kilowatt": "electricity",

    # magnetism
    "magnet": "magnetism",
    "magnetic field": "magnetism",
    "electromagnet": "magnetism",
    "magnetic force": "magnetism",
    "north pole": "magnetism",
    "south pole": "magnetism",
    "compass": "magnetism",
    "magnetic flux": "magnetism",

    # nervous system
    "neuron": "nervous system",
    "synapse": "nervous system",
    "axon": "nervous system",
    "dendrite": "nervous system",
    "neurotransmitter": "nervous system",
    "reflex arc": "nervous system",
    "spinal cord": "nervous system",
    "central nervous system": "nervous system",
    "peripheral nervous system": "nervous system",
    "brain function": "nervous system",

    # evolution
    "natural selection": "evolution",
    "darwin": "evolution",
    "adaptation": "evolution",
    "speciation": "evolution",
    "common ancestor": "evolution",
    "genetic drift": "evolution",
    "fossil record": "evolution",
    "survival of the fittest": "evolution",

    # cell structure
    "nucleus": "cell structure",
    "mitochondria": "cell structure",
    "cell membrane": "cell structure",
    "organelle": "cell structure",
    "ribosome": "cell structure",
    "cytoplasm": "cell structure",
    "endoplasmic reticulum": "cell structure",
    "golgi apparatus": "cell structure",
    "eukaryote": "cell structure",
    "prokaryote": "cell structure",
    "animal cell": "cell structure",
    "plant cell": "cell structure",

    # cellular respiration
    "atp synthesis": "cellular respiration",
    "glycolysis": "cellular respiration",
    "krebs cycle": "cellular respiration",
    "electron transport chain": "cellular respiration",
    "aerobic respiration": "cellular respiration",
    "anaerobic respiration": "cellular respiration",
    "oxidative phosphorylation": "cellular respiration",
    "pyruvate": "cellular respiration",

    # nitrogen cycle
    "nitrification": "nitrogen cycle",
    "denitrification": "nitrogen cycle",
    "nitrogen fixation": "nitrogen cycle",
    "ammonification": "nitrogen cycle",
    "nitrate": "nitrogen cycle",
    "nitrite": "nitrogen cycle",
    "ammonia": "nitrogen cycle",

    # digestion
    "digestive system": "digestion",
    "stomach acid": "digestion",
    "small intestine": "digestion",
    "large intestine": "digestion",
    "peristalsis": "digestion",
    "bile": "digestion",
    "amylase": "digestion",
    "pepsin": "digestion",
    "villi": "digestion",
    "nutrient absorption": "digestion",

    # immune system
    "antibody": "immune system",
    "antigen": "immune system",
    "lymphocyte": "immune system",
    "t cell": "immune system",
    "b cell": "immune system",
    "phagocyte": "immune system",
    "vaccination": "immune system",
    "innate immunity": "immune system",
    "adaptive immunity": "immune system",
    "autoimmune disease": "immune system",

    # sound waves
    "frequency": "sound waves",
    "amplitude": "sound waves",
    "wavelength": "sound waves",
    "decibel": "sound waves",
    "pitch": "sound waves",
    "echo": "sound waves",
    "resonance": "sound waves",
    "ultrasound": "sound waves",
    "longitudinal wave": "sound waves",

    # cybersecurity
    "encryption": "cybersecurity",
    "firewall": "cybersecurity",
    "malware": "cybersecurity",
    "phishing": "cybersecurity",
    "data breach": "cybersecurity",
    "hacker": "cybersecurity",
    "ransomware": "cybersecurity",
    "two-factor authentication": "cybersecurity",
    "network security": "cybersecurity",
})


# RAG Improvement 1: Topic-based query expansion
MAX_EXPANSION_TERMS = 3  # number of expansion terms appended to the query

TOPIC_EXPANSIONS = {
    "water cycle": ["hydrological cycle", "evaporation", "condensation", "precipitation", "transpiration"],
    "carbon cycle": ["co2 cycle", "greenhouse gas", "fossil fuels", "carbon sink", "decomposition"],
    "photosynthesis": ["chlorophyll", "glucose production", "light reactions", "calvin cycle", "chloroplast"],
    "bicycle": ["cycling mechanics", "gear system", "braking", "pedalling", "chain drive"],
    "nitrogen cycle": ["nitrification", "denitrification", "nitrogen fixation", "ammonification"],
    "trigonometry": ["sine cosine tangent", "right triangle ratios", "unit circle", "pythagorean theorem"],
    "genetics": ["dna heredity", "allele genotype phenotype", "mendelian inheritance", "chromosome"],
    "machine learning": ["neural networks", "supervised learning", "gradient descent", "training data"],
    "electricity": ["voltage current resistance", "ohm's law", "circuit design", "conductor insulator"],
    "magnetism": ["magnetic field", "electromagnet", "flux", "pole attraction repulsion"],
    "nervous system": ["neuron synapse", "axon dendrite", "reflex arc", "brain function"],
    "evolution": ["natural selection", "adaptation", "speciation", "genetic drift", "darwin"],
    "cell structure": ["nucleus organelle", "membrane cytoplasm", "mitochondria ribosome", "eukaryote prokaryote"],
    "cellular respiration": ["atp synthesis", "glycolysis", "krebs cycle", "electron transport chain"],
    "digestion": ["stomach enzymes", "small intestine", "peristalsis", "nutrient absorption"],
    "immune system": ["antibody antigen", "lymphocyte", "vaccination", "innate adaptive immunity"],
    "sound waves": ["frequency amplitude", "wavelength decibel", "echo resonance", "longitudinal wave"],
    "cybersecurity": ["encryption firewall", "malware phishing", "data breach", "network security"],
}

def expand_query_with_topic(query: str, topic: str) -> str:
    """
    Expand a query by appending topic-related terms to improve retrieval recall.

    # RAG Improvement 1: Topic-based query expansion

    Args:
        query: The original user query string.
        topic: The detected or resolved topic name.

    Returns:
        Enriched query string with topic expansion terms appended.
    """
    expansions = TOPIC_EXPANSIONS.get(topic.lower(), [])
    if not expansions:
        return query
    expansion_str = " ".join(expansions[:MAX_EXPANSION_TERMS])
    return f"{query} {expansion_str}"


# RAG Improvement 2: Grade-aware retrieval
GRADE_SIGNALS: dict[str, list[str]] = {
    "elementary": ["simple", "basic", "easy", "grade 5", "grade 6", "young", "kid", "child", "primary"],
    "middle": ["intermediate", "grade 7", "grade 8", "middle school"],
    "high": ["advanced", "grade 9", "grade 10", "grade 11", "grade 12", "high school", "detailed", "complex"],
    "university": ["university", "college", "undergraduate", "research", "academic", "scholarly"],
}

def detect_grade_filter(query: str) -> str | None:
    """
    Detect an appropriate grade band from the query text using GRADE_SIGNALS.

    # RAG Improvement 2: Grade-aware retrieval

    Args:
        query: The user query string.

    Returns:
        Grade band string ("elementary", "middle", "high", "university"),
        or None if no grade signal is detected.
    """
    query_lower = query.lower()
    for grade_band, signals in GRADE_SIGNALS.items():
        for signal in signals:
            if signal in query_lower:
                return grade_band
    return None


# RAG Improvement 3: Subject-aware chunking
SUBJECT_CHUNK_SIZES: dict[str, int] = {
    "biology": 500,
    "chemistry": 450,
    "physics": 450,
    "mathematics": 350,
    "geography": 400,
    "environmental science": 500,
    "computer science": 400,
    "transportation": 350,
    "default": 400,
}

def get_chunk_size(subject: str) -> int:
    """
    Return the recommended chunk size (in characters) for a given subject.

    # RAG Improvement 3: Subject-aware chunking
    Longer subjects like biology/environmental science benefit from larger chunks
    that preserve multi-sentence explanations; math benefits from smaller, precise chunks.

    Args:
        subject: Subject name (e.g. "biology", "mathematics").

    Returns:
        Integer character count for chunk size.
    """
    return SUBJECT_CHUNK_SIZES.get(subject.lower(), SUBJECT_CHUNK_SIZES["default"])


# RAG Improvement 4: Subject-specific RAG thresholds
SUBJECT_RAG_THRESHOLDS: dict[str, float] = {
    "biology": 0.55,
    "chemistry": 0.55,
    "physics": 0.58,
    "mathematics": 0.62,
    "geography": 0.50,
    "environmental science": 0.52,
    "computer science": 0.58,
    "transportation": 0.50,
    "default": 0.60,
}

def get_rag_threshold(subject: str) -> float:
    """
    Return the RAG similarity threshold for a given subject.

    # RAG Improvement 4: Subject-specific thresholds
    Some subjects like geography have broader language variety and benefit from
    a lower threshold; precise subjects like mathematics use a higher bar.

    Args:
        subject: Subject name (e.g. "mathematics").

    Returns:
        Float threshold in [0, 1].
    """
    return SUBJECT_RAG_THRESHOLDS.get(subject.lower(), SUBJECT_RAG_THRESHOLDS["default"])


# RAG Improvement 5: Context budget per model
CONTEXT_BUDGETS: dict[str, int] = {
    "tinyllama": 800,
    "phi3": 2000,
    "llama3.2": 2000,
    "mistral": 3000,
    "gpt-3.5-turbo": 3000,
    "gpt-4o-mini": 4000,
    "default": 1500,
}

def get_context_budget(model_name: str) -> int:
    """
    Return the context budget (approximate token limit for retrieved context) for a model.

    # RAG Improvement 5: Context budget per model
    Smaller models like TinyLLaMA have limited context windows; larger models
    can use more retrieved context for better grounding.

    Args:
        model_name: Model identifier (e.g. "phi3", "tinyllama").

    Returns:
        Integer token budget for context assembly.
    """
    return CONTEXT_BUDGETS.get(model_name.lower(), CONTEXT_BUDGETS["default"])
