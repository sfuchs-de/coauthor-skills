#!/usr/bin/env python3
"""Audit fictional theory prose without changing drafts or previous receipts."""
import argparse
import importlib.util
import json
import re
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("theory08_audit_edition", Path(__file__).with_name("edition.py"))
edition = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(edition)
ROOT = edition.ROOT
RANGES = {"T01": (220,350), "T02": (240,380), "T03": (280,450), "T04": (180,280)}
EDITORIAL = re.compile(r"\b(?:state the restriction here|add interpretation|move this to the appendix|"
                       r"rather than imposing it on all household choices|the reader should|we should rewrite)\b", re.I)


def words(text):
    return re.findall(r"[a-z]+(?:'[a-z]+)?", edition.vocabulary.canonical(text))


def audit(folder, overlap=False):
    paths = sorted(folder.glob("*.tex"))
    new_examples = folder.resolve().parent == (ROOT / "evaluation").resolve() and folder.name in {"first", "final"}
    inventory = edition.records()
    rows, windows = [], {}
    for path in paths:
        text = path.read_text()
        cleaned = edition.vocabulary.prose_text(text, ".tex")
        tokens = words(cleaned)
        result = edition.inspect(text, ".tex", inventory=inventory)
        row = {"id": path.stem, "sha256": edition.digest(path), "vocabulary": result,
               "prose_words": len(tokens), "editorial_command_flags": EDITORIAL.findall(cleaned),
               "requested_range": list(RANGES[path.stem]) if new_examples and path.stem in RANGES else None,
               "source_matches": []}
        row["length_passed"] = RANGES[path.stem][0] <= len(tokens) <= RANGES[path.stem][1] if new_examples and path.stem in RANGES else None
        rows.append(row)
        for start in range(len(tokens)-11):
            windows.setdefault(tuple(tokens[start:start+12]), set()).add(path.stem)
    if overlap:
        by_id = {row["id"]: row for row in rows}
        for paper in edition.all_papers():
            ident = paper["id"]
            pages = edition.load(edition.source_root(ident) / "extracted" / f"{ident}.pages.json")
            for page in pages:
                tokens = words(page["text"])
                matched = set()
                for start in range(len(tokens)-11):
                    matched.update(windows.get(tuple(tokens[start:start+12]), set()))
                for sample in matched:
                    by_id[sample]["source_matches"].append({"paper": ident, "pdf_page": page["pdf_page"]})
    return {"samples": rows, "sample_count": len(rows),
            "lexical_passes": sum(r["vocabulary"]["lexical_gate_passed"] for r in rows),
            "unapproved_occurrences": sum(t["count"] for r in rows for t in r["vocabulary"]["unapproved_terms"]),
            "labels_classified": sum(len(r["vocabulary"]["classified_labels"]) for r in rows),
            "length_passes": sum(r["length_passed"] is True for r in rows),
            "overlap_screen_rerun": overlap,
            "overlap_papers": len(edition.all_papers()) if overlap else None,
            "source_match_pages": sum(len(r["source_matches"]) for r in rows),
            "independent_writing_validation": False,
            "scope": "Fictional examples; lexical/depth flags and 12-word source screen are not scientific certification"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", type=Path, default=ROOT / "evaluation/final")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--overlap", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.output and args.output.exists():
        parser.error("Preserve the existing audit")
    result = audit(args.folder, args.overlap)
    if args.output:
        edition.save(args.output, result)
    if args.json:
        print(json.dumps(result, indent=2))
        return
    print(json.dumps({k:v for k,v in result.items() if k != "samples"}, indent=2))
    for row in result["samples"]:
        print(row["id"], row["prose_words"], [t["word"] for t in row["vocabulary"]["unapproved_terms"]])


if __name__ == "__main__":
    main()
