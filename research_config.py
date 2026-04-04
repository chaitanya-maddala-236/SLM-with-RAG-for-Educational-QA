"""
research_config.py
------------------
Configuration constants and test-query definitions for the research
evaluation system.

Usage:
    from research_config import (
        MODELS_TO_EVALUATE, RETRIEVAL_MODES, RESULTS_FILE, TEST_QUERIES,
        EMBEDDING_MODELS, DEFAULT_EMBEDDING,
        CHROMA_DIR_TEMPLATE, COLLECTION_NAME_TEMPLATE,
        MODEL_REGISTRY, get_model_config, get_embedding_config,
    )
"""

# ── Model registry ───────────────────────────────────────────────────────────
# Maps model identifiers to metadata used for evaluation and cost tracking.
# type="slm"  → free / locally-hosted (Ollama) models
# type="llm"  → paid API-hosted models

MODEL_REGISTRY: dict[str, dict] = {
    # ── SLMs (free / local) ──────────────────────────────────────────────────
    "tinyllama": {
        "type": "slm",
        "input_cost_per_1k": 0.0,
        "output_cost_per_1k": 0.0,
        "description": "TinyLlama 1.1B — very fast, minimal RAM, ideal for edge testing",
    },
    "phi3": {
        "type": "slm",
        "input_cost_per_1k": 0.0,
        "output_cost_per_1k": 0.0,
        "description": "Microsoft Phi-3 Mini — strong reasoning for its size",
    },
    "llama3.2": {
        "type": "slm",
        "input_cost_per_1k": 0.0,
        "output_cost_per_1k": 0.0,
        "description": "Meta Llama 3.2 — compact multilingual model",
    },
    "mistral": {
        "type": "slm",
        "input_cost_per_1k": 0.0,
        "output_cost_per_1k": 0.0,
        "description": "Mistral 7B — balanced quality/speed for local inference",
    },
    # ── LLMs (paid API) ──────────────────────────────────────────────────────
    "gpt-3.5-turbo": {
        "type": "llm",
        "input_cost_per_1k": 0.0005,
        "output_cost_per_1k": 0.0015,
        "description": "OpenAI GPT-3.5 Turbo — fast, cost-effective API model",
    },
    "gpt-4o-mini": {
        "type": "llm",
        "input_cost_per_1k": 0.00015,
        "output_cost_per_1k": 0.0006,
        "description": "OpenAI GPT-4o Mini — strong capability at low cost",
    },
}

# ── Experiment axes ──────────────────────────────────────────────────────────

# Dynamically select all SLM entries from MODEL_REGISTRY
MODELS_TO_EVALUATE: list[str] = [
    name for name, cfg in MODEL_REGISTRY.items() if cfg["type"] == "slm"
]
RETRIEVAL_MODES = ["vector_only", "bm25_only", "hybrid"]
RESULTS_FILE = "research_results.txt"

# Embedding support: available embedding models for research evaluation
EMBEDDING_MODELS = [
    {
        "name": "bge-small",
        "model_id": "BAAI/bge-small-en-v1.5",
        "description": "BGE Small — fast, 384-dim (current default)",
        "dimension": 384,
    },
    {
        "name": "bge-base",
        "model_id": "BAAI/bge-base-en-v1.5",
        "description": "BGE Base — balanced, 768-dim",
        "dimension": 768,
    },
    {
        "name": "bge-large",
        "model_id": "BAAI/bge-large-en-v1.5",
        "description": "BGE Large — highest quality, 1024-dim",
        "dimension": 1024,
    },
    {
        "name": "minilm",
        "model_id": "sentence-transformers/all-MiniLM-L6-v2",
        "description": "MiniLM — very fast, 384-dim",
        "dimension": 384,
    },
    {
        "name": "mpnet",
        "model_id": "sentence-transformers/all-mpnet-base-v2",
        "description": "MPNet — strong general purpose, 768-dim",
        "dimension": 768,
    },
    {
        "name": "e5-small",
        "model_id": "intfloat/e5-small-v2",
        "description": "E5 Small — instruction-tuned, 384-dim",
        "dimension": 384,
    },
    {
        "name": "e5-base",
        "model_id": "intfloat/e5-base-v2",
        "description": "E5 Base — instruction-tuned, 768-dim",
        "dimension": 768,
    },
]

# Default embedding (current system)
DEFAULT_EMBEDDING = "bge-small"

# Chroma persist directory template
# Each embedding gets its own collection to avoid dimension mismatch
CHROMA_DIR_TEMPLATE = "./chroma_db_{embedding_name}"
COLLECTION_NAME_TEMPLATE = "educational_rag_{embedding_name}"

