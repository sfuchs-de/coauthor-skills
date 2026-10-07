#!/usr/bin/env python3
"""Record selected source-page provenance and render one check per added source."""
import argparse
import importlib.util
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("theory08_study_edition", HERE / "edition.py")
edition = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(edition)
ROOT = edition.ROOT
PAGES = {"TH01": [2,4,5,16,17,18], "TH02": [1,2,3,12], "TH03": [8,10,11,28],
         "TH04": [4,6,9,13], "TH05": [6,7,17,18], "TH06": [6,8,10,13,20]}
VIEWS = {"TH01": 5, "TH02": 2, "TH03": 28, "TH04": 9, "TH05": 17, "TH06": 10}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    target = ROOT / "analysis/STUDY_RECEIPT.json"
    if target.exists():
        raise ValueError("Preserve the study receipt")
    selected = []
    for ident, pages in PAGES.items():
        extracted = edition.load(ROOT / "extracted" / f"{ident}.pages.json")
        by_page = {p["pdf_page"]: p for p in extracted}
        for page in pages:
            text = by_page[page]["text"]
            selected.append({"paper_id": ident, "pdf_page": page,
                             "text_sha256": edition.hashlib.sha256(text.encode()).hexdigest(),
                             "characters": len(text)})
        if args.render:
            output = ROOT / "visual_review" / ident
            output.parent.mkdir(exist_ok=True)
            view = VIEWS[ident]
            subprocess.run(["pdftoppm", "-f", str(view), "-l", str(view), "-r", "95", "-singlefile", "-png",
                            str(ROOT / "sources" / f"{ident}.pdf"), str(output)], check=True,
                           capture_output=True, timeout=60)
    edition.save(target, {"selected_pages": selected, "selected_page_count": len(selected),
                         "rendered_views": VIEWS if args.render else {},
                         "source_cards_sha256": edition.digest(ROOT / "SOURCE_STUDY.md"),
                         "scope": "Selected reading; local images/full text excluded from portable release"})
    print(json.dumps({"selected_pages": len(selected), "rendered_views": len(VIEWS) if args.render else 0}))


if __name__ == "__main__":
    main()
