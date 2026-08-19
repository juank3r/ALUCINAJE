#!/usr/bin/env python3
"""Run automated tests against a model endpoint or mock adapter.

Usage:
  python tools/run_tests.py --input phrases_expanded.txt --out results --mock
  python tools/run_tests.py --input phrases_expanded.txt --out results --endpoint

If --mock is used, the runner returns deterministic safe responses without calling external services.
If --endpoint is used, set environment variable MODEL_ENDPOINT to the HTTP URL (POST JSON {"input": text}).
"""
import argparse
import json
import os
import time
from datetime import datetime
from pathlib import Path

try:
    import requests
except Exception:
    requests = None


def mock_call(text):
    # deterministic safe mock response
    return {"response": "[MOCK] " + text[:200], "status": "ok"}


def call_endpoint(url, text, timeout=10):
    if requests is None:
        raise RuntimeError('requests not installed; install from requirements.txt')
    start = time.time()
    try:
        r = requests.post(url, json={"input": text}, timeout=timeout)
        r.raise_for_status()
        data = r.json()
        latency = int((time.time() - start) * 1000)
        return {"response": data.get('response', ''), "status": data.get('status', 'ok'), "latency_ms": latency}
    except Exception as e:
        return {"response": str(e), "status": "error", "latency_ms": int((time.time() - start) * 1000)}


def run(input_path: Path, out_dir: Path, mock: bool = True, endpoint: str = None):
    out_dir.mkdir(parents=True, exist_ok=True)
    lines = [l.strip() for l in input_path.read_text(encoding='utf8').splitlines() if l.strip()]
    results = []
    for i, line in enumerate(lines, start=1):
        entry = {"input_id": f"{i}", "variant": line}
        t0 = time.time()
        if mock:
            res = mock_call(line)
            res['latency_ms'] = int((time.time() - t0) * 1000)
        else:
            res = call_endpoint(endpoint, line)
        entry.update(res)
        results.append(entry)
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    out_file = out_dir / f'results_{ts}.json'
    out_file.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf8')
    # compute simple metrics
    total = len(results)
    errors = sum(1 for r in results if r.get('status') != 'ok')
    avg_latency = sum(r.get('latency_ms', 0) for r in results) / max(1, total)
    summary = {"total": total, "errors": errors, "avg_latency_ms": avg_latency, "file": str(out_file)}
    (out_dir / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf8')
    print('Wrote', out_file)
    print('Summary:', summary)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, default='phrases_expanded.txt')
    parser.add_argument('--out', '-o', type=str, default='results')
    parser.add_argument('--mock', action='store_true', help='Use mock adapter (no external calls)')
    parser.add_argument('--endpoint', action='store_true', help='Use MODEL_ENDPOINT env var as endpoint')
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        # fallback to seed
        seed = Path('phrases_seed.txt')
        if seed.exists():
            input_path = seed
            print('Using seed file', seed)
        else:
            raise SystemExit('No input file found: provide --input or generate phrases_expanded.txt')
    mock = args.mock or not args.endpoint
    endpoint = None
    if args.endpoint:
        endpoint = os.environ.get('MODEL_ENDPOINT')
        if not endpoint:
            raise SystemExit('Set MODEL_ENDPOINT env var to use --endpoint')
    run(input_path, Path(args.out), mock=mock, endpoint=endpoint)


if __name__ == '__main__':
    main()
