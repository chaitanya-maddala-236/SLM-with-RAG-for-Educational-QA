"""
embeddings.py
-------------
Embedding model factory for use with LangChain / Chroma.

Supports multiple embedding models configured in research_config.EMBEDDING_MODELS:
  - HuggingFace models (type="huggingface")  – local, no API key needed
  - Ollama-served models (type="ollama")     – requires `ollama pull <model>`
  - OpenAI models (type="openai")            – requires OPENAI_API_KEY

Use get_embeddings(name) to load any supported model.  The legacy
get_bge_embeddings() function is kept as a backward-compatible alias.

Usage:
    from embeddings import get_embeddings, list_embedding_names
    emb = get_embeddings("bge-base")
    names = list_embedding_names()
"""

import os
import warnings

from langchain_community.embeddings import HuggingFaceEmbeddings

# Embedding support: load config from research_config
from research_config import EMBEDDING_MODELS, DEFAULT_EMBEDDING


def _load_huggingface_embeddings(model_id: str) -> HuggingFaceEmbeddings:
    """Load a HuggingFace embedding model (local, CPU).

    Args:
        model_id: HuggingFace model identifier.

    Returns:
        HuggingFaceEmbeddings instance.
    """
    return HuggingFaceEmbeddings(
        model_name=model_id,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def _load_ollama_embeddings(model_id: str):
    """Load an Ollama embedding model (local Ollama server required).

    Args:
        model_id: Ollama model identifier (e.g. "nomic-embed-text").

    Returns:
        OllamaEmbeddings instance.

    Raises:
        ImportError: if langchain_community is not installed.
        ConnectionError: if Ollama server is unreachable.
    """
    from langchain_community.embeddings import OllamaEmbeddings
    return OllamaEmbeddings(model=model_id)


def _load_openai_embeddings(model_id: str):
    """Load an OpenAI embedding model (OPENAI_API_KEY required).

    Args:
        model_id: OpenAI model identifier (e.g. "text-embedding-3-large").

    Returns:
        OpenAIEmbeddings instance.

    Raises:
        ImportError: if langchain_openai is not installed.
        ValueError: if OPENAI_API_KEY is not set.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is not set. "
            "Set it to use OpenAI embeddings."
        )
    try:
        from langchain_openai import OpenAIEmbeddings  # type: ignore[import]
    except ImportError as exc:
        raise ImportError(
            "langchain_openai is required for OpenAI embeddings. "
            "Install it with: pip install langchain-openai"
        ) from exc
    return OpenAIEmbeddings(model=model_id, api_key=api_key)


def get_embeddings(
    embedding_name: str = DEFAULT_EMBEDDING,
):
    """
    Load and return embeddings by name from EMBEDDING_MODELS config.

    Dispatches to the correct backend based on the ``type`` field in the
    EMBEDDING_MODELS config entry:
      - ``"huggingface"`` → local HuggingFace model (default/fallback)
      - ``"ollama"``      → Ollama-served model (requires running Ollama)
      - ``"openai"``      → OpenAI API model (requires OPENAI_API_KEY)

    On first use the model weights are downloaded from HuggingFace or pulled
    from Ollama (~100 MB – 1.3 GB depending on the model).  Subsequent calls
    load from the local cache.

    If loading fails, falls back to DEFAULT_EMBEDDING with an error message.

    Args:
        embedding_name: Key from EMBEDDING_MODELS (e.g. "bge-small",
                        "nomic-embed-text", "text-embedding-3-large").

    Returns:
        LangChain Embeddings instance ready for Chroma.

    Warns:
        UserWarning if *embedding_name* is not found; falls back silently to
        DEFAULT_EMBEDDING.
    """
    # Embedding support: look up config by name
    config = next(
        (e for e in EMBEDDING_MODELS if e["name"] == embedding_name), None
    )
    if config is None:
        warnings.warn(
            f"Unknown embedding '{embedding_name}', using {DEFAULT_EMBEDDING}",
            UserWarning,
            stacklevel=2,
        )
        config = next(e for e in EMBEDDING_MODELS if e["name"] == DEFAULT_EMBEDDING)

    model_id = config["model_id"]
    model_type = config.get("type", "huggingface")
    print(f"  [Embeddings] Loading model: {embedding_name} ({model_id}, type={model_type})")

    try:
        if model_type == "ollama":
            return _load_ollama_embeddings(model_id)
        if model_type == "openai":
            return _load_openai_embeddings(model_id)
        # Default: HuggingFace
        return _load_huggingface_embeddings(model_id)

    except Exception as exc:
        print(
            f"  [Embeddings] Failed to load {embedding_name} ({model_type}): {exc}. "
            f"Falling back to {DEFAULT_EMBEDDING}."
        )
        fallback = next(
            e for e in EMBEDDING_MODELS if e["name"] == DEFAULT_EMBEDDING
        )
        return _load_huggingface_embeddings(fallback["model_id"])


# Embedding support: backward-compatible alias
def get_bge_embeddings(
    model_name: str = "BAAI/bge-small-en-v1.5",
) -> HuggingFaceEmbeddings:
    """
    Backward-compatible wrapper.  Use get_embeddings() instead.

    Args:
        model_name: Ignored — always returns bge-small embeddings.

    Returns:
        HuggingFaceEmbeddings for bge-small.
    """
    return get_embeddings("bge-small")


def get_embedding_info(embedding_name: str) -> dict:
    """
    Return the config dict for the given embedding_name.

    Args:
        embedding_name: Key from EMBEDDING_MODELS (e.g. "bge-base").

    Returns:
        Config dict with keys name, model_id, type, dimension.
        Empty dict if *embedding_name* is not found.
    """
    return next(
        (e for e in EMBEDDING_MODELS if e["name"] == embedding_name), {}
    )


def list_embedding_names() -> list[str]:
    """
    Return list of all available embedding names.

    Returns:
        List of name strings (e.g. ["bge-small", "bge-base-en", ...]).
    """
    return [e["name"] for e in EMBEDDING_MODELS]


def get_embeddings_by_type(embed_type: str) -> list[str]:
    """
    Return embedding names filtered by backend type.

    Args:
        embed_type: One of "huggingface", "ollama", "openai".

    Returns:
        List of embedding names of the requested type.
    """
    return [e["name"] for e in EMBEDDING_MODELS if e.get("type") == embed_type]

