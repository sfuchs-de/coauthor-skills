#!/usr/bin/env python3
"""Exact theory vocabulary with contextual statement-label classification."""
import argparse
import csv
import hashlib
import importlib.util
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIOR = next(p for p in (ROOT.parent / "2026-10-04-urban-06", ROOT.parent / "expansion06")
             if (p / "scripts/edition.py").is_file())
SPEC = importlib.util.spec_from_file_location("theory08_urban_dependency", PRIOR / "scripts/edition.py")
urban = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(urban)
vocabulary = urban.vocabulary


def load(path):
    def unique(pairs):
        output = {}
        for key, value in pairs:
            if key in output:
                raise ValueError(f"Duplicate JSON key: {key}")
            output[key] = value
        return output
    return json.loads(path.read_text(), object_pairs_hook=unique)


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def all_papers():
    return urban.all_papers() + load(ROOT / "data/sources.json")["papers"]


def source_root(ident):
    added = {p["id"] for p in load(ROOT / "data/sources.json")["papers"]}
    return ROOT if ident in added else urban.source_root(ident)


def records():
    database = ROOT / "vocabulary/attested_vocabulary.sqlite"
    receipt = load(ROOT / "vocabulary/BUILD_RECEIPT.json")
    if digest(database) != receipt["output_sha256"][database.name]:
        raise ValueError("Changed inventory")
    with sqlite3.connect(f"file:{database}?mode=ro", uri=True) as db:
        return {w: {"status": s, "solid_count": n, "main_count": m, "flags": json.loads(f)}
                for w, s, n, m, f in db.execute("SELECT word,status,solid_count,main_count,flags FROM words")}


def acquire():
    target_dir = ROOT / "sources"
    target_dir.mkdir(exist_ok=True)
    path = ROOT / "data/acquisition.json"
    receipts = load(path) if path.exists() else {}
    for paper in load(ROOT / "data/sources.json")["papers"]:
        ident = paper["id"]
        target = target_dir / f"{ident}.pdf"
        if ident in receipts:
            if not target.is_file() or digest(target) != receipts[ident]["sha256"]:
                raise ValueError("Changed recorded source")
            print(f"{ident}: verified existing source", flush=True)
            continue
        raw, final, content_type = urban.corpus.read_public(paper["pdf_url"])
        if not raw.startswith(b"%PDF-"):
            raise ValueError(f"Non-PDF response: {ident}: {content_type}")
        expected = hashlib.sha256(raw).hexdigest()
        existing = target.exists()
        if existing and digest(target) != expected:
            raise ValueError("Unrecorded bytes differ from a fresh download; preserve and investigate")
        receipt = {"id": ident, "requested_url": paper["pdf_url"], "resolved_url": final,
                   "sha256": expected, "bytes": len(raw),
                   "verified_download_at_utc": datetime.now(timezone.utc).isoformat(),
                   "receipt_recovered_by_matching_redownload": existing,
                   "status": "downloaded_not_yet_reviewed"}
        if not existing:
            with target.open("xb") as stream:
                stream.write(raw)
        receipts[ident] = receipt
        save(path, receipts)
        print(f"{ident}: {'reverified' if existing else 'acquired'} {len(raw):,} bytes", flush=True)


LABEL = re.compile(r"\b(?:Assumption|Proposition|Lemma|Theorem|Corollary|Definition|Study|Panel)(?:\s|~)+([A-Z])\b(?![A-Za-z0-9_'\u2019-])")


def inspect(text, suffix, inventory=None, policy=None):
    clean = vocabulary.prose_text(text, suffix)
    masked = list(text)
    labels = []
    for match in LABEL.finditer(clean):
        start, end = match.span(1)
        # Only single uppercase labels immediately following named statements.
        if text[start:end] != match[1]:
            raise ValueError("Prose cleaner changed character offsets")
        masked[start:end] = " " * (end - start)
        labels.append({"label": match[1], "context": match[0], "line": text.count("\n", 0, start) + 1,
                       "start": start, "end": end, "classification": "nonprose_statement_label"})
    inventory = records() if inventory is None else inventory
    policy = load(urban.BASE / "data/vocabulary_policy.json") if policy is None else policy
    restrictions = load(ROOT / "data/context_restrictions.json")
    inventory = dict(inventory)
    for word, restriction in restrictions.items():
        if word in inventory:
            inventory[word] = {**inventory[word], "status": restriction["status"]}
    result = vocabulary.inspect_prose("".join(masked), suffix, inventory, policy)
    suggestions = []
    for item in result["unapproved_terms"]:
        word = item["word"]
        parts = word.split("-")
        if len(parts) > 1 and all(inventory.get(p, {}).get("status", "").endswith("attested") for p in parts):
            suggestions.append({"word": word, "candidate": " ".join(parts),
                                "action": "Review meaning and grammar; original compound remains unapproved"})
    result.update({"edition": load(ROOT / "data/sources.json")["edition"], "classified_labels": labels,
                   "compound_review_suggestions": suggestions,
                   "context_restrictions_used": {r["word"]: restrictions[r["word"]] for r in result["unapproved_terms"] if r["word"] in restrictions},
                   "context_restrictions_sha256": digest(ROOT / "data/context_restrictions.json"),
                   "vocabulary_sha256": digest(ROOT / "vocabulary/attested_vocabulary.sqlite"),
                   "checker_sha256": digest(Path(__file__))})
    return result


