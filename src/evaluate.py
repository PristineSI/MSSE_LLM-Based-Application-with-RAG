"""Run the held-out policy questions and save reviewable RAG results."""

from __future__ import annotations

import argparse
import json
import math
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import os

from rag import (
    DEFAULT_MODEL,
    MAX_COMPLETION_TOKENS,
    REASONING_EFFORT,
    answer_question,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
QUESTIONS_PATH = PROJECT_ROOT / "data" / "evaluation" / "questions.json"
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "data" / "evaluation" / "latest-results.json"
LATENCY_SUBSET_SIZE = 15


def section_ids(records: list[dict[str, Any]]) -> list[str]:
    """Convert chunk/citation metadata into IDs such as NL-PEO-001 §2."""
    import re

    found = []
    for record in records:
        match = re.search(r">\s*(\d+)\.", record.get("section", ""))
        if match:
            found.append(f"{record.get('policy_id', '')} §{match.group(1)}")
    return sorted(set(found))


def recall(expected: list[str], actual: list[str]) -> float | None:
    if not expected:
        return None
    return round(len(set(expected) & set(actual)) / len(set(expected)), 4)


def summarize(results: list[dict[str, Any]], latency_ids: list[str]) -> dict[str, Any]:
    timed = [
        row["latency_seconds"] for row in results
        if row.get("latency_seconds") is not None
        and "error" not in row
        and row["id"] in latency_ids
    ]
    if not timed:
        return {
            "latency_question_ids": latency_ids,
            "latency_success_count": 0,
            "latency_p50_seconds": None,
            "latency_p95_seconds": None,
        }
    ordered = sorted(timed)
    p95_index = max(0, math.ceil(0.95 * len(ordered)) - 1)
    return {
        "latency_question_ids": latency_ids,
        "latency_success_count": len(timed),
        "latency_p50_seconds": round(statistics.median(ordered), 3),
        "latency_p95_seconds": round(ordered[p95_index], 3),
    }


def run_evaluation(
    limit: int | None,
    output_path: Path,
    delay: float,
    retry_errors: bool = False,
) -> dict[str, Any]:
    dataset = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
    existing_by_id: dict[str, dict[str, Any]] = {}
    previous_metadata: dict[str, Any] = {}
    if retry_errors:
        if not output_path.is_file():
            raise FileNotFoundError(
                f"Cannot retry errors because no results file exists: {output_path}"
            )
        previous = json.loads(output_path.read_text(encoding="utf-8"))
        previous_metadata = previous.get("metadata", {})
        existing_by_id = {row["id"]: row for row in previous.get("results", [])}
        retry_ids = {
            row_id for row_id, row in existing_by_id.items() if row.get("error")
        }
        questions = [item for item in dataset["questions"] if item["id"] in retry_ids]
        if not questions:
            raise ValueError("The saved evaluation has no failed questions to retry.")
    else:
        questions = dataset["questions"][:limit] if limit else dataset["questions"]

    latency_ids = [item["id"] for item in dataset["questions"][:LATENCY_SUBSET_SIZE]]
    results = []

    for index, item in enumerate(questions, start=1):
        started = time.perf_counter()
        try:
            response = answer_question(item["question"])
            duration = time.perf_counter() - started
            chunks = response["retrieved_chunks"]
            citations = response["citations"]
            expected = item.get("source_sections", [])
            retrieved_sections = section_ids(chunks)
            cited_sections = section_ids(citations)
            row = {
                "id": item["id"],
                "topic": item["topic"],
                "question": item["question"],
                "answerable": item["answerable"],
                "reference_answer": item["reference_answer"],
                "expected_source_sections": expected,
                "answer": response["answer"],
                "model": response.get("model", "not reported"),
                "citations": citations,
                "retrieved_chunks": [
                    {
                        "chunk_id": chunk["chunk_id"],
                        "policy_id": chunk["policy_id"],
                        "title": chunk["title"],
                        "section": chunk["section"],
                        "distance": chunk["distance"],
                    }
                    for chunk in chunks
                ],
                "retrieved_source_sections": retrieved_sections,
                "cited_source_sections": cited_sections,
                "retrieval_section_recall": recall(expected, retrieved_sections),
                "citation_section_recall": recall(expected, cited_sections),
                "latency_seconds": round(duration, 3),
                "manual_review": {
                    "groundedness_0_to_2": None,
                    "citation_accuracy_0_to_2": None,
                    "safe_refusal_for_oos": None,
                    "notes": "",
                },
            }
        except Exception as exc:
            duration = time.perf_counter() - started
            row = {
                "id": item["id"],
                "topic": item["topic"],
                "question": item["question"],
                "answerable": item["answerable"],
                "reference_answer": item["reference_answer"],
                "expected_source_sections": item.get("source_sections", []),
                "error": f"{type(exc).__name__}: {exc}",
                "latency_seconds": round(duration, 3),
                "manual_review": {
                    "groundedness_0_to_2": None,
                    "citation_accuracy_0_to_2": None,
                    "safe_refusal_for_oos": None,
                    "notes": "",
                },
            }
        results.append(row)
        print(f"[{index}/{len(questions)}] {item['id']}: " + ("error" if "error" in row else "done"))
        if index < len(questions) and delay > 0:
            time.sleep(delay)

    if retry_errors:
        existing_by_id.update({row["id"]: row for row in results})
        results = [
            existing_by_id[item["id"]]
            for item in dataset["questions"]
            if item["id"] in existing_by_id
        ]

    current_generation_config = {
        "requested_model": os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL),
        "max_completion_tokens": MAX_COMPLETION_TOKENS,
        "reasoning_effort": REASONING_EFFORT,
    }
    generation_history = previous_metadata.get("generation_config_history")
    if not generation_history:
        generation_history = (
            [
                {
                    "requested_model": os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL),
                    "max_tokens": 400,
                    "reasoning_effort": "provider default",
                }
            ]
            if retry_errors
            else []
        )
    if current_generation_config not in generation_history:
        generation_history.append(current_generation_config)

    output = {
        "metadata": {
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "dataset": str(QUESTIONS_PATH.relative_to(PROJECT_ROOT)),
            "question_count": len(dataset["questions"]) if retry_errors else len(questions),
            "attempted_this_run": len(questions),
            "retried_previous_errors": retry_errors,
            "completed_count": sum("error" not in row for row in results),
            "latency_subset_size": LATENCY_SUBSET_SIZE,
            "latency_note": "p50/p95 use the first 15 questions; a shorter pilot uses all included questions.",
            "manual_review_required": True,
            "delay_seconds_between_requests": delay,
            "generation_config_history": generation_history,
            "mixed_generation_settings": len(generation_history) > 1,
        },
        "summary": summarize(results, latency_ids),
        "results": results,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Run RAG evaluation on the held-out questions.")
    parser.add_argument("--limit", type=int, help="Run only the first N questions (default: all 26).")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH, help="Result JSON path.")
    parser.add_argument("--delay", type=float, default=3.2, help="Pause between API calls in seconds.")
    parser.add_argument(
        "--retry-errors",
        action="store_true",
        help="Retry only questions marked as errors in the existing results file and merge them.",
    )
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be at least 1")
    if args.delay < 0:
        parser.error("--delay must not be negative")
    if args.retry_errors and args.limit is not None:
        parser.error("Do not combine --retry-errors with --limit")

    try:
        output = run_evaluation(args.limit, args.output, args.delay, args.retry_errors)
    except (FileNotFoundError, ValueError) as exc:
        parser.error(str(exc))
    print(f"\nCompleted {output['metadata']['completed_count']} of {output['metadata']['question_count']} questions.")
    print(f"Saved results to: {args.output.resolve()}")
    print(f"Latency p50 (first 15): {output['summary']['latency_p50_seconds']} seconds")
    print(f"Latency p95 (first 15): {output['summary']['latency_p95_seconds']} seconds")
    print("Manually score groundedness, citation accuracy, and safe refusals before reporting.")


if __name__ == "__main__":
    main()
