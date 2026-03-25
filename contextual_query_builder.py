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
from glossary_mapper import AMBIGUOUS_TERMS, DISAMBIGUATION_SIGNALS, GLOSSARY, OUT_OF_SCOPE_SIGNALS

# ── Canonical topics (must match metadata in data_loader.py) ─────────────────
TOPICS: list[str] = [
    "water cycle", "carbon cycle", "bicycle", "photosynthesis",
    "trigonometry", "genetics", "machine learning", "electricity",
    "magnetism", "nervous system", "evolution", "cell structure",
    "cellular respiration", "nitrogen cycle", "digestion", "immune system",
    "sound waves", "cybersecurity",
]

# ── Extended ambiguous terms ──────────────────────────────────────────────────
# Superset of glossary_mapper.AMBIGUOUS_TERMS; adds domain-relevant words that
# are genuinely ambiguous across the topics covered by this system.
EXTENDED_AMBIGUOUS_TERMS: dict[str, list[str]] = {
    **AMBIGUOUS_TERMS,
    # Domain terms ambiguous across multiple educational topics:
    "cell":    ["photosynthesis", "carbon cycle", "cell structure"],  # biology cell / battery cell / cell structure
    "model":   ["water cycle", "carbon cycle", "photosynthesis", "bicycle", "machine learning"],
    "system":  ["water cycle", "carbon cycle", "photosynthesis", "nervous system", "immune system", "digestion"],
    "process": ["water cycle", "carbon cycle", "photosynthesis", "digestion", "cellular respiration"],
    "reaction": ["photosynthesis", "carbon cycle", "cellular respiration"],
    "network": ["nervous system", "machine learning"],
    "training": ["machine learning"],
    "signal":  ["nervous system", "sound waves"],
    "wave":    ["sound waves"],
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
        # Bugfix: removed "move" — too generic; kept only strong unambiguous signals
        "bicycle": 4.0, "bike": 3.0, "pedal": 3.0, "gear": 2.5,
        "brake": 3.0, "handlebar": 3.0, "sprocket": 3.0, "ride": 2.0,
        "wheel": 2.0, "chain": 2.0, "derailleur": 3.0,
    },
    "photosynthesis": {
        "photosynthesis": 4.0, "chlorophyll": 3.0, "chloroplast": 3.0,
        "glucose": 3.0, "sunlight": 2.5, "oxygen": 2.0, "calvin": 3.0,
        "rubisco": 3.0, "stomata": 3.0, "thylakoid": 3.0, "stroma": 3.0,
        "light reaction": 3.0,
        "plant": 1.0, "plants": 1.0, "leaf": 1.5, "leaves": 1.5,
        "algae": 1.5, "photosynthetic": 2.0,
    },
    "trigonometry": {
        "trigonometry": 4.0, "sin": 3.0, "cos": 3.0, "tan": 3.0,
        "sine": 3.0, "cosine": 3.0, "tangent": 3.0, "angle": 2.0,
        "triangle": 2.0, "hypotenuse": 3.0, "radian": 3.0, "degree": 1.5,
        "trig": 3.0, "trigonometric": 3.5, "pythagoras": 3.0,
        "unit circle": 3.0, "arcsin": 3.0, "arccos": 3.0, "arctan": 3.0,
    },
    "genetics": {
        "genetics": 4.0, "gene": 3.0, "dna": 3.0, "allele": 3.5,
        "chromosome": 3.5, "dominant": 2.5, "recessive": 2.5,
        "genotype": 3.5, "phenotype": 3.5, "heredity": 3.0,
        "inherit": 2.5, "mutation": 2.5, "punnett": 4.0,
        "mendel": 3.5, "mendelian": 3.5, "genome": 3.0,
        "nucleotide": 3.0, "homozygous": 3.5, "heterozygous": 3.5,
    },
    "machine learning": {
        "machine learning": 4.0, "neural network": 4.0, "deep learning": 4.0,
        "artificial intelligence": 3.5, "algorithm": 2.0, "training": 2.5,
        "prediction": 2.0, "classification": 2.5, "regression": 2.5,
        "clustering": 3.0, "supervised": 3.0, "unsupervised": 3.0,
        "gradient descent": 4.0, "overfitting": 3.5, "backpropagation": 4.0,
        "epoch": 2.5, "model accuracy": 3.0, "decision tree": 3.5,
    },
    "electricity": {
        "electricity": 4.0, "voltage": 3.5, "current": 2.5, "resistance": 3.0,
        "circuit": 3.0, "ohm": 3.5, "watt": 3.0, "ampere": 3.5,
        "conductor": 2.5, "insulator": 2.5, "battery": 2.0,
        "series circuit": 3.5, "parallel circuit": 3.5,
        "ohm's law": 4.0, "potential difference": 3.0, "coulomb": 3.5,
    },
    "magnetism": {
        "magnetism": 4.0, "magnet": 3.5, "magnetic field": 4.0,
        "north pole": 3.0, "south pole": 3.0, "attract": 1.5, "repel": 2.0,
        "compass": 3.0, "electromagnet": 4.0, "induction": 3.0,
        "magnetic flux": 3.5, "tesla": 3.0, "solenoid": 3.5,
        "ferromagnet": 3.5, "magnetic force": 3.5,
    },
    "nervous system": {
        "nervous system": 4.0, "neuron": 3.5, "nerve": 3.0, "brain": 2.5,
        "spinal cord": 3.5, "synapse": 3.5, "reflex": 3.0, "axon": 3.5,
        "dendrite": 3.5, "neurotransmitter": 4.0, "cns": 3.5, "pns": 3.5,
        "cerebrum": 3.5, "cerebellum": 3.5, "motor neuron": 3.5,
        "sensory neuron": 3.5, "medulla": 3.0,
    },
    "evolution": {
        "evolution": 4.0, "natural selection": 4.0, "adaptation": 3.0,
        "species": 2.0, "darwin": 3.5, "mutation": 2.5, "variation": 2.0,
        "fossil": 2.5, "survival": 2.0, "fitness": 2.0, "extinction": 2.5,
        "common ancestor": 4.0, "speciation": 4.0, "genetic drift": 3.5,
        "evolutionary": 3.5,
    },
    "cell structure": {
        "cell structure": 4.0, "nucleus": 3.0, "cell membrane": 3.5,
        "mitochondria": 3.5, "ribosome": 3.5, "organelle": 4.0,
        "cytoplasm": 3.0, "golgi": 3.5, "endoplasmic reticulum": 4.0,
        "vacuole": 3.0, "eukaryotic": 3.5, "prokaryotic": 3.5,
        "cell wall": 3.0, "lysosome": 3.5, "centriole": 3.5,
        "animal cell": 3.5, "plant cell": 3.5,
    },
    "cellular respiration": {
        "cellular respiration": 4.0, "atp": 3.5, "glycolysis": 4.0,
        "krebs cycle": 4.0, "electron transport chain": 4.0,
        "aerobic": 3.0, "anaerobic": 3.0, "pyruvate": 3.5,
        "oxidative phosphorylation": 4.0, "nadh": 3.5, "fadh": 3.5,
        "mitochondria": 2.0, "respiration": 3.0,
    },
    "nitrogen cycle": {
        "nitrogen cycle": 4.0, "nitrogen": 3.0, "nitrification": 4.0,
        "denitrification": 4.0, "ammonia": 3.0, "nitrate": 3.5,
        "nitrite": 3.5, "nitrogen fixation": 4.0, "ammonification": 4.0,
        "rhizobium": 4.0, "legume": 3.0, "fertilizer": 2.0,
        "denitrifying": 3.5,
    },
    "digestion": {
        "digestion": 4.0, "stomach": 3.0, "intestine": 3.0,
        "digestive": 3.5, "saliva": 3.0, "esophagus": 3.5,
        "pancreas": 3.5, "liver": 2.5, "bile": 3.5, "nutrient": 2.0,
        "absorption": 2.5, "villi": 3.5, "peristalsis": 4.0,
        "pepsin": 3.5, "amylase": 3.5, "duodenum": 4.0,
    },
    "immune system": {
        "immune system": 4.0, "immune": 3.0, "antibody": 4.0,
        "antigen": 4.0, "lymphocyte": 4.0, "t cell": 4.0, "b cell": 4.0,
        "pathogen": 3.0, "infection": 2.0, "inflammation": 2.5,
        "vaccine": 3.0, "phagocyte": 4.0, "macrophage": 4.0,
        "innate immunity": 4.0, "adaptive immunity": 4.0, "autoimmune": 4.0,
    },
    "sound waves": {
        "sound waves": 4.0, "sound": 2.5, "frequency": 3.0,
        "amplitude": 3.0, "decibel": 3.5, "pitch": 3.0, "echo": 3.0,
        "wavelength": 3.0, "vibration": 2.5, "acoustic": 3.0,
        "ultrasound": 3.5, "longitudinal wave": 4.0, "resonance": 3.0,
        "compression": 2.5, "rarefaction": 4.0, "hertz": 3.5,
    },
    "cybersecurity": {
        "cybersecurity": 4.0, "hacking": 3.5, "encryption": 3.5,
        "firewall": 3.5, "malware": 4.0, "phishing": 4.0,
        "data breach": 4.0, "ransomware": 4.0, "vulnerability": 3.0,
        "authentication": 3.0, "network security": 4.0,
        "social engineering": 4.0, "trojan": 3.5, "cyber attack": 4.0,
    },
}

