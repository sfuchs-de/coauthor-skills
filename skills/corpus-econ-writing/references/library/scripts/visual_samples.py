#!/usr/bin/env python3
"""Render a declared PDF sample without altering or redistributing source PDFs."""
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = {
    "D01": 26, "D02": 43, "D03": 22, "D04": 14, "D05": 13,
    "D06": 47, "A01": 9, "A02": 14, "A03": 35, "A04": 30,
    "A05": 17, "A06": 19, "K01": 14, "K02": 21, "K03": 25,
    "K04": 20, "R01": 52, "R02": 42, "R03": 18, "R04": 40,
    "R05": 25, "R06": 2, "R07": 50,
}

def main():
    output = ROOT / "visual_review"
    output.mkdir(exist_ok=True)
    receipts = []
    for ident, page in SAMPLES.items():
        stem = output / f"{ident}-p{page}"
        source = ROOT / "sources" / f"{ident}.pdf"
        subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page),
                        "-singlefile", "-r", "115", "-png", str(source), str(stem)],
                       check=True, capture_output=True)
        path = stem.with_suffix(".png")
        receipts.append({"paper_id": ident, "pdf_page": page,
                         "image": str(path.relative_to(ROOT)),
                         "image_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                         "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                         "status": "rendered_not_yet_inspected"})
    for group in range(4):
        batch = receipts[group * 6:(group + 1) * 6]
        canvas = Image.new("RGB", (1200, 2160), "#dddddd")
        draw = ImageDraw.Draw(canvas)
        for index, item in enumerate(batch):
            x, y = (index % 2) * 600, (index // 2) * 720
            draw.text((x + 15, y + 8), f"{item['paper_id']} / PDF p{item['pdf_page']}", fill="black")
            with Image.open(ROOT / item["image"]) as picture:
                picture.thumbnail((580, 685))
                canvas.paste(picture, (x + (600 - picture.width) // 2, y + 30))
        canvas.save(output / f"contact-{group + 1}.png")
    (ROOT / "data/visual_samples.json").write_text(json.dumps(receipts, indent=2) + "\n")
    print(f"Rendered {len(receipts)} declared pages and four contact sheets")

if __name__ == "__main__":
    main()
