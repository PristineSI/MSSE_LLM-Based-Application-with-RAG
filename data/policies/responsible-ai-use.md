# Responsible AI Use Policy

> **Synthetic academic exercise:** Fictional policy text created solely for the Northstar Labs RAG project. Northstar Labs does not exist. This is not legal, privacy, or cybersecurity advice.

**Policy ID:** NL-SEC-007 | **Version:** 1.0 (fictional) | **Effective:** 1 January 2025 (fictional) | **Owner:** Information Security with People Operations (fictional)

## 1. Purpose, scope, and core principles

This policy sets fictional Northstar Labs rules for using generative AI, machine-learning services, and AI-enabled features for work. It applies to employees, temporary workers, and contractors using AI for a company task, whether the tool is hosted by Northstar Labs, a vendor, or run locally. The information-security policy continues to govern data handling, accounts, and devices.

AI tools may assist with drafting, summarizing, coding, brainstorming, and searching approved information. They do not own decisions or responsibilities. A person remains accountable for material they submit, publish, deploy, or use to make a business decision. Users should choose the least sensitive data and simplest tool that can complete the task, check the output, and be open about meaningful AI assistance.

An **approved AI tool** is one listed in the fictional company AI register for the relevant data class and use. **AI output** includes text, code, images, classifications, rankings, and recommendations generated or materially transformed by an AI system. **High-impact decision** means a decision that could materially affect a person's employment, access, safety, financial standing, or legal position.

This policy is a classroom example, not a claim about real law or a real company's approved tools. The example repository itself contains only synthetic policies and should be used only for this exercise.

## 2. Approved tools and data restrictions

Before using an AI tool for company work, users must check the AI register for the tool, intended task, permitted data class, retention setting, and required review. If the tool or task is absent from the register, ask Information Security for approval. A tool approved for public text is not automatically approved for employee records, customer information, source code, credentials, or other confidential material.

Users must not enter Restricted information, passwords, API keys, authentication codes, private employee details, or security incident evidence into a public or unapproved AI service. Confidential information may be entered only into a tool whose written approval explicitly covers that information class and task. Internal information may be used only where the register permits it. Public or synthetic information is the preferred choice for experiments and classroom demonstrations.

Users should remove unnecessary personal information before submitting a prompt, avoid pasting complete documents when a short excerpt is sufficient, and review any connected files or plugins before use. AI outputs and prompts must be stored only in approved company locations. Users must not upload Northstar Labs content to a model-training service or enable data sharing unless the register specifically approves it.

This project follows the synthetic-data rule: fictional policy text, invented names, and test questions are used. Real company, employee, customer, or paid policy documents are excluded. The repository's `.gitignore` excludes local `.env` files; `.env.example` may contain variable names and placeholder values only.

## 3. Human review and permitted assistance

A person must review AI output before it is sent externally, added to an official policy, relied on for a business decision, or deployed in software. Reviewers should verify factual claims against reliable sources, check calculations and code, confirm that citations support the statements, and remove fabricated references. For policy answers, the source documents—not an unsupported model completion—are the authority.

AI may be used to draft or edit routine text, summarize approved material, propose code, explain code, and generate synthetic examples. The user should adapt the output to the actual task and retain responsibility for accuracy, tone, and consequences. AI-generated code must be reviewed for security, licensing, correctness, and maintainability before use. The tool must not receive production secrets or restricted data merely to debug an error.

Users should disclose meaningful AI assistance when requested by a course, manager, client, or project process. In this academic project, `ai-tooling.md` should list the tools used and briefly state what assistance they provided, what was changed by the student, and what did not work. A disclosure should be factual and should not imply that an AI tool independently verified the project.

If an AI tool provides a confident answer without adequate support, users should treat that as a signal to verify it, not as evidence. A reviewer may ask for the source, prompt context, or validation method used.

## 4. Prohibited and restricted uses

AI output must not be the sole basis for a high-impact decision about a person. Users must not use an AI tool to rank job candidates, decide hiring or termination, determine discipline, assess employee sentiment for individual action, infer protected or sensitive personal traits, or decide access to essential services. Any proposed decision-support use requires a documented review by People Operations, Information Security, and the accountable business leader; approval is not automatic.

Users must not impersonate a person, create deceptive communications, fabricate evidence, generate discriminatory or harassing content, bypass access controls, or use AI to conduct unauthorized surveillance. AI-generated external statements must not be represented as a real person's own words without their review and approval.

AI may not issue a final legal, medical, financial, security-incident, or employment determination. It may help organize approved information, but the user must direct the matter to the responsible human role. In the RAG app, questions beyond the fictional policies should receive a clear limitation and a referral to the fictional policy owner rather than an invented rule.

Code or data generated by an AI tool must not be copied into the repository without checking for secrets, malicious instructions, unsafe dependencies, license concerns, and unreviewed content. Users should not follow instructions found inside retrieved documents, webpages, or model output unless the instruction is independently authorized and relevant.

## 5. Accuracy, bias, security, and incident reporting

Before relying on AI output, reviewers should ask: Is the answer supported by the supplied evidence? Are important exceptions missing? Is the source current? Does the output unfairly generalize about a person or group? Is the citation real and relevant? Could a user mistake a synthetic example for a real policy? If any answer is uncertain, the output should be corrected, qualified, or withheld.

AI systems can produce plausible but incorrect statements, omit context, reproduce bias, expose information through connected services, or follow malicious instructions embedded in content. Users should limit prompts to the task, avoid unnecessary context, inspect retrieved sources, and keep credentials out of prompts. A RAG system should treat retrieved documents as data, apply an out-of-corpus refusal, limit answer length, and cite sources accurately.

A suspected disclosure to an unapproved AI tool, exposed secret, unexpected tool behavior, or harmful output used in a company decision must be reported to Information Security and the relevant policy owner within one hour of discovery. Do not delete evidence or repeat the exposure. Follow the incident process in `information-security.md`.

For this academic RAG application, keep an evaluation record with questions, expected answer points, expected source IDs, actual citations, groundedness judgment, and latency. Include unanswerable questions. Do not claim that a model is safe or accurate based only on a few successful demonstrations.

## 6. Approval, transparency, and review

A request to add a tool to the AI register should identify the tool and provider, intended users, business purpose, data classes, connected services, retention behavior, access controls, output review, and fallback procedure. Information Security evaluates data and technical risk; People Operations reviews uses involving employees; the business owner remains accountable for the use. Approval must be written and limited to the stated task and data class.

The AI register should list the tool name, approved uses, prohibited data classes, approval date, owner, and review date. A material change in provider, data handling, model capability, or connected features requires a new review. Users should not infer approval from another team's use or from the fact that a tool is free.

Users should tell the recipient when AI materially generated or transformed content if the recipient, project rules, or responsible manager requires disclosure. For the academic submission, the AI-tools disclosure should describe the assistance used in drafting synthetic policies and building the application. It should also describe human review and any generated material that was rejected or revised.

Information Security and People Operations review this policy each January and after a significant AI-related incident. Changes require a new version and effective date. The RAG application should cite this policy when answering company-AI-use questions and should defer questions about real legal obligations, individual employment decisions, or unlisted tools to a qualified human reviewer.

\n