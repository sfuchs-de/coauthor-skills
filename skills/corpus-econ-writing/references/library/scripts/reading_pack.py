#!/usr/bin/env python3
"""Addressable excerpts for qualitative review, never an automatic review verdict."""

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def headings(pages):
    results = []
    for page in pages:
        lines = page["text"].splitlines()
        for index, line in enumerate(lines):
            stripped = line.strip()
            numbered = re.match(r"^(?:[IVX]{1,5}(?:\.[A-Z])?\.?|[A-Z]\.|\d+(?:\.\d+)*\.?)\s+[A-Z]", stripped)
            capital = (len(line)-len(line.lstrip()) >= 12 and len(stripped.split()) <= 12
                       and not stripped.endswith(".") and any(word in stripped.lower() for word in
                ["introduction", "conclusion", "identification", "estimation", "equilibrium",
                 "empirical strategy", "model environment", "counterfactual", "preferences",
                 "robustness", "quantification", "data description", "proof of", "proposition"]))
            if numbered and len(stripped.split()) == 2 and len(stripped.split()[1]) <= 3:
                numbered = None
            if (numbered or capital) and len(stripped) < 115 and len(stripped.split()) >= 2:
                if "american economic review" in stripped.lower() or "journal of" in stripped.lower():
                    continue
                results.append({"pdf_page": page["pdf_page"], "line": index+1,
                                "heading_candidate": stripped,
                                "following": "\n".join(lines[index+1:index+24])})
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paper")
    parser.add_argument("--pages", help="Inclusive PDF page range, such as 8:15")
    parser.add_argument("--page-list", nargs="+", type=int)
    parser.add_argument("--lead-words", type=int, help="Explicitly truncated leading-page excerpt")
    parser.add_argument("--outline", action="store_true")
    parser.add_argument("--section-pack", action="store_true")
    parser.add_argument("--to-page", type=int)
    args = parser.parse_args()
    pages = json.loads((ROOT / "extracted" / f"{args.paper}.pages.json").read_text())
    if args.to_page:
        pages = [page for page in pages if page["pdf_page"] <= args.to_page]
    if args.pages or args.page_list:
        if args.pages:
            first, last = map(int, args.pages.split(":"))
            selected = set(range(first, last+1))
        else:
            selected = set(args.page_list)
        for page in pages:
            if page["pdf_page"] in selected:
                text = page["text"]
                if args.lead_words:
                    text = " ".join(text.split()[:args.lead_words]) + "\n[LEADING EXCERPT ONLY]"
                print(f"\n=== {args.paper} PDF PAGE {page['pdf_page']} ===\n{text}")
    elif args.outline or args.section_pack:
        for item in headings(pages):
            print(f"\n=== {args.paper} PDF PAGE {item['pdf_page']}, LINE {item['line']} ===")
            print(item["heading_candidate"])
            if args.section_pack:
                print(item["following"])
    else:
        parser.error("Choose --pages, --outline, or --section-pack")


if __name__ == "__main__":
    main()
