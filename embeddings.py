"""
embeddings.py
-------------
Initialises the BGE embedding model and wraps it for use with LangChain / Chroma.
BGE (BAAI General Embedding) is a state-of-the-art open-source embedding model
well-suited for semantic retrieval tasks.
"""

from langchain_community.embeddings import HuggingFaceEmbeddings


def get_bge_embeddings(model_name: str = "BAAI/bge-small-en-v1.5") -> HuggingFaceEmbeddings:
    """
    Load and return BGE embeddings.

    BGE models expect a query prefix for retrieval tasks:
    "Represent this sentence: " for asymmetric retrieval.
    We pass encode_kwargs so the model normalises vectors (cosine similarity).

    Args:
        model_name: HuggingFace model ID.  bge-small is fast; bge-base is more accurate.

    Returns:
        HuggingFaceEmbeddings instance ready for use with Chroma.
    """
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"},          # use "cuda" if GPU available
        encode_kwargs={"normalize_embeddings": True},  # cosine similarity
    )
    return embeddings
