"""Offline tests for the discovery scanner fingerprints + scope gating (no real network)."""
import importlib.util
import unittest
from pathlib import Path

_P = Path(__file__).resolve().parent.parent / "tools" / "discover.py"
_spec = importlib.util.spec_from_file_location("discover", _P)
disc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(disc)


class TestMatchers(unittest.TestCase):
    def test_self_test(self):
        self.assertEqual(disc.self_test(), 0)  # exercises every matcher (positive + negative)


class TestIterHosts(unittest.TestCase):
    def test_dedup_and_skip_cidr(self):
        scope = {"targets": ["127.0.0.1", "127.0.0.1:8000", "https://h.test:11434", "10.0.0.0/24"]}
        self.assertEqual(disc.iter_hosts(scope), ["127.0.0.1", "h.test"])


class TestProbeHost(unittest.TestCase):
    def setUp(self):
        self._orig = disc._fetch
        self.calls = {}

        def fake_fetch(url, timeout):
            self.calls[url] = self.calls.get(url, 0) + 1
            if url == "http://127.0.0.1:11434/api/tags":
                return (200, {}, "", {"models": [{"name": "llama3"}]})
            if url == "http://127.0.0.1:8000/v1/models":
                return (200, {"server": "uvicorn"}, "", {"data": [{"id": "x"}]})
            return None
        disc._fetch = fake_fetch

    def tearDown(self):
        disc._fetch = self._orig

    def test_bare_host_probes_all_ports(self):
        inv = disc.probe_host("127.0.0.1", {"targets": ["127.0.0.1"]})
        services = sorted(e["service"] for e in inv)
        self.assertIn("ollama", services)
        self.assertIn("vllm", services)

    def test_port_scope_gating(self):
        inv = disc.probe_host("127.0.0.1", {"targets": ["127.0.0.1:11434"]})
        self.assertEqual([e["service"] for e in inv], ["ollama"])
        # the un-authorized 8000 port must never be fetched
        self.assertNotIn("http://127.0.0.1:8000/v1/models", self.calls)


if __name__ == "__main__":
    unittest.main()
