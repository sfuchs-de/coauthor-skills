#!/usr/bin/env python3
"""Versioned corpus extension; retain the original corpus and its portable checks."""
import argparse
import csv
import hashlib
import importlib
import json
import shutil
import sqlite3
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = next(p for p in (ROOT.parent, ROOT.parents[1])
            if (p / "scripts/vocabulary.py").is_file())
sys.path.insert(0, str(BASE / "scripts"))
vocabulary = importlib.import_module("vocabulary")
corpus = importlib.import_module("corpus")


def load(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def rows(path, records, fields):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow({k: json.dumps(record[k], ensure_ascii=False)
                             if isinstance(record[k], (dict, list)) else record[k]
                             for k in fields})


def freeze():
    target = ROOT / "data/BASELINE_FREEZE.json"
    if target.exists():
        raise ValueError("Preserve the previous baseline receipt")
    paths = []
    for folder in ("sources", "extracted", "data", "database", "vocabulary"):
        paths.extend(p for p in (BASE / folder).rglob("*") if p.is_file())
    save(target, {"base_files": {p.relative_to(BASE).as_posix(): digest(p)
                                 for p in sorted(paths)},
                  "edition": load(ROOT / "data/sources.json")["edition"]})


def frozen_matches(path, expected):
    """Accept exact frozen bytes or an explicitly hash-pinned public packaging adaptation.

    Vocabulary, analytical data and scientific source receipts are never adaptable here.
    The original freeze receipts remain unchanged.
    """
    actual = digest(path)
    if actual == expected:
        return True
    relative = path.resolve().relative_to(BASE.resolve()).as_posix()
    allowed = {'database/QUALITY_RECEIPT.json', 'expansion/scripts/edition.py',
               'expansion05/scripts/edition.py', 'expansion06/scripts/edition.py'}
    if relative not in allowed:
        return False
    mapping = BASE / 'PUBLIC_ADAPTATIONS.json'
    if not mapping.is_file():
        return False
    record = load(mapping).get('files', {}).get(relative, {})
    return record.get('source_sha256') == expected and record.get('package_sha256') == actual


def verify_base():
    frozen = load(ROOT / "data/BASELINE_FREEZE.json")
    for name, expected in frozen["base_files"].items():
        path = BASE / name
        if not path.is_file():
            if name.startswith(("sources/", "extracted/")) or name == "data/extraction.json":
                continue  # Full source material is intentionally absent from portable packages.
            raise ValueError(f"Missing original artifact: {name}")
        if not frozen_matches(path, expected):
            raise ValueError(f"Changed original artifact: {name}")


def build():
    verify_base()
    config = load(ROOT / "data/sources.json")
    old = load(BASE / "database/writing_database.json")["papers"]
    added = config["papers"]
    ids = [p["id"] for p in old + added]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate paper ID")
    acquired = load(ROOT / "data/acquisition.json")
    extraction = load(ROOT / "data/extraction.json")
    pages = {p["id"]: load(BASE / "extracted" / f"{p['id']}.pages.json") for p in old}
    for paper in added:
        ident = paper["id"]
        if digest(ROOT / "sources" / f"{ident}.pdf") != acquired[ident]["sha256"]:
            raise ValueError(f"Changed source PDF: {ident}")
        pages[ident] = load(ROOT / "extracted" / f"{ident}.pages.json")
        if [p["pdf_page"] for p in pages[ident]] != list(range(1, extraction[ident]["pdf_pages"] + 1)):
            raise ValueError(f"Incomplete extracted page support: {ident}")
        first, last = paper["main_pages"]
        if not 1 <= first <= last <= len(pages[ident]):
            raise ValueError(f"Invalid main-page scope: {ident}")
    words, occurrences = vocabulary.index_pages(old + added, pages)
    output = ROOT / "vocabulary"
    output.mkdir(exist_ok=True)
    database = output / "attested_vocabulary.sqlite"
    if database.exists():
        raise ValueError("Preserve prior build; create a new edition for changes")
    with sqlite3.connect(database) as db:
        db.executescript("""
          PRAGMA foreign_keys=ON;
          CREATE TABLE words(word TEXT PRIMARY KEY,kind TEXT,status TEXT,full_count INTEGER,
            main_count INTEGER,solid_count INTEGER,standalone_count INTEGER,paper_count INTEGER,
            variants TEXT,flags TEXT);
          CREATE TABLE occurrences(word TEXT REFERENCES words(word),paper_id TEXT,pdf_page INTEGER,
            scope TEXT,evidence_kind TEXT,count INTEGER,
            PRIMARY KEY(word,paper_id,pdf_page,scope,evidence_kind));
          CREATE INDEX by_paper_page ON occurrences(paper_id,pdf_page);
        """)
        db.executemany("INSERT INTO words VALUES(?,?,?,?,?,?,?,?,?,?)", [
            tuple(w[k] for k in ("word", "kind", "status", "full_count", "main_count", "solid_count", "standalone_count", "paper_count"))
            + (json.dumps(w["variants"]), json.dumps(w["flags"])) for w in words])
        db.executemany("INSERT INTO occurrences VALUES(?,?,?,?,?,?)", [
            tuple(o[k] for k in ("word", "paper_id", "pdf_page", "scope", "evidence_kind", "count")) for o in occurrences])
    rows(output / "words.csv", words, ["word", "kind", "status", "full_count", "main_count", "solid_count", "standalone_count", "paper_count", "papers", "variants", "flags"])
    rows(output / "occurrences.csv", occurrences, ["word", "paper_id", "pdf_page", "scope", "evidence_kind", "count"])
    with sqlite3.connect((BASE / "vocabulary/attested_vocabulary.sqlite").as_uri() + "?mode=ro", uri=True) as db:
        old_words = {w: status for w, status in db.execute("SELECT word,status FROM words")}
    added_ids = {p["id"] for p in added}
    delta = [{"word": w["word"], "status": w["status"], "main_count": w["main_count"],
              "previous_status": old_words.get(w["word"], "absent"),
              "new_papers": sorted(set(w["papers"]) & added_ids)} for w in words
             if w["status"].endswith("attested") and not old_words.get(w["word"], "").endswith("attested")]
    rows(output / "new_attestations.csv", delta, ["word", "status", "main_count", "previous_status", "new_papers"])
    counts = {"papers": len(ids), "new_papers": len(added), "included_pages": sum(map(len, pages.values())),
              "new_pages": sum(len(pages[p["id"]]) for p in added), "normalized_forms": len(words),
              "attested_writing_forms": sum(w["status"].endswith("attested") for w in words),
              "new_attested_forms": len(delta), "source_page_records": len(occurrences)}
    save(output / "BUILD_RECEIPT.json", {"counts": counts, "sources_config_sha256": digest(ROOT / "data/sources.json"),
         "new_source_hashes": {p["id"]: acquired[p["id"]]["sha256"] for p in added},
         "new_extraction_hashes": {p["id"]: digest(ROOT / "extracted" / f"{p['id']}.pages.json") for p in added},
         "output_sha256": {p.name: digest(p) for p in sorted(output.iterdir()) if p.is_file()},
         "scope": "Extraction inventory, not manual approval of every token; main ranges are approximate. No free inflections or new concepts."})
    print(json.dumps(counts, indent=2))


def extract():
    config = load(ROOT / "data/sources.json")
    destination = ROOT / "extracted"
    destination.mkdir(exist_ok=True)
    metrics = {}
    for paper in config["papers"]:
        ident = paper["id"]
        source = ROOT / "sources" / f"{ident}.pdf"
        info = subprocess.check_output(["pdfinfo", str(source)], text=True)
        expected = int(re.search(r"(?m)^Pages:\s+(\d+)", info).group(1))
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "text.txt"
            subprocess.run(["pdftotext", "-layout", str(source), str(target)], check=True)
            texts = target.read_text().split("\f")
        if texts and not texts[-1].strip():
            texts.pop()
        if len(texts) != expected:
            raise ValueError(f"Page extraction mismatch: {ident}")
        pages = [{"pdf_page": i, "text": text,
                  "word_count": len(re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", text))}
                 for i, text in enumerate(texts, 1)]
        save(destination / f"{ident}.pages.json", pages)
        metrics[ident] = {"pdf_pages": expected, "included_pages": [1, expected],
                          "extracted_words": sum(p["word_count"] for p in pages),
                          "method": "Poppler pdftotext -layout; PDF count independently checked with pdfinfo"}
        print(f"{ident}: {expected} pages, {metrics[ident]['extracted_words']} recognized words")
    save(ROOT / "data/extraction.json", metrics)


def study(refresh=False):
    config = load(ROOT / "data/sources.json")
    analysis = load(ROOT / "data/analysis.json")
    papers = {p["id"]: p for p in config["papers"]}
    if set(papers) != {c["id"] for c in analysis["cards"]}:
        raise ValueError("Study does not cover every added paper")
    output = ROOT / "analysis"
    output.mkdir(exist_ok=True)
    database = output / "analysis.sqlite"
    if database.exists():
        if not refresh:
            raise ValueError("Preserve prior study output; use --refresh for owned draft exports")
        previous = load(output / "BUILD_RECEIPT.json")
        for name, expected in previous["output_sha256"].items():
            if digest(ROOT / name) != expected:
                raise ValueError("Changed study output; inspect before refreshing")
        database.unlink()
    observations = []
    cards = ["# Expanded Source Study", "", "Eight additional papers; selected passages on 68 PDF pages. The full 502-page extraction is not a claim of full manual reading.", "", "The maps and observations are original editorial analyses. They do not certify proofs, estimates, or an individual coauthor's writing process. Versions are pinned by acquisition hashes, not inferred from a website's current publication status.", ""]
    for card in analysis["cards"]:
        paper = papers[card["id"]]
        available = {p["pdf_page"] for p in load(ROOT / "extracted" / f"{card['id']}.pages.json")}
        if not set(card["read_pages"]) <= available or card["render_page"] not in card["read_pages"]:
            raise ValueError("Invalid review page")
        url = paper.get("pdf_url") or config["author_indexes"][paper["index"]]
        cards += [f"## {card['id']}", "", f"[{paper['title']}]({url})", "", "; ".join(paper["authors"]) + ". " + paper["version"] + ".", "", "Selected passages: PDF pp" + ", ".join(map(str, card["read_pages"])) + ".", "", "**Argument map:** " + card["map"] + ".", ""]
        for number, (page, category, note) in enumerate(card["observations"], 1):
            observations.append({"id": f"{card['id']}-{number:02d}", "paper": card["id"], "pdf_page": page, "category": category, "analysis": note})
            cards.append(f"- PDF p{page}, {category}: {note}")
        cards.append("")
    (ROOT / "SOURCE_STUDY.md").write_text("\n".join(cards) + "\n")
    usage = ["# Additional Economic Usage", "", "Thirty-six distinctions supplement the original 185 entries. Editorial labels are not a whitelist, and examples are not new scientific results. Exact phrase attestation must be checked separately from the presence of component words.", "", "| Term | Meaning | Distinction to preserve | Source analogue |", "|---|---|---|---|"]
    for item in analysis["usage"]:
        ident, page = item["anchor"].split(":")
        if ident not in papers or int(page) not in next(c["read_pages"] for c in analysis["cards"] if c["id"] == ident):
            raise ValueError("Usage anchor was not reviewed")
        usage.append(f"| {item['term']} | {item['meaning']} | {item['distinction']} | [{ident} p{page}](SOURCE_STUDY.md#{ident.lower()}) |")
    (ROOT / "USAGE_SUPPLEMENT.md").write_text("\n".join(usage) + "\n")
    rows(output / "observations.csv", observations, ["id", "paper", "pdf_page", "category", "analysis"])
    rows(output / "usage.csv", analysis["usage"], ["term", "meaning", "distinction", "anchor"])
    with sqlite3.connect(database) as db:
        db.executescript("CREATE TABLE observations(id TEXT PRIMARY KEY,paper TEXT,pdf_page INTEGER,category TEXT,analysis TEXT); CREATE TABLE usage(term TEXT PRIMARY KEY,meaning TEXT,distinction TEXT,anchor TEXT); CREATE VIRTUAL TABLE search USING fts5(id,kind,text);")
        for row in observations:
            db.execute("INSERT INTO observations VALUES(?,?,?,?,?)", tuple(row.values()))
            db.execute("INSERT INTO search VALUES(?,?,?)", (row["id"], "observation", row["analysis"]))
        for row in analysis["usage"]:
            db.execute("INSERT INTO usage VALUES(?,?,?,?)", tuple(row.values()))
            db.execute("INSERT INTO search VALUES(?,?,?)", (row["term"], "usage", row["meaning"] + " " + row["distinction"]))
    save(output / "BUILD_RECEIPT.json", {"input_sha256": digest(ROOT / "data/analysis.json"),
         "new_observations": len(observations), "new_usage_entries": len(analysis["usage"]),
         "selected_passage_pages": sum(len(c["read_pages"]) for c in analysis["cards"]),
         "output_sha256": {p.relative_to(ROOT).as_posix(): digest(p) for p in
                            [database, output / "observations.csv", output / "usage.csv", ROOT / "SOURCE_STUDY.md", ROOT / "USAGE_SUPPLEMENT.md"]}})
    print("Study and searchable usage supplement created")


def render():
    destination = ROOT / "visual_review"
    destination.mkdir(exist_ok=True)
    receipt = {}
    for card in load(ROOT / "data/analysis.json")["cards"]:
        target = destination / f"{card['id']}-{card['render_page']}"
        if target.with_suffix(".png").exists():
            raise ValueError("Preserve prior render")
        subprocess.run(["pdftoppm", "-f", str(card["render_page"]), "-l", str(card["render_page"]),
                        "-scale-to", "1000", "-singlefile", "-png", str(ROOT / "sources" / f"{card['id']}.pdf"), str(target)], check=True)
        receipt[card["id"]] = {"pdf_page": card["render_page"], "image_sha256": digest(target.with_suffix(".png")), "inspection": "pending visual review"}
    save(ROOT / "data/render_receipt.json", receipt)


def verify(full=False):
    verify_base()
    receipt = load(ROOT / "vocabulary/BUILD_RECEIPT.json")
    if digest(ROOT / "data/sources.json") != receipt["sources_config_sha256"]:
        raise ValueError("Changed source configuration")
    for name, expected in receipt["output_sha256"].items():
        if digest(ROOT / "vocabulary" / name) != expected:
            raise ValueError(f"Changed vocabulary output: {name}")
    if full:
        for ident, expected in receipt["new_source_hashes"].items():
            if digest(ROOT / "sources" / f"{ident}.pdf") != expected:
                raise ValueError(f"Changed source: {ident}")
        for ident, expected in receipt["new_extraction_hashes"].items():
            if digest(ROOT / "extracted" / f"{ident}.pages.json") != expected:
                raise ValueError(f"Changed extraction: {ident}")
    with sqlite3.connect((ROOT / "vocabulary/attested_vocabulary.sqlite").as_uri() + "?mode=ro", uri=True) as db:
        if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok" or db.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("Invalid vocabulary database")
        if db.execute("SELECT count(*) FROM words").fetchone()[0] != receipt["counts"]["normalized_forms"]:
            raise ValueError("Wrong word support")
        if db.execute("SELECT count(*) FROM occurrences").fetchone()[0] != receipt["counts"]["source_page_records"]:
            raise ValueError("Wrong occurrence support")
        discrepancy = db.execute("""SELECT word FROM words JOIN occurrences USING(word) GROUP BY word
          HAVING full_count != SUM(count) OR main_count != SUM(CASE WHEN scope='main_range' THEN count ELSE 0 END)
          OR solid_count != SUM(CASE WHEN evidence_kind!='linebreak_fragment' THEN count ELSE 0 END)
          OR paper_count != COUNT(DISTINCT paper_id)""").fetchall()
        if discrepancy:
            raise ValueError("Counts do not match page evidence")
    study_receipt = load(ROOT / "analysis/BUILD_RECEIPT.json")
    if digest(ROOT / "data/analysis.json") != study_receipt["input_sha256"]:
        raise ValueError("Changed study input")
    for name, expected in study_receipt["output_sha256"].items():
        if digest(ROOT / name) != expected:
            raise ValueError(f"Changed study output: {name}")
    with sqlite3.connect((ROOT / "analysis/analysis.sqlite").as_uri() + "?mode=ro", uri=True) as db:
        if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("Invalid study database")
        if db.execute("SELECT count(*) FROM observations").fetchone()[0] != study_receipt["new_observations"]:
            raise ValueError("Wrong study observation support")
        if db.execute("SELECT count(*) FROM usage").fetchone()[0] != study_receipt["new_usage_entries"]:
            raise ValueError("Wrong usage support")
    print(json.dumps({"verified": True, "full_source_check": full, "counts": receipt["counts"]}))


def records():
    receipt = load(ROOT / "vocabulary/BUILD_RECEIPT.json")
    database = ROOT / "vocabulary/attested_vocabulary.sqlite"
    if digest(database) != receipt["output_sha256"][database.name]:
        raise ValueError("Changed vocabulary database")
    with sqlite3.connect(database.as_uri() + "?mode=ro", uri=True) as db:
        return {w: {"solid_count": solid, "status": status, "flags": json.loads(flags), "main_count": main}
                for w, solid, status, flags, main in db.execute("SELECT word,solid_count,status,flags,main_count FROM words")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("freeze", "acquire", "extract", "build", "render"):
        sub.add_parser(name)
    study_parser = sub.add_parser("study")
    study_parser.add_argument("--refresh", action="store_true")
    verify_parser = sub.add_parser("verify")
    verify_parser.add_argument("--full", action="store_true")
    check = sub.add_parser("check")
    check.add_argument("file", type=Path)
    check.add_argument("--strict", action="store_true")
    check.add_argument("--policy", type=Path, default=BASE / "data/vocabulary_policy.json")
    lookup = sub.add_parser("lookup")
    lookup.add_argument("word")
    args = parser.parse_args()
    if args.command == "freeze":
        freeze()
    elif args.command == "acquire":
        corpus.ROOT = ROOT
        corpus.acquire(set())
    elif args.command == "extract":
        extract()
    elif args.command == "study":
        study(args.refresh)
    elif args.command == "render":
        render()
    elif args.command == "build":
        build()
    elif args.command == "verify":
        verify(args.full)
    elif args.command == "lookup":
        word = vocabulary.canonical(args.word)
        print(json.dumps({word: records().get(word)}, indent=2))
        with sqlite3.connect((ROOT / "vocabulary/attested_vocabulary.sqlite").as_uri() + "?mode=ro", uri=True) as db:
            print(json.dumps(db.execute("SELECT paper_id,pdf_page,scope,evidence_kind,count FROM occurrences WHERE word=? ORDER BY scope,paper_id,pdf_page LIMIT 20", (word,)).fetchall()))
    else:
        result = vocabulary.inspect_prose(args.file.read_text(), args.file.suffix, records(), load(args.policy))
        result.update({"edition": load(ROOT / "data/sources.json")["edition"], "file_sha256": digest(args.file)})
        print(json.dumps(result, indent=2))
        if args.strict and not result["lexical_gate_passed"]:
            sys.exit(1)


if __name__ == "__main__":
    main()
