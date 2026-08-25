**English** | [Español](PIPELINE.md)

# Pipeline

![End-to-end pipeline](assets/pipeline.en.svg)

Description
- The pipeline transforms a human seed into a broad set of safe variants that are tested against models. The stages are described below; further down, a high-level ASCII diagram is also kept.

Stages
- 1) Seed: manual seed phrases.
- 2) Expand: generation via paraphrasing, permutations, and rules.
- 3) Filter: apply safety rules (PII, evasion, harmful instructions).
- 4) Test: send to models/agents with time limits and controlled context.
- 5) Eval: automatic metrics + human labeling.
- 6) Iterate: adjust the generator and filters based on results.

ASCII diagram (pipeline):

    +--------+    +----------+    +---------+    +------+    +---------+    +--------+
    |  Seed  | -> |  Expand  | -> | Filters | -> | Test | -> | Evaluator| -> | Human  |
    | (txt)  |    | (paraph) |    |  (safe) |    |(runner)|    | metrics |    | Review |
    +--------+    +----------+    +---------+    +------+    +---------+    +--------+

Operational details
- Each block is parameterizable: number of paraphrases, permutation depth, filter thresholds.
- Tests run in parallel and responses are normalized (JSON with fields: input_id, variant, response, status, latency).
- The Evaluator produces a CSV/JSON with aggregated metrics and individual cases for review.

Examples of generated artifacts
- `phrases_expanded.txt` — list of variants.
- `results/YYYYMMDD_modelX.json` — results per run.
- `metrics/YYYYMMDD_modelX.csv` — aggregated metrics.