# ── Structured test-query suite ──────────────────────────────────────────────
#
# Each entry is a dict with:
#   id                  – unique identifier (string)
#   category            – query category (string)
#   query               – raw query text (string)
#   expected_topic      – expected resolved topic, or None
#   conversation_reset  – True → fresh ConversationMemory before this query
#   depends_on          – id of the query that must precede this one (optional)
#   expected_keywords   – list of strings that should appear in the answer
#   expected_mode       – "RAG", "Partial RAG", or "LLM Fallback"
#   note                – optional explanatory annotation (string)

TEST_QUERIES = [
    # ── DIRECT ──────────────────────────────────────────────────────────────
    {
        "id": "D01", "category": "direct",
        "query": "explain water cycle",
        "expected_topic": "water cycle", "conversation_reset": True,
        "expected_keywords": ["evaporation", "condensation", "precipitation"],
        "expected_mode": "RAG",
    },
    {
        "id": "D02", "category": "direct",
        "query": "how does photosynthesis work",
        "expected_topic": "photosynthesis", "conversation_reset": True,
        "expected_keywords": ["chlorophyll", "glucose", "sunlight"],
        "expected_mode": "RAG",
    },
    {
        "id": "D03", "category": "direct",
        "query": "what is the nitrogen cycle",
        "expected_topic": "nitrogen cycle", "conversation_reset": True,
        "expected_keywords": ["nitrogen", "nitrification", "bacteria"],
        "expected_mode": "RAG",
    },
    {
        "id": "D04", "category": "direct",
        "query": "explain bicycle gears",
        "expected_topic": "bicycle", "conversation_reset": True,
        "expected_keywords": ["gear", "sprocket", "chain"],
        "expected_mode": "RAG",
    },
    {
        "id": "D05", "category": "direct",
        "query": "what is carbon cycle",
        "expected_topic": "carbon cycle", "conversation_reset": True,
        "expected_keywords": ["carbon", "co2", "fossil"],
        "expected_mode": "RAG",
    },

    # ── FOLLOWUP PRONOUN — after D01 ─────────────────────────────────────────
    {
        "id": "F01", "category": "followup_pronoun",
        "query": "how does it work",
        "expected_topic": "water cycle", "conversation_reset": False,
        "depends_on": "D01",
        "expected_keywords": ["evaporation", "water"],
        "expected_mode": "RAG",
        "note": "pronoun it → water cycle",
    },
    {
        "id": "F02", "category": "followup_pronoun",
        "query": "what are its components",
        "expected_topic": "water cycle", "conversation_reset": False,
        "depends_on": "D01",
        "expected_keywords": ["evaporation", "condensation"],
        "expected_mode": "RAG",
        "note": "possessive its → water cycle",
    },
    {
        "id": "F03", "category": "followup_pronoun",
        "query": "why does this happen",
        "expected_topic": "water cycle", "conversation_reset": False,
        "depends_on": "D01",
        "expected_keywords": ["sun", "heat"],
        "expected_mode": "RAG",
        "note": "this → water cycle",
    },
    {
        "id": "F04", "category": "followup_pronoun",
        "query": "where does it occur",
        "expected_topic": "water cycle", "conversation_reset": False,
        "depends_on": "D01",
        "expected_keywords": ["ocean", "atmosphere"],
        "expected_mode": "RAG",
        "note": "it location → water cycle",
    },

    # ── FOLLOWUP SHORT — after D02 ───────────────────────────────────────────
    {
        "id": "S01", "category": "followup_short",
        "query": "advantages",
        "expected_topic": "photosynthesis", "conversation_reset": False,
        "depends_on": "D02",
        "expected_keywords": ["oxygen", "glucose"],
        "expected_mode": "RAG",
        "note": "single word → advantages of photosynthesis",
    },
    {
        "id": "S02", "category": "followup_short",
        "query": "limitations?",
        "expected_topic": "photosynthesis", "conversation_reset": False,
        "depends_on": "D02",
        "expected_keywords": ["light", "temperature"],
        "expected_mode": "RAG",
    },
    {
        "id": "S03", "category": "followup_short",
        "query": "give example",
        "expected_topic": "photosynthesis", "conversation_reset": False,
        "depends_on": "D02",
        "expected_keywords": ["plant", "leaf"],
        "expected_mode": "RAG",
    },
    {
        "id": "S04", "category": "followup_short",
        "query": "explain more",
        "expected_topic": "photosynthesis", "conversation_reset": False,
        "depends_on": "D02",
        "expected_keywords": ["chlorophyll"],
        "expected_mode": "RAG",
    },
    {
        "id": "S05", "category": "followup_short",
        "query": "why?",
        "expected_topic": "photosynthesis", "conversation_reset": False,
        "depends_on": "D02",
        "expected_keywords": ["sun", "energy"],
        "expected_mode": "RAG",
    },

    # ── CONTINUATION — after D03 ─────────────────────────────────────────────
    {
        "id": "C01", "category": "continuation",
        "query": "and what are its stages",
        "expected_topic": "nitrogen cycle", "conversation_reset": False,
        "depends_on": "D03",
        "expected_keywords": ["nitrification", "fixation"],
        "expected_mode": "RAG",
    },
    {
        "id": "C02", "category": "continuation",
        "query": "what about applications",
        "expected_topic": "nitrogen cycle", "conversation_reset": False,
        "depends_on": "D03",
        "expected_keywords": ["fertilizer"],
        "expected_mode": "RAG",
    },
    {
        "id": "C03", "category": "continuation",
        "query": "also tell me disadvantages",
        "expected_topic": "nitrogen cycle", "conversation_reset": False,
        "depends_on": "D03",
        "expected_keywords": ["pollution"],
        "expected_mode": "RAG",
    },

    # ── AMBIGUOUS ────────────────────────────────────────────────────────────
    {
        "id": "A01", "category": "ambiguous",
        "query": "what is cycle",
        "expected_topic": "water cycle", "conversation_reset": False,
        "depends_on": "D01",
        "expected_keywords": ["water", "evaporation"],
        "expected_mode": "RAG",
        "note": "cycle → water cycle via memory",
    },
    {
        "id": "A02", "category": "ambiguous",
        "query": "how does a cycle move",
        "expected_topic": "bicycle", "conversation_reset": False,
        "depends_on": "D01",
        "expected_keywords": ["pedal", "wheel"],
        "expected_mode": "RAG",
        "note": "cycle+move → bicycle topic shift",
    },
    {
        "id": "A03", "category": "ambiguous",
        "query": "what is the calvin cycle",
        "expected_topic": "photosynthesis", "conversation_reset": True,
        "expected_keywords": ["calvin", "rubisco", "glucose"],
        "expected_mode": "RAG",
    },
    {
        "id": "A04", "category": "ambiguous",
        "query": "explain the process",
        "expected_topic": "photosynthesis", "conversation_reset": False,
        "depends_on": "A03",
        "expected_keywords": ["light", "chlorophyll"],
        "expected_mode": "RAG",
        "note": "process → photosynthesis via memory",
    },

    # ── TOPIC SHIFT ──────────────────────────────────────────────────────────
    {
        "id": "T01", "category": "topic_shift",
        "query": "explain photosynthesis",
        "expected_topic": "photosynthesis", "conversation_reset": False,
        "depends_on": "D01",
        "expected_keywords": ["chlorophyll", "glucose"],
        "expected_mode": "RAG",
        "note": "shift from water cycle",
    },
    {
        "id": "T02", "category": "topic_shift",
        "query": "now explain bicycle brakes",
        "expected_topic": "bicycle", "conversation_reset": False,
        "depends_on": "T01",
        "expected_keywords": ["brake", "friction"],
        "expected_mode": "RAG",
        "note": "shift from photosynthesis",
    },
    {
        "id": "T03", "category": "topic_shift",
        "query": "what about carbon cycle now",
        "expected_topic": "carbon cycle", "conversation_reset": False,
        "depends_on": "T02",
        "expected_keywords": ["carbon", "co2"],
        "expected_mode": "RAG",
        "note": "shift from bicycle",
    },

    # ── OUT OF SCOPE ─────────────────────────────────────────────────────────
    {
        "id": "O01", "category": "out_of_scope",
        "query": "how does a car engine work",
        "expected_topic": None, "conversation_reset": True,
        "expected_keywords": [], "expected_mode": "LLM Fallback",
    },
    {
        "id": "O02", "category": "out_of_scope",
        "query": "what are advantages of it",
        "expected_topic": "car engine", "conversation_reset": False,
        "depends_on": "O01",
        "expected_keywords": [], "expected_mode": "LLM Fallback",
        "note": "it → car engine from memory",
    },
    {
        "id": "O03", "category": "out_of_scope",
        "query": "explain agriculture",
        "expected_topic": None, "conversation_reset": True,
        "expected_keywords": [], "expected_mode": "LLM Fallback",
    },
    {
        "id": "O04", "category": "out_of_scope",
        "query": "limitations of it",
        "expected_topic": "agriculture", "conversation_reset": False,
        "depends_on": "O03",
        "expected_keywords": [], "expected_mode": "LLM Fallback",
        "note": "it → agriculture from memory",
    },

    # ── PARTIAL RAG ──────────────────────────────────────────────────────────
    {
        "id": "P01", "category": "partial_rag",
        "query": "explain dispersion of light",
        "expected_topic": None, "conversation_reset": True,
        "expected_keywords": ["light", "wavelength"],
        "expected_mode": "Partial RAG",
    },
    {
        "id": "P02", "category": "partial_rag",
        "query": "why does it occur",
        "expected_topic": "dispersion of light", "conversation_reset": False,
        "depends_on": "P01",
        "expected_keywords": ["wavelength"],
        "expected_mode": "Partial RAG",
    },

    # ── VAGUE ────────────────────────────────────────────────────────────────
    {
        "id": "V01", "category": "vague",
        "query": "cycle",
        "expected_topic": None, "conversation_reset": True,
        "expected_keywords": [], "expected_mode": "LLM Fallback",
    },
    {
        "id": "V02", "category": "vague",
        "query": "explain",
        "expected_topic": None, "conversation_reset": True,
        "expected_keywords": [], "expected_mode": "LLM Fallback",
    },
    {
        "id": "V03", "category": "vague",
        "query": "   ",
        "expected_topic": None, "conversation_reset": True,
        "expected_keywords": [], "expected_mode": "LLM Fallback",
    },

    # ── COMPOUND ─────────────────────────────────────────────────────────────
    {
        "id": "M01", "category": "compound",
        "query": "explain photosynthesis and also bicycle gears",
        "expected_topic": "photosynthesis", "conversation_reset": True,
        "expected_keywords": ["chlorophyll", "gear"],
        "expected_mode": "RAG",
    },
    {
        "id": "M02", "category": "compound",
        "query": "compare water cycle and carbon cycle",
        "expected_topic": "water cycle", "conversation_reset": True,
        "expected_keywords": ["water", "carbon"],
        "expected_mode": "RAG",
    },

    # ── NORMALISATION ────────────────────────────────────────────────────────
    {
        "id": "N01", "category": "normalisation",
        "query": "what's the water cycle",
        "expected_topic": "water cycle", "conversation_reset": True,
        "expected_keywords": ["evaporation"],
        "expected_mode": "RAG",
    },
    {
        "id": "N02", "category": "normalisation",
        "query": "HOW DOES PHOTOSYNTHESIS WORK???",
        "expected_topic": "photosynthesis", "conversation_reset": True,
        "expected_keywords": ["chlorophyll"],
        "expected_mode": "RAG",
    },
    {
        "id": "N03", "category": "normalisation",
        "query": "doesn't the carbon cycle affect climate",
        "expected_topic": "carbon cycle", "conversation_reset": True,
        "expected_keywords": ["carbon", "climate"],
        "expected_mode": "RAG",
    },
]


