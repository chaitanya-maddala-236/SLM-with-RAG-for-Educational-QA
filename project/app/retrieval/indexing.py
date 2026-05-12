from __future__ import annotations

import logging
from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from project.app.retrieval.legacy import (
    BM25Index,
    build_bm25_index,
    get_embeddings,
    get_texts_and_metadatas,
)

logger = logging.getLogger(__name__)


def build_chunked_corpus(chunk_size: int, chunk_overlap: int) -> list[Document]:
    texts, metadatas = get_texts_and_metadatas()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    docs: list[Document] = []
    for text, metadata in zip(texts, metadatas):
        for chunk in splitter.split_text(text):
            docs.append(Document(page_content=chunk, metadata=metadata))
    logger.info("Built chunked corpus with %d chunks", len(docs))
    return docs


def build_dense_store(
    docs: list[Document],
    embedding_name: str,
    persist_dir: str = "project/datasets/chroma_edu",
    collection_name: str = "edu_slm_rag",
) -> Chroma:
    Path(persist_dir).mkdir(parents=True, exist_ok=True)
    embeddings = get_embeddings(embedding_name)
    store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_dir,
        collection_name=collection_name,
    )
    logger.info("Dense store built at %s", persist_dir)
    return store


def build_sparse_index(docs: list[Document]) -> BM25Index | None:
    return build_bm25_index(docs)
