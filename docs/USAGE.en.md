**English** | [Español](USAGE.md)

# Quick start — how to generate the corpus and run tests

1) Generate variants from the seed

```bash
python safe_corpus_generator.py
# generates `phrases_expanded.txt` in the project directory
```

2) Quick review
- Open `phrases_expanded.txt` and check random samples.

3) Running tests

Use the included runner [`tools/run_tests.py`](../tools/run_tests.py):

```bash
# Mock mode (deterministic, no external calls)
python tools/run_tests.py --input phrases_expanded.txt --out results --mock

# Against a real endpoint (POST JSON {"input": text})
export MODEL_ENDPOINT="https://your-endpoint/infer"
python tools/run_tests.py --input phrases_expanded.txt --out results --endpoint
```

Generates `results/results_*.json` (one entry per variant) and `results/summary.json` (aggregate).

Minimal output format (JSON per entry):

{
  "input_id": "uuid",
  "variant": "input text",
  "response": "response text",
  "status": "ok|rejected|timeout",
  "latency_ms": 123,
}

4) Evaluation
- Use `docs/PIPELINE.en.md` to understand metrics and generate `metrics/*.csv`.
