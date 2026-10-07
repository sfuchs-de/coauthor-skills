#!/usr/bin/env python3
"""Record lexical, originality, length, and evidence checks separately from ratings."""
import argparse
import collections
import json
import re
import shutil
import sqlite3
import tempfile
from pathlib import Path
import edition

ROOT = edition.ROOT
BASE = edition.BASE


def save_new(path, value):
    if path.exists():
        raise ValueError("Preserve prior audit: choose a new output")
    edition.save(path, value)


def instruction_hashes():
    return {name: edition.digest(ROOT / name) for name in
            ("ARGUMENT_AND_EXPOSITION.md", "WORKED_EXAMPLES.md", "VOCABULARY_POLICY.md")}


def freeze():
    path = ROOT / "evaluation/FREEZE_RECEIPT.json"
    if path.exists():
        raise ValueError("Evaluation already frozen")
    cases = edition.load(ROOT / "evaluation/CASES.json")
    first = ROOT / "evaluation/first-drafts"
    first.mkdir(exist_ok=False)
    for case in cases["cases"]:
        shutil.copyfile(ROOT / "evaluation/samples" / f"{case['id']}.tex", first / f"{case['id']}.tex")
    save_new(path, {"cases_sha256": edition.digest(ROOT / "evaluation/CASES.json"),
                    "instruction_hashes": instruction_hashes(),
                    "first_draft_hashes": {p.name: edition.digest(p) for p in sorted(first.glob("*.tex"))},
                    "sources_config_sha256": edition.digest(ROOT / "data/sources.json"),
                    "independent_generation": False, "independent_review": False,
                    "scope": "Same-context formative exercises; no blind or causal comparison claim"})


def norm_words(text):
    return edition.vocabulary.study.normalize(text).split()


def windows(words, width=12):
    return {tuple(words[i:i+width]) for i in range(max(0, len(words)-width+1))}


def screen(paths):
    candidate = {str(p): windows(norm_words(edition.vocabulary.prose_text(p.read_text(), ".tex"))) for p in paths}
    needed = set().union(*candidate.values())
    matches = collections.defaultdict(set)
    old = edition.load(BASE / "data/sources.json")["papers"]
    new = edition.load(ROOT / "data/sources.json")["papers"]
    for source_root, papers in ((BASE, old), (ROOT, new)):
        for paper in papers:
            for page in edition.load(source_root / "extracted" / f"{paper['id']}.pages.json"):
                present = windows(norm_words(page["text"])) & needed
                for phrase in present:
                    matches[phrase].add((paper["id"], page["pdf_page"]))
    return {p: sorted({where for phrase in phrases for where in matches[phrase]})
            for p, phrases in candidate.items()}


def check_freeze():
    frozen = edition.load(ROOT / "evaluation/FREEZE_RECEIPT.json")
    if edition.digest(ROOT / "evaluation/CASES.json") != frozen["cases_sha256"]:
        raise ValueError("Changed writing brief")
    expected = frozen["instruction_hashes"]
    amendment_path = ROOT / "evaluation/INSTRUCTION_AMENDMENT.json"
    if amendment_path.exists():
        amendment = edition.load(amendment_path)
        if amendment["previous_hashes"] != expected or not amendment.get("reason"):
            raise ValueError("Invalid instruction amendment")
        expected = amendment["current_hashes"]
    if instruction_hashes() != expected:
        raise ValueError("Changed evaluation instructions")
    if edition.digest(ROOT / "data/sources.json") != frozen["sources_config_sha256"]:
        raise ValueError("Changed source configuration")
    for name, expected in frozen["first_draft_hashes"].items():
        if edition.digest(ROOT / "evaluation/first-drafts" / name) != expected:
            raise ValueError("Changed first draft")
    return {**frozen, "instruction_hashes": expected}


