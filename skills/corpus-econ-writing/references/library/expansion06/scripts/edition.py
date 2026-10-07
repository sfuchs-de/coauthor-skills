#!/usr/bin/env python3
"""Opt-in urban corpus, preserving the base and editions04/05."""
import argparse
import importlib.util
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def dependency(local, portable):
    return next(p for p in (ROOT.parent / local, ROOT.parent / portable)
                if (p / "scripts/edition.py").is_file())


PRIOR04 = dependency("2026-10-03-expanded-04", "expansion")
PRIOR05 = dependency("2026-10-04-authors-05", "expansion05")
spec = importlib.util.spec_from_file_location("urban_previous", PRIOR05 / "scripts/edition.py")
authors = importlib.util.module_from_spec(spec)
spec.loader.exec_module(authors)
helpers = authors.previous
BASE = authors.BASE
load, save, rows, digest = helpers.load, helpers.save, helpers.rows, helpers.digest
vocabulary, corpus = helpers.vocabulary, helpers.corpus
helpers.ROOT = ROOT
authors.ROOT = ROOT


def all_papers():
    return (load(BASE / "database/writing_database.json")["papers"]
            + load(PRIOR04 / "data/sources.json")["papers"]
            + load(PRIOR05 / "data/sources.json")["papers"]
            + load(ROOT / "data/sources.json")["papers"])


def source_root(ident):
    for root in (ROOT, PRIOR05, PRIOR04):
        if ident in {p["id"] for p in load(root / "data/sources.json")["papers"]}:
            return root
    return BASE


def freeze():
    helpers.freeze()
    target = ROOT / "data/PREVIOUS_FREEZE.json"
    if target.exists():
        raise ValueError("Preserve previous freeze")
    saved = {}
    for name, root in (("04", PRIOR04), ("05", PRIOR05)):
        saved[name] = {p.relative_to(root).as_posix(): digest(p) for p in sorted(root.rglob("*"))
                      if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
                      and "packaging" not in p.relative_to(root).parts}
    save(target, {"editions": saved})


def verify_previous(full=False):
    helpers.verify_base()
    for name, root in (("04", PRIOR04), ("05", PRIOR05)):
        for item, expected in load(ROOT / "data/PREVIOUS_FREEZE.json")["editions"][name].items():
            path = root / item
            excluded = item.startswith(("sources/", "extracted/", "visual_review/")) or item == "data/extraction.json"
            if not full and excluded and not path.exists():
                continue
            if not path.is_file() or not helpers.frozen_matches(path, expected):
                raise ValueError(f"Changed prior artifact {name}: {item}")


def index_pages(pages):
    # Preserve the earlier English-index exclusions in the combined inventory.
    config = load(PRIOR05 / "data/sources.json")
    exclusions = config.get("index_exclusions", [])
    indexed = {ident: [dict(page) for page in values] for ident, values in pages.items()}
    import unicodedata
    receipt = []
    for item in exclusions:
        page = indexed[item["paper_id"]][item["pdf_page"] - 1]
        text = unicodedata.normalize("NFC", page["text"])
        start, end = item["start"], item["end"]
        if text.count(start) != 1 or text.count(end) != 1 or text.index(start) >= text.index(end):
            raise ValueError("Ambiguous inherited language exclusion")
        left, right = text.index(start), text.index(end)
        receipt.append({**item, "removed_utf8_sha256": helpers.hashlib.sha256(text[left:right].encode()).hexdigest(),
                        "removed_characters": right-left})
        page["text"] = text[:left] + text[right:]
    return indexed, receipt


