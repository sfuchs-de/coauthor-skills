#!/usr/bin/env python3
"""Versioned author extension using the frozen base and edition04 as dependencies."""
import argparse
import importlib.util
import json
import sqlite3
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREVIOUS = next(p for p in (ROOT.parent / "2026-10-03-expanded-04", ROOT.parent / "expansion")
                if (p / "scripts/edition.py").is_file())
SPEC = importlib.util.spec_from_file_location("previous_edition", PREVIOUS / "scripts/edition.py")
previous = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(previous)
BASE = previous.BASE
previous.ROOT = ROOT
load, save, rows, digest = previous.load, previous.save, previous.rows, previous.digest
vocabulary, corpus = previous.vocabulary, previous.corpus


def freeze():
    previous.freeze()
    paths = [p for p in PREVIOUS.rglob("*") if p.is_file() and "__pycache__" not in p.parts
             and p.suffix != ".pyc" and "packaging" not in p.relative_to(PREVIOUS).parts]
    save(ROOT / "data/PREVIOUS_FREEZE.json", {"files": {p.relative_to(PREVIOUS).as_posix(): digest(p)
                                                        for p in sorted(paths)}})


def verify_previous(full=False):
    for name, expected in load(ROOT / "data/PREVIOUS_FREEZE.json")["files"].items():
        path = PREVIOUS / name
        excluded = name.startswith(("sources/", "extracted/", "visual_review/")) or name == "data/extraction.json"
        if excluded and not full and not path.exists():
            continue
        if not path.is_file() or not previous.frozen_matches(path, expected):
            raise ValueError(f"Changed or missing previous artifact: {name}")


def all_papers():
    return (load(BASE / "database/writing_database.json")["papers"]
            + load(PREVIOUS / "data/sources.json")["papers"] + load(ROOT / "data/sources.json")["papers"])


def index_pages(pages):
    """Exclude declared non-English abstract spans without altering raw extraction."""
    indexed = {ident: [dict(page) for page in values] for ident, values in pages.items()}
    exclusions = []
    for item in load(ROOT / "data/sources.json").get("index_exclusions", []):
        page = indexed[item["paper_id"]][item["pdf_page"] - 1]
        value = unicodedata.normalize("NFC", page["text"])
        start, end = item["start"], item["end"]
        if value.count(start) != 1 or value.count(end) != 1:
            raise ValueError("Ambiguous language exclusion")
        left, right = value.index(start), value.index(end)
        if left >= right:
            raise ValueError("Reversed language exclusion")
        removed = value[left:right]
        exclusions.append({**item, "removed_utf8_sha256": previous.hashlib.sha256(removed.encode()).hexdigest(),
                           "removed_characters": len(removed)})
        page["text"] = value[:left] + value[right:]
    return indexed, exclusions


