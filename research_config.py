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
        MODEL_REGISTRY, SLM_MODELS, LLM_MODELS,
        get_model_config, get_embedding_config,
    )
"""

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── Model registry ───────────────────────────────────────────────────────────
# List of model metadata dicts used for evaluation and cost tracking.
# type="SLM"  → free / locally-hosted (Ollama) models
# type="LLM"  → Groq API-hosted models

MODEL_REGISTRY = [
    {"name": "tinyllama", "type": "SLM", "provider": "ollama",
     "model_id": "tinyllama", "params_billions": 1.1,
     "context_window": 2048, "cost_per_1k_input_tokens": 0.0,
     "cost_per_1k_output_tokens": 0.0},
    {"name": "phi3", "type": "SLM", "provider": "ollama",
     "model_id": "phi3", "params_billions": 3.8,
     "context_window": 4096, "cost_per_1k_input_tokens": 0.0,
     "cost_per_1k_output_tokens": 0.0},
    {"name": "gemma2", "type": "SLM", "provider": "ollama",
     "model_id": "gemma2:2b", "params_billions": 2.0,
     "context_window": 8192, "cost_per_1k_input_tokens": 0.0,
     "cost_per_1k_output_tokens": 0.0},
    {"name": "llama3.2", "type": "SLM", "provider": "ollama",
     "model_id": "llama3.2", "params_billions": 3.0,
     "context_window": 4096, "cost_per_1k_input_tokens": 0.0,
     "cost_per_1k_output_tokens": 0.0},
    {"name": "mistral", "type": "SLM", "provider": "ollama",
     "model_id": "mistral", "params_billions": 7.0,
     "context_window": 8192, "cost_per_1k_input_tokens": 0.0,
     "cost_per_1k_output_tokens": 0.0},
    # ── Groq API LLMs ─────────────────────────────────────────────────────────
    {"name": "groq-llama3-8b", "type": "LLM", "provider": "groq",
     "model_id": "llama3-8b-8192", "params_billions": 8.0,
     "context_window": 8192, "cost_per_1k_input_tokens": 0.00005,
     "cost_per_1k_output_tokens": 0.00008},
    {"name": "groq-llama3-70b", "type": "LLM", "provider": "groq",
     "model_id": "llama-3.3-70b-versatile", "params_billions": 70.0,
     "context_window": 128000, "cost_per_1k_input_tokens": 0.00059,
     "cost_per_1k_output_tokens": 0.00079},
    # NOTE: "groq-mixtral" is kept as a backward-compatible alias; the underlying
    # model was migrated from the decommissioned mixtral-8x7b-32768 (56 B) to
    # llama-3.1-8b-instant (8 B) — see https://console.groq.com/docs/deprecations
    {"name": "groq-mixtral", "type": "LLM", "provider": "groq",
     "model_id": "llama-3.1-8b-instant", "params_billions": 8.0,
     "context_window": 131072, "cost_per_1k_input_tokens": 0.00005,
     "cost_per_1k_output_tokens": 0.00008,
     "description": "groq-mixtral alias → llama-3.1-8b-instant (Mixtral decommissioned)"},
    {"name": "groq-gemma2", "type": "LLM", "provider": "groq",
     "model_id": "gemma2-9b-it", "params_billions": 9.0,
     "context_window": 8192, "cost_per_1k_input_tokens": 0.00020,
     "cost_per_1k_output_tokens": 0.00020},
    # ── Groq vision LLM (for multimodal image analysis) ────────────────────────
    # llama-3.2-11b-vision-preview is the dedicated vision model used by
    # VisionImageAnalyzer when GROQ_API_KEY is set.  Listed here so it appears
    # in model-cost tracking and research comparisons.
    {"name": "groq-llama-vision", "type": "LLM", "provider": "groq",
     "model_id": "llama-3.2-11b-vision-preview", "params_billions": 11.0,
     "context_window": 8192, "cost_per_1k_input_tokens": 0.00018,
     "cost_per_1k_output_tokens": 0.00018,
     "description": "Vision-capable Llama 3.2 11B — used by VisionImageAnalyzer for image understanding"},
]

# ── Derived model lists ──────────────────────────────────────────────────────

SLM_MODELS = [m["name"] for m in MODEL_REGISTRY if m["type"] == "SLM"]
LLM_MODELS = [m["name"] for m in MODEL_REGISTRY if m["type"] == "LLM"]
GROQ_MODELS = [m["name"] for m in MODEL_REGISTRY if m.get("provider") == "groq"]
# ALL_MODELS includes every registered model regardless of provider.
ALL_MODELS = [m["name"] for m in MODEL_REGISTRY]

# ── Experiment axes ──────────────────────────────────────────────────────────

# MODELS_TO_EVALUATE covers all registered models so that every evaluation
# mode (model_comparison, token_comparison, slm_vs_llm, full_matrix, …)
# compares both local Ollama SLMs and Groq API LLMs side-by-side.
# Models that are unavailable at runtime are skipped automatically by
# ResearchEvaluator._is_model_available().
MODELS_TO_EVALUATE = ALL_MODELS


def _validate_model_axes() -> None:
    """Validate derived model lists used as experiment axes."""
    expected_all_models = [m["name"] for m in MODEL_REGISTRY]
    if ALL_MODELS != expected_all_models:
        raise ValueError(
            "ALL_MODELS must be the flattened list of all registered model names."
        )

    if MODELS_TO_EVALUATE != ALL_MODELS:
        raise ValueError(
            "MODELS_TO_EVALUATE must include every registered model in ALL_MODELS."
        )

    if SLM_MODELS and not any(model in MODELS_TO_EVALUATE for model in SLM_MODELS):
        raise ValueError(
            "MODELS_TO_EVALUATE must include at least one SLM when SLM models are registered."
        )

    if LLM_MODELS and not any(model in MODELS_TO_EVALUATE for model in LLM_MODELS):
        raise ValueError(
            "MODELS_TO_EVALUATE must include at least one LLM when LLM models are registered."
        )


_validate_model_axes()

RETRIEVAL_MODES = ["vector_only", "bm25_only", "hybrid"]

# ── Per-comparison output files (one file per comparison type) ────────────────
RESULTS_DIR = "results"
RESULTS_FILE = f"{RESULTS_DIR}/research_results.txt"
ABLATION_RESULTS_FILE = f"{RESULTS_DIR}/ablation_results.txt"
MODEL_COMPARISON_FILE = f"{RESULTS_DIR}/model_comparison_results.txt"
EMBEDDING_COMPARISON_FILE = f"{RESULTS_DIR}/embedding_comparison_results.txt"
FULL_MATRIX_FILE = f"{RESULTS_DIR}/full_matrix_results.txt"
TOKEN_COMPARISON_FILE = f"{RESULTS_DIR}/token_comparison_results.txt"
SLM_VS_LLM_FILE = f"{RESULTS_DIR}/slm_vs_llm_results.txt"
MULTIMODAL_RESULTS_FILE = f"{RESULTS_DIR}/multimodal_results.txt"

# Embedding support: available embedding models for research evaluation
EMBEDDING_MODELS = [
    {"name": "bge-small", "model_id": "BAAI/bge-small-en-v1.5",
     "dimension": 384, "type": "huggingface",
     "description": "BGE Small — fast, default embedding"},
    # bge-base-en (requested benchmark model)
    {"name": "bge-base-en", "model_id": "BAAI/bge-base-en-v1.5",
     "dimension": 768, "type": "huggingface",
     "description": "BGE Base EN — benchmark, balanced quality/speed"},
    # backward-compat alias
    {"name": "bge-base", "model_id": "BAAI/bge-base-en-v1.5",
     "dimension": 768, "type": "huggingface",
     "description": "BGE Base (alias for bge-base-en)"},
    {"name": "bge-large", "model_id": "BAAI/bge-large-en-v1.5",
     "dimension": 1024, "type": "huggingface",
     "description": "BGE Large — highest retrieval quality"},
    # all-MiniLM-L6-v2 (requested benchmark model)
    {"name": "all-MiniLM-L6-v2",
     "model_id": "sentence-transformers/all-MiniLM-L6-v2",
     "dimension": 384, "type": "huggingface",
     "description": "MiniLM L6-v2 — benchmark, very fast, lightweight"},
    # backward-compat alias
    {"name": "minilm",
     "model_id": "sentence-transformers/all-MiniLM-L6-v2",
     "dimension": 384, "type": "huggingface",
     "description": "MiniLM (alias for all-MiniLM-L6-v2)"},
    {"name": "mpnet",
     "model_id": "sentence-transformers/all-mpnet-base-v2",
     "dimension": 768, "type": "huggingface",
     "description": "MPNet Base — strong general-purpose embeddings"},
    {"name": "e5-small", "model_id": "intfloat/e5-small-v2",
     "dimension": 384, "type": "huggingface",
     "description": "E5 Small — instruction-tuned, compact"},
    {"name": "e5-base", "model_id": "intfloat/e5-base-v2",
     "dimension": 768, "type": "huggingface",
     "description": "E5 Base — instruction-tuned, larger"},
    # nomic-embed-text via Ollama (requested benchmark model)
    {"name": "nomic-embed-text", "model_id": "nomic-embed-text",
     "dimension": 768, "type": "ollama",
     "description": "Nomic Embed Text — benchmark, local via Ollama"},
    # text-embedding-3-large via OpenAI API (requested benchmark model)
    {"name": "text-embedding-3-large", "model_id": "text-embedding-3-large",
     "dimension": 3072, "type": "openai",
     "description": "OpenAI text-embedding-3-large — benchmark, requires OPENAI_API_KEY"},
]

# Default embedding (current system)
DEFAULT_EMBEDDING = "bge-small"

# Chroma persist directory template
# Each embedding gets its own collection to avoid dimension mismatch
CHROMA_DIR_TEMPLATE = "./chroma_db_{embedding_name}"
COLLECTION_NAME_TEMPLATE = "educational_rag_{embedding_name}"

# ── Chunking / Embedding Techniques ──────────────────────────────────────────
# Supported chunking strategies for build_vector_store:
#   "fixed"           – RecursiveCharacterTextSplitter (default, existing behaviour)
#   "sliding_window"  – Sliding-window chunking with configurable window/step
#   "semantic"        – Sentence-group semantic chunking (cosine-similarity based)
CHUNKING_STRATEGIES = ["fixed", "sliding_window", "semantic"]
DEFAULT_CHUNKING_STRATEGY = "fixed"

# Sliding-window chunking parameters
SLIDING_WINDOW_SIZE = 400      # characters per window
SLIDING_WINDOW_STEP = 200      # step between windows (50 % overlap)

# Semantic chunking parameters
SEMANTIC_CHUNK_MIN_SIZE = 100   # minimum chars to keep a semantic chunk
SEMANTIC_SIMILARITY_THRESHOLD = 0.75  # cosine sim threshold to split

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
    {"id": "D01", "category": "direct",
     "query": "explain water cycle",
     "expected_topic": "water cycle", "conversation_reset": True,
     "expected_keywords": ["evaporation", "condensation", "precipitation"],
     "expected_mode": "RAG"},
    {"id": "D02", "category": "direct",
     "query": "how does photosynthesis work",
     "expected_topic": "photosynthesis", "conversation_reset": True,
     "expected_keywords": ["chlorophyll", "glucose", "sunlight"],
     "expected_mode": "RAG"},
    {"id": "D03", "category": "direct",
     "query": "what is the nitrogen cycle",
     "expected_topic": "nitrogen cycle", "conversation_reset": True,
     "expected_keywords": ["nitrogen", "bacteria", "ammonia"],
     "expected_mode": "RAG"},
    {"id": "D04", "category": "direct",
     "query": "explain bicycle gears",
     "expected_topic": "bicycle", "conversation_reset": True,
     "expected_keywords": ["gear", "sprocket", "chain"],
     "expected_mode": "RAG"},
    {"id": "D05", "category": "direct",
     "query": "what is carbon cycle",
     "expected_topic": "carbon cycle", "conversation_reset": True,
     "expected_keywords": ["carbon", "co2", "fossil"],
     "expected_mode": "RAG"},

    # ── FOLLOWUP PRONOUN — after D01 ─────────────────────────────────────────
    {"id": "F01", "category": "followup_pronoun",
     "query": "how does it work",
     "expected_topic": "water cycle", "conversation_reset": False,
     "depends_on": "D01",
     "expected_keywords": ["evaporation", "water"],
     "expected_mode": "RAG", "note": "it → water cycle"},
    {"id": "F02", "category": "followup_pronoun",
     "query": "what are its components",
     "expected_topic": "water cycle", "conversation_reset": False,
     "depends_on": "D01",
     "expected_keywords": ["evaporation", "condensation"],
     "expected_mode": "RAG"},
    {"id": "F03", "category": "followup_pronoun",
     "query": "why does this happen",
     "expected_topic": "water cycle", "conversation_reset": False,
     "depends_on": "D01", "expected_keywords": ["sun", "heat"],
     "expected_mode": "RAG"},

    # ── FOLLOWUP SHORT — after D02 ───────────────────────────────────────────
    {"id": "S01", "category": "followup_short",
     "query": "advantages", "expected_topic": "photosynthesis",
     "conversation_reset": False, "depends_on": "D02",
     "expected_keywords": ["oxygen", "glucose"],
     "expected_mode": "RAG"},
    {"id": "S02", "category": "followup_short",
     "query": "limitations?", "expected_topic": "photosynthesis",
     "conversation_reset": False, "depends_on": "D02",
     "expected_keywords": ["light", "temperature"],
     "expected_mode": "RAG"},
    {"id": "S03", "category": "followup_short",
     "query": "give example", "expected_topic": "photosynthesis",
     "conversation_reset": False, "depends_on": "D02",
     "expected_keywords": ["plant", "leaf"], "expected_mode": "RAG"},
    {"id": "S04", "category": "followup_short",
     "query": "explain more", "expected_topic": "photosynthesis",
     "conversation_reset": False, "depends_on": "D02",
     "expected_keywords": ["chlorophyll"], "expected_mode": "RAG"},

    # ── CONTINUATION — after D03 ─────────────────────────────────────────────
    {"id": "C01", "category": "continuation",
     "query": "and what are its stages",
     "expected_topic": "nitrogen cycle", "conversation_reset": False,
     "depends_on": "D03",
     "expected_keywords": ["nitrification", "fixation"],
     "expected_mode": "RAG"},
    {"id": "C02", "category": "continuation",
     "query": "what about applications",
     "expected_topic": "nitrogen cycle", "conversation_reset": False,
     "depends_on": "D03", "expected_keywords": ["fertilizer"],
     "expected_mode": "RAG"},

    # ── AMBIGUOUS ────────────────────────────────────────────────────────────
    {"id": "A01", "category": "ambiguous", "query": "what is cycle",
     "expected_topic": "water cycle", "conversation_reset": False,
     "depends_on": "D01",
     "expected_keywords": ["water", "evaporation"],
     "expected_mode": "RAG"},
    {"id": "A02", "category": "ambiguous",
     "query": "how does a cycle move",
     "expected_topic": "bicycle", "conversation_reset": False,
     "depends_on": "D01",
     "expected_keywords": ["pedal", "wheel"], "expected_mode": "RAG",
     "note": "cycle+move → bicycle shift"},
    {"id": "A03", "category": "ambiguous",
     "query": "what is the calvin cycle",
     "expected_topic": "photosynthesis", "conversation_reset": True,
     "expected_keywords": ["calvin", "rubisco"],
     "expected_mode": "RAG"},

    # ── TOPIC SHIFT ──────────────────────────────────────────────────────────
    {"id": "T01", "category": "topic_shift",
     "query": "explain photosynthesis",
     "expected_topic": "photosynthesis", "conversation_reset": False,
     "depends_on": "D01",
     "expected_keywords": ["chlorophyll", "glucose"],
     "expected_mode": "RAG", "note": "shift from water cycle"},
    {"id": "T02", "category": "topic_shift",
     "query": "now explain bicycle brakes",
     "expected_topic": "bicycle", "conversation_reset": False,
     "depends_on": "T01",
     "expected_keywords": ["brake", "friction"], "expected_mode": "RAG"},

    # ── OUT OF SCOPE ─────────────────────────────────────────────────────────
    {"id": "O01", "category": "out_of_scope",
     "query": "how does a car engine work",
     "expected_topic": None, "conversation_reset": True,
     "expected_keywords": [], "expected_mode": "LLM Fallback"},
    {"id": "O02", "category": "out_of_scope",
     "query": "what are advantages of it",
     "expected_topic": "car engine", "conversation_reset": False,
     "depends_on": "O01", "expected_keywords": [],
     "expected_mode": "LLM Fallback",
     "note": "it → car engine from memory"},

    # ── VAGUE ────────────────────────────────────────────────────────────────
    {"id": "V01", "category": "vague", "query": "cycle",
     "expected_topic": None, "conversation_reset": True,
     "expected_keywords": [], "expected_mode": "LLM Fallback"},
    {"id": "V02", "category": "vague", "query": "   ",
     "expected_topic": None, "conversation_reset": True,
     "expected_keywords": [], "expected_mode": "LLM Fallback"},

    # ── NEW SUBJECTS ─────────────────────────────────────────────────────────
    {"id": "CH01", "category": "chemistry",
     "query": "explain atomic structure",
     "expected_topic": "atomic structure", "conversation_reset": True,
     "expected_keywords": ["proton", "electron", "neutron"],
     "expected_mode": "RAG"},
    {"id": "CH02", "category": "chemistry",
     "query": "what is chemical bonding",
     "expected_topic": "chemical bonding", "conversation_reset": True,
     "expected_keywords": ["ionic", "covalent", "electron"],
     "expected_mode": "RAG"},
    {"id": "PH01", "category": "physics",
     "query": "what are newtons laws of motion",
     "expected_topic": "newton's laws", "conversation_reset": True,
     "expected_keywords": ["force", "mass", "acceleration"],
     "expected_mode": "RAG"},
    {"id": "PH02", "category": "physics",
     "query": "what is dispersion of light",
     "expected_topic": "light and optics", "conversation_reset": True,
     "expected_keywords": ["wavelength", "prism", "spectrum"],
     "expected_mode": "RAG",
     "note": "previously failed — should work with new corpus"},
    {"id": "MA01", "category": "mathematics",
     "query": "explain trigonometry basics",
     "expected_topic": "trigonometry", "conversation_reset": True,
     "expected_keywords": ["sine", "cosine", "tangent", "angle"],
     "expected_mode": "RAG"},
    {"id": "CS01", "category": "computer_science",
     "query": "what are sorting algorithms",
     "expected_topic": "algorithms", "conversation_reset": True,
     "expected_keywords": ["sort", "bubble", "merge"],
     "expected_mode": "RAG"},
    {"id": "CS02", "category": "computer_science",
     "query": "explain machine learning",
     "expected_topic": "machine learning", "conversation_reset": True,
     "expected_keywords": ["training", "model", "data"],
     "expected_mode": "RAG"},
    {"id": "EN01", "category": "environmental",
     "query": "explain renewable energy",
     "expected_topic": "renewable energy", "conversation_reset": True,
     "expected_keywords": ["solar", "wind", "sustainable"],
     "expected_mode": "RAG"},
    {"id": "XS01", "category": "cross_subject",
     "query": "how does photosynthesis relate to carbon cycle",
     "expected_topic": "photosynthesis", "conversation_reset": True,
     "expected_keywords": ["co2", "carbon", "plant"],
     "expected_mode": "RAG", "note": "cross topic query"},

    # ── NORMALISATION ────────────────────────────────────────────────────────
    {"id": "NM01", "category": "normalisation",
     "query": "what's the water cycle",
     "expected_topic": "water cycle", "conversation_reset": True,
     "expected_keywords": ["evaporation"], "expected_mode": "RAG"},
    {"id": "NM02", "category": "normalisation",
     "query": "HOW DOES PHOTOSYNTHESIS WORK???",
     "expected_topic": "photosynthesis", "conversation_reset": True,
     "expected_keywords": ["chlorophyll"], "expected_mode": "RAG"},
]


# ── Helper functions ─────────────────────────────────────────────────────────

def get_model_config(name: str) -> dict | None:
    """
    Return the MODEL_REGISTRY entry for *name*, or None if not found.

    Args:
        name: Model name as listed in MODEL_REGISTRY (e.g. "phi3", "gpt-4o-mini").

    Returns:
        Dict with model metadata, or None if *name* is not registered.
    """
    return next((m for m in MODEL_REGISTRY if m["name"] == name), None)


def get_embedding_config(name: str) -> dict | None:
    """
    Return the EMBEDDING_MODELS entry matching *name*, or None if not found.

    Args:
        name: The ``name`` field of the desired embedding entry
              (e.g. "bge-small", "minilm").

    Returns:
        Dict with embedding metadata, or None if *name* is not found.
    """
    return next((e for e in EMBEDDING_MODELS if e["name"] == name), None)
