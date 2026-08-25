"""Offline tests for the engagement report generator (tools/report.py)."""
import importlib.util
import unittest
from pathlib import Path

_P = Path(__file__).resolve().parent.parent / "tools" / "report.py"
_spec = importlib.util.spec_from_file_location("report", _P)
rep = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rep)


class TestBuildReport(unittest.TestCase):
    def test_counts_and_severity(self):
        evals = [{"dataset": "jbb", "metrics": {"attack_success_rate": 0.42}}]
        agents = [{"tool": "agent_probes", "results": [
            {"id": "secret_exfiltration", "owasp": "LLM06", "severity": "critical", "success": True},
            {"id": "direct_injection", "owasp": "A1", "severity": "medium", "success": True},
            {"id": "tool_misuse", "owasp": "A2", "severity": "high", "success": False},
        ]}]
        r = rep.build_report(evals, agents, inventory=[{"target": "t1"}])
        self.assertEqual(r["summary"]["findings"], 3)   # exfil + direct + llm_jailbreak
        self.assertEqual(r["summary"]["overall_severity"], "critical")
        self.assertEqual(r["findings"][0]["severity"], "critical")  # sorted desc
        self.assertEqual(r["summary"]["targets"], 1)

    def test_no_findings(self):
        evals = [{"dataset": "jbb", "metrics": {"attack_success_rate": 0.0}}]
        r = rep.build_report(evals, [], [])
        self.assertEqual(r["summary"]["findings"], 0)
        self.assertEqual(r["summary"]["overall_severity"], "none")

    def test_asr_below_threshold_no_finding(self):
        r = rep.build_report([{"dataset": "jbb", "metrics": {"attack_success_rate": 0.05}}], [], [])
        self.assertEqual(r["summary"]["findings"], 0)


class TestRenderHtml(unittest.TestCase):
    def test_html_contains_key_parts(self):
        r = rep.build_report([], [{"tool": "agent_probes", "results": [
            {"id": "tool_misuse", "owasp": "A2", "severity": "high", "success": True}]}], [])
        doc = rep.render_html(r)
        self.assertIn("Informe de red team", doc)
        self.assertIn("tool_misuse", doc)
        self.assertIn("<!doctype html>", doc)


class TestSelfTest(unittest.TestCase):
    def test_self_test(self):
        self.assertEqual(rep.self_test(), 0)


if __name__ == "__main__":
    unittest.main()
