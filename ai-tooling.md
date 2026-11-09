# AI Tooling Disclosure

This project uses AI assistance as part of an academic exercise. The fictional Northstar Labs policies are synthetic examples and do not represent a real employer.

## Tools and contributions

- OpenAI Codex (GPT-6) assisted with drafting and revising synthetic policy documents, planning the corpus and evaluation questions, and implementing the ingestion, indexing, retrieval, answer-generation, Flask, and evaluation code. It also helped prepare documentation and setup instructions.
- OpenRouter free-model API (openrouter/free) is used by the application at runtime to generate answers from retrieved synthetic policy excerpts. This router can select different available free models, so the exact model may vary; evaluation output records the provider-reported model when available.

## Student review and decisions

The student selected the fictional policy scope, chose to include resignation/termination and responsible AI policies, and specified that unused annual-leave days above the five-day carry-over cap expire on December 31. The student created the local Python environment and API key configuration, ran the retrieval and answer-generation scripts, and launched the Flask app locally. Add any further edits or decisions made during review before submission.

## Limitations and reflection

AI assistance did not independently verify policy content, code, security, evaluation metrics, or assignment compliance. Generated policies are fictional and should not be used as real company policy. The OpenRouter free-model route is variable; record the model when available and manually score outputs. Add a brief personal reflection describing what assistance was useful, what you changed, and any AI output that needed correction or did not work as expected.
