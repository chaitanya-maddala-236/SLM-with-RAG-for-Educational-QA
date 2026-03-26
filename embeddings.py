"""
embeddings.py
-------------
Embedding model factory for use with LangChain / Chroma.

Supports multiple embedding models configured in research_config.EMBEDDING_MODELS.
Use get_embeddings(name) to load any supported model.  The legacy
get_bge_embeddings() function is kept as a backward-compatible alias.

Usage:
    from embeddings import get_embeddings, list_embedding_names
    emb = get_embeddings("bge-base")
    names = list_embedding_names()
"""

import warnings

from langchain_community.embeddings import HuggingFaceEmbeddings

# Embedding support: load config from research_config
from research_config import EMBEDDING_MODELS, DEFAULT_EMBEDDING


def get_embeddings(
    embedding_name: str = DEFAULT_EMBEDDING,
) -> HuggingFaceEmbeddings:
    """
    Load and return embeddings by name from EMBEDDING_MODELS config.

    Looks up *embedding_name* in EMBEDDING_MODELS.  If not found, falls back
    to DEFAULT_EMBEDDING with a warning.

    All embeddings use:
        model_kwargs={"device": "cpu"}
        encode_kwargs={"normalize_embeddings": True}

    On first use the model weights are downloaded from HuggingFace (~100 MB –
    1.3 GB depending on the model).  Subsequent calls load from the local
    HuggingFace cache.

    If the model download fails (e.g. no internet), the function prints an
    error message and falls back to DEFAULT_EMBEDDING.

    Args:
        embedding_name: Key from EMBEDDING_MODELS (e.g. "bge-small").

    Returns:
        HuggingFaceEmbeddings instance ready for Chroma.

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
    print(f"  [Embeddings] Loading model: {embedding_name} ({model_id})")

    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=model_id,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    except (OSError, ConnectionError) as exc:
        print(
            f"  [Embeddings] Failed to load {embedding_name}: {exc}. "
            f"Falling back to {DEFAULT_EMBEDDING}."
        )
        fallback = next(
            e for e in EMBEDDING_MODELS if e["name"] == DEFAULT_EMBEDDING
        )
        embeddings = HuggingFaceEmbeddings(
            model_name=fallback["model_id"],
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    return embeddings


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
        Config dict with keys name, model_id, description, dimension.
        Empty dict if *embedding_name* is not found.
    """
    return next(
        (e for e in EMBEDDING_MODELS if e["name"] == embedding_name), {}
    )


def list_embedding_names() -> list[str]:
    """
    Return list of all available embedding names.

    Returns:
        List of name strings (e.g. ["bge-small", "bge-base", ...]).
    """
    return [e["name"] for e in EMBEDDING_MODELS]

