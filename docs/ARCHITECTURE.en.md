**English** | [Español](ARCHITECTURE.md)

# ALUCINAJE project architecture

![ALUCINAJE architecture](assets/architecture.en.svg)

Summary
- ALUCINAJE is designed as a modular pipeline to generate safe adversarial corpora, run automated tests against models/agents, and record metrics.

Main components
- `Seed Corpus` — seed files (`phrases_seed.txt`) with supervised human inputs.
- `Generator` — `safe_corpus_generator.py`: paraphrasing, permutations, and controlled fuzzing.
- `Filters` — automatic rules to avoid sensitive content (safety filters, forbidden-word lists, PII detectors).
- `Test Runner` — orchestrator that sends variants to the model/agent, applies timeouts, and captures responses.
- `Evaluator` — modules that compute metrics: refusal rate, semantic divergence, toxicity, accuracy.
- `Human in the Loop` — manual review of borderline cases and filter tuning.
- `Storage` — versioning of corpora, results, and traces for auditing.

Data flows
- Editing → Seed Corpus → Generator → Candidate Variants → Filters → Test Runner → Results → Evaluator → Human Review → Augmented corpus

Storage and reproducibility
- Each run saves: seed used, generator parameters, version of the tested model, and results with a timestamp.
- Recommend using version control (git) and artifact storage (S3 / Azure Blob / Git LFS depending on scale).

Security and governance
- Do not store tokens, credentials, or sensitive data in the corpus.
- Keep a log of access, tests, and responsible parties.
- Disclosure plan for discovered vulnerabilities.

References
- See `methodology.en.md` for the operational flow and classification criteria.