def audit(folder, output, sources=False):
    frozen = check_freeze()
    cases = edition.load(ROOT / "evaluation/CASES.json")["cases"]
    if {p.stem for p in folder.glob("*.tex")} != {c["id"] for c in cases}:
        raise ValueError("Missing or unexpected case output")
    paths = sorted(folder.glob("*.tex"))
    matches = screen(paths) if sources else {}
    records = edition.records()
    policy = edition.load(BASE / "data/vocabulary_policy.json")
    result = {}
    for case in cases:
        path = folder / f"{case['id']}.tex"
        text = path.read_text()
        cleaned = edition.vocabulary.prose_text(text, ".tex")
        count = len(re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*", cleaned))
        result[case["id"]] = {"sha256": edition.digest(path),
            "lexical": edition.vocabulary.inspect_prose(text, ".tex", records, policy),
            "words_approximate": count, "requested_range": case["words"],
            "length_passed": case["words"][0] <= count <= case["words"][1],
            "paragraphs_approximate": len([p for p in re.split(r"\n\s*\n", cleaned) if p.strip()]),
            "source_screen_rerun": sources, "exact_12_word_match_pages": matches.get(str(path)),
            "substantive_review": "Separate manual review; not inferred from lexical or length checks"}
    payload = {"cases": result, "cases_sha256": frozen["cases_sha256"],
               "instruction_hashes": frozen["instruction_hashes"],
               "vocabulary_sha256": edition.digest(ROOT / "vocabulary/attested_vocabulary.sqlite"),
               "policy_sha256": edition.digest(BASE / "data/vocabulary_policy.json"),
               "independent_generation": False, "independent_review": False}
    save_new(output, payload)
    print(json.dumps({"cases": len(result), "lexical_passes": sum(v["lexical"]["lexical_gate_passed"] for v in result.values()),
                      "issues": {k: [w["word"] for w in v["lexical"]["unapproved_terms"]] for k, v in result.items()},
                      "lengths": {k: v["words_approximate"] for k, v in result.items()},
                      "source_matches": {k: v["exact_12_word_match_pages"] for k, v in result.items()}}, indent=2))


def examples(output, sources=False):
    check_freeze()
    path = ROOT / "WORKED_EXAMPLES.md"
    passages = [line[2:] for line in path.read_text().splitlines() if line.startswith("> ")]
    if len(passages) != 10:
        raise ValueError("Expected ten revised worked examples")
    with tempfile.TemporaryDirectory() as temporary:
        files = []
        for i, text in enumerate(passages, 1):
            target = Path(temporary) / f"E{i:02d}.tex"
            target.write_text(text)
            files.append(target)
        matches = screen(files) if sources else {}
        words = edition.records()
        policy = edition.load(BASE / "data/vocabulary_policy.json")
        result = {p.stem: {"sha256": edition.digest(p),
                 "lexical": edition.vocabulary.inspect_prose(p.read_text(), ".tex", words, policy),
                 "exact_12_word_match_pages": matches.get(str(p))} for p in files}
    save_new(output, {"worked_examples_sha256": edition.digest(path), "source_screen_rerun": sources,
                      "examples": result, "independent_review": False})
    print(json.dumps({"examples": len(result), "lexical_passes": sum(r["lexical"]["lexical_gate_passed"] for r in result.values()),
                      "source_match_cases": sum(bool(r["exact_12_word_match_pages"]) for r in result.values())}))


def summarize(output):
    check_freeze()
    ratings = edition.load(ROOT / "evaluation/RATINGS.json")
    checked = edition.load(ROOT / "evaluation/CHECKED_AUDIT.json")
    example_report = edition.load(ROOT / "evaluation/EXAMPLE_AUDIT.json")
    expected = {case["id"] for case in edition.load(ROOT / "evaluation/CASES.json")["cases"]}
    if {row["id"] for row in ratings["cases"]} != expected or len(ratings["cases"]) != len(expected):
        raise ValueError("Incomplete or duplicate ratings")
    means, cases = [], {}
    for row in ratings["cases"]:
        ident = row["id"]
        path = ROOT / "evaluation/samples" / f"{ident}.tex"
        check = checked["cases"][ident]
        if edition.digest(path) != check["sha256"]:
            raise ValueError("Ratings refer to an unchecked sample")
        values = [value for value in row["scores"].values() if value is not None]
        if not values or any(not 0 <= value <= 4 or value * 2 != int(value * 2) for value in values):
            raise ValueError("Invalid editorial scale")
        score = sum(values) / len(values) * 2.5
        means.append(score)
        cases[ident] = {"sample_sha256": check["sha256"], "scores": row["scores"],
                        "self_rating_10": score, "fidelity_passed": row["fidelity_passed"],
                        "lexical_passed": check["lexical"]["lexical_gate_passed"],
                        "length_passed": check["length_passed"], "words": check["words_approximate"]}
    save_new(output, {"ratings_sha256": edition.digest(ROOT / "evaluation/RATINGS.json"),
        "checked_audit_sha256": edition.digest(ROOT / "evaluation/CHECKED_AUDIT.json"),
        "example_audit_sha256": edition.digest(ROOT / "evaluation/EXAMPLE_AUDIT.json"),
        "cases": cases, "equal_case_mean_self_rating_10": sum(means) / len(means),
        "short_example_lexical_passes": sum(r["lexical"]["lexical_gate_passed"] for r in example_report["examples"].values()),
        "independent_generation": False, "independent_review": False,
        "scope": "Hash-bound same-context editorial self-review; not a causal improvement or author-similarity estimate"})
    samples = ROOT / "evaluation/SAMPLES.md"
    if samples.exists():
        raise ValueError("Preserve the existing sample reader")
    sections = ["# Connected Writing Examples", "",
                "Original fictional exercises, not BCN results or text copied from the corpus. "
                "The first drafts and repairs are preserved. These are revised examples, not evidence "
                "of reliable first-pass generation or independent validation.", ""]
    for case in edition.load(ROOT / "evaluation/CASES.json")["cases"]:
        sections.extend([f"## {case['id']}", "", (ROOT / "evaluation/samples" / f"{case['id']}.tex").read_text(), ""])
    samples.write_text("\n".join(sections))
    print(json.dumps({"self_rating_10": sum(means) / len(means), "cases": len(cases), "independent_review": False}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["freeze", "audit", "examples", "summarize"])
    parser.add_argument("--samples", type=Path, default=ROOT / "evaluation/samples")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--sources", action="store_true", help="Full local sources required; not included in package")
    args = parser.parse_args()
    if args.command == "freeze":
        freeze()
    else:
        if not args.output:
            parser.error("Choose a new output receipt")
        if args.command == "summarize":
            summarize(args.output.resolve())
        elif args.command == "examples":
            examples(args.output.resolve(), args.sources)
        else:
            audit(args.samples.resolve(), args.output.resolve(), args.sources)


if __name__ == "__main__":
    main()
