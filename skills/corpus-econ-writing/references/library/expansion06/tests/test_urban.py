import contextlib
import io
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT / "scripts"))
import edition
import audit_examples


class UrbanExtension(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config=edition.load(ROOT / "data/sources.json")
        cls.study=edition.load(ROOT / "data/analysis.json")
        cls.receipt=edition.load(ROOT / "vocabulary/BUILD_RECEIPT.json")
        cls.audit=edition.load(ROOT / "evaluation/CHECKED_AUDIT.json")
        cls.records=edition.helpers.records()

    def test_01_combined_support(self):
        ids=[p["id"] for p in edition.all_papers()]
        self.assertEqual(len(ids),53)
        self.assertEqual(len(set(ids)),53)

    def test_02_urban_support(self):
        self.assertEqual({p["id"] for p in self.config["papers"]},{f"U{i:02d}" for i in range(1,9)})

    def test_03_opt_in(self):
        self.assertIn("opt-in",self.config["activation"])
        self.assertIn("default remains edition05",self.config["activation"])

    def test_04_versions(self):
        self.assertFalse(any("to be checked" in p["version"] for p in self.config["papers"]))
        self.assertTrue(all(p["main_pages"][1]>p["main_pages"][0] for p in self.config["papers"]))

    def test_05_counts(self):
        self.assertEqual(self.receipt["counts"],{"papers":53,"new_papers":8,"included_pages":2930,
            "new_pages":513,"normalized_forms":23589,"attested_writing_forms":22108,
            "new_attested_forms":2254,"source_page_records":525402})

    def test_06_source_owner(self):
        self.assertEqual(edition.source_root("R01"),edition.BASE)
        self.assertEqual(edition.source_root("R10"),edition.PRIOR04)
        self.assertEqual(edition.source_root("W01"),edition.PRIOR05)
        self.assertEqual(edition.source_root("U01"),edition.ROOT)

    def test_07_previous_freeze(self):
        edition.verify_previous()

    def test_08_inventory_delta(self):
        with sqlite3.connect(edition.PRIOR05 / "vocabulary/attested_vocabulary.sqlite") as db:
            old={w for w,s in db.execute("SELECT word,status FROM words") if s.endswith("attested")}
        new={w for w,r in self.records.items() if r["status"].endswith("attested")}
        self.assertEqual(len(new-old),2254)
        self.assertFalse(old-new)

    def test_09_inherited_exclusion(self):
        prior=edition.load(edition.PRIOR05 / "vocabulary/BUILD_RECEIPT.json")
        self.assertEqual(self.receipt["index_exclusions"],prior["index_exclusions"])

    def test_10_source_hashes(self):
        self.assertEqual(set(self.receipt["new_source_hashes"]),{f"U{i:02d}" for i in range(1,9)})
        self.assertTrue(all(len(h)==64 for h in self.receipt["new_source_hashes"].values()))

    def test_11_study_support(self):
        self.assertEqual(sum(len(c["read_pages"]) for c in self.study["cards"]),55)
        self.assertEqual(sum(len(c["observations"]) for c in self.study["cards"]),32)
        for c in self.study["cards"]:
            self.assertIn(c["render_page"],c["read_pages"])
            self.assertTrue(all(o[0] in c["read_pages"] for o in c["observations"]))

    def test_12_usage_support(self):
        self.assertEqual(len(self.study["usage"]),24)
        for u in self.study["usage"]:
            ident,p=u["anchor"].split(":")
            self.assertIn(int(p),next(c["read_pages"] for c in self.study["cards"] if c["id"]==ident))

    def test_13_visual_support(self):
        observations=edition.load(ROOT / "data/visual_observations.json")
        self.assertEqual(len(observations["pages"]),8)
        actual={(p["paper"],p["pdf_page"]) for p in observations["pages"]}
        self.assertEqual(actual,{(c["id"],c["render_page"]) for c in self.study["cards"]})

    def test_14_six_repairs(self):
        replay=audit_examples.audit()
        self.assertEqual(len(replay["examples"]),6)
        for ident,result in replay["examples"].items():
            self.assertTrue(result["lexical"]["lexical_gate_passed"])
            self.assertEqual(result["text_sha256"],self.audit["examples"][ident]["text_sha256"])

    def test_15_overlap_record_not_replay(self):
        self.assertTrue(self.audit["source_screen_rerun"])
        self.assertTrue(all(r["exact_12_word_match_pages"]==[] for r in self.audit["examples"].values()))
        self.assertFalse(audit_examples.audit()["source_screen_rerun"])

    def test_16_first_failure_preserved(self):
        first=edition.load(ROOT / "evaluation/FIRST_AUDIT.json")
        self.assertEqual(sum(r["lexical"]["lexical_gate_passed"] for r in first["examples"].values()),5)

    def test_17_unknown_rejected(self):
        policy=edition.load(edition.BASE / "data/vocabulary_policy.json")
        self.assertFalse(edition.vocabulary.inspect_prose("zzzznewunattestedword",".tex",self.records,policy)["lexical_gate_passed"])

    def test_18_plain_prose_passes(self):
        policy=edition.load(edition.BASE / "data/vocabulary_policy.json")
        self.assertTrue(edition.vocabulary.inspect_prose("The model explains rents and income.",".tex",self.records,policy)["lexical_gate_passed"])

    def test_19_duplicate_keys_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary) / "duplicate.json"
            path.write_text('{"papers":[],"papers":[]}')
            with self.assertRaisesRegex(ValueError,"Duplicate"):
                edition.load(path)

    def test_20_full_offline_integrity(self):
        with contextlib.redirect_stdout(io.StringIO()): edition.verify()


if __name__=="__main__": unittest.main()
