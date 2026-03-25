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

SUBJECT_KEYWORDS.update({
    "mathematics": [
        "angle", "triangle", "hypotenuse", "radian", "degree",
        "trig", "trigonometric", "pythagoras",
        "algebra", "calculus", "differentiation", "integration", "function",
        "equation", "polynomial", "matrix", "matrices", "vector", "logarithm",
        "sequence", "series", "probability", "statistics", "geometry",
    ],
    "technology": [
        "artificial intelligence", "cybersecurity", "hacking", "ransomware",
        "software", "code", "programming", "internet", "digital", "computer",
        "cloud computing", "blockchain", "iot",
    ],
    "chemistry": [
        "atom", "molecule", "element", "compound", "bond", "ionic", "covalent",
        "acid", "base", "reaction", "chemical", "periodic table", "valence",
        "electron", "proton", "neutron", "mole", "concentration", "titration",
        "organic", "polymer",
    ],
    "health science": [
        "immune", "immunity", "antibody", "antigen", "vaccine", "pathogen",
        "digestion", "nutrient", "absorption", "metabolism", "hormone",
        "homeostasis", "health", "disease", "symptom", "treatment",
    ],
})

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

TOPIC_KEYWORDS.update({
    "trigonometry": [
        "trigonometry", "sin", "cos", "tan", "sine", "cosine", "tangent",
        "angle", "triangle", "hypotenuse", "adjacent", "opposite", "radian",
        "degree", "right angle", "trig", "trigonometric", "pythagoras",
        "pythagorean", "unit circle", "soh cah toa", "arcsin", "arccos",
        "arctan", "secant", "cosecant", "cotangent",
    ],
    "genetics": [
        "genetics", "gene", "dna", "allele", "chromosome", "dominant",
        "recessive", "genotype", "phenotype", "heredity", "inherit",
        "mutation", "trait", "punnett", "mendel", "mendelian", "genome",
        "nucleotide", "rna", "codon", "dna sequence", "heritability",
        "hybrid", "homozygous", "heterozygous", "locus",
    ],
    "machine learning": [
        "machine learning", "neural network", "algorithm", "training data",
        "prediction", "classification", "regression", "clustering", "feature",
        "supervised learning", "unsupervised learning", "deep learning",
        "artificial intelligence", "gradient descent", "overfitting", "bias",
        "variance", "model accuracy", "decision tree", "random forest",
        "support vector", "backpropagation", "epoch", "batch size",
    ],
    "electricity": [
        "electricity", "voltage", "current", "resistance", "circuit",
        "ohm", "watt", "electron", "conductor", "insulator", "battery",
        "charge", "coulomb", "ampere", "series circuit", "parallel circuit",
        "electric field", "power", "potential difference", "ohm's law",
        "kilowatt", "capacitor",
    ],
    "magnetism": [
        "magnetism", "magnet", "magnetic field", "north pole", "south pole",
        "attract", "repel", "compass", "ferromagnet", "electromagnet",
        "induction", "magnetic flux", "tesla", "solenoid", "magnetic force",
        "poles",
    ],
    "nervous system": [
        "nervous system", "neuron", "nerve", "brain", "spinal cord",
        "synapse", "reflex", "motor neuron", "sensory neuron", "dendrite",
        "axon", "neurotransmitter", "central nervous system", "peripheral",
        "cns", "pns", "cerebrum", "cerebellum", "medulla",
    ],
    "evolution": [
        "evolution", "natural selection", "adaptation", "species", "darwin",
        "mutation", "variation", "fossil", "selection pressure", "survival",
        "fitness", "extinction", "common ancestor", "speciation",
        "evolutionary", "descent", "genetic drift", "selection",
    ],
    "cell structure": [
        "cell structure", "nucleus", "cell membrane", "mitochondria",
        "ribosome", "organelle", "cytoplasm", "golgi apparatus",
        "endoplasmic reticulum", "vacuole", "eukaryotic", "prokaryotic",
        "cell wall", "lysosome", "animal cell", "plant cell", "chloroplast",
        "centriole", "nucleolus",
    ],
    "cellular respiration": [
        "cellular respiration", "atp", "glycolysis", "mitochondria",
        "aerobic respiration", "anaerobic respiration", "krebs cycle",
        "electron transport chain", "nadh", "fadh", "pyruvate",
        "oxidative phosphorylation", "respiration", "metabolic",
    ],
    "nitrogen cycle": [
        "nitrogen cycle", "nitrogen", "nitrification", "denitrification",
        "ammonia", "nitrate", "nitrite", "nitrogen fixation", "decomposer",
        "lightning", "fertilizer", "ammonification", "legume",
        "rhizobium", "denitrifying bacteria",
    ],
    "digestion": [
        "digestion", "stomach", "intestine", "digestive", "saliva",
        "esophagus", "pancreas", "liver", "bile", "nutrient", "absorption",
        "gut", "colon", "pepsin", "amylase", "villi", "peristalsis",
        "gastric", "duodenum", "enzyme",
    ],
    "immune system": [
        "immune system", "immune", "antibody", "antigen", "white blood cell",
        "lymphocyte", "t cell", "b cell", "pathogen", "infection",
        "inflammation", "vaccine", "immunity", "phagocyte", "macrophage",
        "innate immunity", "adaptive immunity", "autoimmune", "allergen",
    ],
    "sound waves": [
        "sound waves", "sound", "wave", "frequency", "amplitude", "decibel",
        "pitch", "echo", "wavelength", "vibration", "acoustic", "ultrasound",
        "hearing", "longitudinal wave", "compression", "rarefaction",
        "resonance", "hertz",
    ],
    "cybersecurity": [
        "cybersecurity", "hacking", "encryption", "firewall", "malware",
        "virus", "phishing", "password", "data breach", "network security",
        "cyber attack", "vulnerability", "authentication", "ransomware",
        "trojan", "social engineering", "ssl", "tls", "two-factor",
    ],
})


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
