"""
data_loader.py
--------------
Defines the educational knowledge base for the RAG system.
Each document has: text, subject, topic, grade metadata.
Topics covered: water cycle, carbon cycle, bicycle, photosynthesis.
"""

from extended_corpus_v2 import EXTENDED_DOCUMENTS_V2
from extended_corpus_v3 import EXTENDED_DOCUMENTS_V3
from extended_corpus_v4 import GEOGRAPHY_EXTENDED_V3
from extended_corpus_v5 import EXTENDED_DOCUMENTS_V5
from extended_corpus_v6 import EXTENDED_DOCUMENTS_V6
from extended_corpus_v7 import EXTENDED_DOCUMENTS_V7
from extended_corpus_v8 import EXTENDED_DOCUMENTS_V8
from extended_corpus_v9 import EXTENDED_DOCUMENTS_V9

EDUCATIONAL_DOCUMENTS = [
    # ── WATER CYCLE ──────────────────────────────────────────────────────────
    {
        "text": (
            "The water cycle, also called the hydrological cycle, is the continuous movement "
            "of water through Earth's systems. Water evaporates from oceans and lakes when "
            "heated by the sun, rises as water vapour, cools to form clouds through condensation, "
            "and falls back as precipitation — rain or snow."
        ),
        "subject": "geography",
        "topic": "water cycle",
        "grade": "6",
    },
    {
        "text": (
            "Evaporation is the key driver of the water cycle. Heat energy from the sun converts "
            "liquid water from oceans, rivers, and lakes into water vapour. This vapour rises "
            "into the atmosphere, where cooler temperatures cause it to condense around tiny dust "
            "particles, forming clouds and eventually precipitation."
        ),
        "subject": "geography",
        "topic": "water cycle",
        "grade": "6",
    },
    {
        "text": (
            "Transpiration is the process by which plants release water vapour through tiny pores "
            "called stomata in their leaves. Together with evaporation from soil and water bodies, "
            "it is called evapotranspiration. This contributes significantly to the moisture "
            "present in the atmosphere and is an important part of the water cycle."
        ),
        "subject": "biology",
        "topic": "water cycle",
        "grade": "7",
    },
    {
        "text": (
            "Groundwater recharge occurs when precipitation soaks into the soil through a process "
            "called infiltration. This water replenishes aquifers underground. Groundwater can "
            "re-enter rivers and the ocean through springs, completing the cycle. Run-off occurs "
            "when water flows over land into rivers and ultimately into the sea."
        ),
        "subject": "geography",
        "topic": "water cycle",
        "grade": "7",
    },

    # ── CARBON CYCLE ─────────────────────────────────────────────────────────
    {
        "text": (
            "The carbon cycle describes how carbon atoms move through Earth's atmosphere, "
            "oceans, soil, and living organisms. Plants absorb carbon dioxide (CO₂) from the "
            "atmosphere during photosynthesis. Animals obtain carbon by eating plants. When "
            "organisms die, decomposers break them down, releasing CO₂ back into the atmosphere."
        ),
        "subject": "biology",
        "topic": "carbon cycle",
        "grade": "8",
    },
    {
        "text": (
            "Fossil fuels — coal, oil, and natural gas — are ancient carbon stores formed from "
            "buried organic matter over millions of years. Burning them releases CO₂ back into "
            "the atmosphere rapidly, disrupting the natural carbon cycle and contributing to "
            "climate change. This is why they are called carbon emissions."
        ),
        "subject": "environmental science",
        "topic": "carbon cycle",
        "grade": "9",
    },
    {
        "text": (
            "The ocean acts as a major carbon sink, absorbing about 25% of human CO₂ emissions. "
            "Marine organisms like coral and shellfish use dissolved CO₂ to build calcium "
            "carbonate shells. When they die, the shells sink and eventually form limestone "
            "rock, locking carbon away for geological timescales."
        ),
        "subject": "environmental science",
        "topic": "carbon cycle",
        "grade": "9",
    },

    # ── BICYCLE ──────────────────────────────────────────────────────────────
    {
        "text": (
            "A bicycle is a human-powered vehicle with two wheels connected by a frame. "
            "The rider sits on a saddle, steers using handlebars, and propels the bicycle "
            "by pushing pedals that turn a chain drive connected to the rear wheel. "
            "Bicycles are one of the most energy-efficient forms of transportation ever invented."
        ),
        "subject": "transportation",
        "topic": "bicycle",
        "grade": "5",
    },
    {
        "text": (
            "The gear system on a bicycle lets the rider adjust mechanical advantage. "
            "Shifting to a smaller front sprocket or larger rear sprocket makes pedalling "
            "easier when climbing hills. Shifting to a larger front sprocket increases speed "
            "on flat roads. Derailleur gears work by moving the chain between sprockets of "
            "different sizes."
        ),
        "subject": "physics",
        "topic": "bicycle",
        "grade": "8",
    },
    {
        "text": (
            "Bicycle brakes work by applying friction to the wheel rim or disc. Rim brakes "
            "use rubber pads pressed against the metal rim. Disc brakes clamp a rotor attached "
            "to the wheel hub. When the rider squeezes the brake lever, a cable or hydraulic "
            "fluid transmits force to the caliper, slowing the bicycle."
        ),
        "subject": "physics",
        "topic": "bicycle",
        "grade": "8",
    },
    {
        "text": (
            "Riding a bicycle involves balance and gyroscopic stability. A moving bicycle "
            "stays upright partly because spinning wheels act like gyroscopes that resist "
            "changes in orientation. Riders also maintain balance by subtly steering — a "
            "technique called countersteering — which shifts the centre of mass over the "
            "wheel contact points."
        ),
        "subject": "physics",
        "topic": "bicycle",
        "grade": "9",
    },

    # ── PHOTOSYNTHESIS ───────────────────────────────────────────────────────
    {
        "text": (
            "Photosynthesis is the process by which green plants, algae, and some bacteria "
            "convert sunlight, water, and carbon dioxide into glucose and oxygen. It occurs "
            "mainly in the chloroplasts of plant cells, which contain the green pigment "
            "chlorophyll. The overall equation is: 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂."
        ),
        "subject": "biology",
        "topic": "photosynthesis",
        "grade": "7",
    },
    {
        "text": (
            "The light-dependent reactions of photosynthesis occur in the thylakoid membranes "
            "of the chloroplast. Chlorophyll absorbs sunlight and uses the energy to split water "
            "molecules, releasing oxygen as a by-product. The energy is stored as ATP and NADPH, "
            "which power the next stage of photosynthesis."
        ),
        "subject": "biology",
        "topic": "photosynthesis",
        "grade": "10",
    },
    {
        "text": (
            "The Calvin cycle (light-independent reactions) takes place in the stroma of the "
            "chloroplast. Using ATP and NADPH from the light reactions, the cycle fixes carbon "
            "dioxide into organic molecules through a process called carbon fixation. The enzyme "
            "RuBisCO catalyses the first step, combining CO₂ with a 5-carbon molecule to "
            "ultimately produce glucose."
        ),
        "subject": "biology",
        "topic": "photosynthesis",
        "grade": "11",
    },
    {
        "text": (
            "Factors that affect the rate of photosynthesis include light intensity, CO₂ "
            "concentration, and temperature. At low light levels, increasing light speeds "
            "up photosynthesis. However, at high light intensities the rate plateaus because "
            "other factors become limiting. Chlorophyll best absorbs red and blue light, "
            "reflecting green light — which is why plants appear green."
        ),
        "subject": "biology",
        "topic": "photosynthesis",
        "grade": "8",
    },
]