# ── Helper functions ─────────────────────────────────────────────────────────

def get_model_config(model_name: str) -> dict:
    """
    Return the MODEL_REGISTRY entry for *model_name*.

    Args:
        model_name: Key used in MODEL_REGISTRY (e.g. "phi3", "gpt-4o-mini").

    Returns:
        Dict with keys: type, input_cost_per_1k, output_cost_per_1k, description.

    Raises:
        KeyError: If *model_name* is not registered.
    """
    if model_name not in MODEL_REGISTRY:
        raise KeyError(
            f"Model '{model_name}' not found in MODEL_REGISTRY. "
            f"Available models: {list(MODEL_REGISTRY)}"
        )
    return MODEL_REGISTRY[model_name]


def get_embedding_config(embedding_name: str) -> dict:
    """
    Return the EMBEDDING_MODELS entry matching *embedding_name*.

    Args:
        embedding_name: The ``name`` field of the desired embedding entry
                        (e.g. "bge-small", "minilm").

    Returns:
        Dict with keys: name, model_id, description, dimension.

    Raises:
        KeyError: If *embedding_name* is not found in EMBEDDING_MODELS.
    """
    for entry in EMBEDDING_MODELS:
        if entry["name"] == embedding_name:
            return entry
    raise KeyError(
        f"Embedding '{embedding_name}' not found in EMBEDDING_MODELS. "
        f"Available embeddings: {[e['name'] for e in EMBEDDING_MODELS]}"
    )
