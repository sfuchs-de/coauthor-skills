import importlib.util
import json
import math
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import edition
import audit


class CorpusExtensionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.words = edition.records()
        cls.policy = edition.load(edition.BASE / "data/vocabulary_policy.json")

    def test_exact_paper_support(self):
        with sqlite3.connect(ROOT / "vocabulary/attested_vocabulary.sqlite") as db:
            ids = {p for p, in db.execute("SELECT DISTINCT paper_id FROM occurrences")}
        self.assertEqual(len(ids), 31)
        self.assertIn("R10", ids)

    def test_new_word_requires_page_attestation(self):
        self.assertEqual(self.words["afford"]["status"], "main_text_attested")
        with sqlite3.connect(ROOT / "vocabulary/attested_vocabulary.sqlite") as db:
            self.assertIn(("R09", 7), db.execute("SELECT paper_id,pdf_page FROM occurrences WHERE word='afford'").fetchall())

    def test_unknown_form_rejected(self):
        result = edition.vocabulary.inspect_prose("zzzznewunattestedword", ".tex", self.words, self.policy)
        self.assertFalse(result["lexical_gate_passed"])

    def test_no_free_inflections(self):
        result = edition.vocabulary.inspect_prose("affordzzzz", ".tex", self.words, self.policy)
        self.assertFalse(result["lexical_gate_passed"])

    def test_no_new_exceptions(self):
        self.assertEqual(self.policy["exceptions"], [])

    def test_duplicate_json_key_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "duplicate.json"
            path.write_text('{"term":1,"term":2}')
            with self.assertRaises(ValueError):
                edition.load(path)

    def test_changed_brief_rejected(self):
        frozen = edition.load(ROOT / "evaluation/FREEZE_RECEIPT.json")
        def changed(path):
            if path.name == "FREEZE_RECEIPT.json":
                return {**frozen, "cases_sha256": "incorrect"}
            return json.loads(path.read_text())
        with patch.object(edition, "load", side_effect=changed):
            with self.assertRaises(ValueError):
                audit.check_freeze()

    def test_changed_instructions_rejected(self):
        with patch.object(audit, "instruction_hashes", return_value={"incorrect": "hash"}):
            with self.assertRaises(ValueError):
                audit.check_freeze()

    def test_first_drafts_preserved(self):
        audit.check_freeze()

    def test_every_checked_case_bound_to_hash(self):
        receipt = edition.load(ROOT / "evaluation/CHECKED_AUDIT.json")
        for ident, row in receipt["cases"].items():
            self.assertEqual(edition.digest(ROOT / "evaluation/samples" / f"{ident}.tex"), row["sha256"])
            self.assertTrue(row["lexical"]["lexical_gate_passed"])
            self.assertTrue(row["length_passed"])
            self.assertEqual(row["exact_12_word_match_pages"], [])

    def test_study_page_anchors(self):
        config = {p["id"]: p for p in edition.load(ROOT / "data/sources.json")["papers"]}
        analysis = edition.load(ROOT / "data/analysis.json")
        self.assertEqual(len(analysis["cards"]), 8)
        self.assertEqual(sum(len(c["observations"]) for c in analysis["cards"]), 48)
        self.assertEqual(len(analysis["usage"]), 36)
        for card in analysis["cards"]:
            self.assertIn(card["id"], config)
            for page, _, _ in card["observations"]:
                self.assertIn(page, card["read_pages"])

    def test_searchable_study(self):
        with sqlite3.connect(ROOT / "analysis/analysis.sqlite") as db:
            self.assertGreater(db.execute("SELECT count(*) FROM search WHERE search MATCH 'normalization'").fetchone()[0], 0)

    def test_short_examples_bound_to_current_guide(self):
        receipt = edition.load(ROOT / "evaluation/EXAMPLE_AUDIT.json")
        self.assertEqual(edition.digest(ROOT / "WORKED_EXAMPLES.md"), receipt["worked_examples_sha256"])
        self.assertEqual(len(receipt["examples"]), 10)
        for row in receipt["examples"].values():
            self.assertTrue(row["lexical"]["lexical_gate_passed"])
            self.assertEqual(row["exact_12_word_match_pages"], [])

    def test_ratings_bound_to_checked_samples(self):
        summary = edition.load(ROOT / "evaluation/SUMMARY.json")
        self.assertEqual(summary["ratings_sha256"], edition.digest(ROOT / "evaluation/RATINGS.json"))
        self.assertFalse(summary["independent_review"])
        for ident, row in summary["cases"].items():
            self.assertEqual(row["sample_sha256"], edition.digest(ROOT / "evaluation/samples" / f"{ident}.tex"))
        self.assertAlmostEqual(summary["equal_case_mean_self_rating_10"],
            sum(row["self_rating_10"] for row in summary["cases"].values()) / 4)

    def test_changed_vocabulary_hash_rejected(self):
        original = edition.load
        def changed(path):
            record = original(path)
            if path == ROOT / "vocabulary/BUILD_RECEIPT.json":
                record["output_sha256"]["attested_vocabulary.sqlite"] = "incorrect"
            return record
        with patch.object(edition, "load", side_effect=changed):
            with self.assertRaisesRegex(ValueError, "Changed vocabulary database"):
                edition.records()


