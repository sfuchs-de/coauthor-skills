#!/usr/bin/env python3
"""Index all extractable word forms and check draft prose against this corpus."""
import argparse
import collections
import csv
import hashlib
import json
import re
import sqlite3
import sys
import unicodedata
from pathlib import Path
import study

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "vocabulary"
LETTER = r"[^\W\d_]"
WORD = rf"{LETTER}+(?:['\u2019]{LETTER}+)*(?:[-\u2010\u2011]{LETTER}+(?:['\u2019]{LETTER}+)*)*"
TOKEN = re.compile(rf"(?P<broken>{LETTER}+-[ \t]*\n[ \t]*{LETTER}+)|(?P<word>{WORD})", re.UNICODE)
REFERENCE = re.compile(r"(?mi)^\s*(?:references|bibliography|literature cited)\s*$")

def canonical(word):
    word = word.replace("\u2019", "'").replace("\u2010", "-").replace("\u2011", "-")
    word = unicodedata.normalize("NFKD", word.casefold())
    return "".join(char for char in word if not unicodedata.combining(char))

def tokenize(text, solid_forms=frozenset()):
    for match in TOKEN.finditer(text):
        if match.group("broken"):
            left, right = re.split(r"-[ \t]*\n[ \t]*", match.group())
            fused, compound = canonical(left + right), canonical(left + "-" + right)
            if fused in solid_forms:
                units = [(left + right, match.start(), "reconstructed")]
            elif compound in solid_forms:
                units = [(left + "-" + right, match.start(), "reconstructed")]
            else:
                units = [(left, match.start(), "linebreak_fragment"),
                         (right, match.end() - len(right), "linebreak_fragment")]
        else:
            units = [(match.group(), match.start(), "unbroken")]
        for form, offset, evidence_kind in units:
            yield {"form": form, "word": canonical(form), "offset": offset,
                   "kind": "compound" if "-" in canonical(form) else "word",
                   "evidence_kind": evidence_kind}
            if "-" in canonical(form):
                for component in form.replace("\u2010", "-").replace("\u2011", "-").split("-"):
                    yield {"form": component, "word": canonical(component), "offset": offset,
                           "kind": "word", "evidence_kind": "compound_component"}

def index_pages(papers, pages_by_paper):
    solid = set()
    for pages in pages_by_paper.values():
        for page in pages:
            solid.update(token["word"] for token in tokenize(page["text"])
                         if token["evidence_kind"] != "linebreak_fragment")
    records, occurrences = {}, collections.Counter()
    for paper in papers:
        for page in pages_by_paper[paper["id"]]:
            main = paper["main_pages"][0] <= page["pdf_page"] <= paper["main_pages"][1]
            boundary = REFERENCE.search(page["text"])
            for token in tokenize(page["text"], solid):
                scope = "main_range" if main and (not boundary or token["offset"] < boundary.start()) else "other_pages"
                word = token["word"]
                item = records.setdefault(word, {"word": word, "kind": token["kind"],
                    "full_count": 0, "main_count": 0, "solid_count": 0,
                    "standalone_count": 0, "variants": collections.Counter(), "papers": set()})
                item["full_count"] += 1
                item["main_count"] += scope == "main_range"
                item["solid_count"] += token["evidence_kind"] != "linebreak_fragment"
                item["standalone_count"] += token["evidence_kind"] == "unbroken"
                item["variants"][token["form"]] += 1
                item["papers"].add(paper["id"])
                occurrences[(word, paper["id"], page["pdf_page"], scope, token["evidence_kind"])] += 1
    output = []
    for word, item in sorted(records.items()):
        flags = []
        non_latin = any(char.isalpha() and char not in "abcdefghijklmnopqrstuvwxyz" for char in word)
        if non_latin or not re.search(r"[a-z]", word) or (len(word) == 1 and word not in ("a", "i")):
            status = "symbol_or_nonEnglish"
        elif not item["solid_count"]:
            status = "extraction_fragment"
        else:
            status = "main_text_attested" if item["main_count"] else "other_pages_attested"
        if item["full_count"] == 1:
            flags.append("single_occurrence")
        if all(form.isupper() for form in item["variants"]):
            flags.append("uppercase_only_check_name_or_notation")
        if not item["standalone_count"]:
            flags.append("no_unbroken_standalone_form")
        output.append({**item, "status": status, "flags": flags,
                       "paper_count": len(item["papers"]), "papers": sorted(item["papers"]),
                       "variants": dict(sorted(item["variants"].items()))})
    locations = [{"word": word, "paper_id": paper, "pdf_page": page, "scope": scope,
                  "evidence_kind": kind, "count": count}
                 for (word, paper, page, scope, kind), count in sorted(occurrences.items())]
    return output, locations

