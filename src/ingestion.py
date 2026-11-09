"""Load and chunk the synthetic Markdown policy corpus for RAG."""

from __future__ import annotations

import re
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_POLICIES_DIR = PROJECT_ROOT / "data" / "policies"

# These are character counts, not token counts. Header splitting keeps policy
# sections together; the recursive splitter only breaks sections that are long.
CHUNK_SIZE = 1_200
CHUNK_OVERLAP = 200

HEADERS_TO_SPLIT_ON = [
    ("#", "h1"),
    ("##", "h2"),
    ("###", "h3"),
]

POLICY_ID_PATTERN = re.compile(r"^\*\*Policy ID:\*\*\s*([A-Z0-9-]+)", re.MULTILINE)


def _policy_id(text: str, path: Path) -> str:
    """Read the stable policy ID from the document's metadata line."""
    match = POLICY_ID_PATTERN.search(text)
    if match is None:
        raise ValueError(f"Missing '**Policy ID:**' metadata in {path.name}")
    return match.group(1)


def _policy_title(text: str, path: Path) -> str:
    """Use the first Markdown heading as the human-readable policy title."""
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("-", " ").title()


def load_policy_chunks(
    policies_dir: Path = DEFAULT_POLICIES_DIR,
    *,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[Document]:
    """Read policy Markdown files and return heading-aware chunks.

    Only ``*.md`` files in the policy directory are read. Evaluation material
    lives elsewhere and is intentionally excluded from the ingestion source.
    Each returned Document includes a stable chunk ID, source policy ID,
    filename, title, section path, and chunk position within its section.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be non-negative and smaller than chunk_size")
    if not policies_dir.is_dir():
        raise FileNotFoundError(f"Policy directory not found: {policies_dir}")

    policy_paths = sorted(policies_dir.glob("*.md"))
    if not policy_paths:
        raise FileNotFoundError(f"No Markdown policy files found in: {policies_dir}")

    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=HEADERS_TO_SPLIT_ON,
        strip_headers=False,
    )
    character_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
    )

    all_chunks: list[Document] = []
    for path in policy_paths:
        text = path.read_text(encoding="utf-8-sig").strip()
        if not text:
            raise ValueError(f"Policy file is empty: {path.name}")

        policy_id = _policy_id(text, path)
        title = _policy_title(text, path)
        section_documents = markdown_splitter.split_text(text)
        chunk_number = 0

        for section_document in section_documents:
            section_metadata = section_document.metadata
            section_parts = [
                section_metadata[key]
                for key in ("h1", "h2", "h3")
                if section_metadata.get(key)
            ]
            section_path = " > ".join(section_parts) if section_parts else title

            source_document = Document(
                page_content=section_document.page_content,
                metadata={
                    **section_metadata,
                    "policy_id": policy_id,
                    "source_file": path.name,
                    "source_title": title,
                    "section_path": section_path,
                },
            )
            section_chunks = character_splitter.split_documents([source_document])

            for section_chunk_index, chunk in enumerate(section_chunks, start=1):
                chunk_number += 1
                chunk.metadata.update(
                    {
                        "policy_id": policy_id,
                        "source_file": path.name,
                        "source_title": title,
                        "section_path": section_path,
                        "section_chunk_index": section_chunk_index,
                        "chunk_id": f"{policy_id}-CH{chunk_number:04d}",
                    }
                )
                all_chunks.append(chunk)

    return all_chunks


def main() -> None:
    """Print a small preview so learners can inspect chunking before indexing."""
    chunks = load_policy_chunks()
    source_files = sorted({chunk.metadata["source_file"] for chunk in chunks})
    print(f"Loaded {len(source_files)} policy files into {len(chunks)} chunks.")
    print(f"Chunk size: {CHUNK_SIZE} characters; overlap: {CHUNK_OVERLAP} characters.")
    print("\nFirst three chunks:")
    for chunk in chunks[:3]:
        metadata = chunk.metadata
        print(
            f"- {metadata['chunk_id']} | {metadata['source_file']} | "
            f"{metadata['section_path']} | {len(chunk.page_content)} characters"
        )


if __name__ == "__main__":
    main()
