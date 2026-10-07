#!/usr/bin/env python3
"""Audit analysis links and the generated database without network access."""
import ast
import csv
import hashlib
import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]

def main():
    receipt_path = ROOT / "database/QUALITY_RECEIPT.json"
    data = json.loads((ROOT / "database/writing_database.json").read_text())
    known_observations = {item["id"] for item in data["observations"]}
    known_rules = {item["id"] for item in data["rules"]}
    missing_links, unknown_ids = [], []
    checked_links = 0
    markdowns = list(ROOT.glob("*.md")) + list((ROOT / "reviews").glob("*.md")) + list((ROOT / "vocabulary").glob("*.md"))
    for path in markdowns:
        text = path.read_text()
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
            if urlsplit(target).scheme or target.startswith("#"):
                continue
            local = unquote(target.split("#", 1)[0])
            checked_links += 1
            if not (path.parent / local).exists() and (path.parent / local).resolve() != receipt_path:
                missing_links.append({"file": str(path.relative_to(ROOT)), "target": target})
        for ident in re.findall(r"\b(?:[DAKR]\d{2}-\d{2}|W\d{3})\b", text):
            if ident not in known_observations and ident not in known_rules:
                unknown_ids.append({"file": str(path.relative_to(ROOT)), "id": ident})
    if missing_links or unknown_ids:
        raise ValueError(json.dumps({"missing_links": missing_links, "unknown_ids": unknown_ids}))
    python_files = list((ROOT / "scripts").glob("*.py")) + list((ROOT / "tests").glob("*.py"))
    for path in python_files:
        ast.parse(path.read_text(), filename=str(path))
    with sqlite3.connect(f"file:{ROOT / 'database/writing_database.sqlite'}?mode=ro", uri=True) as db:
        integrity = db.execute("PRAGMA integrity_check").fetchone()[0]
        foreign_keys = db.execute("PRAGMA foreign_key_check").fetchall()
        expected = {"papers": len(data["papers"]), "observations": len(data["observations"]),
                    "rules": len(data["rules"]), "dictionary": len(data["dictionary"]),
                    "literal_frequency": len(data["literal_frequencies"]),
                    "rule_evidence": sum(len(rule["evidence"]) for rule in data["rules"])}
        counts = {table: db.execute(f"SELECT count(*) FROM {table}").fetchone()[0] for table in expected}
        expected_search = sum(expected[key] for key in ("papers", "observations", "rules", "dictionary"))
        actual_search = db.execute("SELECT count(*) FROM search").fetchone()[0]
        if integrity != "ok" or foreign_keys or counts != expected or expected_search != actual_search:
            raise ValueError("Database integrity, cross-export counts, or search coverage failed")
        searches = {query: db.execute("SELECT count(*) FROM search WHERE search MATCH ?", (query,)).fetchone()[0]
                    for query in ('envelop*', '"fixed effects"', 'normalization', 'robustness')}
        if not all(searches.values()):
            raise ValueError("An expected writing topic is absent from search")
    csv_tables = {"papers": "papers.csv", "observations": "observations.csv", "rules": "rules.csv",
                  "dictionary": "dictionary.csv", "literal_frequency": "literal_frequencies.csv"}
    csv_counts = {}
    for table, filename in csv_tables.items():
        with (ROOT / "database" / filename).open(newline="") as handle:
            csv_counts[table] = sum(1 for _ in csv.DictReader(handle))
        if csv_counts[table] != counts[table]:
            raise ValueError(f"CSV count mismatch: {filename}")
    test_run = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
                              cwd=ROOT, capture_output=True, text=True, timeout=60)
    if test_run.returncode:
        raise ValueError(f"Unit tests failed:\n{test_run.stdout}\n{test_run.stderr}")
    test_count = re.search(r"Ran (\d+) tests?", test_run.stderr)
    if not test_count:
        raise ValueError("Unit suite did not report an executed test count")
    unit_tests = {"executed": int(test_count.group(1)), "exit_code": test_run.returncode,
                  "suite_output": test_run.stdout + test_run.stderr}
    vocabulary_checks = {}
    for fixture, expected_code, expected_pass in (("vocabulary_pass.txt", 0, True), ("vocabulary_fail.txt", 1, False)):
        outcome = subprocess.run([sys.executable, "scripts/vocabulary.py", "check", f"tests/fixtures/{fixture}", "--strict"],
                                 cwd=ROOT, capture_output=True, text=True, timeout=60)
        details = json.loads(outcome.stdout)
        if outcome.returncode != expected_code or details["lexical_gate_passed"] != expected_pass:
            raise ValueError(f"Vocabulary strict-gate integration failed: {fixture}")
        vocabulary_checks[fixture] = {"exit_code": outcome.returncode, "report": details}
    verified_vocabulary = subprocess.run([sys.executable, "scripts/vocabulary.py", "verify"],
                                        cwd=ROOT, capture_output=True, text=True, timeout=60)
    if verified_vocabulary.returncode:
        raise ValueError(f"Vocabulary verification failed: {verified_vocabulary.stderr}")
    vocabulary_verification = json.loads(verified_vocabulary.stdout)
    portable_files = markdowns + python_files + list((ROOT / "data").glob("*")) + list((ROOT / "database").glob("*.csv"))
    portable_files += [ROOT / "database/writing_database.json", ROOT / "database/writing_database.sqlite"]
    hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in sorted(portable_files) if path.is_file()}
    receipt = {"sqlite_integrity": integrity, "foreign_key_errors": foreign_keys,
               "table_counts": counts, "csv_counts": csv_counts, "unit_tests": unit_tests,
               "vocabulary_cli_checks": vocabulary_checks, "vocabulary_verification": vocabulary_verification,
               "search_rows": actual_search, "search_topic_hits": searches,
               "local_markdown_links_checked": checked_links, "missing_local_links": missing_links,
               "unknown_evidence_ids": unknown_ids, "python_files_parsed": len(python_files),
               "network_used_by_quality_check": False, "analysis_file_sha256": hashes}
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({key: value for key, value in receipt.items()
                      if key not in ("analysis_file_sha256", "unit_tests")}, indent=2))
    print(f"Executed {unit_tests['executed']} unit tests: PASS")

if __name__ == "__main__":
    main()
