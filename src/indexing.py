"""Build and synchronize the persistent local Chroma policy index."""

from __future__ import annotations

from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

from ingestion import DEFAULT_POLICIES_DIR, PROJECT_ROOT, load_policy_chunks


CHROMA_DIR = PROJECT_ROOT / "chroma"
COLLECTION_NAME = "northstar_policy_chunks"
BATCH_SIZE = 100


def build_policy_index() -> tuple[int, int]:
    """Upsert current policy chunks and remove stale IDs from this collection.

    Chroma's default embedding function uses its local ONNX MiniLM model. The
    evaluation set is never read here; only the policy loader's Markdown source
    directory is used.
    """
    chunks = load_policy_chunks(DEFAULT_POLICIES_DIR)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=DefaultEmbeddingFunction(),
        metadata={
            "hnsw:space": "cosine",
            "corpus": "synthetic Northstar Labs academic policy corpus",
            "embedding_model": "Chroma DefaultEmbeddingFunction (ONNX MiniLM L6 V2)",
        },
    )

    ids = [str(chunk.metadata["chunk_id"]) for chunk in chunks]
    documents = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]
    wanted_ids = set(ids)

    existing_ids = set(collection.get()["ids"])
    stale_ids = sorted(existing_ids - wanted_ids)
    if stale_ids:
        collection.delete(ids=stale_ids)

    for start in range(0, len(chunks), BATCH_SIZE):
        end = start + BATCH_SIZE
        collection.upsert(
            ids=ids[start:end],
            documents=documents[start:end],
            metadatas=metadatas[start:end],
        )

    return len(chunks), collection.count()


def main() -> None:
    chunk_count, indexed_count = build_policy_index()
    print(f"Synced {chunk_count} policy chunks to the local Chroma index.")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Index directory: {CHROMA_DIR}")
    print(f"Chunks stored: {indexed_count}")
    print("The evaluation question set was not indexed.")


if __name__ == "__main__":
    main()
