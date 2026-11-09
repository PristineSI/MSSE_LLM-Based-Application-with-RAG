# Northstar Labs Policy Assistant

A local Retrieval-Augmented Generation (RAG) application for asking questions about a fictional company's policies. The project is being built as an academic exercise.

## Important: fictional training corpus

All policy documents created for this project are synthetic examples, written solely for this academic exercise. Northstar Labs is fictional. The policies do not represent any real company's rules and are not legal, HR, or business advice. No private or paid policy documents are used.

## Project status

The repository, Python environment, and seven-document synthetic policy corpus are set up. The policy loader, chunker, persistent local Chroma index, retrieval module, grounded answer generation module, and local Flask chat page/API are implemented. A preliminary recovery evaluation and student-vetted AI-assisted manual scores are documented; a final single-configuration benchmark remains pending. The app is intended to run and be demonstrated locally; public deployment is not planned.

## Synthetic policy corpus

The fictional policy corpus currently contains seven Markdown documents:

- Leave and time off
- Remote and hybrid work
- Business expenses and reimbursement
- Information security and acceptable use
- Company holidays and coverage
- Resignation and termination of appointment
- Responsible AI use

All documents are synthetic, created solely for this academic exercise, and contain no real company or employee policies.

## Design

- Flask provides the local chat page and the `/chat` and `/health` endpoints.
- LangChain handles Markdown-aware splitting and document metadata; Chroma stores the local vector index and performs semantic retrieval.
- The retrieval function returns the top matching policy chunks and their source metadata.
- Answer generation sends only those excerpts to an OpenRouter OpenAI-compatible chat endpoint. A free-model router is the default, and the model can be changed through `.env`.
- Answers must cite matching policy IDs and section paths. If retrieval finds no sufficiently close chunks or generation returns no traceable citation, the system refuses to answer.
- A cosine-distance cutoff and 220-word answer limit are initial guardrails and should be tuned and assessed with the separate evaluation set.

The local index is ignored by Git and can be rebuilt from the synthetic policy Markdown files.

## Setup

Use Windows Command Prompt from the repository root. Create and activate the virtual environment, then install the recorded dependencies:

```bat
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

The Python version used during initial setup was 3.14.4.

## Configure answer generation

Create an OpenRouter API key, then copy `.env.example` to `.env` and put the key in `OPENROUTER_API_KEY`. Keep `.env` private; it is excluded by `.gitignore`. The default model setting is `openrouter/free`; free inference is rate limited and model availability can change. You can set `OPENROUTER_MODEL` to another compatible model ID if needed.

The vector search and embeddings run locally. Generating an answer sends the question and retrieved synthetic policy passages to the configured LLM provider.

## Preview policy ingestion

With the virtual environment active, run this from the repository root to load only the Markdown files in `data/policies`, split them into heading-aware chunks, and print a short preview:

```bat
python src\ingestion.py
```

The evaluation set in `data/evaluation` is kept separate and is not read by the ingestion script.

## Build the local vector index

With the virtual environment active, run this from the repository root:

```bat
python src\indexing.py
```

The first run downloads Chroma's local ONNX MiniLM embedding model. The resulting persistent database is stored in the ignored `chroma/` directory. Re-run the command after changing a policy document to synchronize the index. The evaluation questions are not indexed.

## Retrieval and answer generation

To retrieve relevant policy chunks and their metadata:

```bat
python src\retrieval.py
```

Run this command to ask a question through retrieval and answer generation:

```bat
python src\rag.py
```

## Evaluation

The held-out evaluation set contains 26 questions. From the project root, run python src\evaluate.py to evaluate all questions. This makes 26 requests to the configured provider and saves answers, sources, latency, and manual-review fields to data/evaluation/latest-results.json. The p50 and p95 latency figures use the first 15 questions. Review groundedness, citation accuracy, and out-of-scope refusals manually; the runner does not assign those scores. See docs/design-and-evaluation.md for the scoring guide. To retry only provider-error questions in an existing results file, run python src\evaluate.py --retry-errors. A retry after changing generation settings produces a mixed-configuration recovery result; run all 26 questions again with one configuration for final reported metrics. To run a 15-question pilot first, run python src\evaluate.py --limit 15.

## AI assistance

The tools used and their contributions are documented in ai-tooling.md.


## Run locally

With the virtual environment active and `.env` configured, run the Flask app from the project root:

```bat
python src\app.py
```

Open `http://127.0.0.1:5000` in your browser. The local interface displays the generated answer, citation metadata, and retrieved policy passages. The JSON endpoints are:

- `GET /health` — reports whether the local Chroma collection is available and how many chunks it contains.
- `POST /chat` — accepts `{"question": "..."}` and returns the answer, citations, and retrieved snippets.

The server binds to `127.0.0.1` for a local demonstration. Stop it with `Ctrl+C` in Command Prompt.

## Continuous integration

GitHub Actions runs the workflow in `.github/workflows/ci.yml` on pushes and pull requests to `main`, and can also be started manually. It installs the project dependencies, parses Python files for syntax errors, checks policy ingestion, and runs offline route and ingestion checks. The workflow does not need an OpenRouter API key, create a Chroma index, or call the model. The demo remains local, so this project does not automatically deploy the app.



\n