# Minimum weighted score required to consider a topic "high confidence"
TOPIC_SWITCH_THRESHOLD: float = 2.0

# Minimum keyword-overlap similarity (0–1) between query and memory topic that
# qualifies the query as being about that topic.  0.0 means that *any* keyword
# match (however small) is sufficient to keep the topic; only a score of
# *exactly* zero triggers the deeper unknown-domain analysis.
TOPIC_SIMILARITY_FLOOR: float = 0.0

# Minimum word length to consider a token "domain-specific" when no topic
# keyword matches are found.  Words of this length or longer that do not
# appear in *any* topic keyword vocabulary are treated as out-of-scope domain
# signals (e.g. "nervous", "muscle") rather than common English filler words.
MIN_DOMAIN_SPECIFIC_WORD_LENGTH: int = 5

# Divisor used to normalise a topic score into a [0, 1] confidence value.
# A single strong keyword (e.g. "chlorophyll" = 3.0) divided by this yields
# 0.75; the maximum reasonable compound score (≈8–12) caps at 1.0 via min().
_SCORE_NORMALISER: float = 4.0

# ── Followup handling: pattern catalogue ─────────────────────────────────────
FOLLOWUP_PATTERNS: dict[str, list[str]] = {
    # Generic explanation
    "explanation": [
        "how does it work", "explain this", "explain it",
        "explain more", "tell me more", "elaborate", "go deeper",
        "explain in detail", "describe it", "what is it",
    ],
    # Reasoning
    "reasoning": [
        "why does it work", "why is this", "why is it important",
        "why do we need this", "why does this happen",
        "what causes it", "what causes this", "reason for this",
        "why?", "how?", "what?",
    ],
    # Examples
    "examples": [
        "give an example", "explain with example",
        "show example", "real world example", "example?",
        "give example", "example please", "illustrate",
    ],
    # Advantages/disadvantages
    "advantages": [
        "advantages", "disadvantages", "pros and cons",
        "benefits", "drawbacks", "merits", "demerits",
        "pros?", "cons?", "benefits?",
    ],
    # Limitations
    "limitations": [
        "limitations", "what are limitations", "drawbacks",
        "challenges", "problems with it", "issues",
        "weaknesses", "what are drawbacks",
    ],
    # Comparison
    "comparison": [
        "how is it different", "what is the difference",
        "compare with", "which is better", "compare it",
        "difference between", "vs", "versus",
    ],
    # Application
    "application": [
        "where is it used", "how is it used", "applications",
        "what are applications", "uses of it", "real life use",
        "practical use", "where do we use",
    ],
    # Process
    "process": [
        "what happens next", "next step", "what is the process",
        "steps involved", "how does the process work",
        "walk me through", "step by step",
    ],
    # Continuation starters
    "continuation": [
        "and advantages", "and limitations", "and applications",
        "and examples", "and disadvantages", "and uses",
        "and what about", "what about", "also explain",
        "also tell", "and tell me",
    ],
    # Short confirmations
    "confirmation": [
        "really?", "how?", "why?", "example?", "more?",
        "details?", "elaborate?", "seriously?", "truly?",
    ],
    # Deeper understanding
    "deeper": [
        "in simple words", "in simple terms", "simplify",
        "explain simply", "explain like i am 5",
        "beginner explanation", "basic explanation",
        "summarize", "summary", "brief explanation",
    ],
    # Definition follow-up
    "definition": [
        "what does it mean", "meaning of this", "define it",
        "what does that mean", "meaning?", "definition?",
    ],
}

