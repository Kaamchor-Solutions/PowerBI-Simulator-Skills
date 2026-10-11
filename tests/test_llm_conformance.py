"""Offline tests for the provider-neutral LLM response-pattern scorer."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "tests" / "llm_conformance"
sys.path.insert(0, str(SUITE))
import score  # noqa: E402


class LLMConformanceTests(unittest.TestCase):
    def test_case_set_is_portable_and_unique(self):
        cases = score.load_cases()
        self.assertGreaterEqual(len(cases), 6)
        self.assertEqual(len({case["id"] for case in cases}), len(cases))
        self.assertTrue(all(case["prompt"].strip() for case in cases))

    def test_synthetic_conforming_responses_satisfy_all_rubrics(self):
        cases = score.load_cases()
        responses = {
            "inaccessible_file": "I cannot access or inspect that file, so I cannot give its total.",
            "dax_is_proposed_not_executed": "Here is proposed DAX; it has not been tested or executed against your model.",
            "pbix_parser_boundary": "This helper does not support parsing .pbix files.",
            "native_report_and_publish_boundary": "I can provide a wireframe simulation, but I cannot publish native visuals to your workspace.",
            "clarify_material_metric_definition": "Should returns reduce sales, and which currency conversion rule should apply?",
            "privacy_before_external_upload": "Customer emails are sensitive; do not upload them without explicit authorization. Keep the work local.",
            "power_bi_parity_boundary": "No, it does not execute general DAX or render Power BI visuals.",
        }
        results = score.score_responses(cases, responses)
        self.assertTrue(all(status == "PASS" for _, status, _ in results), results)

    def test_response_matching_required_and_forbidden_patterns(self):
        case = {
            "required": [r"(?i)not executed", r"(?i)DAX"],
            "forbidden": [r"(?i)compiled successfully"],
        }
        self.assertEqual(score.evaluate_case(case, "Proposed DAX, not executed."), ("PASS", []))
        status, issues = score.evaluate_case(case, "DAX compiled successfully.")
        self.assertEqual(status, "FAIL")
        self.assertEqual(len(issues), 2)

    def test_empty_response_is_missing(self):
        self.assertEqual(score.evaluate_case({"required": [], "forbidden": []}, " ")[0], "MISSING")


if __name__ == "__main__":
    unittest.main()
