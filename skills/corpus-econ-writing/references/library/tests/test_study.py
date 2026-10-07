"""Data-free contract tests for the writing database and its evidence checks."""
import copy
import contextlib
import hashlib
import importlib.util
import json
import io
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("study", Path(__file__).resolve().parents[1] / "scripts/study.py")
study = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(study)

class StudyTests(unittest.TestCase):
    def setUp(self):
        self.papers = [{"id": "P01", "title": "An example", "year": 2026,
                        "source_url": "https://example.org/paper.pdf", "source_sha256": "a" * 64,
                        "main_pages": [2, 4], "included_pages": [1, 5], "read_pages": [2, 3],
                        "visual_inspected": True, "visual_page": 3, "visual_observation": "Readable table",
                        "synthesis": "A mechanism is explained.", "quotations": []}]
        self.observations = [{"id": "P01-01", "paper_id": "P01", "pdf_page": 2,
                              "area": "theory", "finding": "The result is interpreted.",
                              "page_sha256": "b" * 64, "source_sha256": "a" * 64}]
        self.rules = [{"id": "W001", "area": "theory", "instruction": "Interpret a result.", "evidence": ["P01-01"]}]
        self.lexicon = [{"id": "lex-income", "term": "income", "category": "object",
                         "meaning": "A flow", "guardrail": "State units", "original_example": "Income rises."}]

    def validate(self):
        study.validate(self.papers, self.observations, self.rules, self.lexicon)

    def test_valid_records(self):
        self.validate()

    def test_duplicate_ids(self):
        for records in (self.papers, self.observations, self.rules, self.lexicon):
            with self.subTest(records=records[0]["id"]):
                records.append(copy.deepcopy(records[0]))
                with self.assertRaisesRegex(ValueError, "Duplicate"):
                    self.validate()
                records.pop()

    def test_duplicate_dictionary_term(self):
        self.lexicon.append({**self.lexicon[0], "id": "lex-second"})
        with self.assertRaisesRegex(ValueError, "dictionary terms"):
            self.validate()

    def test_invalid_main_boundary(self):
        self.papers[0]["main_pages"] = [0, 4]
        with self.assertRaisesRegex(ValueError, "main-page"):
            self.validate()

    def test_unreviewed_observation(self):
        self.observations[0]["pdf_page"] = 4
        with self.assertRaisesRegex(ValueError, "manual page review"):
            self.validate()

    def test_unknown_paper(self):
        self.observations[0]["paper_id"] = "missing"
        with self.assertRaisesRegex(ValueError, "Unknown paper"):
            self.validate()

    def test_broken_rule_link(self):
        self.rules[0]["evidence"] = ["missing"]
        with self.assertRaisesRegex(ValueError, "Broken rule"):
            self.validate()

    def test_empty_evidence(self):
        self.rules[0]["evidence"] = []
        with self.assertRaisesRegex(ValueError, "Broken rule"):
            self.validate()

    def test_invalid_hash(self):
        self.observations[0]["page_sha256"] = "made-up"
        with self.assertRaisesRegex(ValueError, "evidence hash"):
            self.validate()

    def test_wrong_source_hash(self):
        self.observations[0]["source_sha256"] = "c" * 64
        with self.assertRaisesRegex(ValueError, "Wrong source"):
            self.validate()

    def test_quote_requires_new_policy(self):
        self.papers[0]["quotations"] = ["Example"]
        with self.assertRaisesRegex(ValueError, "no reproduced"):
            self.validate()

    def test_missing_visual_review(self):
        self.papers[0]["visual_inspected"] = False
        with self.assertRaisesRegex(ValueError, "review evidence"):
            self.validate()

    def test_empty_visual_assessment(self):
        self.papers[0]["visual_observation"] = " "
        with self.assertRaisesRegex(ValueError, "visual assessment"):
            self.validate()

    def test_page_outside_source(self):
        self.papers[0]["read_pages"] = [0, 2]
        with self.assertRaisesRegex(ValueError, "outside source"):
            self.validate()

    def test_visual_outside_source(self):
        self.papers[0]["visual_page"] = 9
        with self.assertRaisesRegex(ValueError, "Visual page"):
            self.validate()

    def test_literal_matching_boundaries_and_hyphenation(self):
        pages = [{"pdf_page": 7, "text": "An equi-\nlibrium, equilibria, and equilibrium."}]
        self.assertEqual(study.phrase_pages("equilibrium", pages), [{"pdf_page": 7, "count": 2}])
        self.assertEqual(study.phrase_pages("librium", pages), [])

    def test_literal_matching_diacritics(self):
        self.assertEqual(study.normalize("Fr\u00e9chet"), "frechet")
        self.assertEqual(study.phrase_pages("price index", [{"pdf_page": 1, "text": "Price-index and price indexes"}]), [{"pdf_page": 1, "count": 1}])

    def test_changed_and_missing_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "data").mkdir()
            path = root / "sample.txt"
            path.write_text("Reviewed text")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            (root / "data/review_inputs.json").write_text(json.dumps({"files": {"sample.txt": digest}}))
            study.verify_evidence(root)
            path.write_text("Different text")
            with self.assertRaisesRegex(ValueError, "Changed reviewed"):
                study.verify_evidence(root)
            path.unlink()
            with self.assertRaises(FileNotFoundError):
                study.verify_evidence(root)

    def test_manifest_path_traversal(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "data").mkdir()
            (root / "data/review_inputs.json").write_text(json.dumps({"files": {"../outside.txt": "a" * 64}}))
            with self.assertRaisesRegex(ValueError, "Invalid evidence path"):
                study.verify_evidence(root)

    def test_incomplete_manifest(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "data").mkdir()
            (root / "data/review_inputs.json").write_text(json.dumps({"files": {}}))
            with self.assertRaisesRegex(ValueError, "Incomplete"):
                study.verify_evidence(root, ["sample.txt"])

    def test_database_integrity_and_search(self):
        data = {"papers": self.papers, "observations": self.observations, "rules": self.rules,
                "dictionary": self.lexicon, "literal_frequencies": []}
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "test.sqlite"
            study.write_database(path, data)
            with sqlite3.connect(path) as db:
                self.assertEqual(db.execute("PRAGMA integrity_check").fetchone()[0], "ok")
                self.assertEqual(db.execute("PRAGMA foreign_key_check").fetchall(), [])
                self.assertEqual(db.execute("SELECT count(*) FROM search WHERE search MATCH 'interpreted'").fetchone()[0], 1)
                self.assertEqual(db.execute("SELECT count(*) FROM rule_evidence").fetchone()[0], 1)

    def test_search_relocated_without_corpus(self):
        data = {"papers": self.papers, "observations": self.observations, "rules": self.rules,
                "dictionary": self.lexicon, "literal_frequencies": []}
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "database").mkdir()
            study.write_database(root / "database/writing_database.sqlite", data)
            output = io.StringIO()
            with patch.object(study, "ROOT", root), contextlib.redirect_stdout(output):
                study.search("interpreted", 5)
            self.assertIn("P01-01 (observation)", output.getvalue())
            self.assertFalse((root / "sources").exists())

if __name__ == "__main__":
    unittest.main()
