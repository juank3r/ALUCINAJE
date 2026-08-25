**English** | [Español](forbidden_question_categories.md)

# Taxonomy of forbidden categories (forbidden_question)

These are the **13 categories** of prohibited content used by the
[`verazuo/jailbreak_llms`](https://github.com/verazuo/jailbreak_llms) dataset
(`data/forbidden_question/forbidden_question_set.csv`). They are **only classification labels**,
they contain no prompts or payloads.

They are used in ALUCINAJE to **label and group test cases** and to measure robustness by category
(e.g., correct refusal rate by content type). See [`docs/DATA_SOURCES.en.md`](../docs/DATA_SOURCES.en.md).

| # | Category (EN) | Brief description |
|---|----------------|-------------------|
| 1 | Illegal Activity | Illegal activities in general |
| 2 | Hate Speech | Hate speech / discrimination |
| 3 | Malware | Generation of malicious software |
| 4 | Physical Harm | Physical harm to people |
| 5 | Economic Harm | Economic harm |
| 6 | Fraud | Fraud and deception |
| 7 | Pornography | Explicit sexual content |
| 8 | Political Lobbying | Political campaigns / lobbying |
| 9 | Privacy Violence | Privacy violation |
| 10 | Legal Opinion | Unqualified legal advice |
| 11 | Financial Advice | Unqualified financial advice |
| 12 | Health Consultation | Unqualified medical consultation |
| 13 | Gov Decision | Government / administration decisions |

Source and license: `verazuo/jailbreak_llms` (MIT). Attribution in [`docs/DATA_SOURCES.en.md`](../docs/DATA_SOURCES.en.md).

## Mapping to JailbreakBench (10 categories)

[JBB-Behaviors](https://jailbreakbench.github.io/) uses 10 categories (aligned with usage policies).
Approximate correspondence with verazuo's 13:

| JBB (10) | verazuo (13) |
|---|---|
| Harassment/Discrimination | Hate Speech |
| Malware/Hacking | Malware |
| Physical Harm | Physical Harm |
| Economic Harm | Economic Harm |
| Fraud/Deception | Fraud |
| Disinformation | (Political Lobbying / — ) |
| Sexual/Adult Content | Pornography |
| Privacy | Privacy Violence |
| Expert Advice | Legal Opinion · Financial Advice · Health Consultation |
| Government Decision-Making | Gov Decision |

Source: P. Chao et al., "JailbreakBench", NeurIPS 2024. The per-category breakdown in
`tools/eval_jailbreaks.py` uses the `Category` label from the chosen dataset.
