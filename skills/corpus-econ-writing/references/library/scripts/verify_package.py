#!/usr/bin/env python3
"""Verify a source-free library or its self-contained skill package."""
import argparse
import csv
import hashlib
import json
import platform
import re
import sqlite3
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest() if hasattr(hashlib, "file_digest") else hashlib.sha256(stream.read()).hexdigest()


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicate_keys)


def safe_file(root, name):
    relative = Path(name)
    if not name or relative.is_absolute() or ".." in relative.parts or "\\" in name:
        raise ValueError(f"Unsafe manifest path: {name}")
    candidate = root.resolve()
    for part in relative.parts:
        candidate = candidate / part
        if candidate.is_symlink():
            raise ValueError(f"Symlink is not a frozen artifact: {name}")
    if not candidate.is_file():
        raise ValueError(f"Missing package file: {name}")
    return candidate


def verify_manifest(root):
    manifest = read_json(root / "PACKAGE_MANIFEST.json")
    if manifest.get("schema_version") != 1 or not manifest.get("files"):
        raise ValueError("Missing or incompatible package manifest")
    for name, record in manifest["files"].items():
        path = safe_file(root, name)
        if path.stat().st_size != record["size"] or digest(path) != record["sha256"]:
            raise ValueError(f"Changed package file: {name}")
    expected = set(manifest["files"]) | {"PACKAGE_MANIFEST.json"}
    actual = set()
    for path in root.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"Symlink in package: {path.relative_to(root)}")
        if "__pycache__" in path.parts:
            continue
        if path.is_file():
            actual.add(path.relative_to(root).as_posix())
    if actual != expected:
        raise ValueError(f"Unexpected or missing package files: {sorted(actual ^ expected)}")
    return manifest


def verify_links(root):
    checked = 0
    for path in root.rglob("*.md"):
        text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
        for target in re.findall(r"\]\(([^)]+)\)", text):
            target = target.strip("<>")
            if not target or target.startswith("#") or urlsplit(target).scheme:
                continue
            candidate = (path.parent / unquote(target.split("#", 1)[0])).resolve()
            if not candidate.is_relative_to(root.resolve()) or not candidate.exists():
                raise ValueError(f"Broken/outside Markdown link: {path.relative_to(root)} -> {target}")
            checked += 1
    return checked


def csv_count(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def require_equal(actual, expected, label):
    if actual != expected:
        raise ValueError(f"{label}: {actual!r} != {expected!r}")


def verify_data(library):
    analysis = read_json(library / "database/writing_database.json")
    receipt = read_json(library / "database/BUILD_RECEIPT.json")
    counts = receipt["counts"]
    with sqlite3.connect((library / "database/writing_database.sqlite").as_uri() + "?mode=ro", uri=True) as db:
        require_equal(db.execute("PRAGMA integrity_check").fetchone()[0], "ok", "Analysis integrity")
        require_equal(db.execute("PRAGMA foreign_key_check").fetchall(), [], "Analysis foreign keys")
        for table, key, filename in (("papers", "papers", "papers.csv"), ("observations", "observations", "observations.csv"),
                                     ("rules", "rules", "rules.csv"), ("dictionary", "dictionary_entries", "dictionary.csv"),
                                     ("literal_frequency", "literal_frequency_records", "literal_frequencies.csv")):
            require_equal(db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0], counts[key], table)
            json_key = "literal_frequencies" if table == "literal_frequency" else table
            require_equal(len(analysis[json_key]), counts[key], f"JSON {table}")
            require_equal(csv_count(library / "database" / filename), counts[key], f"CSV {table}")
        require_equal(db.execute("SELECT COUNT(*) FROM rule_evidence e LEFT JOIN observations o ON o.id=e.observation_id WHERE o.id IS NULL").fetchone()[0], 0, "Rule links")
        search_hits = db.execute("SELECT COUNT(*) FROM search WHERE search MATCH 'income'").fetchone()[0]
        if not search_hits:
            raise ValueError("Analysis FTS5 search returned no income evidence")
    vocabulary = read_json(library / "vocabulary/BUILD_RECEIPT.json")
    for name, expected in vocabulary["output_sha256"].items():
        require_equal(digest(safe_file(library, "vocabulary/" + name)), expected, f"Frozen vocabulary {name}")
    for name, expected in vocabulary["input_sha256"].items():
        if name != "data/extraction.json":
            require_equal(digest(safe_file(library, name)), expected, f"Frozen input {name}")
    word_data = read_json(library / "vocabulary/attested_vocabulary.json")
    vcounts = vocabulary["counts"]
    require_equal(word_data["counts"], vcounts, "Vocabulary JSON counts")
    require_equal(len(word_data["words"]), vcounts["normalized_forms"], "Vocabulary JSON forms")
    require_equal(len(word_data["occurrences"]), vcounts["source_page_records"], "Vocabulary JSON occurrences")
    require_equal(csv_count(library / "vocabulary/words.csv"), vcounts["normalized_forms"], "Vocabulary CSV forms")
    require_equal(csv_count(library / "vocabulary/occurrences.csv"), vcounts["source_page_records"], "Vocabulary CSV occurrences")
    with sqlite3.connect((library / "vocabulary/attested_vocabulary.sqlite").as_uri() + "?mode=ro", uri=True) as db:
        require_equal(db.execute("PRAGMA integrity_check").fetchone()[0], "ok", "Vocabulary integrity")
        require_equal(db.execute("PRAGMA foreign_key_check").fetchall(), [], "Vocabulary foreign keys")
        require_equal(db.execute("SELECT COUNT(*) FROM words").fetchone()[0], vcounts["normalized_forms"], "SQL forms")
        require_equal(db.execute("SELECT COUNT(*) FROM occurrences").fetchone()[0], vcounts["source_page_records"], "SQL occurrences")
        require_equal(dict(db.execute("SELECT status,COUNT(*) FROM words GROUP BY status")), vcounts["status_counts"], "SQL statuses")
        require_equal(db.execute("SELECT COUNT(*) FROM words w LEFT JOIN (SELECT word,SUM(count) AS total FROM occurrences GROUP BY word) o ON w.word=o.word WHERE w.full_count != o.total OR o.total IS NULL").fetchone()[0], 0, "Occurrence totals")
        known = {row[0] for row in db.execute("SELECT DISTINCT paper_id FROM occurrences")}
        require_equal(known, {p["id"] for p in analysis["papers"]}, "Vocabulary source IDs")
    return {"analysis_counts": counts, "vocabulary_counts": vcounts, "fts5_hits": search_hits}


