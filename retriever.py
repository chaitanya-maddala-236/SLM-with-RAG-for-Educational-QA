"""
retriever.py
------------
Builds and manages the Chroma vector store.
Provides a retrieval function that returns the top-K most relevant documents.
"""

import os
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from embeddings import get_bge_embeddings
from data_loader import get_texts_and_metadatas

CHROMA_PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "educational_rag"


def build_vector_store(persist: bool = True) -> Chroma:
    """
    Create (or reload from disk) the Chroma vector store with all educational documents.

    On first run:  embeds documents and saves to CHROMA_PERSIST_DIR.
    On later runs: loads the persisted store (much faster).

    Args:
        persist: If True, persist the store to disk.

    Returns:
        Initialised Chroma vector store.
    """
    embeddings = get_bge_embeddings()

    if persist and os.path.exists(CHROMA_PERSIST_DIR):
        print("  [Chroma] Loading existing vector store from disk...")
        store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=CHROMA_PERSIST_DIR,
        )
        # Sanity check: make sure the collection is non-empty
        if store._collection.count() > 0:
            return store
        print("  [Chroma] Store empty – rebuilding...")

    print("  [Chroma] Building vector store (embedding documents)...")
    texts, metadatas = get_texts_and_metadatas()

    docs = [
        Document(page_content=text, metadata=meta)
        for text, meta in zip(texts, metadatas)
    ]

    store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PERSIST_DIR if persist else None,
    )

    if persist:
        store.persist()
        print(f"  [Chroma] Persisted {len(docs)} documents to {CHROMA_PERSIST_DIR}")

    return store


def retrieve_top_k(
    vector_store: Chroma,
    query: str,
    k: int = 5,
    topic_filter: str | None = None,
    subject_filter: str | None = None,
) -> list[Document]:
    """
    Retrieve the top-K documents most semantically similar to the query.

    Optionally filter by topic and/or subject via Chroma metadata filtering.
    Falls back to unfiltered retrieval if no documents match the filter.

    Args:
        vector_store:   Initialised Chroma store.
        query:          The (possibly rewritten) query string.
        k:              Number of documents to return (3–5 recommended).
        topic_filter:   If set, restrict to documents with this topic.
        subject_filter: If set, restrict to documents with this subject.

    Returns:
        List of LangChain Document objects, ordered by relevance (most relevant first).
    """
    where_clause: dict | None = None

    if topic_filter and subject_filter:
        where_clause = {
            "$and": [
                {"topic": {"$eq": topic_filter}},
                {"subject": {"$eq": subject_filter}},
            ]
        }
    elif topic_filter:
        where_clause = {"topic": {"$eq": topic_filter}}
    elif subject_filter:
        where_clause = {"subject": {"$eq": subject_filter}}

    try:
        if where_clause:
            docs = vector_store.similarity_search(query, k=k, filter=where_clause)
        else:
            docs = vector_store.similarity_search(query, k=k)

        # If filtered search returns too few results, fall back to unfiltered
        if where_clause and len(docs) < 2:
            print(f"  [Retriever] Filter returned only {len(docs)} doc(s); "
                  "falling back to unfiltered retrieval.")
            docs = vector_store.similarity_search(query, k=k)

    except Exception as e:
        print(f"  [Retriever] Error during retrieval: {e}. Falling back to unfiltered.")
        docs = vector_store.similarity_search(query, k=k)

    return docs
