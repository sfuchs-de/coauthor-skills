#!/usr/bin/env python3
"""Build and validate an evidence-linked, source-free writing database."""
import argparse
import csv
import hashlib
import json
import platform
import re
import sqlite3
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read_json(path):
    return json.loads(path.read_text())

def unique(records, key, kind):
    counts = Counter(item[key] for item in records)
    duplicates = [ident for ident, count in counts.items() if count > 1]
    if duplicates:
        raise ValueError(f"Duplicate {kind}: {duplicates}")

def normalize(text):
    text = re.sub(r"([A-Za-z])-\s*\n\s*([a-z])", r"\1\2", text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()

def phrase_pages(term, pages):
    target = normalize(term)
    pattern = re.compile(r"(?<!\w)" + re.escape(target) + r"(?!\w)")
    hits = []
    for page in pages:
        normalized_page = page.get("normalized_text")
        if normalized_page is None:
            normalized_page = normalize(page["text"])
        count = len(pattern.findall(normalized_page))
        if count:
            hits.append({"pdf_page": page["pdf_page"], "count": count})
    return hits

def freeze_evidence(root=ROOT):
    target = root / "data/review_inputs.json"
    if target.exists():
        raise ValueError("Evidence manifest already exists; preserve this edition")
    sources = read_json(root / "data/sources.json")["papers"]
    samples = read_json(root / "data/visual_samples.json")
    paths = [f"extracted/{paper['id']}.{suffix}" for paper in sources
             for suffix in ("pages.json", "txt")]
    paths.extend(sample["image"] for sample in samples)
    unique([{"path": path} for path in paths], "path", "evidence files")
    files = {path: hashlib.sha256((root / path).read_bytes()).hexdigest()
             for path in paths}
    target.write_text(json.dumps({"schema_version": 1,
        "scope": "Frozen extracts and rendered pages used by this review; not a certification of every extracted passage",
        "files": files}, indent=2) + "\n")
    print(f"Froze {len(files)} evidence files")

def verify_evidence(root, required_paths=None):
    manifest = read_json(root / "data/review_inputs.json")
    if required_paths is not None and set(manifest["files"]) != set(required_paths):
        raise ValueError("Incomplete or incompatible reviewed-evidence manifest")
    for path, expected in manifest["files"].items():
        candidate = Path(path)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise ValueError(f"Invalid evidence path: {path}")
        actual = hashlib.sha256((root / candidate).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"Changed reviewed evidence: {path}")

def validate(papers, observations, rules, lexicon):
    unique(papers, "id", "paper IDs")
    unique(observations, "id", "observation IDs")
    unique(rules, "id", "rule IDs")
    unique(lexicon, "id", "dictionary IDs")
    unique(lexicon, "term", "dictionary terms")
    by_paper = {paper["id"]: paper for paper in papers}
    observation_ids = {item["id"] for item in observations}
    for paper in papers:
        first, last = paper["main_pages"]
        include_first, include_last = paper["included_pages"]
        if not include_first <= first <= last <= include_last:
            raise ValueError(f"Invalid main-page boundary: {paper['id']}")
        if not paper["read_pages"] or not paper["visual_inspected"]:
            raise ValueError(f"Missing review evidence: {paper['id']}")
        if not set(paper["read_pages"]) <= set(range(include_first, include_last + 1)):
            raise ValueError(f"Review page outside source: {paper['id']}")
        if paper["visual_page"] not in range(include_first, include_last + 1):
            raise ValueError(f"Visual page outside source: {paper['id']}")
        if not paper["visual_observation"].strip():
            raise ValueError(f"Missing visual assessment: {paper['id']}")
        if paper.get("quotations"):
            raise ValueError("This edition declares no reproduced source quotations")
    for item in observations:
        if item["paper_id"] not in by_paper:
            raise ValueError(f"Unknown paper in observation: {item['id']}")
        paper = by_paper[item["paper_id"]]
        if item["pdf_page"] not in paper["read_pages"]:
            raise ValueError(f"Observation without manual page review: {item['id']}")
        if not re.fullmatch(r"[0-9a-f]{64}", item["page_sha256"]) or not re.fullmatch(r"[0-9a-f]{64}", item["source_sha256"]):
            raise ValueError(f"Missing evidence hash: {item['id']}")
        if item["source_sha256"] != paper["source_sha256"]:
            raise ValueError(f"Wrong source hash: {item['id']}")
    for rule in rules:
        if not rule["evidence"] or not set(rule["evidence"]) <= observation_ids:
            raise ValueError(f"Broken rule evidence: {rule['id']}")

def compile_data(root=ROOT):
    config = read_json(root / "data/sources.json")
    unique(config["papers"], "id", "source IDs")
    acquisition = read_json(root / "data/acquisition.json")
    extraction = read_json(root / "data/extraction.json")
    reviews = []
    for name in ("reviews.json", "reviews_middle.json", "reviews_redding.json"):
        reviews.extend(read_json(root / "data" / name)["papers"])
    unique(reviews, "id", "review IDs")
    review_map = {review["id"]: review for review in reviews}
    for ident, amendment in read_json(root / "data/review_amendments.json").items():
        review = review_map[ident]
        review["read_pages"] = sorted(set(review["read_pages"] + amendment.get("add_read_pages", [])))
        review["observations"].extend(amendment.get("add_observations", []))
        if "main_pages" in amendment:
            review["main_pages"] = amendment["main_pages"]
    if set(review_map) != {paper["id"] for paper in config["papers"]}:
        raise ValueError("Corpus and manual review IDs differ")
    visual = read_json(root / "data/visual_observations.json")["papers"]
    samples = read_json(root / "data/visual_samples.json")
    unique(samples, "paper_id", "visual sample IDs")
    sample_map = {item["paper_id"]: item for item in samples}
    required = [f"extracted/{paper['id']}.{suffix}" for paper in config["papers"]
                for suffix in ("pages.json", "txt")]
    required.extend(sample["image"] for sample in samples)
    verify_evidence(root, required)
    papers, observations, frequencies = [], [], []
    with (root / "data/dictionary.tsv").open(newline="") as handle:
        lexicon = list(csv.DictReader(handle, delimiter="\t"))
    for item in lexicon:
        item["id"] = "lex-" + normalize(item["term"]).replace(" ", "-")
        item["entry_kind"] = "recommended usage; examples are original and hypothetical"
    for source in config["papers"]:
        ident = source["id"]
        pdf_hash = hashlib.sha256((root / "sources" / f"{ident}.pdf").read_bytes()).hexdigest()
        if pdf_hash != acquisition[ident]["sha256"]:
            raise ValueError(f"Changed source PDF: {ident}")
        review = review_map[ident]
        pages = read_json(root / "extracted" / f"{ident}.pages.json")
        unique(pages, "pdf_page", f"{ident} extracted page IDs")
        include_first, include_last = extraction[ident]["included_pages"]
        if {page["pdf_page"] for page in pages} != set(range(include_first, include_last + 1)):
            raise ValueError(f"Missing or extra extracted pages: {ident}")
        page_map = {page["pdf_page"]: page for page in pages}
        sample = sample_map[ident]
        if sample["source_sha256"] != pdf_hash:
            raise ValueError(f"Stale rendered sample: {ident}")
        if hashlib.sha256((root / sample["image"]).read_bytes()).hexdigest() != sample["image_sha256"]:
            raise ValueError(f"Changed rendered sample: {ident}")
        main = []
        for page in pages:
            if review["main_pages"][0] <= page["pdf_page"] <= review["main_pages"][1]:
                copy = dict(page)
                copy["text"] = re.split(r"(?mi)^\s*(?:references|bibliography|literature cited)\s*$",
                                        copy["text"], maxsplit=1)[0]
                copy["normalized_text"] = normalize(copy["text"])
                main.append(copy)
        paper = {**source, **{key: value for key, value in review.items() if key != "observations"},
                 "source_url": acquisition[ident]["requested_url"], "source_sha256": pdf_hash,
                 "pdf_pages": extraction[ident]["pdf_pages"],
                 "included_pages": extraction[ident]["included_pages"],
                 "analyzable_pages": extraction[ident]["analyzable_pages"],
                 "extracted_words": extraction[ident]["extracted_words"],
                 "manual_review_mode": "selected substantive passages, not entire listed pages",
                 "manual_review_status": "completed_passage_review",
                 "visual_inspected": True, "visual_page": sample["pdf_page"],
                 "visual_observation": visual[ident], "quotations": [],
                 "typography_samples": extraction[ident]["sampled_typography"]}
        papers.append(paper)
        for index, (page, area, finding) in enumerate(review["observations"], 1):
            text = page_map[page]["text"]
            observations.append({"id": f"{ident}-{index:02}", "paper_id": ident,
                                 "pdf_page": page, "area": area, "finding": finding,
                                 "status": "manual_passage_observation",
                                 "source_sha256": pdf_hash,
                                 "page_sha256": hashlib.sha256(text.encode()).hexdigest()})
        for entry in lexicon:
            hits = phrase_pages(entry["term"], main)
            if hits:
                frequencies.append({"lexicon_id": entry["id"], "paper_id": ident,
                                    "count": sum(hit["count"] for hit in hits), "pages": hits})
    rules = read_json(root / "data/rules.json")["rules"]
    validate(papers, observations, rules, lexicon)
    return {"schema_version": 1, "papers": papers, "observations": observations,
            "rules": rules, "dictionary": lexicon, "literal_frequencies": frequencies,
            "frequency_caution": "Approximate normalized literal matches in declared main pages; math, headers, and extraction artifacts can remain. Not an NLP measure of style or a prescription to use frequent words.",
            "environment": {"python": platform.python_version(), "sqlite": sqlite3.sqlite_version,
                            "platform": platform.platform()}}

def csv_output(path, records, fields):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for record in records:
            writer.writerow({key: json.dumps(value, ensure_ascii=False) if isinstance(value, (list, dict))
                             else value for key, value in record.items()})

def write_database(path, data):
    if path.exists():
        path.unlink()
    with sqlite3.connect(path) as db:
        db.execute("PRAGMA foreign_keys=ON")
        db.executescript("""
            CREATE TABLE papers(id TEXT PRIMARY KEY, title TEXT, year INTEGER, source_url TEXT, payload TEXT);
            CREATE TABLE observations(id TEXT PRIMARY KEY, paper_id TEXT REFERENCES papers(id), pdf_page INTEGER, area TEXT, finding TEXT);
            CREATE TABLE rules(id TEXT PRIMARY KEY, area TEXT, instruction TEXT);
            CREATE TABLE rule_evidence(rule_id TEXT REFERENCES rules(id), observation_id TEXT REFERENCES observations(id), PRIMARY KEY(rule_id, observation_id));
            CREATE TABLE dictionary(id TEXT PRIMARY KEY, term TEXT UNIQUE, category TEXT, meaning TEXT, guardrail TEXT, example TEXT);
            CREATE TABLE literal_frequency(lexicon_id TEXT REFERENCES dictionary(id), paper_id TEXT REFERENCES papers(id), count INTEGER, pages TEXT, PRIMARY KEY(lexicon_id,paper_id));
            CREATE VIRTUAL TABLE search USING fts5(id UNINDEXED, kind UNINDEXED, text);
        """)
        for paper in data["papers"]:
            db.execute("INSERT INTO papers VALUES(?,?,?,?,?)", (paper["id"], paper["title"], paper["year"], paper["source_url"], json.dumps(paper)))
            db.execute("INSERT INTO search VALUES(?,?,?)", (paper["id"], "paper", paper["title"] + " " + paper["synthesis"]))
        for item in data["observations"]:
            db.execute("INSERT INTO observations VALUES(?,?,?,?,?)", tuple(item[key] for key in ("id", "paper_id", "pdf_page", "area", "finding")))
            db.execute("INSERT INTO search VALUES(?,?,?)", (item["id"], "observation", item["area"] + " " + item["finding"]))
        for rule in data["rules"]:
            db.execute("INSERT INTO rules VALUES(?,?,?)", (rule["id"], rule["area"], rule["instruction"]))
            db.executemany("INSERT INTO rule_evidence VALUES(?,?)", [(rule["id"], evidence) for evidence in rule["evidence"]])
            db.execute("INSERT INTO search VALUES(?,?,?)", (rule["id"], "rule", rule["area"] + " " + rule["instruction"]))
        for item in data["dictionary"]:
            db.execute("INSERT INTO dictionary VALUES(?,?,?,?,?,?)", tuple(item[key] for key in ("id", "term", "category", "meaning", "guardrail", "original_example")))
            db.execute("INSERT INTO search VALUES(?,?,?)", (item["id"], "dictionary", " ".join(item[key] for key in ("term", "meaning", "guardrail", "original_example"))))
        for item in data["literal_frequencies"]:
            db.execute("INSERT INTO literal_frequency VALUES(?,?,?,?)", (item["lexicon_id"], item["paper_id"], item["count"], json.dumps(item["pages"])))
        if db.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("Database foreign keys failed")

def build():
    data = compile_data()
    output = ROOT / "database"
    output.mkdir(exist_ok=True)
    (output / "writing_database.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    write_database(output / "writing_database.sqlite", data)
    csv_output(output / "papers.csv", data["papers"], ["id", "title", "year", "authors", "genre", "publication", "version", "source_url", "source_sha256", "main_pages", "read_pages", "manual_review_status", "visual_page", "synthesis"])
    csv_output(output / "observations.csv", data["observations"], ["id", "paper_id", "pdf_page", "area", "finding", "source_sha256", "page_sha256"])
    csv_output(output / "dictionary.csv", data["dictionary"], ["id", "term", "category", "meaning", "guardrail", "original_example", "entry_kind"])
    csv_output(output / "rules.csv", data["rules"], ["id", "area", "instruction", "evidence"])
    csv_output(output / "literal_frequencies.csv", data["literal_frequencies"], ["lexicon_id", "paper_id", "count", "pages"])
    cards = ROOT / "reviews"
    cards.mkdir(exist_ok=True)
    lines = ["# Paper Catalogue", "", "PDF pages refer to exact downloaded versions. Main-page ranges delimit computational text samples, not a claim that every page was read. Manual review covers selected passages on the listed pages. All sources were hash-checked.", "", "| ID | Paper | Year / genre | Exact source version |", "|---|---|---|---|"]
    gallery = ["# Rendered Sample Gallery", "", "Local copyrighted page images for this review only. One sample per paper, not a whole-document visual audit.", ""]
    for paper in data["papers"]:
        ident = paper["id"]
        lines.append(f"| [{ident}](reviews/{ident}.md) | [{paper['title']}]({paper['source_url']}) | {paper['year']} / {paper['genre']} | {paper['version']} |")
        card = [f"# {ident}: {paper['title']}", "", ", ".join(paper["authors"]), "", f"**Source:** [{paper['publication']} / author PDF]({paper['source_url']})", f"**Version:** {paper['version']}", f"**SHA-256:** `{paper['source_sha256']}`", f"**Declared main pages:** {paper['main_pages'][0]}-{paper['main_pages'][1]}", f"**Manual passage sample:** {', '.join(map(str,paper['read_pages']))}", "", "## Exposition Assessment", paper["synthesis"], "", "## Page-Linked Observations"]
        for observation in data["observations"]:
            if observation["paper_id"] == ident:
                card.append(f"- `{observation['id']}` / PDF p{observation['pdf_page']} / {observation['area']}: {observation['finding']}")
        card.extend(["", "## Rendered Sample", f"PDF p{paper['visual_page']}: {paper['visual_observation']}", "", "## Review Boundary", "Selected passages and one rendered page were examined. This does not certify all prose, appendices, proofs, empirical claims, or the author's individual contribution to coauthored wording. Numerical results were not re-estimated."])
        (cards / f"{ident}.md").write_text("\n".join(card) + "\n")
        gallery.extend([f"## {ident}, PDF p{paper['visual_page']}", f"![{ident} selected page](visual_review/{ident}-p{paper['visual_page']}.png)", paper["visual_observation"], ""])
    (ROOT / "catalogue.md").write_text("\n".join(lines) + "\n")
    (ROOT / "GALLERY.md").write_text("\n".join(gallery) + "\n")
    dictionary = ["# Economic Writing Dictionary", "", "This is the curated explanatory dictionary, not a list of automatically approved publication words. Apply [Corpus-restricted writing](VOCABULARY_POLICY.md) and check [term attestation](vocabulary/curated_dictionary_attestation.csv). Some entries are useful private editing labels or necessary technical distinctions whose wording does not occur in the corpus; they require substitution or a justified exception in future research prose.", "", f"{len(data['dictionary'])} entries are recommended usages, not a claim that every phrase appears in every paper. Examples are original and hypothetical, not quotations or new research findings. Literal source matches are separately recorded in the database; frequency is not a writing prescription.", ""]
    for category in dict.fromkeys(item["category"] for item in data["dictionary"]):
        dictionary.extend(["## " + category.title(), ""])
        for item in data["dictionary"]:
            if item["category"] == category:
                dictionary.extend(["### " + item["term"], item["meaning"], "", "**Use carefully:** " + item["guardrail"], "", "**Example:** " + item["original_example"], ""])
    (ROOT / "DICTIONARY.md").write_text("\n".join(dictionary) + "\n")
    evidence_map = {item["id"]: item for item in data["observations"]}
    register = ["# Evidence-Linked Writing Rules", "",
        "Recommendations derived from selected examples, not universal author practices. Each link names an original-paraphrase observation and its exact PDF page. The paper card links to the source version.", ""]
    for rule in data["rules"]:
        register.extend([f"## {rule['id']}: {rule['area']}", rule["instruction"], ""])
        for ident in rule["evidence"]:
            item = evidence_map[ident]
            register.append(f"- [{ident}, PDF p{item['pdf_page']}](reviews/{item['paper_id']}.md): {item['finding']}")
        register.append("")
    (ROOT / "RULES.md").write_text("\n".join(register) + "\n")
    counts = {"papers": len(data["papers"]), "observations": len(data["observations"]), "rules": len(data["rules"]), "dictionary_entries": len(data["dictionary"]), "raw_pdf_pages": sum(p["pdf_pages"] for p in data["papers"]), "included_pdf_pages": sum(p["analyzable_pages"] for p in data["papers"]), "manually_sampled_pages": sum(len(set(p["read_pages"])) for p in data["papers"]), "visual_pages": len(data["papers"]), "literal_frequency_records": len(data["literal_frequencies"])}
    receipt = {"counts": counts, "environment": data["environment"], "source_hashes_verified": True, "reviewed_extract_hashes_verified": True, "visual_hashes_verified": True, "page_references_verified": True, "rule_links_verified": True, "source_quotations_reproduced": 0, "no_research_documents_modified_by_builder": True}
    (output / "BUILD_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(counts, indent=2))

def search(query, limit):
    with sqlite3.connect(ROOT / "database/writing_database.sqlite") as db:
        rows = db.execute("SELECT id, kind, snippet(search,2,'[',']','...',28) FROM search WHERE search MATCH ? ORDER BY rank LIMIT ?", (query, limit)).fetchall()
    for ident, kind, result in rows:
        print(f"{ident} ({kind}): {result}")

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build")
    sub.add_parser("validate")
    sub.add_parser("freeze-evidence")
    query = sub.add_parser("search")
    query.add_argument("query")
    query.add_argument("--limit", type=int, default=15)
    args = parser.parse_args()
    if args.command == "build":
        build()
    elif args.command == "freeze-evidence":
        freeze_evidence()
    elif args.command == "validate":
        data = compile_data()
        print(f"Validated {len(data['papers'])} sources, {len(data['observations'])} observations, and all evidence links")
    else:
        search(args.query, args.limit)

if __name__ == "__main__":
    main()
