"""Retrieve relevant policy chunks from the local Chroma index."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

from indexing import CHROMA_DIR, COLLECTION_NAME

DEFAULT_TOP_K = 4


def retrieve_chunks(question: str, *, top_k: int = DEFAULT_TOP_K) -> list[dict[str, Any]]:
    """Return the closest policy chunks with citation metadata and distance.

    Chroma's cosine distance is lower for more similar results. The evaluation
    workflow should be used to tune retrieval settings against the corpus.
    """
    cleaned_question = question.strip()
    if not cleaned_question:
        raise ValueError("Question must not be empty.")
    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    if not Path(CHROMA_DIR).exists():
        raise FileNotFoundError(
            f"Local Chroma index not found at {CHROMA_DIR}. "
            "Build it first with: python src\\indexing.py"
        )

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    try:
        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=DefaultEmbeddingFunction(),
        )
    except Exception as exc:
        raise RuntimeError(
            f"Chroma collection '{COLLECTION_NAME}' is unavailable. "
            "Build it first with: python src\\indexing.py"
        ) from exc

    if collection.count() == 0:
        return []

    result = collection.query(
        query_texts=[cleaned_question],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )
    documents = result["documents"][0] or []
    metadatas = result["metadatas"][0] or []
    distances = result["distances"][0] or []

    chunks: list[dict[str, Any]] = []
    for document, metadata, distance in zip(documents, metadatas, distances):
        metadata = metadata or {}
        chunks.append(
            {
                "chunk_id": metadata.get("chunk_id", "unknown"),
                "policy_id": metadata.get("policy_id", "unknown"),
                "title": metadata.get("source_title", "Unknown policy"),
                "source_file": metadata.get("source_file", ""),
                "section": metadata.get("section_path", ""),
                "text": document or "",
                "distance": float(distance),
            }
        )
    return chunks

def main() -> None:
    """Ask for a query and print retrieved chunks with citation metadata."""
    import json

    question = input("Policy question to retrieve: ").strip()
    if not question:
        print("Enter a question to retrieve policy chunks.")
        return
    try:
        chunks = retrieve_chunks(question)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"Retrieval error: {exc}")
        return
    for rank, chunk in enumerate(chunks, start=1):
        print(f"\n--- Result {rank} ---")
        print(json.dumps({key: value for key, value in chunk.items() if key != "text"}, indent=2))
        print(chunk["text"])


if __name__ == "__main__":
    main()

\n