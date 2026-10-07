#!/usr/bin/env python3
"""Check original urban repairs and optionally screen local full-text overlap."""
import argparse
import collections
import json
from pathlib import Path
import edition


def windows(text):
    words = edition.vocabulary.study.normalize(text).split()
    return {tuple(words[i:i+12]) for i in range(max(0,len(words)-11))}


def audit(sources=False):
    path=edition.ROOT / "WORKED_EXAMPLES.md"
    passages=[line[2:] for line in path.read_text().splitlines() if line.startswith("> ")]
    if len(passages)!=6:
        raise ValueError("Expected six repairs")
    candidates={f"E{i:02d}":windows(v) for i,v in enumerate(passages,1)}
    matches=collections.defaultdict(set)
    if sources:
        needed=set().union(*candidates.values())
        for paper in edition.all_papers():
            for page in edition.load(edition.source_root(paper["id"]) / "extracted" / f"{paper['id']}.pages.json"):
                for phrase in windows(page["text"]) & needed:
                    matches[phrase].add((paper["id"],page["pdf_page"]))
    records=edition.helpers.records()
    policy=edition.load(edition.BASE / "data/vocabulary_policy.json")
    results={}
    for i,value in enumerate(passages,1):
        ident=f"E{i:02d}"
        results[ident]={"text_sha256":edition.helpers.hashlib.sha256(value.encode()).hexdigest(),
            "lexical":edition.vocabulary.inspect_prose(value,".tex",records,policy),
            "exact_12_word_match_pages":sorted({where for phrase in candidates[ident] for where in matches[phrase]}) if sources else None}
    return {"worked_examples_sha256":edition.digest(path),
            "vocabulary_sha256":edition.digest(edition.ROOT / "vocabulary/attested_vocabulary.sqlite"),
            "source_config_sha256":edition.digest(edition.ROOT / "data/sources.json"),
            "policy_sha256":edition.digest(edition.BASE / "data/vocabulary_policy.json"),
            "examples":results,"source_screen_rerun":sources,"independent_review":False,
            "fidelity_review":"Premises and limits checked in WORKED_EXAMPLES.md; editorial review, not inferred from lexical or overlap gates"}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources",action="store_true")
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    report=audit(args.sources)
    if args.output:
        if args.output.exists(): parser.error("Preserve previous receipts")
        edition.save(args.output,report)
    print(json.dumps({"examples":len(report["examples"]),
        "lexical_passes":sum(r["lexical"]["lexical_gate_passed"] for r in report["examples"].values()),
        "unapproved":{k:[w["word"] for w in r["lexical"]["unapproved_terms"]] for k,r in report["examples"].items()},
        "overlap":{k:r["exact_12_word_match_pages"] for k,r in report["examples"].items()}}))


if __name__=="__main__": main()