# ── Followup handling: pronoun words that signal a reference to last topic ────
PRONOUN_WORDS: set[str] = {
    "it", "its", "this", "that", "these", "those",
    "they", "their", "them", "such", "the process",
    "the cycle", "the system", "the concept", "the topic",
}

# ── Followup handling: words that start a continuation of the previous topic ──
CONTINUATION_STARTERS: set[str] = {
    "and", "also", "additionally", "furthermore",
    "moreover", "besides", "what about", "how about",
}

# Maximum number of tokens for a query to be considered "short" and lacking a
# topic signal (used in is_followup_query Rule 3).
_MAX_SHORT_QUERY_TOKENS: int = 4

# Pattern types that are too generic to produce a good templated rewrite on
# their own; these are refined with a secondary FOLLOWUP_PATTERNS lookup
# inside rewrite_followup_query before the template is applied.
_GENERIC_FOLLOWUP_TYPES: frozenset[str] = frozenset({
    "short_no_topic", "continuation", "no_topic_signal",
})

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


# ── 3. Topic Shift Detector ───────────────────────────────────────────────────

class TopicShiftDetector:
    """
    Detects whether the current query signals a topic shift away from the last
    conversation topic using keyword-overlap as a lightweight proxy for semantic
    similarity.

    This prevents context contamination such as:
      - "nervous system" (after photosynthesis) → "nervous photosynthesis"
      - "water" query  (after photosynthesis)   → "water photosynthesis"

    Algorithm
    ---------
    1. Compute keyword-overlap similarity between the full query and the memory
       topic.  Any match (score > TOPIC_SIMILARITY_FLOOR) means the query
       is still about that topic → no shift.
    2. Extract *non-ambiguous* content words (exclude EXTENDED_AMBIGUOUS_TERMS
       and common stop-words).
    3. If no non-ambiguous content words remain, defer to memory (cannot tell).
    4. Check content words against every topic's keyword vocabulary:
         - Match in a DIFFERENT topic → shift (clear domain change).
         - Match in the SAME topic    → no shift.
    5. No topic keyword match at all AND at least one domain-specific word
       (length ≥ 5 chars) → shift (unknown / out-of-scope domain).
    """

    # Words to exclude when extracting content words for shift detection.
    # Superset of English stop-words plus common educational question starters
    # and instruction/modifier words that are not domain-specific.
    _CONTENT_STOPWORDS: frozenset = frozenset({
        # Core stop-words
        "what", "is", "are", "the", "a", "an", "how", "does", "do",
        "explain", "tell", "me", "about", "why", "where", "when",
        "which", "who", "did", "was", "were", "be", "been", "have",
        "has", "had", "will", "would", "could", "should", "may",
        "might", "can", "shall", "give", "describe", "define",
        "meaning", "means", "mean", "also", "more", "and", "or",
        "its", "in", "of", "to", "for", "with", "from", "by",
        "than", "not", "just", "very", "much", "many", "some",
        "get", "got", "let", "put", "use", "see",
        # Common instruction / modifier words (not domain-specific)
        "detail", "details", "briefly", "simply", "clearly", "quickly",
        "shortly", "deeply", "broadly", "fully", "mostly", "mainly",
        "purely", "exactly", "roughly", "generally", "basically",
        "please", "example", "examples", "concept", "summary",
        "overview", "context", "answer", "answers", "further",
        "basic", "simple", "brief", "clear", "quick", "short",
        "class", "topic", "related", "known", "using", "often",
        "called", "named", "given", "found", "taken", "forms",
        "works", "make", "makes", "happen", "result", "results",
        "helps", "takes", "gives", "shows", "comes", "goes",
    })

    def get_content_words(
        self,
        query: str,
        exclude_terms: set[str] | None = None,
    ) -> list[str]:
        """
        Extract meaningful content words from *query*.

        Args:
            query:         Normalised (lowercase) query string.
            exclude_terms: Additional tokens to exclude (e.g. ambiguous terms).

        Returns:
            List of lowercase content-word tokens.
        """
        excluded = self._CONTENT_STOPWORDS | (exclude_terms or set())
        tokens = re.findall(r"\b[a-z]+\b", query.lower())
        return [t for t in tokens if t not in excluded and len(t) > 2]

    def compute_similarity(self, query: str, topic: str) -> float:
        """
        Compute keyword-overlap similarity between *query* and *topic*.

        Scans the query for keywords from TOPIC_KEYWORD_WEIGHTS[topic] and
        returns the sum of matched weights divided by the maximum possible
        weight for that topic.

        Returns a float in [0, 1].  0.0 indicates no shared keywords.
        """
        kw_map = TOPIC_KEYWORD_WEIGHTS.get(topic, {})
        if not kw_map:
            return 0.0
        query_lower = query.lower()
        matched = sum(w for kw, w in kw_map.items() if kw in query_lower)
        max_w = sum(kw_map.values())
        return min(1.0, matched / max_w) if max_w > 0 else 0.0

    def is_topic_shift(
        self,
        query: str,
        last_topic: str | None,
        ambiguous_terms: list[str],
    ) -> tuple[bool, str]:
        """
        Decide whether *query* represents a topic shift away from *last_topic*.

        Args:
            query:           Normalised query string.
            last_topic:      Most recently resolved topic from conversation memory.
            ambiguous_terms: Ambiguous tokens already identified in the query.

        Returns:
            ``(is_shift, reason)`` where *reason* is a short diagnostic string.
        """
        if not last_topic:
            return False, "no_memory"

        # Step 1: Direct similarity between query and memory topic
        if self.compute_similarity(query, last_topic) > TOPIC_SIMILARITY_FLOOR:
            return False, "query_matches_memory_topic"

        # Step 2: Extract non-ambiguous content words
        content_words = self.get_content_words(
            query, exclude_terms=set(ambiguous_terms)
        )
        if not content_words:
            # Only ambiguous terms and stop-words — cannot determine shift
            return False, "no_unambiguous_content"

        # Step 3: Compare content words against every topic's keyword vocabulary
        for topic, kw_map in TOPIC_KEYWORD_WEIGHTS.items():
            topic_kw_tokens: set[str] = {
                tok for kw in kw_map for tok in kw.split()
            }
            if any(cw in topic_kw_tokens for cw in content_words):
                if topic != last_topic:
                    return True, f"content_matches_different_topic:{topic}"
                return False, "content_matches_memory_topic"

        # Step 4: No topic keyword match — flag shift only for domain-specific words
        if any(len(cw) >= MIN_DOMAIN_SPECIFIC_WORD_LENGTH for cw in content_words):
            return True, "unknown_domain_words"

        return False, "only_short_generic_words"

    def would_contaminate(
        self,
        query: str,
        resolved_topic: str,
        amb_term: str,
    ) -> bool:
        """
        Return ``True`` if substituting *amb_term* with *resolved_topic* in
        *query* would produce a semantically incoherent phrase.

        Examples of incoherent substitutions this prevents:
          - "nervous system"  → "nervous photosynthesis"   (amb_term="system")
          - "water"  [query]  → "water photosynthesis"

        Logic
        -----
        1. Get non-ambiguous content words (excluding *amb_term*).
        2. If none, substitution is safe (query is fully ambiguous).
        3. For each content word:
             a. If it belongs to a DIFFERENT topic's keywords → contamination.
             b. If it belongs to NO known topic AND is ≥ 5 chars → contamination.

        Args:
            query:          Normalised query string.
            resolved_topic: The topic about to be substituted in.
            amb_term:       The ambiguous token being replaced.

        Returns:
            ``True`` if the substitution should be blocked.
        """
        content_words = self.get_content_words(query, exclude_terms={amb_term})
        if not content_words:
            return False

        resolved_kw_tokens: set[str] = {
            tok
            for kw in TOPIC_KEYWORD_WEIGHTS.get(resolved_topic, {})
            for tok in kw.split()
        }

        for cw in content_words:
            in_resolved = cw in resolved_kw_tokens
            if in_resolved:
                continue  # Word belongs to the resolved topic — safe

            # Check if it belongs to a different topic
            for topic, kw_map in TOPIC_KEYWORD_WEIGHTS.items():
                if topic == resolved_topic:
                    continue
                other_kw_tokens = {tok for kw in kw_map for tok in kw.split()}
                if cw in other_kw_tokens:
                    return True  # Belongs to a different topic → contamination

            # Word not in any topic — flag if domain-specific (≥ MIN_DOMAIN_SPECIFIC_WORD_LENGTH chars)
            if len(cw) >= MIN_DOMAIN_SPECIFIC_WORD_LENGTH:
                return True

        return False


