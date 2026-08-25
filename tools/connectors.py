#!/usr/bin/env python3
"""Endpoint connectors for red-team evaluation.

Provides one `query(target, prompt, service=...)` that speaks the API of the target service and
returns a normalized `{response, status, latency_ms}`. Request-building and response-parsing are
pure functions so they can be unit-tested offline (no network).

Scope enforcement is the CALLER's responsibility: check `tools/scope.require_in_scope(target, scope)`
before calling `query()`. This module never talks to a target that the caller has not authorized.
"""
import time

try:
    import requests
except Exception:  # pragma: no cover - optional for offline unit tests
    requests = None

SERVICES = ("generic", "ollama", "openai", "anthropic")

DEFAULT_MODEL = {
    "ollama": "llama3",
    "openai": "gpt-3.5-turbo",
    "anthropic": "claude-3-5-sonnet-20241022",
}


def build_request(service, base, prompt, model=None, api_key=None):
    """Return (url, headers, json_payload) for the given service. Pure function."""
    base = (base or "").rstrip("/")
    if service == "ollama":
        return (base + "/api/generate", {},
                {"model": model or DEFAULT_MODEL["ollama"], "prompt": prompt, "stream": False})
    if service == "openai":
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        return (base + "/v1/chat/completions", headers,
                {"model": model or DEFAULT_MODEL["openai"],
                 "messages": [{"role": "user", "content": prompt}]})
    if service == "anthropic":
        headers = {"x-api-key": api_key or "", "anthropic-version": "2023-06-01",
                   "content-type": "application/json"}
        return (base + "/v1/messages", headers,
                {"model": model or DEFAULT_MODEL["anthropic"], "max_tokens": 1024,
                 "messages": [{"role": "user", "content": prompt}]})
    # generic: the framework's default {"input": ...} -> {"response": ...}
    return (base, {}, {"input": prompt})


def parse_response(service, data):
    """Extract the assistant text from a service's JSON response. Pure function; never raises."""
    try:
        if service == "ollama":
            return data.get("response", "")
        if service == "openai":
            return data["choices"][0]["message"]["content"]
        if service == "anthropic":
            return data["content"][0]["text"]
        return data.get("response", "")
    except Exception:
        return ""


def query(target, prompt, service="generic", model=None, api_key=None, timeout=30):
    """Send one prompt to `target` and return {response, status, latency_ms}.

    Caller MUST have enforced scope before calling this.
    """
    if requests is None:
        raise RuntimeError("requests not installed; install from requirements.txt")
    url, headers, payload = build_request(service, target, prompt, model, api_key)
    start = time.time()
    try:
        r = requests.post(url, json=payload, headers=headers or None, timeout=timeout)
        r.raise_for_status()
        text = parse_response(service, r.json())
        return {"response": text, "status": "ok", "latency_ms": int((time.time() - start) * 1000)}
    except Exception as e:  # pragma: no cover - network dependent
        return {"response": "", "status": f"error: {e}",
                "latency_ms": int((time.time() - start) * 1000)}
