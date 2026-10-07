import contextlib
import importlib.util
import io
import json
import sqlite3
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import edition
import audit_examples


class AuthorExtension(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = edition.load(ROOT / "data/sources.json")
        cls.analysis = edition.load(ROOT / "data/analysis.json")
        cls.receipt = edition.load(ROOT / "vocabulary/BUILD_RECEIPT.json")
        cls.audit = edition.load(ROOT / "evaluation/CHECKED_AUDIT.json")
        cls.records = edition.previous.records()

    def test_01_combined_ids(self):
        ids = [p["id"] for p in edition.all_papers()]
        self.assertEqual(len(ids), 45)
        self.assertEqual(len(set(ids)), 45)

    def test_02_added_ids(self):
        self.assertEqual(len(self.config["papers"]), 14)

    def test_03_author_counts(self):
        self.assertEqual({name:sum(p["index"] == name for p in self.config["papers"])
            for name in self.config["author_indexes"]}, {"kalouptsidi":4,"wong":4,"leibovici":4,"redding":2})

    def test_04_pinned_versions(self):
        self.assertFalse(any("pending" in p["version"] for p in self.config["papers"]))
        self.assertTrue(all(len(p["authors"]) > 0 for p in self.config["papers"]))

    def test_05_counts(self):
        self.assertEqual(self.receipt["counts"], {"papers":45,"new_papers":14,"included_pages":2417,
            "new_pages":699,"normalized_forms":21265,"attested_writing_forms":19854,
            "new_attested_forms":4002,"source_page_records":445232})

    def test_06_source_hash_support(self):
        expected = {p["id"] for p in self.config["papers"]}
        self.assertEqual(set(self.receipt["new_source_hashes"]), expected)
        self.assertEqual(set(self.receipt["new_extraction_hashes"]), expected)

    def test_07_previous_inventory_hash(self):
        self.assertEqual(self.receipt["previous_inventory_sha256"],
            edition.digest(edition.PREVIOUS / "vocabulary/attested_vocabulary.sqlite"))

    def test_08_exact_delta(self):
        with sqlite3.connect(edition.PREVIOUS / "vocabulary/attested_vocabulary.sqlite") as db:
            old = {w for w,s in db.execute("SELECT word,status FROM words") if s.endswith("attested")}
        current = {w for w,r in self.records.items() if r["status"].endswith("attested")}
        self.assertEqual(len(current - old), 4002)
        self.assertFalse(old - current)

    def test_09_exclusions_declared(self):
        self.assertEqual([(r["paper_id"],r["pdf_page"]) for r in self.receipt["index_exclusions"]], [("L04",1),("L04",2)])
        self.assertTrue(all(r["removed_characters"] > 0 and len(r["removed_utf8_sha256"]) == 64
                            for r in self.receipt["index_exclusions"]))

    def test_10_exclusion_retains_english(self):
        pages = {"L04":[{"pdf_page":1,"text":"English Qualite\u0301 de vie, productivite\u0301 des entreprises French    Albouy is also affiliated notes"},
                         {"pdf_page":2,"text":"Header pour les allophones, French 1. Introduction English"}]}
        filtered, _ = edition.index_pages(pages)
        self.assertNotIn("French", filtered["L04"][0]["text"])
        self.assertIn("notes", filtered["L04"][0]["text"])
        self.assertIn("Introduction English", filtered["L04"][1]["text"])
        self.assertIn("French", pages["L04"][0]["text"])

    def test_11_ambiguous_exclusion_rejected(self):
        with self.assertRaisesRegex(ValueError,"Ambiguous"):
            edition.index_pages({"L04":[{"text":"Qualité de vie, productivité des entreprises repeated Qualité de vie, productivité des entreprises    Albouy is also affiliated"}]})

    def test_12_reversed_exclusion_rejected(self):
        with self.assertRaisesRegex(ValueError,"Reversed"):
            edition.index_pages({"L04":[{"text":"    Albouy is also affiliated Qualité de vie, productivité des entreprises"}]})

    def test_13_observations(self):
        self.assertEqual(sum(len(c["observations"]) for c in self.analysis["cards"]), 56)

    def test_14_selected_pages(self):
        self.assertEqual(sum(len(c["read_pages"]) for c in self.analysis["cards"]), 83)
        self.assertTrue(all(c["render_page"] in c["read_pages"] for c in self.analysis["cards"]))

    def test_15_usage_anchors(self):
        self.assertEqual(len(self.analysis["usage"]), 28)
        for u in self.analysis["usage"]:
            ident,page = u["anchor"].split(":")
            card = next(c for c in self.analysis["cards"] if c["id"] == ident)
            self.assertIn(int(page), card["read_pages"])

    def test_16_visual_inspection(self):
        data = edition.load(ROOT / "data/visual_observations.json")
        self.assertEqual(len(data["pages"]), 14)
        self.assertEqual({p["paper"] for p in data["pages"]}, {p["id"] for p in self.config["papers"]})

    def test_17_searchable_study(self):
        with sqlite3.connect(ROOT / "analysis/analysis.sqlite") as db:
            self.assertEqual(db.execute("SELECT count(*) FROM observations").fetchone()[0], 56)
            self.assertEqual(db.execute("SELECT count(*) FROM usage").fetchone()[0], 28)
            self.assertGreater(db.execute("SELECT count(*) FROM search WHERE search MATCH 'identification'").fetchone()[0], 0)

    def test_18_no_new_exception(self):
        self.assertEqual(edition.load(edition.BASE / "data/vocabulary_policy.json")["exceptions"], [])

    def test_19_examples_pass(self):
        replay = audit_examples.audit()
        self.assertEqual(len(replay["examples"]), 6)
        self.assertTrue(all(r["lexical"]["lexical_gate_passed"] for r in replay["examples"].values()))

    def test_20_example_hashes(self):
        replay = audit_examples.audit()
        self.assertEqual(replay["worked_examples_sha256"], self.audit["worked_examples_sha256"])
        self.assertEqual({k:r["text_sha256"] for k,r in replay["examples"].items()},
                         {k:r["text_sha256"] for k,r in self.audit["examples"].items()})

    def test_21_overlap_evidence_not_rerun(self):
        self.assertTrue(self.audit["source_screen_rerun"])
        self.assertTrue(all(r["exact_12_word_match_pages"] == [] for r in self.audit["examples"].values()))
        self.assertFalse(audit_examples.audit()["source_screen_rerun"])

    def test_22_unknown_rejected(self):
        result = edition.vocabulary.inspect_prose("zzzznewunattestedword", ".tex", self.records,
            edition.load(edition.BASE / "data/vocabulary_policy.json"))
        self.assertFalse(result["lexical_gate_passed"])

    def test_23_plain_passage(self):
        result = edition.vocabulary.inspect_prose("The model explains income and prices.", ".tex", self.records,
            edition.load(edition.BASE / "data/vocabulary_policy.json"))
        self.assertTrue(result["lexical_gate_passed"])

    def test_24_integrated_verification(self):
        with contextlib.redirect_stdout(io.StringIO()):
            edition.verify()


if __name__ == "__main__":
    unittest.main()
