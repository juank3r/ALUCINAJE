#!/usr/bin/env python3
"""Scope / Rules-of-Engagement gate.

Hard red line of the framework: NOTHING is discovered, connected to, or attacked unless the
target is explicitly authorized in `scope.yaml`. Out-of-scope targets are refused.

Usage:
  python tools/scope.py --show
  python tools/scope.py --check https://ollama.internal.acme.test:11434
"""
import argparse
import ipaddress
from pathlib import Path
from urllib.parse import urlparse

try:
    import yaml
except Exception:  # pragma: no cover - yaml resolved via requirements in CI
    yaml = None

DEFAULT_SCOPE = "scope.yaml"


def load_scope(path: str = DEFAULT_SCOPE) -> dict:
    p = Path(path)
    if not p.exists():
        raise SystemExit(f"No scope file '{path}'. Define authorized targets before running.")
    if yaml is None:
        raise SystemExit("PyYAML required to read the scope file: pip install pyyaml")
    data = yaml.safe_load(p.read_text(encoding="utf8")) or {}
    if not data.get("targets"):
        raise SystemExit("Scope has no 'targets' — refusing (nothing is authorized).")
    return data


def host_port(target: str):
    """Return (host, port) from a URL, host:port, or bare host/IP."""
    t = (target or "").strip()
    if "://" in t:
        u = urlparse(t)
        return u.hostname, u.port
    if t.count(":") == 1 and "/" not in t:
        h, _, p = t.partition(":")
        try:
            return h, int(p)
        except ValueError:
            return t, None
    return t, None


def _same_ip(a: str, b: str) -> bool:
    try:
        return ipaddress.ip_address(a) == ipaddress.ip_address(b)
    except ValueError:
        return False


def _matches(host: str, port, entry: str) -> bool:
    e = (entry or "").strip()
    if not host:
        return False
    # URL entry: match hostname (and port if the entry pins one)
    if "://" in e:
        eu = urlparse(e)
        if eu.hostname and eu.hostname.lower() == host.lower():
            if eu.port and port and eu.port != port:
                return False
            return True
        return False
    # CIDR entry: only meaningful for IP targets
    if "/" in e:
        try:
            return ipaddress.ip_address(host) in ipaddress.ip_network(e, strict=False)
        except ValueError:
            return False
    # host:port entry
    if e.count(":") == 1:
        eh, _, ep = e.partition(":")
        if eh.lower() != host.lower() and not _same_ip(eh, host):
            return False
        try:
            return port is None or int(ep) == port
        except ValueError:
            return True
    # bare host or IP: authorizes all ports on that host
    return _same_ip(e, host) or e.lower() == host.lower()


def in_scope(target: str, scope: dict) -> bool:
    host, port = host_port(target)
    return any(_matches(host, port, e) for e in scope.get("targets", []))


def require_in_scope(target: str, scope: dict) -> None:
    if not in_scope(target, scope):
        raise SystemExit(
            f"REFUSED: '{target}' is OUT OF SCOPE. Add it to scope.yaml with written authorization."
        )


def canary(scope: dict) -> str:
    return scope.get("canary", "ALUCINAJE-CANARY")


def main():
    ap = argparse.ArgumentParser(description="Scope / Rules-of-Engagement gate")
    ap.add_argument("--scope", default=DEFAULT_SCOPE)
    ap.add_argument("--check", help="Target to check (URL, host:port, or IP)")
    ap.add_argument("--show", action="store_true", help="Print engagement + authorized targets")
    args = ap.parse_args()
    scope = load_scope(args.scope)
    if args.show:
        print("engagement:", scope.get("engagement", {}))
        print("targets:", scope.get("targets"))
        print("canary:", canary(scope))
    if args.check:
        verdict = "IN SCOPE" if in_scope(args.check, scope) else "OUT OF SCOPE"
        print(f"{args.check}: {verdict}")


if __name__ == "__main__":
    main()
