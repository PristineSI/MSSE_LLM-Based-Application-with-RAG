# Synthetic Policy Corpus Plan

## Purpose and status

This plan defines a fictional policy corpus for the Northstar Labs Policy Assistant. All documents will be authored for this academic exercise. Northstar Labs is fictional, and none of the policy text should be presented as real company policy or professional advice.

The assignment calls for approximately 5–20 short documents totaling 30–120 pages. The seven Markdown policy drafts are complete and total 9,804 words. At a planning estimate of about 230 words per page, the corpus is approximately 43 page-equivalents. Actual rendered page count depends on formatting and should be checked when the documents are laid out.

## Planned documents

| File | Topic | Example information to define |
| --- | --- | --- |
| `leave-and-time-off.md` | Annual leave, sick leave, requesting leave, carry-over | Eligibility, notice periods, approval steps, limits, exceptions |
| `remote-work.md` | Hybrid work, remote-work requests, availability | Eligible roles, schedule expectations, equipment, approval process |
| `expenses.md` | Reimbursable costs and expense claims | Spending limits, receipts, submission deadlines, excluded costs |
| `information-security.md` | Device use, passwords, data handling, incident reporting | Approved devices, access rules, reporting window, prohibited actions |
| `holidays.md` | Company holidays and holiday scheduling | Annual calendar, office closure, coverage, time-off interactions |
| `resignation-and-termination.md` | Employee resignation and company-initiated termination of appointment | Written notice, transition, approvals, property return, access closure, administrative questions |
| `responsible-ai-use.md` | Use of generative AI and AI-enabled tools for company work | Approved tools and data, human review, prohibited uses, disclosure, incident reporting |

Each document should have a title, version, fictional effective date, clear headings, definitions where useful, rules, steps, exceptions, and a fictional role or team responsible for questions. The documents should use consistent terminology and avoid conflicting rules unless a conflict is intentional and included in evaluation questions.

## Evaluation-set plan

The prepared set contains 26 questions: three answerable questions for each of the seven policy topics, plus five questions that are out of scope or require a refusal. Record expected answers and the source passage or document for each answer. Use 10–20 questions for latency measurement, consistent with the assignment instructions.

## Design notes

- Use Markdown so the initial corpus is easy to read, edit, and version in Git.
- The loader splits on Markdown headings, then uses 1,200-character chunks with 200-character overlap for longer sections. Each chunk keeps its policy ID, filename, title, section path, and chunk ID as metadata.
- Chroma uses its local ONNX MiniLM L6 V2 embedding function and persists vectors under `chroma/`. The evaluation set remains outside the index.
- Keep every policy fully synthetic and free of real personal, company-confidential, or paid content.
- Give each document a stable ID or filename so responses can cite it consistently.
- Add a small number of unanswerable questions to check that the assistant does not invent policy details.





\n