class MathematicalFixtureTests(unittest.TestCase):
    def test_producer_envelope_independent_example(self):
        # F(L0,x)=sqrt(L0)+sqrt(x), x*=p^2/(4r^2): a fixture, not a new paper model.
        p, r, labor, delta = 2.0, 3.0, 4.0, 1e-5
        value = lambda price: price * math.sqrt(labor) + price**2 / (4*r)
        output = math.sqrt(labor) + p/(2*r)
        derivative = (value(p+delta)-value(p-delta))/(2*delta)
        self.assertAlmostEqual(derivative, output, places=9)
        self.assertAlmostEqual(value(p+delta)-value(p)-output*delta, delta**2/(4*r), places=14)

    def test_household_envelope_and_budget_geometry(self):
        p, r, labor, h, outside, delta = 2.0, 3.0, 4.0, 0.3, 10.0, 1e-5
        income = lambda price: outside + h * (price*math.sqrt(labor)+price**2/(4*r))
        v0 = income(p)
        initial_c = v0/(2*p)  # Independent log-utility fixture, not imposed in L01.
        output = math.sqrt(labor)+p/(2*r)
        ev = lambda price: income(price)*math.sqrt(p/price)-v0
        derivative = (ev(p+delta)-ev(p-delta))/(2*delta)
        geometry = h*output-initial_c
        self.assertAlmostEqual(derivative, geometry, places=8)
        errors = [abs(ev(p+d)-geometry*d) for d in (1e-3, 5e-4)]
        self.assertTrue(3.8 < errors[0]/errors[1] < 4.2)

    def test_inverse_does_not_imply_feedback_convergence(self):
        feedback = 1.2
        self.assertNotEqual(1-feedback, 0)
        inverse = 1/(1-feedback)
        self.assertTrue(math.isfinite(inverse))
        self.assertGreater(sum(feedback**t for t in range(30)), sum(feedback**t for t in range(10)))

    def test_fictional_income_cost_and_tax_units(self):
        self.assertAlmostEqual(3.2-1.6, 1.6)
        self.assertAlmostEqual(2.4-1.6, .8)
        self.assertAlmostEqual(-.5-1.6, -2.1)
        self.assertAlmostEqual(.34-.30, .04)
        self.assertNotAlmostEqual((.34-.30)/.30*100, .04)

    def test_ranks_do_not_determine_sign(self):
        positive = [1, 2, 3]
        negative = [-3, -2, -1]
        self.assertEqual(sorted(range(3), key=positive.__getitem__), sorted(range(3), key=negative.__getitem__))
        self.assertGreater(sum(positive), 0)
        self.assertLess(sum(negative), 0)


if __name__ == "__main__":
    unittest.main()
