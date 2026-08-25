#!/usr/bin/env python3
"""Discovery / fingerprinting of AI services (read-only, scoped).

Probes the AUTHORIZED targets from scope.yaml for common self-hosted AI runtimes and agent platforms
(Ollama, vLLM / OpenAI-compatible, LM Studio, LocalAI/llama.cpp, HF TGI, Open WebUI, Gradio, ...) and
writes an `inventory.json` of what is exposed.

SAFETY (red lines):
  - Read-only HTTP GET probes only. No writes, no attacks here.
  - Only targets authorized in scope.yaml are probed; a recipe port is skipped unless that host:port is
    in scope (a bare host authorizes all ports; host:port authorizes only that port).

Usage:
  python tools/discover.py --scope scope.yaml --out inventory.json
  python tools/discover.py --self-test        # offline: validate fingerprint matchers, no network
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import requests
except Exception:  # pragma: no cover - optional for --self-test
    requests = None


# ---- Fingerprint matchers (pure functions) --------------------------------------------------------
def m_ollama_tags(status, headers, text, data):
    if status == 200 and isinstance(data, dict) and "models" in data:
        return {"service": "ollama",
                "models": [m.get("name") for m in data["models"] if isinstance(m, dict)],
                "auth_required": False}
    return None


def m_ollama_root(status, headers, text, data):
    if "ollama is running" in (text or "").lower():
        return {"service": "ollama", "models": [], "auth_required": False}
    return None


def m_openai_models(status, headers, text, data):
    if status in (401, 403):
        return {"service": "openai-compatible", "models": [], "auth_required": True}
    if status == 200 and isinstance(data, dict) and isinstance(data.get("data"), list):
        server = (headers or {}).get("server", "").lower()
        svc = "vllm" if ("vllm" in server or "uvicorn" in server) else "openai-compatible"
        return {"service": svc,
                "models": [d.get("id") for d in data["data"] if isinstance(d, dict)],
                "auth_required": False}
    return None


def m_tgi_info(status, headers, text, data):
    if status == 200 and isinstance(data, dict) and "model_id" in data:
        return {"service": "tgi", "models": [data.get("model_id")], "auth_required": False}
    return None


def m_open_webui(status, headers, text, data):
    if "open webui" in (text or "").lower():
        return {"service": "open-webui", "models": [], "auth_required": False}
    return None


def m_gradio(status, headers, text, data):
    if status == 200 and isinstance(data, dict) and (
            "components" in data or "gradio" in json.dumps(data).lower()):
        return {"service": "gradio", "models": [], "auth_required": False}
    return None


# recipe: (port, path, matcher). Read-only GET on each.
RECIPES = [
    (11434, "/api/tags", m_ollama_tags),
    (11434, "/", m_ollama_root),
    (8000, "/v1/models", m_openai_models),
    (1234, "/v1/models", m_openai_models),
    (8080, "/v1/models", m_openai_models),
    (8080, "/info", m_tgi_info),
    (5000, "/v1/models", m_openai_models),
    (3000, "/", m_open_webui),
    (7860, "/config", m_gradio),
]


def iter_hosts(scope):
    """Hosts to probe. CIDR ranges are NOT expanded (no mass scanning — red line)."""
    import scope as scopemod
    hosts = []
    seen = set()
    for entry in scope.get("targets", []):
        if "://" not in entry and "/" in entry:
            continue  # CIDR/range: skipped on purpose (probe explicit hosts only)
        h, _ = scopemod.host_port(entry)
        if h and h not in seen:
            seen.add(h)
            hosts.append(h)
    return hosts


def _fetch(url, timeout):
    if requests is None:
        raise RuntimeError("requests not installed; install from requirements.txt")
    try:
        r = requests.get(url, timeout=timeout)
        try:
            data = r.json()
        except Exception:
            data = None
        return r.status_code, dict(r.headers), r.text[:2000], data
    except Exception:
        return None


def probe_host(host, scope, timeout=4):
    """Read-only probe of one authorized host across the recipe ports. Returns inventory entries."""
    import scope as scopemod
    found = {}
    for port, path, matcher in RECIPES:
        if not scopemod.in_scope(f"{host}:{port}", scope):
            continue  # this port is not authorized
        url = f"http://{host}:{port}{path}"
        resp = _fetch(url, timeout)
        if resp is None:
            continue
        hit = matcher(*resp)
        if hit:
            key = (host, port)
            # keep the richest hit per host:port (prefer one that lists models)
            if key not in found or (hit.get("models") and not found[key].get("models")):
                found[key] = {"target": f"http://{host}:{port}", "host": host, "port": port, **hit}
    return list(found.values())


def run(scope_path, out_path: Path, timeout=4):
    import scope as scopemod
    scope = scopemod.load_scope(scope_path)
    inventory = []
    for host in iter_hosts(scope):
        inventory.extend(probe_host(host, scope, timeout=timeout))
    out_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False), encoding="utf8")
    print(f"Wrote {out_path} ({len(inventory)} services)")
    for e in inventory:
        print(f"  {e['target']:<32} {e['service']:<18} models={e.get('models')} "
              f"auth={e.get('auth_required')}")
    return inventory


def self_test() -> int:
    """Validate fingerprint matchers offline (no network)."""
    assert m_ollama_tags(200, {}, "", {"models": [{"name": "llama3"}, {"name": "mistral"}]}) == {
        "service": "ollama", "models": ["llama3", "mistral"], "auth_required": False}
    assert m_ollama_root(200, {}, "Ollama is running", None)["service"] == "ollama"
    ov = m_openai_models(200, {"server": "uvicorn"}, "", {"data": [{"id": "gpt-x"}]})
    assert ov["service"] == "vllm" and ov["models"] == ["gpt-x"]
    assert m_openai_models(200, {}, "", {"data": [{"id": "m1"}]})["service"] == "openai-compatible"
    assert m_openai_models(401, {}, "", None)["auth_required"] is True
    assert m_tgi_info(200, {}, "", {"model_id": "bigscience/bloom"})["models"] == ["bigscience/bloom"]
    assert m_open_webui(200, {}, "<title>Open WebUI</title>", None)["service"] == "open-webui"
    assert m_gradio(200, {}, "", {"components": []})["service"] == "gradio"
    # negatives
    assert m_ollama_tags(200, {}, "", {"foo": 1}) is None
    assert m_openai_models(404, {}, "", None) is None
    print("discover self-test OK")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scope", default="scope.yaml", help="Path to scope.yaml (RoE)")
    ap.add_argument("--out", default="inventory.json")
    ap.add_argument("--timeout", type=int, default=4)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        sys.exit(self_test())
    run(args.scope, Path(args.out), timeout=args.timeout)


if __name__ == "__main__":
    main()