def build():
    verify_previous(True)
    papers = all_papers()
    if len({p["id"] for p in papers}) != len(papers):
        raise ValueError("Duplicate paper ID")
    acquired = load(ROOT / "data/acquisition.json")
    extraction = load(ROOT / "data/extraction.json")
    added = {p["id"] for p in load(ROOT / "data/sources.json")["papers"]}
    pages = {}
    for paper in papers:
        ident = paper["id"]
        pages[ident] = load(source_root(ident) / "extracted" / f"{ident}.pages.json")
        support = {p["pdf_page"] for p in pages[ident]}
        first, last = paper["main_pages"]
        if first > last or not set(range(first,last+1)) <= support:
            raise ValueError(f"Invalid main-page support {ident}")
        if ident in added:
            if digest(ROOT / "sources" / f"{ident}.pdf") != acquired[ident]["sha256"]:
                raise ValueError("Changed added source")
            if [p["pdf_page"] for p in pages[ident]] != list(range(1, extraction[ident]["pdf_pages"]+1)):
                raise ValueError("Incomplete extraction")
    indexed, exclusions = index_pages(pages)
    words, occurrences = vocabulary.index_pages(papers,indexed)
    output = ROOT / "vocabulary"
    output.mkdir(exist_ok=True)
    database = output / "attested_vocabulary.sqlite"
    if database.exists():
        raise ValueError("Preserve existing inventory")
    with sqlite3.connect(database) as db:
        db.executescript("""PRAGMA foreign_keys=ON;
          CREATE TABLE words(word TEXT PRIMARY KEY,kind TEXT,status TEXT,full_count INTEGER,
            main_count INTEGER,solid_count INTEGER,standalone_count INTEGER,paper_count INTEGER,
            variants TEXT,flags TEXT);
          CREATE TABLE occurrences(word TEXT REFERENCES words(word),paper_id TEXT,pdf_page INTEGER,
            scope TEXT,evidence_kind TEXT,count INTEGER,PRIMARY KEY(word,paper_id,pdf_page,scope,evidence_kind));
          CREATE INDEX by_paper_page ON occurrences(paper_id,pdf_page);""")
        db.executemany("INSERT INTO words VALUES(?,?,?,?,?,?,?,?,?,?)", [
            tuple(w[k] for k in ("word","kind","status","full_count","main_count","solid_count","standalone_count","paper_count"))
            + (json.dumps(w["variants"]),json.dumps(w["flags"])) for w in words])
        db.executemany("INSERT INTO occurrences VALUES(?,?,?,?,?,?)",[
            tuple(o[k] for k in ("word","paper_id","pdf_page","scope","evidence_kind","count")) for o in occurrences])
    rows(output / "words.csv",words,["word","kind","status","full_count","main_count","solid_count","standalone_count","paper_count","papers","variants","flags"])
    rows(output / "occurrences.csv",occurrences,["word","paper_id","pdf_page","scope","evidence_kind","count"])
    with sqlite3.connect(PRIOR05 / "vocabulary/attested_vocabulary.sqlite") as db:
        old = dict(db.execute("SELECT word,status FROM words"))
    delta = [{"word":w["word"],"status":w["status"],"main_count":w["main_count"],
              "previous_status":old.get(w["word"],"absent"),"new_papers":sorted(set(w["papers"]) & added)}
             for w in words if w["status"].endswith("attested") and not old.get(w["word"],"").endswith("attested")]
    rows(output / "new_attestations.csv",delta,["word","status","main_count","previous_status","new_papers"])
    counts = {"papers":len(papers),"new_papers":len(added),"included_pages":sum(map(len,pages.values())),
              "new_pages":sum(len(pages[p]) for p in added),"normalized_forms":len(words),
              "attested_writing_forms":sum(w["status"].endswith("attested") for w in words),
              "new_attested_forms":len(delta),"source_page_records":len(occurrences)}
    save(output / "BUILD_RECEIPT.json",{"counts":counts,"sources_config_sha256":digest(ROOT / "data/sources.json"),
         "index_exclusions":exclusions,"previous_inventory_sha256":digest(PRIOR05 / "vocabulary/attested_vocabulary.sqlite"),
         "new_source_hashes":{p:acquired[p]["sha256"] for p in sorted(added)},
         "new_extraction_hashes":{p:digest(ROOT / "extracted" / f"{p}.pages.json") for p in sorted(added)},
         "output_sha256":{p.name:digest(p) for p in sorted(output.iterdir()) if p.is_file()},
         "scope":"Opt-in exact normalized attestation; not semantic approval or free inflection; delta relative to edition05"})
    print(json.dumps(counts,indent=2))


def verify(full=False):
    verify_previous(full)
    helpers.verify(full)
    with sqlite3.connect(ROOT / "vocabulary/attested_vocabulary.sqlite") as db:
        if {p for p, in db.execute("SELECT DISTINCT paper_id FROM occurrences")} != {p["id"] for p in all_papers()}:
            raise ValueError("Wrong combined support")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command",required=True)
    for name in ("freeze","acquire","extract","build","study","render"):
        sub.add_parser(name)
    sub.add_parser("verify").add_argument("--full",action="store_true")
    sub.add_parser("lookup").add_argument("word")
    check = sub.add_parser("check")
    check.add_argument("file",type=Path)
    check.add_argument("--strict",action="store_true")
    check.add_argument("--policy",type=Path,default=BASE / "data/vocabulary_policy.json")
    args = parser.parse_args()
    if args.command == "freeze": freeze()
    elif args.command == "acquire":
        corpus.ROOT=ROOT
        corpus.acquire(set())
    elif args.command == "extract": helpers.extract()
    elif args.command == "build": build()
    elif args.command == "study": authors.study()
    elif args.command == "render": helpers.render()
    elif args.command == "verify": verify(args.full)
    elif args.command == "lookup":
        word=vocabulary.canonical(args.word)
        with sqlite3.connect(ROOT / "vocabulary/attested_vocabulary.sqlite") as db:
            evidence=db.execute("SELECT paper_id,pdf_page,scope,evidence_kind,count FROM occurrences WHERE word=? ORDER BY scope,paper_id,pdf_page LIMIT 30",(word,)).fetchall()
        print(json.dumps({"word":word,"record":helpers.records().get(word),"evidence":evidence},indent=2))
    else:
        result=vocabulary.inspect_prose(args.file.read_text(),args.file.suffix,helpers.records(),load(args.policy))
        result.update({"edition":load(ROOT / "data/sources.json")["edition"],"file_sha256":digest(args.file)})
        print(json.dumps(result,indent=2))
        if args.strict and not result["lexical_gate_passed"]: sys.exit(1)


if __name__ == "__main__": main()
