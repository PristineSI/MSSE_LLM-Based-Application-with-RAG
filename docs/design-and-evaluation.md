# Design and Evaluation

## System design

This is a local, single-user RAG demonstration over a fictional policy corpus. Evaluation questions are held out and are never passed to ingestion or indexing.

Policy Markdown files are split into heading-aware chunks with source metadata. Chroma uses its local ONNX MiniLM embedding function and stores the index under the ignored chroma directory. Each question retrieves the four closest chunks. Generation receives the question and those excerpts, must cite the policy ID and section, and is instructed to refuse unsupported questions. The cosine-distance cutoff of 0.80 and 220-word answer limit are initial heuristics, not validated thresholds. The current generation request allows 1,000 completion tokens and requests low reasoning effort.

The Flask server binds to 127.0.0.1. The root route serves the local chat page; POST /chat returns an answer, citations, and retrieved passages; GET /health reports index availability and chunk count. The API key is loaded from a local .env file and must not be committed. The question and retrieved fictional passages are sent to OpenRouter for generation; retrieval and embeddings run locally.

## Continuous integration

GitHub Actions runs on pushes and pull requests to main. The workflow installs the pinned requirements, parses application and test sources for syntax errors, runs the policy-ingestion preview, and executes offline unit checks for the loader and Flask routes. These checks do not require an API key, create a vector index, or make external model calls. There is no deployment job because the project is designed for a local demonstration and deployment is optional in the assignment.

## Evaluation design

The held-out dataset contains 26 items: 21 answerable questions (three per policy topic) and five out-of-scope questions. The runner is src/evaluate.py. It saves generated answers, model names when reported by the provider, retrieved and cited source sections, distance scores, per-question latency, and review fields to data/evaluation/latest-results.json.

The evaluation was run from the project root with the virtual environment active and .env configured. The initial run attempted all 26 questions, followed by retries of provider-error rows. The run uses a free model router that selected different models across requests. Initial requests used a 400-token cap and provider-default reasoning; error retries used a 1,000-token cap and low reasoning effort. The merged results therefore use mixed generation settings and are preliminary rather than a controlled final benchmark.

### Measures and scoring

Each applicable answer received a score from 0 to 2.

- Groundedness: 0 = unsupported or materially contradicted; 1 = partly supported or missing important qualifications; 2 = all material claims supported by policy text. An unjustified refusal to an answerable question scores 0 because it fails to reflect available evidence.
- Citation accuracy: 0 = absent or materially wrong; 1 = partly correct or incomplete; 2 = cited policy and section support the associated claims. Missing required citations score 0. Q26 has no expected source section, so citation accuracy is not applicable.
- Safe-refusal quality for out-of-scope questions: 0 = unsafe substantive answer; 1 = safe refusal but missing an expected referral or next step; 2 = safe refusal with an appropriate next step.
- Retrieval section recall: expected source sections found in retrieved chunks divided by the number of expected source sections.
- Citation section recall: expected source sections represented in returned citations divided by expected source sections. This is a section-recall measure and is not the same as citation accuracy.
- Latency: p50 and p95 over successful responses in the first 15 questions. The measure includes local retrieval and external model generation time.

Percentages normalize the 0–2 scores: sum of applicable scores divided by twice the number of applicable outputs, multiplied by 100. Q05 is excluded from answer-quality denominators because no answer was returned. Q26 is excluded from citation accuracy because the evaluation defines no expected source citation.

## Preliminary recovery results — 9 November 2026

The student manually vetted and agreed with the AI-assisted scores recorded in data/evaluation/latest-results.json.

| Measure | Result | Notes |
| --- | ---: | --- |
| Dataset | 26 questions | 21 answerable, 5 out of scope |
| Pipeline outputs returned | 25/26 (96.2%) | Q05 remained a provider output-limit failure |
| Groundedness | 29/50 = 58.0% | 25 applicable outputs; answerable false refusals were scored 0 |
| Citation accuracy | 23/48 = 47.9% | 24 applicable outputs; missing or incomplete expected citations lower the score |
| Safe-refusal quality | 5/10 = 50.0% | Five out-of-scope responses; all avoided unsupported substantive advice but omitted expected next steps |
| Mean expected-section retrieval recall, completed answerable questions | 92.5% | 18.5/20 mean per-question recall; Q19 missed its expected section and Q16 retrieved one of two |
| Mean expected-section citation recall, completed answerable questions | 57.5% | 11.5/20 mean per-question recall |
| Latency, first 15 questions | p50 5.713 s; p95 11.022 s | 14 successful outputs; Q05 excluded |

The main weakness was at the generation and citation-validation stage. Retrieval found the expected source sections for most answerable questions, but the system often returned a generic refusal instead of a cited answer. Of 20 answerable questions with completed outputs, eight received a generic refusal. Seven of those had the expected policy section in the retrieved chunks; Q19 did not, making it a retrieval miss. The saved results contain only the post-validation answer, so they cannot show whether each generic refusal came from the model or from the app replacing an answer whose citation did not match its strict format.

The varying free-model route, strict citation-format validation, one retrieval miss, and one provider output-limit failure likely contributed. Q05 selected recursive/flint-v1.0:free, reached finish_reason=length at the 1,000-token completion limit, and returned no answer text. Out-of-scope responses generally avoided unsupported advice but often omitted specific referrals, including urgent care for Q26. These findings are preliminary because model selection varied and generation settings changed during retries.

## Interpretation and remaining limits

The reviewed percentages describe end-to-end grounded-answer performance under the stated scoring rules. They are not a clean comparison across fixed model settings. The 92.5% and 57.5% section-recall values are separate retrieval/citation coverage measures; neither substitutes for the manually reviewed groundedness or citation-accuracy scores.

The corpus and company are fictional. Free-model availability and behavior may change. The distance threshold, top-k value, prompt, and output limit remain heuristics. This project is an academic prototype, not an HR or legal advice system. A further final benchmark would require rerunning all 26 questions under one generation configuration and recording the model used for each response.
