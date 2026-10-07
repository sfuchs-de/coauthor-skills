import importlib.util
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location("vocabulary", SCRIPTS / "vocabulary.py")
v = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(v)

class VocabularyTests(unittest.TestCase):
    def build_sample(self):
        papers = [{"id": "P01", "main_pages": [1, 2]}]
        pages = {"P01": [{"pdf_page": 1, "text": "Income rises. Prices and prices affect income. Fr\u00e9chet choices. First-order valuation. Expen-\nditure changes expenditure. Oneunbrokenword."},
                         {"pdf_page": 2, "text": "Residents buy services.\nREFERENCES\nBibliographyonlyword."},
                         {"pdf_page": 3, "text": "Supplementonlyword and unverifiedfrag-\nment."}]}
        words, occurrences = v.index_pages(papers, pages)
        return {w["word"]: w for w in words}, occurrences

    def test_every_page_including_references(self):
        words, _ = self.build_sample()
        self.assertEqual(words["bibliographyonlyword"]["status"], "other_pages_attested")
        self.assertEqual(words["supplementonlyword"]["main_count"], 0)

    def test_occurrence_totals(self):
        words, occurrences = self.build_sample()
        for word, item in words.items():
            self.assertEqual(item["full_count"], sum(o["count"] for o in occurrences if o["word"] == word))

    def test_verified_linebreak_join(self):
        words, _ = self.build_sample()
        self.assertEqual(words["expenditure"]["full_count"], 2)
        self.assertNotIn("expen", words)

    def test_unverified_linebreak_not_licensed(self):
        words, _ = self.build_sample()
        self.assertEqual(words["unverifiedfrag"]["status"], "extraction_fragment")
        self.assertNotIn("unverifiedfragment", words)

    def test_compound_and_components(self):
        words, _ = self.build_sample()
        self.assertEqual(words["first-order"]["kind"], "compound")
        self.assertIn("first", words)
        self.assertIn("order", words)

    def test_case_accent_and_apostrophe_normalization(self):
        self.assertEqual(v.canonical("FR\u00c9CHET"), "frechet")
        self.assertEqual(v.canonical("workers\u2019"), "workers'")

    def test_no_free_inflections(self):
        words, _ = self.build_sample()
        result = v.inspect_prose("Prices change incomes.", ".txt", words, {"exceptions": []})
        self.assertIn("incomes", [i["word"] for i in result["unapproved_terms"]])

    def test_new_compound_flagged(self):
        words, _ = self.build_sample()
        result = v.inspect_prose("Income-prices.", ".txt", words, {"exceptions": []})
        self.assertEqual(result["unapproved_terms"][0]["word"], "income-prices")

    def test_reference_only_is_reviewed_not_invented(self):
        words, _ = self.build_sample()
        result = v.inspect_prose("Bibliographyonlyword.", ".txt", words, {"exceptions": []})
        self.assertTrue(result["lexical_gate_passed"])
        self.assertEqual(result["context_review"][0]["status"], "other_pages_attested")

    def test_exception_requires_necessity(self):
        with self.assertRaisesRegex(ValueError, "necessity"):
            v.exceptions_from({"exceptions": [{"term": "newterm", "status": "approved"}]})

    def test_pending_exception_not_approved(self):
        self.assertEqual(v.exceptions_from({"exceptions": [{"term": "newterm", "status": "pending"}]}), {})

    def test_duplicate_exception(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            v.exceptions_from({"exceptions": [{"term": "newterm"}, {"term": "newterm"}]})

    def test_approved_exception(self):
        words, _ = self.build_sample()
        policy = {"exceptions": [{"term": "newterm", "status": "approved", "necessity": "Named source", "why_no_attested_alternative": "Official name", "approved_by": "Author"}]}
        result = v.inspect_prose("newterm", ".txt", words, policy)
        self.assertTrue(result["lexical_gate_passed"])
        self.assertEqual(result["approved_exceptions_used"], ["newterm"])

    def test_tex_preserves_prose_excludes_math_refs_comments(self):
        cleaned = v.prose_text("\\section{Income}\nPrices $inventedmath$ \\citep{inventedkey}. % inventedcomment\n\\footnote{Residents buy services.}", ".tex")
        self.assertIn("Residents buy services", cleaned)
        for excluded in ("inventedmath", "inventedkey", "inventedcomment", "section", "footnote"):
            self.assertNotIn(excluded, cleaned)

    def test_markdown_preserves_label_excludes_code_url(self):
        cleaned = v.prose_text("[Income](https://example.com/invented) `inventedcode`\n```\ninventedblock\n```", ".md")
        self.assertIn("Income", cleaned)
        self.assertNotIn("invented", cleaned)

    def test_line_numbers_preserved(self):
        words, _ = self.build_sample()
        result = v.inspect_prose("Income $unknown$\n\\footnote{zzzzunattested}", ".tex", words, {"exceptions": []})
        self.assertEqual(result["unapproved_terms"][0]["lines"], [2])

if __name__ == "__main__":
    unittest.main()
