**English** | [Español](methodology.md)

Methodology for LLM robustness testing (ALUCINAJE)

Objective:
- Provide a responsible framework for evaluating the robustness and behavior of models and agents without helping to evade security controls.

Scope:
- Safe adversarial test cases (ambiguity, contradictory instructions, long context, context injection, formatting failures).
- It does not include or generate phrases intended for "jailbreak" that instruct evading policies or controls.

Work phases:
1. Collection: extract public examples and metadata from the target repository and site (README, issues, usage examples).
2. Classification: label examples by category (ambiguity, confusing-instruction, context, technical social-engineering, etc.). For prohibited content, use the taxonomy in `data/forbidden_question_categories.md`.
3. Generation: create safe variations via paraphrasing, templates, and controlled fuzzing.
4. Evaluation: run automated tests against models/agents and record metrics (response, refusal, toxicity, accuracy, policy compliance).
5. Reporting and remediation: summarize findings, classify risks, and propose mitigations.

Test types and example metrics:
- Robustness to ambiguous instructions: measure the rate of out-of-policy responses.
- Consistency: coherence between responses to variants of the same intent.
- Context injection: verify that the model prioritizes valid instructions and remembers restrictions.
- Metrics: failure rate, correct-refusal rate, semantic changes from paraphrasing, response time.

Governance and ethics:
- Maintain records, a testing lead, and a responsible-disclosure plan for vulnerabilities.