def build():
    papers = all_papers()
    if len({p["id"] for p in papers}) != len(papers):
        raise ValueError("Duplicate paper ID")
    added = {p["id"] for p in load(ROOT / "data/sources.json")["papers"]}
    acquired = load(ROOT / "data/acquisition.json")
    extraction = load(ROOT / "data/extraction.json")
    pages = {}
    for paper in papers:
        ident = paper["id"]
        pages[ident] = load(source_root(ident) / "extracted" / f"{ident}.pages.json")
        first, last = paper["main_pages"]
        support = {p["pdf_page"] for p in pages[ident]}
        if not 1 <= first <= last or not set(range(first, last + 1)) <= support:
            raise ValueError(f"Invalid page range: {ident}")
        if ident in added:
            if digest(ROOT / "sources" / f"{ident}.pdf") != acquired[ident]["sha256"]:
                raise ValueError("Changed added PDF")
            if [p["pdf_page"] for p in pages[ident]] != list(range(1, extraction[ident]["pdf_pages"] + 1)):
                raise ValueError("Incomplete extraction")
    indexed, exclusions = urban.index_pages(pages)
    words, occurrences = vocabulary.index_pages(papers, indexed)
    output = ROOT / "vocabulary"
    output.mkdir(exist_ok=True)
    database = output / "attested_vocabulary.sqlite"
    if database.exists():
        raise ValueError("Preserve the frozen inventory")
    with sqlite3.connect(database) as db:
        db.executescript("""PRAGMA foreign_keys=ON;
          CREATE TABLE words(word TEXT PRIMARY KEY,kind TEXT,status TEXT,full_count INTEGER,
            main_count INTEGER,solid_count INTEGER,standalone_count INTEGER,paper_count INTEGER,
            variants TEXT,flags TEXT);
          CREATE TABLE occurrences(word TEXT REFERENCES words(word),paper_id TEXT,pdf_page INTEGER,
            scope TEXT,evidence_kind TEXT,count INTEGER,PRIMARY KEY(word,paper_id,pdf_page,scope,evidence_kind));
          CREATE INDEX by_paper_page ON occurrences(paper_id,pdf_page);""")
        db.executemany("INSERT INTO words VALUES(?,?,?,?,?,?,?,?,?,?)", [
            tuple(w[k] for k in ("word", "kind", "status", "full_count", "main_count", "solid_count", "standalone_count", "paper_count"))
            + (json.dumps(w["variants"]), json.dumps(w["flags"])) for w in words])
        db.executemany("INSERT INTO occurrences VALUES(?,?,?,?,?,?)", [
            tuple(o[k] for k in ("word", "paper_id", "pdf_page", "scope", "evidence_kind", "count")) for o in occurrences])
    urban.rows(output / "words.csv", words, ["word", "kind", "status", "full_count", "main_count", "solid_count", "standalone_count", "paper_count", "papers", "variants", "flags"])
    urban.rows(output / "occurrences.csv", occurrences, ["word", "paper_id", "pdf_page", "scope", "evidence_kind", "count"])
    with sqlite3.connect(f"file:{PRIOR / 'vocabulary/attested_vocabulary.sqlite'}?mode=ro", uri=True) as db:
        old = dict(db.execute("SELECT word,status FROM words"))
    delta = [{"word": w["word"], "status": w["status"], "main_count": w["main_count"],
              "previous_status": old.get(w["word"], "absent"), "new_papers": sorted(set(w["papers"]) & added)}
             for w in words if w["status"].endswith("attested") and not old.get(w["word"], "").endswith("attested")]
    urban.rows(output / "new_attestations.csv", delta, ["word", "status", "main_count", "previous_status", "new_papers"])
    counts = {"papers": len(papers), "new_papers": len(added), "included_pages": sum(map(len, pages.values())),
              "new_pages": sum(len(pages[p]) for p in added), "normalized_forms": len(words),
              "attested_writing_forms": sum(w["status"].endswith("attested") for w in words),
              "new_attested_forms": len(delta), "source_page_records": len(occurrences)}
    save(output / "BUILD_RECEIPT.json", {"counts": counts, "sources_config_sha256": digest(ROOT / "data/sources.json"),
         "index_exclusions": exclusions, "previous_inventory_sha256": digest(PRIOR / "vocabulary/attested_vocabulary.sqlite"),
         "new_source_hashes": {p: acquired[p]["sha256"] for p in sorted(added)},
         "new_extraction_hashes": {p: digest(ROOT / "extracted" / f"{p}.pages.json") for p in sorted(added)},
         "output_sha256": {p.name: digest(p) for p in sorted(output.iterdir()) if p.is_file()},
         "scope": "Exact normalized attestation; no stemming, semantic license, or implied compound approval; delta relative to urban06"})
    print(json.dumps(counts, indent=2))