def build():
    previous.verify_base()
    verify_previous(True)
    papers = all_papers()
    if len({p["id"] for p in papers}) != len(papers):
        raise ValueError("Duplicate paper ID")
    acquired = load(ROOT / "data/acquisition.json")
    extraction = load(ROOT / "data/extraction.json")
    pages = {}
    added = {p["id"] for p in load(ROOT / "data/sources.json")["papers"]}
    prior_ids = {p["id"] for p in load(PREVIOUS / "data/sources.json")["papers"]}
    for paper in papers:
        ident = paper["id"]
        source_root = ROOT if ident in added else PREVIOUS if ident in prior_ids else BASE
        pages[ident] = load(source_root / "extracted" / f"{ident}.pages.json")
        support = {page["pdf_page"] for page in pages[ident]}
        first, last = paper["main_pages"]
        if first > last or not set(range(first, last + 1)) <= support:
            raise ValueError(f"Invalid main-text page support: {ident}")
        if ident in added:
            if digest(ROOT / "sources" / f"{ident}.pdf") != acquired[ident]["sha256"]:
                raise ValueError("Changed added PDF")
            if [p["pdf_page"] for p in pages[ident]] != list(range(1, extraction[ident]["pdf_pages"] + 1)):
                raise ValueError("Incomplete extracted page support")
    indexed, exclusions = index_pages(pages)
    words, occurrences = vocabulary.index_pages(papers, indexed)
    output = ROOT / "vocabulary"
    output.mkdir(exist_ok=True)
    database = output / "attested_vocabulary.sqlite"
    if database.exists():
        raise ValueError("Preserve the existing inventory")
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
            + (json.dumps(w["variants"]), json.dumps(w["flags"])) for w in words])
        db.executemany("INSERT INTO occurrences VALUES(?,?,?,?,?,?)", [
            tuple(o[k] for k in ("word","paper_id","pdf_page","scope","evidence_kind","count")) for o in occurrences])
    rows(output / "words.csv", words, ["word","kind","status","full_count","main_count","solid_count","standalone_count","paper_count","papers","variants","flags"])
    rows(output / "occurrences.csv", occurrences, ["word","paper_id","pdf_page","scope","evidence_kind","count"])
    with sqlite3.connect(PREVIOUS / "vocabulary/attested_vocabulary.sqlite") as db:
        old = dict(db.execute("SELECT word,status FROM words"))
    delta = [{"word":w["word"], "status":w["status"], "main_count":w["main_count"],
              "previous_status":old.get(w["word"], "absent"), "new_papers":sorted(set(w["papers"]) & added)}
             for w in words if w["status"].endswith("attested") and not old.get(w["word"], "").endswith("attested")]
    rows(output / "new_attestations.csv", delta, ["word","status","main_count","previous_status","new_papers"])
    counts = {"papers":len(papers),"new_papers":len(added),"included_pages":sum(map(len,pages.values())),
        "new_pages":sum(len(pages[p]) for p in added),"normalized_forms":len(words),
        "attested_writing_forms":sum(w["status"].endswith("attested") for w in words),
        "new_attested_forms":len(delta),"source_page_records":len(occurrences)}
    save(output / "BUILD_RECEIPT.json", {"counts":counts,"sources_config_sha256":digest(ROOT / "data/sources.json"),
        "index_exclusions":exclusions,
        "previous_inventory_sha256":digest(PREVIOUS / "vocabulary/attested_vocabulary.sqlite"),
        "new_source_hashes":{ident:acquired[ident]["sha256"] for ident in sorted(added)},
        "new_extraction_hashes":{ident:digest(ROOT / "extracted" / f"{ident}.pages.json") for ident in sorted(added)},
        "output_sha256":{p.name:digest(p) for p in sorted(output.iterdir()) if p.is_file()},
        "scope":"Exact normalized attestation, not semantic approval or free inflection; delta relative to edition04"})
    print(json.dumps(counts, indent=2))


