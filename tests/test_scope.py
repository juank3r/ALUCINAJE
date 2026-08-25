"""Offline tests for the scope / RoE gate (tools/scope.py). No yaml file needed."""
import importlib.util
import unittest
from pathlib import Path

_P = Path(__file__).resolve().parent.parent / "tools" / "scope.py"
_spec = importlib.util.spec_from_file_location("scope", _P)
scope = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(scope)

SCOPE = {
    "canary": "CANARY-X",
    "targets": [
        "127.0.0.1",
        "10.0.0.0/24",
        "https://ollama.acme.test:11434",
        "host.local:8000",
    ],
}


class TestInScope(unittest.TestCase):
    def test_authorized(self):
        for t in [
            "127.0.0.1",
            "http://127.0.0.1:11434",
            "10.0.0.5",
            "10.0.0.200:8000",
            "https://ollama.acme.test:11434/api/generate",
            "host.local:8000",
        ]:
            with self.subTest(t=t):
                self.assertTrue(scope.in_scope(t, SCOPE))

    def test_refused(self):
        for t in [
            "10.0.1.5",                       # outside CIDR
            "https://ollama.acme.test:9999",  # wrong port on URL entry
            "host.local:9000",                # wrong port on host:port entry
            "evil.example.com",
            "192.168.1.1",
        ]:
            with self.subTest(t=t):
                self.assertFalse(scope.in_scope(t, SCOPE))

    def test_require_refuses_out_of_scope(self):
        with self.assertRaises(SystemExit):
            scope.require_in_scope("evil.example.com", SCOPE)

    def test_canary(self):
        self.assertEqual(scope.canary(SCOPE), "CANARY-X")


if __name__ == "__main__":
    unittest.main()