EDUCATIONAL_DOCUMENTS += EXTENDED_DOCUMENTS_V2
EDUCATIONAL_DOCUMENTS += EXTENDED_DOCUMENTS_V3
EDUCATIONAL_DOCUMENTS += GEOGRAPHY_EXTENDED_V3
EDUCATIONAL_DOCUMENTS += EXTENDED_DOCUMENTS_V5
EDUCATIONAL_DOCUMENTS += EXTENDED_DOCUMENTS_V6
EDUCATIONAL_DOCUMENTS += EXTENDED_DOCUMENTS_V7
EDUCATIONAL_DOCUMENTS += EXTENDED_DOCUMENTS_V8
EDUCATIONAL_DOCUMENTS += EXTENDED_DOCUMENTS_V9


def get_documents() -> list[dict]:
    """Return the full list of educational documents."""
    return EDUCATIONAL_DOCUMENTS


def get_texts_and_metadatas() -> tuple[list[str], list[dict]]:
    """Split documents into (texts, metadatas) for embedding."""
    texts = [doc["text"] for doc in EDUCATIONAL_DOCUMENTS]
    metadatas = [
        {"subject": doc["subject"], "topic": doc["topic"], "grade": doc["grade"]}
        for doc in EDUCATIONAL_DOCUMENTS
    ]
    return texts, metadatas


