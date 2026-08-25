"""Offline tests for connectors request-building and response-parsing (no network)."""
import importlib.util
import unittest
from pathlib import Path

_P = Path(__file__).resolve().parent.parent / "tools" / "connectors.py"
_spec = importlib.util.spec_from_file_location("connectors", _P)
conn = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(conn)


class TestBuildRequest(unittest.TestCase):
    def test_ollama(self):
        url, headers, payload = conn.build_request("ollama", "http://h:11434/", "hi", model="m")
        self.assertTrue(url.endswith("/api/generate"))
        self.assertEqual(payload["model"], "m")
        self.assertEqual(payload["prompt"], "hi")
        self.assertFalse(payload["stream"])

    def test_openai_auth(self):
        url, headers, payload = conn.build_request("openai", "http://h:8000", "hi", api_key="k")
        self.assertTrue(url.endswith("/v1/chat/completions"))
        self.assertEqual(headers["Authorization"], "Bearer k")
        self.assertEqual(payload["messages"][0]["content"], "hi")

    def test_anthropic(self):
        url, headers, payload = conn.build_request("anthropic", "http://h", "hi", api_key="k")
        self.assertTrue(url.endswith("/v1/messages"))
        self.assertEqual(headers["x-api-key"], "k")
        self.assertIn("anthropic-version", headers)

    def test_generic(self):
        url, headers, payload = conn.build_request("generic", "http://h/infer", "hi")
        self.assertEqual(url, "http://h/infer")
        self.assertEqual(payload, {"input": "hi"})


class TestParseResponse(unittest.TestCase):
    def test_parsers(self):
        self.assertEqual(conn.parse_response("ollama", {"response": "x"}), "x")
        self.assertEqual(conn.parse_response("openai",
                         {"choices": [{"message": {"content": "y"}}]}), "y")
        self.assertEqual(conn.parse_response("anthropic", {"content": [{"text": "z"}]}), "z")
        self.assertEqual(conn.parse_response("generic", {"response": "g"}), "g")

    def test_parse_is_graceful(self):
        self.assertEqual(conn.parse_response("openai", {}), "")
        self.assertEqual(conn.parse_response("anthropic", {"content": []}), "")


if __name__ == "__main__":
    unittest.main()