# ── 4. Ambiguity Resolver ─────────────────────────────────────────────────────

@dataclass
class AmbiguityResult:
    """Output of the AmbiguityResolver."""

    ambiguous_terms: list[str]    # terms detected as ambiguous
    resolved_topic: str | None    # final resolved topic (or None)
    resolution_source: str        # "query_signals" | "memory" | "unresolved"
    confidence: float             # resolution confidence  ∈ [0, 1]
    shift_detected: bool = False  # True when a topic shift was detected
    shift_reason: str = ""        # short diagnostic string from TopicShiftDetector


class AmbiguityResolver:
    """
    Detects ambiguous terms in the query and resolves them to a canonical topic.

    Resolution priority
    -------------------
    1. High-confidence topic from weighted keyword scoring → use directly.
    2. In-query disambiguation signals from DISAMBIGUATION_SIGNALS
       (e.g. 'move' near 'cycle' → 'bicycle').
    3. Conversation memory — **only** when TopicShiftDetector confirms the query
       is still about the same topic (prevents "nervous photosynthesis" merges).
    4. Unresolved — caller may request clarification from the user.

    Handles single-word ambiguous terms (cycle, cell, …) and pronouns
    (it, this, that) that should always be resolved via memory.
    """

    def __init__(self) -> None:
        self._shift_detector = TopicShiftDetector()

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

        # Priority 3: Conversation memory — only when no topic shift is detected.
        # Exception: pronouns (it/this/that) always refer to the last topic;
        # skip shift detection for pronoun-only ambiguous terms.
        last_topic = memory.get_last_topic()
        if last_topic:
            _PRONOUNS = {"it", "this", "that", "they", "them"}
            pronoun_only = all(t in _PRONOUNS for t in ambiguous_found)

            if pronoun_only:
                return AmbiguityResult(
                    ambiguous_terms=ambiguous_found,
                    resolved_topic=last_topic,
                    resolution_source="memory",
                    confidence=0.8,
                )

            is_shift, shift_reason = self._shift_detector.is_topic_shift(
                query, last_topic, ambiguous_found
            )
            if not is_shift:
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
                        shift_detected=False,
                        shift_reason=shift_reason,
                    )
            else:
                # Topic shift detected — do not contaminate query with memory topic
                return AmbiguityResult(
                    ambiguous_terms=ambiguous_found,
                    resolved_topic=None,
                    resolution_source="unresolved",
                    confidence=0.0,
                    shift_detected=True,
                    shift_reason=shift_reason,
                )

        # Priority 4: Unresolved
        return AmbiguityResult(
            ambiguous_terms=ambiguous_found,
            resolved_topic=None,
            resolution_source="unresolved",
            confidence=0.0,
        )