def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def build():
    data = study.compile_data()
    pages = {paper["id"]: study.read_json(ROOT / "extracted" / f"{paper['id']}.pages.json")
             for paper in data["papers"]}
    words, locations = index_pages(data["papers"], pages)
    OUTPUT.mkdir(exist_ok=True)
    source_hashes = {paper["id"]: paper["source_sha256"] for paper in data["papers"]}
    counts = {"papers": len(data["papers"]), "included_pages": sum(len(p) for p in pages.values()),
              "normalized_forms": len(words), "word_forms": sum(w["kind"] == "word" for w in words),
              "compound_forms": sum(w["kind"] == "compound" for w in words),
              "attested_writing_forms": sum(w["status"].endswith("attested") for w in words),
              "status_counts": dict(collections.Counter(w["status"] for w in words)),
              "source_page_records": len(locations)}
    payload = {"schema_version": 1, "counts": counts, "source_sha256": source_hashes,
        "coverage": "Every included extracted page, not only manually sampled passages. Main-range tags are page/heading approximations, not perfect prose classification.",
        "normalization": "Case and accents folded; apostrophe variants unified; Unicode ligatures decomposed. No stemming or free inflection allowance. Hyphen-line breaks joined only with independent unbroken attestation; uncertain fragments retained but not licensed.",
        "limitations": "Exhaustive relative to extractable alphabetic forms, not error-free PDF recognition or semantic definitions. Math, names, and bibliography can contribute tokens. Occurrence is not endorsement or permission for a new concept.",
        "words": words, "occurrences": locations}
    (OUTPUT / "attested_vocabulary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    study.csv_output(OUTPUT / "words.csv", words, ["word", "kind", "status", "full_count", "main_count", "solid_count", "standalone_count", "paper_count", "papers", "variants", "flags"])
    study.csv_output(OUTPUT / "occurrences.csv", locations, ["word", "paper_id", "pdf_page", "scope", "evidence_kind", "count"])
    database = OUTPUT / "attested_vocabulary.sqlite"
    if database.exists():
        database.unlink()
    with sqlite3.connect(database) as db:
        db.execute("PRAGMA foreign_keys=ON")
        db.executescript("""
            CREATE TABLE words(word TEXT PRIMARY KEY, kind TEXT, status TEXT, full_count INTEGER, main_count INTEGER, solid_count INTEGER, standalone_count INTEGER, paper_count INTEGER, variants TEXT, flags TEXT);
            CREATE TABLE occurrences(word TEXT REFERENCES words(word), paper_id TEXT, pdf_page INTEGER, scope TEXT, evidence_kind TEXT, count INTEGER, PRIMARY KEY(word,paper_id,pdf_page,scope,evidence_kind));
            CREATE INDEX by_paper_page ON occurrences(paper_id,pdf_page);
            CREATE TABLE metadata(key TEXT PRIMARY KEY, value TEXT);
        """)
        db.executemany("INSERT INTO words VALUES(?,?,?,?,?,?,?,?,?,?)", [
            (w["word"], w["kind"], w["status"], w["full_count"], w["main_count"], w["solid_count"],
             w["standalone_count"], w["paper_count"], json.dumps(w["variants"]), json.dumps(w["flags"])) for w in words])
        db.executemany("INSERT INTO occurrences VALUES(?,?,?,?,?,?)", [tuple(o[k] for k in ("word", "paper_id", "pdf_page", "scope", "evidence_kind", "count")) for o in locations])
        db.executemany("INSERT INTO metadata VALUES(?,?)", [(key, json.dumps(payload[key])) for key in ("schema_version", "counts", "source_sha256", "coverage", "normalization", "limitations")])
        if db.execute("PRAGMA foreign_key_check").fetchall() or db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("Vocabulary database integrity failed")
        for row in db.execute("SELECT w.word FROM words w JOIN occurrences o USING(word) GROUP BY w.word HAVING w.full_count != sum(o.count)"):
            raise ValueError(f"Unreconciled occurrence count: {row[0]}")
    by_word = {w["word"]: w for w in words}
    frequencies = collections.Counter()
    for match in data["literal_frequencies"]:
        frequencies[match["lexicon_id"]] += match["count"]
    attestation = []
    for item in data["dictionary"]:
        terms = {t["word"] for t in tokenize(item["term"]) if t["kind"] == "word"}
        unattested = sorted(t for t in terms if t not in by_word or not by_word[t]["status"].endswith("attested"))
        attestation.append({"id": item["id"], "term": item["term"],
            "main_literal_phrase_count": frequencies[item["id"]], "unattested_component_words": unattested,
            "instruction": "Editorial vocabulary; not automatically publication vocabulary" if unattested or not frequencies[item["id"]] else "Attested phrase; verify economic context"})
    study.csv_output(OUTPUT / "curated_dictionary_attestation.csv", attestation, ["id", "term", "main_literal_phrase_count", "unattested_component_words", "instruction"])
    lines = ["# Corpus Vocabulary Inventory", "", f"{counts['normalized_forms']:,} normalized forms from all {counts['included_pages']:,} included extracted pages. This is an exhaustive index of this extraction, not a claim that every form is clean prose or that every word has been given a semantic definition.", "", "The curated usage dictionary remains separate. No inflections are added merely because a related form occurs. Plain main-text usage is preferred; source attestation does not establish context or authorize new technical concepts.", "", "## Status Counts", ""]
    lines.extend(f"- `{status}`: {count:,}" for status, count in sorted(counts["status_counts"].items()))
    lines.extend(["", "## Files", "", "- [Word list and counts](words.csv)", "- [Every source-page occurrence](occurrences.csv)", "- [SQLite lookup](attested_vocabulary.sqlite)", "- [Full JSON](attested_vocabulary.json)", "- [Curated dictionary attestation](curated_dictionary_attestation.csv)", "", "## Most Frequent Main-Range Forms", "", "Frequency is not an instruction to repeat these words. Single-letter forms are omitted below, but retained in the inventory.", "", "| Form | Main count | Papers |", "|---|---:|---:|"])
    for w in sorted((w for w in words if w["status"] == "main_text_attested" and len(w["word"]) > 1 and w["kind"] == "word"), key=lambda w: (-w["main_count"], w["word"]))[:100]:
        lines.append(f"| {w['word']} | {w['main_count']:,} | {w['paper_count']} |")
    (OUTPUT / "README.md").write_text("\n".join(lines) + "\n")
    outputs = [OUTPUT / filename for filename in ("words.csv", "occurrences.csv", "attested_vocabulary.json", "attested_vocabulary.sqlite", "curated_dictionary_attestation.csv", "README.md")]
    input_paths = ["data/sources.json", "data/acquisition.json", "data/extraction.json", "data/reviews.json", "data/reviews_middle.json", "data/reviews_redding.json", "data/review_amendments.json", "data/dictionary.tsv", "scripts/study.py", "scripts/vocabulary.py"]
    receipt = {"counts": counts, "source_sha256": source_hashes, "evidence_manifest_sha256": file_hash(ROOT / "data/review_inputs.json"),
               "input_sha256": {path: file_hash(ROOT / path) for path in input_paths},
               "extracted_hashes_verified": True, "sqlite_integrity": "ok", "occurrence_totals_verified": True,
               "output_sha256": {p.name: file_hash(p) for p in outputs}, "network_used": False}
    (OUTPUT / "BUILD_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(counts, indent=2))

def verify():
    receipt = study.read_json(OUTPUT / "BUILD_RECEIPT.json")
    if file_hash(ROOT / "data/review_inputs.json") != receipt["evidence_manifest_sha256"]:
        raise ValueError("Changed corpus evidence manifest")
    study.verify_evidence(ROOT)
    for path, expected in receipt["input_sha256"].items():
        if file_hash(ROOT / path) != expected:
            raise ValueError(f"Changed vocabulary input: {path}")
    config = study.read_json(ROOT / "data/sources.json")["papers"]
    if set(receipt["source_sha256"]) != {paper["id"] for paper in config}:
        raise ValueError("Incompatible corpus")
    for ident, expected in receipt["source_sha256"].items():
        if file_hash(ROOT / "sources" / f"{ident}.pdf") != expected:
            raise ValueError(f"Changed corpus PDF: {ident}")
    for filename, expected in receipt["output_sha256"].items():
        if file_hash(OUTPUT / filename) != expected:
            raise ValueError(f"Changed vocabulary output: {filename}")
    with sqlite3.connect(f"file:{OUTPUT / 'attested_vocabulary.sqlite'}?mode=ro", uri=True) as db:
        if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok" or db.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("Vocabulary database integrity failed")
        totals = db.execute("SELECT count(*) FROM words").fetchone()[0]
        locations = db.execute("SELECT count(*) FROM occurrences").fetchone()[0]
        if totals != receipt["counts"]["normalized_forms"] or locations != receipt["counts"]["source_page_records"]:
            raise ValueError("Vocabulary row-count mismatch")
        discrepant = db.execute("""SELECT w.word FROM words w JOIN occurrences o USING(word)
            GROUP BY w.word HAVING w.full_count != sum(o.count)
            OR w.main_count != sum(CASE WHEN o.scope='main_range' THEN o.count ELSE 0 END)
            OR w.solid_count != sum(CASE WHEN o.evidence_kind!='linebreak_fragment' THEN o.count ELSE 0 END)
            OR w.standalone_count != sum(CASE WHEN o.evidence_kind='unbroken' THEN o.count ELSE 0 END)
            OR w.paper_count != count(DISTINCT o.paper_id)""").fetchall()
        if discrepant:
            raise ValueError("Vocabulary counts do not reconcile with page evidence")
    csv_counts = {}
    with (ROOT / "data/dictionary.tsv").open(newline="") as handle:
        dictionary_count = sum(1 for _ in csv.DictReader(handle, delimiter="\t"))
    for filename, expected in (("words.csv", totals), ("occurrences.csv", locations), ("curated_dictionary_attestation.csv", dictionary_count)):
        with (OUTPUT / filename).open(newline="") as handle:
            csv_counts[filename] = sum(1 for _ in csv.DictReader(handle))
        if csv_counts[filename] != expected:
            raise ValueError(f"Vocabulary CSV mismatch: {filename}")
    result = {"all_output_hashes_verified": True, "source_hashes_verified": True,
              "sqlite_integrity": "ok", "page_counts_reconciled": True, "csv_counts": csv_counts,
              "network_used": False}
    (OUTPUT / "VERIFY_RECEIPT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

def mask(match):
    return "".join("\n" if c == "\n" else " " for c in match.group())

def prose_text(text, suffix):
    if suffix == ".tex":
        text = re.sub(r"(?m)(?<!\\)%[^\n]*", mask, text)
        text = re.sub(r"\\begin\{(equation\*?|align\*?|gather\*?|multline\*?|displaymath|math|tikzpicture|verbatim|lstlisting)\}.*?\\end\{\1\}", mask, text, flags=re.S)
        text = re.sub(r"\\\[.*?\\\]|\\\(.*?\\\)|(?<!\\)\$\$.*?(?<!\\)\$\$|(?<!\\)\$[^$]*?(?<!\\)\$", mask, text, flags=re.S)
        text = re.sub(r"\\(?:cite\w*|ref|eqref|label|input|include|includegraphics|bibliography|bibliographystyle|url)(?:\[[^\]]*\])*\{[^}]*\}", mask, text)
        text = re.sub(r"\\href\{[^}]*\}", mask, text)
        text = re.sub(r"\\(?:begin|end)\{[^}]*\}", mask, text)
        text = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", mask, text)
    else:
        text = re.sub(r"```.*?```|~~~.*?~~~|`[^`\n]+`", mask, text, flags=re.S)
        text = re.sub(r"\]\([^)]*\)", mask, text)
    text = re.sub(r"https?://\S+", mask, text)
    return text

def exceptions_from(policy):
    entries = policy.get("exceptions", [])
    study.unique(entries, "term", "vocabulary exceptions")
    approved = {}
    for entry in entries:
        if entry.get("status") == "approved":
            if not all(isinstance(entry.get(k), str) and entry[k].strip() for k in ("term", "necessity", "why_no_attested_alternative", "approved_by")):
                raise ValueError("Approved exception lacks a necessity/alternative/approval record")
            if TOKEN.fullmatch(entry["term"]) is None:
                raise ValueError("Record exceptions as individual words or compounds")
            key = canonical(entry["term"])
            if key in approved:
                raise ValueError("Duplicate normalized vocabulary exception")
            approved[key] = entry
    return approved

def inspect_prose(text, suffix, vocabulary, policy):
    approved = exceptions_from(policy)
    cleaned = prose_text(text, suffix)
    solid = {word for word, item in vocabulary.items() if item["solid_count"]}
    issues, warnings, exceptions_used = {}, {}, set()
    checked = 0
    for token in tokenize(cleaned, solid):
        if token["evidence_kind"] == "compound_component":
            continue
        checked += 1
        word = token["word"]
        line = cleaned.count("\n", 0, token["offset"]) + 1
        if word in approved:
            exceptions_used.add(word)
            continue
        item = vocabulary.get(word)
        if item is None or not item["status"].endswith("attested"):
            issue = issues.setdefault(word, {"word": word, "form": token["form"], "reason": "unattested" if item is None else item["status"], "count": 0, "lines": []})
            issue["count"] += 1
            if line not in issue["lines"]:
                issue["lines"].append(line)
        elif item["status"] == "other_pages_attested" or item["flags"]:
            warnings[word] = {"word": word, "status": item["status"], "flags": item["flags"], "main_count": item["main_count"]}
    return {"checked_tokens": checked, "unapproved_terms": sorted(issues.values(), key=lambda x: (-x["count"], x["word"])),
            "context_review": sorted(warnings.values(), key=lambda x: x["word"]), "approved_exceptions_used": sorted(exceptions_used),
            "lexical_gate_passed": not issues, "scope": "Target-file prose only; not an expanded TeX dependency graph or a semantic/math audit. Math, citations, links, comments, and code are excluded; unfamiliar TeX macros need manual review."}

def lookup(word):
    with sqlite3.connect(f"file:{OUTPUT / 'attested_vocabulary.sqlite'}?mode=ro", uri=True) as db:
        key = canonical(word)
        row = db.execute("SELECT word,status,full_count,main_count,paper_count,flags FROM words WHERE word=?", (key,)).fetchone()
        if row is None:
            print(f"Not attested: {word}")
            return
        print(json.dumps(dict(zip(("word", "status", "full_count", "main_count", "paper_count", "flags"), row)), indent=2))
        for result in db.execute("SELECT paper_id,pdf_page,scope,evidence_kind,count FROM occurrences WHERE word=? ORDER BY scope,paper_id,pdf_page LIMIT 20", (key,)):
            print(f"{result[0]} PDF p{result[1]} / {result[2]} / {result[3]} / {result[4]}")

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build")
    sub.add_parser("verify")
    get = sub.add_parser("lookup")
    get.add_argument("word")
    check = sub.add_parser("check")
    check.add_argument("file", type=Path)
    check.add_argument("--policy", type=Path, default=ROOT / "data/vocabulary_policy.json")
    check.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    if args.command == "build":
        build()
    elif args.command == "verify":
        verify()
    elif args.command == "lookup":
        lookup(args.word)
    else:
        receipt = study.read_json(OUTPUT / "BUILD_RECEIPT.json")
        database = OUTPUT / "attested_vocabulary.sqlite"
        if file_hash(database) != receipt["output_sha256"][database.name]:
            raise ValueError("Changed vocabulary export")
        with sqlite3.connect(f"file:{database}?mode=ro", uri=True) as db:
            records = {word: {"solid_count": solid, "status": status, "flags": json.loads(flags), "main_count": main}
                       for word, solid, status, flags, main in db.execute("SELECT word,solid_count,status,flags,main_count FROM words")}
        result = inspect_prose(args.file.read_text(), args.file.suffix.lower(), records, study.read_json(args.policy))
        result.update({"file": str(args.file.resolve()), "file_sha256": file_hash(args.file), "vocabulary_sha256": receipt["output_sha256"][database.name],
                       "policy_sha256": file_hash(args.policy), "checker_sha256": file_hash(Path(__file__))})
        print(json.dumps(result, indent=2))
        if args.strict and not result["lexical_gate_passed"]:
            sys.exit(1)

if __name__ == "__main__":
    main()
