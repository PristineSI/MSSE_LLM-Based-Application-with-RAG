"""Local Flask interface and JSON API for the policy RAG pipeline."""

from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from indexing import CHROMA_DIR, COLLECTION_NAME
from rag import answer_question

app = Flask(__name__, template_folder="templates", static_folder="static")
MAX_QUESTION_CHARS = 1_000


@app.get("/")
def home():
    """Render the local policy assistant chat page."""
    return render_template("index.html")


@app.get("/health")
def health():
    """Report whether the local policy index can be opened."""
    try:
        import chromadb

        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        collection = client.get_collection(name=COLLECTION_NAME)
        return jsonify(
            {
                "status": "ok",
                "index": "available",
                "collection": COLLECTION_NAME,
                "chunks": collection.count(),
            }
        ), 200
    except Exception as exc:
        return jsonify(
            {
                "status": "error",
                "index": "unavailable",
                "detail": str(exc),
            }
        ), 503


@app.post("/chat")
def chat():
    """Answer one question and return its citations and source snippets."""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Send a JSON object with a 'question' field."}), 400

    question = payload.get("question")
    if not isinstance(question, str) or not question.strip():
        return jsonify({"error": "The 'question' field must be a non-empty string."}), 400
    question = question.strip()
    if len(question) > MAX_QUESTION_CHARS:
        return jsonify(
            {"error": f"Questions must be {MAX_QUESTION_CHARS} characters or fewer."}
        ), 400

    try:
        result = answer_question(question)
    except (RuntimeError, FileNotFoundError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 503

    snippets = [
        {
            "chunk_id": chunk["chunk_id"],
            "policy_id": chunk["policy_id"],
            "title": chunk["title"],
            "section": chunk["section"],
            "source_file": chunk["source_file"],
            "text": chunk["text"],
            "distance": chunk["distance"],
        }
        for chunk in result["retrieved_chunks"]
    ]
    return jsonify(
        {
            "answer": result["answer"],
            "citations": result["citations"],
            "snippets": snippets,
        }
    ), 200


if __name__ == "__main__":
    # Bind to loopback so the academic demo is available only on this computer.
    app.run(host="127.0.0.1", port=5000, debug=False)