def study():
    analysis = load(ROOT / "data/analysis.json")
    papers = {p["id"]:p for p in load(ROOT / "data/sources.json")["papers"]}
    if {c["id"] for c in analysis["cards"]} != set(papers):
        raise ValueError("Missing source study")
    output = ROOT / "analysis"
    output.mkdir(exist_ok=True)
    database = output / "analysis.sqlite"
    if database.exists():
        raise ValueError("Preserve the study")
    selected = sum(len(c["read_pages"]) for c in analysis["cards"])
    text = ["# Additional Author Study", "", f"{len(papers)} added papers; selected passages on {selected} PDF pages. Full extraction does not imply full manual reading.",
        "", "These are editorial analyses of coauthored papers, not claims of individual author style or verification of research results.", ""]
    observations = []
    for card in analysis["cards"]:
        paper = papers[card["id"]]
        support = {p["pdf_page"] for p in load(ROOT / "extracted" / f"{card['id']}.pages.json")}
        if not set(card["read_pages"]) <= support or card["render_page"] not in card["read_pages"]:
            raise ValueError("Invalid study support")
        url = paper.get("pdf_url") or load(ROOT / "data/sources.json")["author_indexes"][paper["index"]]
        text.extend([f"## {card['id']}", "", f"[{paper['title']}]({url})", "",
                     "; ".join(paper["authors"]) + ". " + paper["version"] + ".", "",
                     "Selected passages: PDF pp" + ", ".join(map(str,card["read_pages"])) + ".", "",
                     "**Argument map:** " + card["map"] + ".", ""])
        for i, (page,category,note) in enumerate(card["observations"],1):
            if page not in card["read_pages"]:
                raise ValueError("Unreviewed observation anchor")
            observations.append({"id":f"{card['id']}-{i:02d}","paper":card["id"],"pdf_page":page,"category":category,"analysis":note})
            text.append(f"- PDF p{page}, {category}: {note}")
        text.append("")
    (ROOT / "SOURCE_STUDY.md").write_text("\n".join(text) + "\n")
    usage = ["# Additional Economic Usage", "", "Usage distinctions are editorial aids, not vocabulary or concept approval.", "",
             "| Term | Meaning | Distinction | Source analogue |", "|---|---|---|---|"]
    for item in analysis["usage"]:
        ident,page = item["anchor"].split(":")
        if ident not in papers or int(page) not in next(c["read_pages"] for c in analysis["cards"] if c["id"]==ident):
            raise ValueError("Unreviewed usage anchor")
        usage.append(f"| {item['term']} | {item['meaning']} | {item['distinction']} | [{ident} p{page}](SOURCE_STUDY.md#{ident.lower()}) |")
    (ROOT / "USAGE_SUPPLEMENT.md").write_text("\n".join(usage) + "\n")
    rows(output / "observations.csv",observations,["id","paper","pdf_page","category","analysis"])
    rows(output / "usage.csv",analysis["usage"],["term","meaning","distinction","anchor"])
    with sqlite3.connect(database) as db:
        db.executescript("CREATE TABLE observations(id TEXT PRIMARY KEY,paper TEXT,pdf_page INTEGER,category TEXT,analysis TEXT);CREATE TABLE usage(term TEXT PRIMARY KEY,meaning TEXT,distinction TEXT,anchor TEXT);CREATE VIRTUAL TABLE search USING fts5(id,kind,text);")
        for row in observations:
            db.execute("INSERT INTO observations VALUES(?,?,?,?,?)",tuple(row.values()))
            db.execute("INSERT INTO search VALUES(?,?,?)",(row["id"],"observation",row["analysis"]))
        for row in analysis["usage"]:
            db.execute("INSERT INTO usage VALUES(?,?,?,?)",tuple(row.values()))
            db.execute("INSERT INTO search VALUES(?,?,?)",(row["term"],"usage",row["meaning"] + " " + row["distinction"]))
    save(output / "BUILD_RECEIPT.json", {"input_sha256":digest(ROOT / "data/analysis.json"),
        "new_observations":len(observations),"new_usage_entries":len(analysis["usage"]),"selected_passage_pages":selected,
        "output_sha256":{p.relative_to(ROOT).as_posix():digest(p) for p in
            (database,output / "observations.csv",output / "usage.csv",ROOT / "SOURCE_STUDY.md",ROOT / "USAGE_SUPPLEMENT.md")}})


def verify(full=False):
    verify_previous(full)
    previous.verify(full)
    with sqlite3.connect(ROOT / "vocabulary/attested_vocabulary.sqlite") as db:
        if {p for p, in db.execute("SELECT DISTINCT paper_id FROM occurrences")} != {p["id"] for p in all_papers()}:
            raise ValueError("Wrong combined paper support")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest="command",required=True)
    for name in ("freeze","acquire","extract","build","study","render"):
        sub.add_parser(name)
    sub.add_parser("verify").add_argument("--full",action="store_true")
    sub.add_parser("lookup").add_argument("word")
    check=sub.add_parser("check")
    check.add_argument("file",type=Path)
    check.add_argument("--strict",action="store_true")
    check.add_argument("--policy",type=Path,default=BASE / "data/vocabulary_policy.json")
    args=parser.parse_args()
    if args.command=="freeze": freeze()
    elif args.command=="acquire":
        corpus.ROOT=ROOT
        corpus.acquire(set())
    elif args.command=="extract": previous.extract()
    elif args.command=="build": build()
    elif args.command=="study": study()
    elif args.command=="render": previous.render()
    elif args.command=="verify": verify(args.full)
    elif args.command=="lookup":
        word=vocabulary.canonical(args.word)
        with sqlite3.connect(ROOT / "vocabulary/attested_vocabulary.sqlite") as db:
            evidence=db.execute("SELECT paper_id,pdf_page,scope,evidence_kind,count FROM occurrences WHERE word=? ORDER BY scope,paper_id,pdf_page LIMIT 30",(word,)).fetchall()
        print(json.dumps({"word":word,"record":previous.records().get(word),"evidence":evidence},indent=2))
    else:
        result=vocabulary.inspect_prose(args.file.read_text(),args.file.suffix,previous.records(),load(args.policy))
        result.update({"edition":load(ROOT / "data/sources.json")["edition"],"file_sha256":digest(args.file)})
        print(json.dumps(result,indent=2))
        if args.strict and not result["lexical_gate_passed"]: sys.exit(1)


if __name__=="__main__": main()
