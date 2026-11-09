"""Offline checks for the Flask interface; no LLM request is made."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from app import app  # noqa: E402


class FlaskRouteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()

    def test_home_page_loads(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Northstar Labs Policy Assistant", response.data)

    def test_chat_rejects_empty_question(self) -> None:
        response = self.client.post("/chat", json={"question": "  "})
        self.assertEqual(response.status_code, 400)

    def test_chat_rejects_question_over_limit(self) -> None:
        response = self.client.post("/chat", json={"question": "x" * 1_001})
        self.assertEqual(response.status_code, 400)

    def test_chat_returns_answer_sources_and_snippets(self) -> None:
        fake_result = {
            "answer": "Employees may carry five days [NL-PEO-001, Section 2].",
            "citations": [
                {
                    "policy_id": "NL-PEO-001",
                    "title": "Leave and Time-Off Policy",
                    "section": "Leave and Time-Off Policy > 2. Annual leave",
                    "source_file": "leave-and-time-off.md",
                    "chunk_id": "NL-PEO-001-CH0001",
                    "snippet": "Employees may carry five days.",
                }
            ],
            "retrieved_chunks": [
                {
                    "chunk_id": "NL-PEO-001-CH0001",
                    "policy_id": "NL-PEO-001",
                    "title": "Leave and Time-Off Policy",
                    "section": "Leave and Time-Off Policy > 2. Annual leave",
                    "source_file": "leave-and-time-off.md",
                    "text": "Employees may carry five days.",
                    "distance": 0.2,
                }
            ],
        }
        with patch("app.answer_question", return_value=fake_result) as answer_question:
            response = self.client.post("/chat", json={"question": "Carry-over limit?"})

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["answer"], fake_result["answer"])
        self.assertEqual(payload["citations"][0]["policy_id"], "NL-PEO-001")
        self.assertEqual(payload["snippets"][0]["chunk_id"], "NL-PEO-001-CH0001")
        answer_question.assert_called_once_with("Carry-over limit?")


if __name__ == "__main__":
    unittest.main()
