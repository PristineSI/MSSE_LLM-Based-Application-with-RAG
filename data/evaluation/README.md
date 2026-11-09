# Evaluation question set

`questions.json` contains 26 questions: three answerable questions for each of the seven synthetic policy topics and five out-of-scope questions. Each entry includes a reference answer and expected policy section IDs. Reference answers are scoring guides; the application does not need to match them word for word.

Keep this file separate from `data/policies` and do not ingest it into the retrieval index. It is the held-out evaluation set. Score answerable questions for factual support and citation accuracy. Score unanswerable questions for a clear refusal or safe referral without invented policy details. Measure latency on a consistent subset of 10–20 questions and record the chosen subset in the evaluation report.

The policy corpus is fictional and was written solely for this academic exercise. The legal, tax, medical, and specific AI-vendor questions are deliberate out-of-scope checks.
