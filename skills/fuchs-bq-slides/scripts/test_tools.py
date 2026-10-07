#!/usr/bin/env python3
"""Focused behavior tests; compiled slides still require separate visual QA."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from pypdf import PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, FloatObject, NameObject, TextStringObject

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("audit_deck", HERE / "audit_deck.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class ToolTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def fixture(self, broken_link=False):
        pdf = self.root / "test.pdf"
        writer = PdfWriter()
        for _ in range(2):
            writer.add_blank_page(width=453.543, height=255.118)
        writer.add_named_destination("bq_main_end", 0)
        writer.add_named_destination("backup", 1)
        link = DictionaryObject({
            NameObject("/Type"): NameObject("/Annot"),
            NameObject("/Subtype"): NameObject("/Link"),
            NameObject("/Rect"): ArrayObject([FloatObject(n) for n in [2, 2, 20, 10]]),
            NameObject("/A"): DictionaryObject({
                NameObject("/S"): NameObject("/GoTo"),
                NameObject("/D"): TextStringObject("missing" if broken_link else "backup"),
            }),
        })
        writer.add_annotation(0, link)
        writer.write(pdf)
        pdf.with_suffix(".nav").write_text(
            "\\beamer@framepages {1}{1}\n\\beamer@framepages {2}{2}\n")
        pdf.with_suffix(".log").write_text("Output written on test.pdf (2 pages).\n")
        ledger = self.root / "slides.json"
        ledger.write_text(json.dumps({"slides": [{"label": "bq_main_end", "role": "main",
            "minutes": 1.5, "job": "Summarize", "sources": ["test fixture"],
            "backup_labels": ["backup"]}]}))
        return pdf, ledger

    def test_valid_counts_links_and_timing(self):
        pdf, ledger = self.fixture()
        report, rows = audit.check(pdf, ledger)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["main_pdf_pages"], 1)
        self.assertEqual(report["planned_minutes"], 1.5)
        self.assertEqual(report["internal_links"], 1)
        self.assertEqual(rows[1]["section"], "backup")

    def test_broken_destination_is_rejected(self):
        pdf, ledger = self.fixture(broken_link=True)
        report, _ = audit.check(pdf, ledger)
        self.assertFalse(report["automated_checks_passed"])
        self.assertTrue(any("unknown destination" in error for error in report["errors"]))

    def test_overflow_and_missing_nav_are_not_passes(self):
        pdf, ledger = self.fixture()
        pdf.with_suffix(".log").write_text("Overfull \\vbox (20pt too high)\n")
        pdf.with_suffix(".nav").unlink()
        report, _ = audit.check(pdf, ledger)
        self.assertGreaterEqual(len(report["errors"]), 2)

    def test_duplicate_ledger_and_bad_time_are_rejected(self):
        pdf, ledger = self.fixture()
        data = json.loads(ledger.read_text())
        data["slides"][0]["minutes"] = -1
        data["slides"].append(data["slides"][0].copy())
        ledger.write_text(json.dumps(data))
        report, _ = audit.check(pdf, ledger)
        self.assertTrue(any("duplicate ledger" in error for error in report["errors"]))
        self.assertTrue(any("speaking time" in error for error in report["errors"]))

    def test_initializer_copies_assets_and_refuses_overwrite(self):
        destination = self.root / "new-deck"
        command = [sys.executable, str(HERE / "init_deck.py"), str(destination)]
        first = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertTrue((destination / "bq-theme.sty").is_file())
        sentinel = destination / "deck.tex"
        sentinel.write_text("User edit must survive\n")
        second = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(second.returncode, 0)
        self.assertEqual(sentinel.read_text(), "User edit must survive\n")


if __name__ == "__main__":
    unittest.main()
