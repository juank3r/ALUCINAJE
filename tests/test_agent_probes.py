"""Offline tests for the agent attack suite detectors + aggregation (no network)."""
import importlib.util
import unittest
from pathlib import Path

_P = Path(__file__).resolve().parent.parent / "tools" / "agent_probes.py"
_spec = importlib.util.spec_from_file_location("agent_probes", _P)
ap = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ap)


class TestMarkers(unittest.TestCase):
    def test_markers_derive(self):
        m = ap.markers("CANARY-X")
        self.assertEqual(m["canary"], "CANARY-X")
        self.assertIn("CANARY-X", m["secret"])
        self.assertIn("CANARY-X", m["sink"])


class TestDetectors(unittest.TestCase):
    def test_each_probe_detects_and_ignores(self):
        self.assertEqual(ap.self_test(), 0)  # runs all detector asserts internally

    def test_exfil_requires_both_sink_and_secret(self):
        m = ap.markers("Z")
        det = next(p for p in ap.PROBES if p["id"] == "secret_exfiltration")["detect"]
        # only the sink, no secret -> not a real exfil
        self.assertFalse(det(f"visit {m['sink']} now", m["canary"], m["secret"], m["sink"]))
        self.assertTrue(det(f"{m['sink']}?d={m['secret']}", m["canary"], m["secret"], m["sink"]))


class TestAggregate(unittest.TestCase):
    def test_mixed(self):
        results = [
            {"id": "direct_injection", "owasp": "A1", "severity": "medium", "success": True},
            {"id": "indirect_injection", "owasp": "A1i", "severity": "high", "success": False},
            {"id": "secret_exfiltration", "owasp": "LLM06", "severity": "critical", "success": True},
            {"id": "tool_misuse", "owasp": "A2", "severity": "high", "success": False},
        ]
        agg = ap.aggregate(results)
        self.assertEqual(agg["findings"], 2)
        self.assertEqual(agg["injection_success_rate"], 0.5)
        self.assertTrue(agg["exfil_channel"])
        self.assertEqual(agg["max_severity"], "critical")
        self.assertFalse(agg["tool_misuse"])


if __name__ == "__main__":
    unittest.main()
