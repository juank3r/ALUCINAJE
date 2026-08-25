**English** | [Español](DATA_SOURCES.md)

# Data sources and provenance

This document is the **source of truth** on where the prompts that feed the ALUCINAJE
pipeline come from and, above all, on **what is imported and what is NOT**.

![Data provenance](assets/data-provenance.en.svg)

## Principle

ALUCINAJE generates **safe adversarial corpora** to measure the robustness of LLMs. From external
sources it imports **safe adversarial phrases, taxonomy, and metadata**; the actual jailbreak
*payloads* are **cited as an external source, not copied** into this repository. The
`is_probably_jailbreak()` filter in [`tools/import_and_sanitize.py`](../tools/import_and_sanitize.py)
discards content that instructs how to evade controls.

## Actual state (verified on 2026-08-20)

- The [`.github/workflows/import-and-sanitize.yml`](../.github/workflows/import-and-sanitize.yml) workflow
  is **manual** (`workflow_dispatch`) and only publishes an **artifact** (`phrases_imported_sanitized.txt`).
- There is **no imported content committed** in the repo: `phrases_seed.txt` contains 9 seed phrases
  written by hand. Import ≠ content in the repo.
- To incorporate imported phrases into the seed you must go through **human review** and
  [`tools/prepare_pr_from_approved.py`](../tools/prepare_pr_from_approved.py).

### Actual import result (verified run)

Running the workflow over the two repos, the sanitization produced (summary from `.summary.json`):

| Metric | Value |
|---|---|
| Files scanned | 269 |
| Candidates | 37 332 |
| Dropped (short) | 994 |
| Dropped (jailbreak) | 1 779 |
| Dropped (duplicates) | 7 715 |
| "kept" | 26 843 |

> [!WARNING]
> The "kept" set is **NOT safe**. The filter is **lexical** (keywords) and lets a lot of
> problematic content through: operational jailbreak guidance and **sexually explicit material about real
> people**. That is why it is **not dumped into the seed**: `phrases_seed.txt` is kept **curated by hand**. These
> repos are almost entirely jailbreaks/NSFW, so **there is no safe corpus to mine** from them.
> Details of the filtering and its limits in [`FILTERING.md`](FILTERING.en.md).

## Upstream sources

### 1. `verazuo/jailbreak_llms`
- URL: https://github.com/verazuo/jailbreak_llms
- Description: dataset from the CCS'24 paper — 15,140 prompts collected from Reddit, Discord, websites, and
  open-source datasets, of which **1,405 are jailbreaks**. It is "the jailbreak website" the
  project refers to.
- Popularity: ⭐ ~3.8k.
- **License: MIT** (allows reuse with attribution).
- Relevant structure:
  - `data/prompts/` — `jailbreak_prompts_2023_05_07.csv`, `jailbreak_prompts_2023_12_25.csv`,
    `regular_prompts_2023_05_07.csv`, `regular_prompts_2023_12_25.csv`.
  - `data/forbidden_question/` — `forbidden_question_set.csv`,
    `forbidden_question_set_with_prompts.csv.zip` (taxonomy of forbidden categories).
  - `code/` — utilities from the paper.
- What we take: **the `forbidden_question` taxonomy (categories) and statistics**; neutral/regular
  safe phrases after the filter. Jailbreak prompts are cited, not imported.

### 2. `Goochbeater/Spiritual-Spell-Red-Teaming`
- URL: https://github.com/Goochbeater/Spiritual-Spell-Red-Teaming
- Description: collection of red-teaming/jailbreak guides by provider (mainly Claude).
- Popularity: ⭐ ~3.2k.
- **License: none declared** → by default *all rights reserved*. **Its content must not be
  redistributed**; it is only cited/linked.
- Structure (`Jailbreak-Guide/`): `Anthropic/` (Claude 3.7/4, Opus 4.5/4.6, Claude Code, Fable 5…),
  `ChatGPT/`, `Gemini/`, `Grok/`, `Other LLMs/`, `System Prompts/`, `ENI-Tutor/`,
  `Jailbroken POE bots/`.
- What we take: **only the taxonomy/structure as a reference** (which attack categories exist).
  No payload is copied, due to licensing and project policy.

### 3. `JailbreakBench/JBB-Behaviors` (evaluation benchmark)
- URL: https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors · https://jailbreakbench.github.io/
- Description: standard benchmark (NeurIPS 2024). **100 harmful behaviors + 100 twin benign**,
  10 categories. Fields `Goal`, `Target`, `Behavior`, `Category`, `Source`.
- Use in ALUCINAJE: **only as an evaluation set** in `tools/eval_jailbreaks.py --dataset jbb`
  (downloaded at runtime, not committed). The benign ones feed the **over-refusal** metric.
- Attribution: P. Chao et al., "JailbreakBench: An Open Robustness Benchmark for Jailbreaking LLMs",
  NeurIPS 2024.

## How it is imported (defensive flow)

1. Run the **Import and Sanitize External Prompts** workflow (dispatch) or locally:
   ```bash
   python tools/import_and_sanitize.py \
     --repos https://github.com/verazuo/jailbreak_llms \
             https://github.com/Goochbeater/Spiritual-Spell-Red-Teaming \
     --out phrases_imported_sanitized.txt
   ```
   It also generates `phrases_imported_sanitized.summary.json` with the **metadata summary**
   (number of repos, files scanned, candidates, dropped by the filter, final phrases).
2. **Review** `phrases_imported_sanitized.txt` by hand (see the warning above: the filter is weak).
3. Approve and propose a PR with
   `python tools/prepare_pr_from_approved.py --approved approved_phrases.txt`.

## Imported taxonomy

What is imported safely is the **category taxonomy** from `forbidden_question`
(labels only, no payloads): see [`data/forbidden_question_categories.md`](../data/forbidden_question_categories.en.md).

## Correct use of jailbreaks: evaluation (not seed)

Jailbreak prompts **are not copied or expanded**. The correct way to use them is as an
**evaluation set**: [`tools/eval_jailbreaks.py`](../tools/eval_jailbreaks.py) downloads them at
test time from upstream (MIT), sends them to an endpoint, and computes the **refusal rate**, without
storing them in the repo.

```bash
# self-test (sin red ni payloads)
python tools/eval_jailbreaks.py --self-test
# contra un endpoint real
MODEL_ENDPOINT="https://tu-endpoint/infer" python tools/eval_jailbreaks.py --limit 100 --out metrics
```

## Attribution

When reusing `verazuo/jailbreak_llms` (MIT), cite:
> H. Shen et al., "In-The-Wild Jailbreak Prompts on LLMs", ACM CCS 2024. Repo: verazuo/jailbreak_llms.

`Goochbeater/Spiritual-Spell-Red-Teaming` is linked as a reference; its content is not redistributed.