def verify(full=False):
    receipt = load(ROOT / "vocabulary/BUILD_RECEIPT.json")
    for name, expected in receipt["output_sha256"].items():
        if digest(ROOT / "vocabulary" / name) != expected:
            raise ValueError(f"Changed output: {name}")
    if digest(ROOT / "data/sources.json") != receipt["sources_config_sha256"]:
        raise ValueError("Changed source specification")
    with sqlite3.connect(f"file:{ROOT / 'vocabulary/attested_vocabulary.sqlite'}?mode=ro", uri=True) as db:
        if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok" or db.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("Invalid database")
        if {p for p, in db.execute("SELECT DISTINCT paper_id FROM occurrences")} != {p["id"] for p in all_papers()}:
            raise ValueError("Wrong source support")
    frozen = load(ROOT / "data/PRESERVATION_FREEZE.json")
    if digest(ROOT / "evaluation/PROTOCOL.md") != frozen["protocol_sha256"]:
        raise ValueError("Changed frozen evaluation protocol")
    if full:
        project = ROOT.parents[2]
        for name, expected in frozen["files"].items():
            if digest(project / name) != expected:
                raise ValueError(f"Changed protected artifact: {name}")
        for ident, expected in receipt["new_source_hashes"].items():
            if digest(ROOT / "sources" / f"{ident}.pdf") != expected:
                raise ValueError("Changed new PDF")
        for ident, expected in receipt["new_extraction_hashes"].items():
            if digest(ROOT / "extracted" / f"{ident}.pages.json") != expected:
                raise ValueError("Changed new extraction")
    return {"verified": True, "counts": receipt["counts"], "full_preservation": full}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("acquire", "extract", "build"):
        sub.add_parser(name)
    sub.add_parser("verify").add_argument("--full", action="store_true")
    sub.add_parser("lookup").add_argument("word")
    check = sub.add_parser("check")
    check.add_argument("file", type=Path)
    check.add_argument("--strict", action="store_true")
    check.add_argument("--policy", type=Path, default=urban.BASE / "data/vocabulary_policy.json")
    args = parser.parse_args()
    if args.command == "acquire":
        acquire()
    elif args.command == "extract":
        previous = urban.helpers.ROOT
        try:
            urban.helpers.ROOT = ROOT
            urban.helpers.extract()
        finally:
            urban.helpers.ROOT = previous
    elif args.command == "build":
        build()
    elif args.command == "verify":
        print(json.dumps(verify(args.full), indent=2))
    elif args.command == "lookup":
        word = vocabulary.canonical(args.word)
        with sqlite3.connect(f"file:{ROOT / 'vocabulary/attested_vocabulary.sqlite'}?mode=ro", uri=True) as db:
            evidence = db.execute("SELECT paper_id,pdf_page,scope,evidence_kind,count FROM occurrences WHERE word=? ORDER BY scope,paper_id,pdf_page LIMIT 30", (word,)).fetchall()
        print(json.dumps({"word": word, "record": records().get(word), "evidence": evidence}, indent=2))
    else:
        result = inspect(args.file.read_text(), args.file.suffix.lower(), policy=load(args.policy))
        result.update({"file_sha256": digest(args.file), "policy_sha256": digest(args.policy)})
        print(json.dumps(result, indent=2))
        if args.strict and not result["lexical_gate_passed"]:
            sys.exit(1)


if __name__ == "__main__":
    main()
