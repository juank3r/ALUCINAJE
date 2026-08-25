**English** | [Español](HOME.md)

## ALUCINAJE — Wiki

Welcome to ALUCINAJE — a project to generate, test, and improve the robustness of LLMs and agents through responsible adversarial corpora.

================================================================================

						  .----.   .----.  .----.   .----.
						 /      \ /      \/      \ /      \
						/  .-.  /  .-.  /  .-.  /  .-.  /
					   |  (   )|  (   )|  (   )|  (   )|
						\  `-'  \  `-'  \  `-'  \  `-'  /
						 `-----' `-----' `-----' `-----'

================================================================================

Main sections (jump to any):

- **Architecture** — components and data flow. See: [ARCHITECTURE](ARCHITECTURE.en.md)
- **Methodology** — process to create, classify, and evaluate phrases. See: [methodology](../methodology.en.md)
- **Pipeline** — diagram and step-by-step explanation. See: [PIPELINE](PIPELINE.en.md)
- **Data sources** — where the prompts come from and how they are filtered. See: [DATA_SOURCES](DATA_SOURCES.en.md)
- **Corpus** — seeds and how to expand with `safe_corpus_generator.py`.
- **Risks and consequences** — impact and mitigation against jailbreaks. See: [JAILBREAK_RISKS](JAILBREAK_RISKS.en.md)
- **Quick start** — generate the corpus and run tests. See: [USAGE](USAGE.en.md)
- **ASCII art and gallery** — contributed works and diagrams. See: [ASCII_ART](ASCII_ART.txt)

How to use this wiki

1. Read the **Methodology** (`methodology.en.md`) to understand the responsible framework.
2. Generate the corpus with `python safe_corpus_generator.py` and review `phrases_expanded.txt`.
3. Run the automated tests (tbd in `docs/USAGE.en.md`) and analyze metrics.

Contribute

- Add new phrases in `phrases_seed.txt` (legal and safe content only).
- Open PRs for methodology improvements or new tests.