def get_chunked_texts_and_metadatas(
    chunk_size: int = 400,
    chunk_overlap: int = 50,
) -> tuple[list[str], list[dict]]:
    """
    Return (texts, metadatas) after splitting each document into smaller chunks
    using a RecursiveCharacterTextSplitter.

    Chunking improves retrieval precision for long documents by ensuring that
    each vector-store entry covers a focused concept rather than a broad topic.

    Args:
        chunk_size:    Maximum number of characters per chunk (default 400).
        chunk_overlap: Number of overlapping characters between consecutive
                       chunks so that context at chunk boundaries is not lost
                       (default 50).

    Returns:
        Two parallel lists:
          - texts:     The chunked text strings.
          - metadatas: Corresponding metadata dicts (topic, subject, grade,
                       plus ``chunk_index`` and ``source_doc_index``).
    """
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", ", ", " ", ""],
    )

    chunked_texts: list[str] = []
    chunked_metadatas: list[dict] = []

    for doc_idx, doc in enumerate(EDUCATIONAL_DOCUMENTS):
        chunks = splitter.split_text(doc["text"])
        for chunk_idx, chunk in enumerate(chunks):
            chunked_texts.append(chunk)
            chunked_metadatas.append({
                "subject": doc["subject"],
                "topic": doc["topic"],
                "grade": doc["grade"],
                "chunk_index": chunk_idx,
                "source_doc_index": doc_idx,
            })

    return chunked_texts, chunked_metadatas


def get_corpus_stats() -> dict:
    """Compute and return statistics about EDUCATIONAL_DOCUMENTS.

    Returns a dict with:
        total_documents     : int
        unique_topics       : int
        unique_subjects     : int
        topics_under_5      : dict[str, int]  topics with fewer than 5 docs
        topics_over_10      : dict[str, int]  topics with more than 10 docs
        subject_distribution: dict[str, int]
        grade_distribution  : dict[str, int]
        average_text_length : float  (characters)
        topic_distribution  : dict[str, int]
    """
    from collections import Counter

    topic_counts: dict[str, int] = Counter(doc["topic"] for doc in EDUCATIONAL_DOCUMENTS)
    subject_counts: dict[str, int] = Counter(doc["subject"] for doc in EDUCATIONAL_DOCUMENTS)
    grade_counts: dict[str, int] = Counter(doc["grade"] for doc in EDUCATIONAL_DOCUMENTS)
    avg_len = (
        sum(len(doc["text"]) for doc in EDUCATIONAL_DOCUMENTS) / len(EDUCATIONAL_DOCUMENTS)
        if EDUCATIONAL_DOCUMENTS
        else 0.0
    )

    return {
        "total_documents": len(EDUCATIONAL_DOCUMENTS),
        "unique_topics": len(topic_counts),
        "unique_subjects": len(subject_counts),
        "topics_under_5": {t: c for t, c in topic_counts.items() if c < 5},
        "topics_over_10": {t: c for t, c in topic_counts.items() if c > 10},
        "subject_distribution": dict(subject_counts),
        "grade_distribution": dict(grade_counts),
        "average_text_length": avg_len,
        "topic_distribution": dict(topic_counts),
    }


def get_topic_coverage_warnings() -> list[str]:
    """Return topic names that have fewer than 5 documents in the corpus."""
    stats = get_corpus_stats()
    return list(stats["topics_under_5"].keys())
