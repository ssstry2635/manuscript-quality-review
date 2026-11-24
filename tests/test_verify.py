import sys
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "scripts"))
import verify
from evidence import anchor, inventory, load

class VerificationTests(unittest.TestCase):
    def setUp(self):
        self.examples = PROJECT / "examples"
        self.model = load(self.examples / "input.json")

    def test_a_quote_on_the_wrong_line_fails(self):
        sources, _ = inventory(self.examples, self.model["sources"])
        with self.assertRaisesRegex(ValueError, "Quote absent"):
            anchor({"source_id": "doc", "start": 1, "end": 1,
                    "quote": "a phrase never present"}, sources)

    def test_source_hash_detects_a_changed_file(self):
        self.model["sources"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            inventory(self.examples, self.model["sources"])

    def test_conflict_scope_and_missing_reference_are_distinct(self):
        report = verify.audit(self.model, self.examples)
        self.assertEqual([r["status"] for r in report["comparisons"]],
                         ["numeric_discrepancy", "scope_review_required"])
        self.assertEqual(report["comparisons"][1]["different_scope_fields"], ["population"])
        self.assertEqual(report["citations"][0]["status"], "pending")

    def test_rounding_overlap_is_compatible(self):
        self.model["claims"][0].update(value="12", places=0)
        self.model["claims"][1].update(value="12.4", places=1)
        self.assertEqual(verify.audit(self.model, self.examples)["comparisons"][0]["status"],
                         "rounding_compatible")

    def test_confirmed_finding_needs_evidence(self):
        self.model["findings"][0]["anchors"] = []
        with self.assertRaisesRegex(ValueError, "needs evidence"):
            verify.audit(self.model, self.examples)