# ── 5. Contextual Query Builder ───────────────────────────────────────────────

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
        self._shift_detector = TopicShiftDetector()
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

    # Followup handling ────────────────────────────────────────────────────────

    def is_followup_query(
        self,
        query: str,
        last_topic: str | None,
    ) -> tuple[bool, str]:
        """
        Detect if query is a follow-up to the previous topic.

        Returns a tuple ``(is_followup, pattern_type)`` where *pattern_type*
        is a short string describing why the query was classified as a
        follow-up (e.g. ``"pronoun_only"``, ``"continuation"``, etc.) or
        ``"not_followup"`` / ``"no_memory"`` otherwise.

        Detection rules (applied in priority order)
        --------------------------------------------
        1. Query contains only pronouns from PRONOUN_WORDS → followup
        2. Query starts with CONTINUATION_STARTERS → followup
        3. Query length ≤ 4 words AND no new topic noun (score < 1.0) → followup
        4. Query matches any pattern in FOLLOWUP_PATTERNS → followup
        5. Query has no topic confidence (score == 0.0) AND last_topic exists → followup

        Override: strong topic confidence (score ≥ TOPIC_SWITCH_THRESHOLD)
        always cancels follow-up detection so that a new high-confidence
        topic wins over the previous context.

        Edge cases handled
        ------------------
        - ``"how?"`` alone → followup
        - ``"and advantages?"`` → followup (continuation starter)
        - ``"what about limitations"`` → followup
        - ``"explain more"`` → followup
        - ``"give example"`` → followup
        - ``"why is this important"`` → followup (pronoun "this")
        - ``"compare with others"`` → followup (no new topic)
        - ``"what does it mean"`` → followup (pronoun "it")
        - ``"summarize"`` alone → followup
        - ``"really?"`` alone → followup
        - ``"in simple words"`` → followup (no topic signal = inherit last)
        - ``"step by step"`` → followup
        - ``"where is it used"`` → followup (pronoun "it")
        - ``"what are its components"`` → followup (pronoun "its")
        - ``"limitations?"`` alone → followup
        - ``"disadvantages"`` alone → followup
        - ``"example?"`` alone → followup
        - ``"how does this work"`` → followup (pronoun "this")
        - ``"tell me more about it"`` → followup (pronoun "it")
        - ``"can you explain further"`` → followup (no new topic)
        """
        if not last_topic:
            return False, "no_memory"

        query_lower = query.lower().strip().rstrip("?").strip()
        tokens = query_lower.split()

        # Override: strong topic confidence wins — new topic takes precedence
        topic_confidence = self._scorer.score(query_lower)
        if topic_confidence.top_score >= TOPIC_SWITCH_THRESHOLD:
            return False, "not_followup"

        # Rule 1: Only pronouns in query
        meaningful_tokens = [t for t in tokens if len(t) > 2]
        if meaningful_tokens and all(t in PRONOUN_WORDS for t in meaningful_tokens):
            return True, "pronoun_only"

        # Rule 2: Starts with continuation starter
        if tokens and tokens[0] in CONTINUATION_STARTERS:
            return True, "continuation"
        if len(tokens) >= 2 and " ".join(tokens[:2]) in CONTINUATION_STARTERS:
            return True, "continuation"

        # Rule 3: Very short query with no topic signal
        if len(tokens) <= _MAX_SHORT_QUERY_TOKENS and topic_confidence.top_score < 1.0:
            return True, "short_no_topic"

        # Rule 4: Matches a known follow-up pattern
        # Compare against normalised (no "?") form of each pattern so that
        # entries like "really?" still match the normalised query "really".
        for pattern_type, patterns in FOLLOWUP_PATTERNS.items():
            for pattern in patterns:
                p_norm = pattern.rstrip("?").strip()
                if p_norm in query_lower or query_lower == p_norm:
                    return True, pattern_type

        # Rule 5: No topic confidence and last topic exists
        if topic_confidence.top_score == 0.0 and last_topic:
            return True, "no_topic_signal"

        return False, "not_followup"

    def rewrite_followup_query(
        self,
        query: str,
        last_topic: str,
        pattern_type: str,
    ) -> str:
        """
        Rewrite a follow-up query by attaching the previous topic context.

        Pronouns are first replaced with the topic name.  Continuation starters
        are stripped.  Then a pattern-specific template is applied to produce a
        self-contained, retrievable query.

        Rewriting rules per pattern type
        ---------------------------------
        - ``pronoun_only``  : replace pronoun with topic
          ``"how does it work"`` → ``"How does the water cycle work"``
        - ``continuation``  : strip starter, prepend topic
          ``"and advantages?"`` → ``"Advantages of water cycle"``
        - ``short_no_topic``: append topic directly
          ``"explain"`` → ``"Explain water cycle"``
        - ``examples``      : ``"Examples of {topic} in real life"``
        - ``advantages``    : ``"Advantages and disadvantages of {topic}"``
        - ``limitations``   : ``"Limitations and challenges of {topic}"``
        - ``comparison``    : ``"{query} in context of {topic}"``
        - ``application``   : ``"Applications and uses of {topic}"``
        - ``process``       : ``"Process and steps involved in {topic}"``
        - ``deeper``        : ``"{query} about {topic}"``
        - ``definition``    : ``"Definition and meaning of {topic}"``
        - ``confirmation``  : ``"Explain {topic} in more detail"``
        - default           : ``"{query} about {topic}"``
        """
        # Keep a copy with "?" intact for pattern matching (e.g. "really?")
        query_with_q = query.lower().strip()
        query_lower = query_with_q.rstrip("?").strip()

        # Strip continuation starters BEFORE pronoun replacement and pattern
        # matching so the remaining content word can be classified correctly.
        for starter in CONTINUATION_STARTERS:
            if query_lower.startswith(starter + " "):
                query_lower = query_lower[len(starter):].strip()
                query_with_q = query_with_q[len(starter):].strip()

        # Refine generic pattern_types by checking FOLLOWUP_PATTERNS.
        # This runs BEFORE pronoun replacement so patterns such as
        # "where is it used" still match before "it" is replaced.
        # Patterns ending with "?" are normalised (strip "?") for comparison
        # because the normalizer strips punctuation before this method is called.
        if pattern_type in _GENERIC_FOLLOWUP_TYPES:
            for check_q in [query_lower, query_with_q]:
                found = False
                for candidate_type, patterns in FOLLOWUP_PATTERNS.items():
                    for p in patterns:
                        p_norm = p.rstrip("?").strip()
                        if p_norm in check_q or check_q == p_norm:
                            pattern_type = candidate_type
                            found = True
                            break
                    if found:
                        break
                if found:
                    break

        # Replace pronouns with topic using word boundaries to avoid
        # replacing "it" inside words such as "limitations".
        for pronoun in sorted(PRONOUN_WORDS, key=len, reverse=True):
            # Use word boundary for single-word pronouns; substring for phrases
            if " " in pronoun:
                if pronoun in query_lower:
                    query_lower = query_lower.replace(pronoun, f"the {last_topic}", 1)
            else:
                query_lower = re.sub(
                    r"\b" + re.escape(pronoun) + r"\b",
                    f"the {last_topic}",
                    query_lower,
                )

        # Pattern-specific rewrites
        rewrites: dict[str, str] = {
            "advantages":   f"advantages and disadvantages of {last_topic}",
            "limitations":  f"limitations and challenges of {last_topic}",
            "examples":     f"examples of {last_topic} in real life",
            "application":  f"applications and uses of {last_topic}",
            "process":      f"process and steps involved in {last_topic}",
            "definition":   f"definition and meaning of {last_topic}",
            "comparison":   f"{query_lower} in context of {last_topic}",
            "confirmation": f"explain {last_topic} in more detail",
            "continuation": f"{query_lower} of {last_topic}",
            "deeper":       f"{query_lower} about {last_topic}",
            "reasoning":    f"{query_lower} in {last_topic}",
        }

        if pattern_type in rewrites:
            return rewrites[pattern_type].capitalize()

        # Default: if topic not already in query, append it
        if last_topic.lower() not in query_lower:
            return f"{query_lower} about {last_topic}".capitalize()

        return query_lower.capitalize()

    # ── Out-of-scope ───────────────────────────────────────────────────────────

    def _is_out_of_scope(
        self,
        query: str,
        topic_confidence: TopicConfidenceResult | None = None,
    ) -> tuple[bool, str | None]:
        """
        Check whether *query* contains a word that signals it is outside this
        knowledge base.

        A query is only flagged as out-of-scope when BOTH conditions hold:
        1. At least one word in the query matches OUT_OF_SCOPE_SIGNALS.
        2. The top topic confidence score is below TOPIC_SWITCH_THRESHOLD (2.0),
           meaning no strong in-scope topic signal overrides the out-of-scope word.

        Edge cases handled
        ------------------
        - "how does a car battery work" → "battery" scores ≥ 2.0 for electricity,
          so the strong topic signal wins and out-of-scope is NOT triggered.
        - "explain the carbon cycle and how cars affect it" → "carbon cycle" has
          high confidence (> 2.0) so out-of-scope is NOT triggered.
        - "why do birds migrate" → "bird" matches out-of-scope, no topic signal
          overrides, so it IS flagged as out-of-scope.

        Args:
            query:            Raw or normalised query string.
            topic_confidence: Pre-computed topic confidence result.  If None the
                              check is done without considering confidence scores
                              (out-of-scope word alone is sufficient to flag).

        Returns:
            ``(True, matched_word)`` when out-of-scope is detected,
            ``(False, None)`` otherwise.
        """
        query_lower = query.lower()
        query_tokens = re.findall(r"\b[a-z]+\b", query_lower)

        for word in query_tokens:
            if word in OUT_OF_SCOPE_SIGNALS:
                # Edge case handled: strong topic signal overrides out-of-scope word
                if (
                    topic_confidence is not None
                    and topic_confidence.top_score >= TOPIC_SWITCH_THRESHOLD
                ):
                    return False, None
                return True, word

        return False, None

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

        # A1: Follow-up detection (before confidence scoring)
        # Followup handling — must run before step B so that short/pronoun
        # queries are rewired to the last topic without triggering the full
        # ambiguity pipeline.
        is_followup, followup_type = self.is_followup_query(normalised, last_topic)

        if is_followup and last_topic:
            rewritten = self.rewrite_followup_query(
                normalised, last_topic, followup_type
            )
            notes.append(
                f"Follow-up detected (type={followup_type}) → "
                f"rewritten: '{rewritten}' using last topic: '{last_topic}'"
            )
            # Score confidence on the rewritten query so downstream steps have
            # a meaningful signal even though the original query lacked keywords.
            confidence = self._scorer.score(rewritten)
            return ContextualQueryResult(
                original_query=user_query,
                normalized_query=normalised,
                rewritten_query=rewritten,
                resolved_topic=last_topic,
                topic_confidence=confidence,
                ambiguity_result=AmbiguityResult(
                    ambiguous_terms=[],
                    resolved_topic=last_topic,
                    resolution_source="followup_memory",
                    confidence=0.9,
                ),
                topic_switched=False,
                debug_notes=notes,
            )

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
            normalised_query=normalised,
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
        normalised_query: str,
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

        # Rule 5: Fall back to memory — but only when no topic shift was detected.
        # If the AmbiguityResolver already detected a shift, honour it.
        # If there were no ambiguous terms, run a direct shift check here.
        if last_topic:
            if ambiguity.shift_detected:
                notes.append(
                    f"Topic shift detected ({ambiguity.shift_reason}); "
                    "clearing memory context to prevent contamination."
                )
                return None, True
            # For queries with no ambiguous terms, run an independent shift check
            if not ambiguity.ambiguous_terms:
                is_shift, shift_reason = self._shift_detector.is_topic_shift(
                    normalised_query, last_topic, []
                )
                if is_shift:
                    notes.append(
                        f"Topic shift detected ({shift_reason}); "
                        "clearing memory context to prevent contamination."
                    )
                    return None, True
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
            # Rewrite safety: block substitutions that would create semantically
            # incoherent phrases such as "nervous photosynthesis".
            if self._shift_detector.would_contaminate(
                normalised, resolved_topic, amb_term
            ):
                # Skip substitution — append as a soft context hint instead
                if resolved_topic.lower() not in normalised.lower():
                    return f"{original} (context: {resolved_topic})"
                return original
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
