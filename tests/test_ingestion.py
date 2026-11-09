"""Checks that the policy corpus loads with citation metadata."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from ingestion import load_policy_chunks  # noqa: E402


class PolicyIngestionTests(unittest.TestCase):
    def test_policy_chunks_include_source_and_citation_metadata(self) -> None:
        chunks = load_policy_chunks()
        self.assertTrue(chunks)

        source_files = {chunk.metadata["source_file"] for chunk in chunks}
        self.assertEqual(len(source_files), 7)
        self.assertTrue(all(name.endswith(".md") for name in source_files))
        self.assertNotIn("questions.json", source_files)

        for chunk in chunks:
            for field in (
                "chunk_id",
                "policy_id",
                "source_file",
                "source_title",
                "section_path",
            ):
                self.assertTrue(chunk.metadata.get(field), f"Missing {field} on a chunk")


if __name__ == "__main__":
    unittest.main()