def run_command(args, cwd, expected=0):
    result = subprocess.run([sys.executable, *map(str, args)], cwd=cwd, capture_output=True, text=True, timeout=120)
    if result.returncode != expected:
        raise ValueError(f"Unexpected exit {result.returncode} for {args[0]}: {result.stderr[-3000:]}")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write a verification receipt outside the immutable package")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.output and args.output.resolve().is_relative_to(root):
        parser.error("Write receipts outside the frozen package")
    manifest = verify_manifest(root)
    library = root / "references/library" if (root / "SKILL.md").exists() else root
    if library != root:
        verify_manifest(library)
    data = verify_data(library)
    links = verify_links(root)
    tests = run_command(["-B", "-m", "unittest", "discover", "-s", library / "tests", "-v"], root)
    match = re.search(r"Ran (\d+) tests", tests.stderr)
    if not match or int(match[1]) < 45:
        raise ValueError("Incomplete unit-test execution")
    fixtures = {}
    for name, code in (("vocabulary_pass", 0), ("vocabulary_fail", 1)):
        result = run_command(["-B", library / "scripts/vocabulary.py", "check", library / f"tests/fixtures/{name}.txt", "--strict"], root, code)
        report = json.loads(result.stdout)
        require_equal(report["lexical_gate_passed"], code == 0, name)
        fixtures[name] = {"exit_code": code, "checked_tokens": report["checked_tokens"], "unapproved_terms": report["unapproved_terms"]}
    lookup = run_command(["-B", library / "scripts/vocabulary.py", "lookup", "heterogeneity"], root)
    if '"word": "heterogeneity"' not in lookup.stdout:
        raise ValueError("Vocabulary lookup failed")
    summary = {"package_verified": True, "package_kind": manifest["kind"], "manifest_sha256": digest(root / "PACKAGE_MANIFEST.json"),
               "packaged_files_checked": len(manifest["files"]), "local_links_checked": links,
               "unit_tests_passed": int(match[1]), "strict_fixtures": fixtures, **data,
               "environment": {"python": platform.python_version(), "sqlite": sqlite3.sqlite_version},
               "source_pdf_checks_rerun": False, "network_required": False,
               "limits": "Artifact integrity and checker behavior only; not a repeated source review, semantic audit, or independent collaborator test."}
    rendered = json.dumps(summary, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
