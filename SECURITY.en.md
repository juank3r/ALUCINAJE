**English** | [Español](SECURITY.md)

# Security policy

ALUCINAJE is a **defensive** project for measuring LLM robustness. This policy covers the
responsible disclosure of security issues in the project itself (not in third-party models).

## Scope

- Failures in filtering/sanitization that allow unsafe content into the corpus.
- Leaks of sensitive data (PII, credentials) in corpora, artifacts, or metrics.
- Issues in the evaluation harness (e.g. persisting payloads that should be ephemeral).

## How to report

Open a private advisory with **GitHub Security Advisories** in the repository, or an issue with the
`security` label **without** including sensitive/operational content. Include reproduction steps and the impact.

## Commitments

- Acknowledgment of receipt and reasonable triage.
- Prioritized fixes according to severity; a mitigation plan (blocking, credential rotation,
  stakeholder notification) per [`docs/JAILBREAK_RISKS.en.md`](docs/JAILBREAK_RISKS.en.md).

## Known findings

- The `is_probably_jailbreak()` filter is **lexical** (keywords), not semantic: it can let
  paraphrased jailbreaks through. Current mitigation: nothing from the import is committed automatically and
  `phrases_seed.txt` is kept curated by hand. Details in [`docs/FILTERING.en.md`](docs/FILTERING.en.md).
