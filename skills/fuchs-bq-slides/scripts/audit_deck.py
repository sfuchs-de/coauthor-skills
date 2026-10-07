#!/usr/bin/env python3
"""Check a Beamer build and optionally render it; visual review remains manual."""
import argparse
import csv
import json
import math
from numbers import Real
from pathlib import Path
import re
import shutil
import subprocess
import sys

from pypdf import PdfReader


def check(pdf, ledger_path=None, main_end_label="bq_main_end"):
    errors = []
    reader = PdfReader(pdf)
    destinations = reader.named_destinations
    count = len(reader.pages)
    if count == 0:
        errors.append("PDF has no pages")
    for number, page in enumerate(reader.pages, 1):
        width, height = float(page.mediabox.width), float(page.mediabox.height)
        if height <= 0 or abs(width / height - 16 / 9) > .03:
            errors.append(f"Page {number} is not 16:9")

    nav = pdf.with_suffix(".nav")
    frames = []
    if nav.is_file():
        frames = [tuple(map(int, pair)) for pair in re.findall(
            r"\\beamer@framepages\s*\{(\d+)\}\s*\{(\d+)\}", nav.read_text())]
        cursor = 1
        for start, end in frames:
            if start != cursor or end < start or end > count:
                errors.append(f"Invalid/noncontiguous frame range: {start}--{end}")
            cursor = end + 1
        if not frames or cursor != count + 1:
            errors.append("NAV frame ranges do not cover the PDF")
    else:
        errors.append("Missing NAV file: logical-frame coverage is unverified")

    log = pdf.with_suffix(".log")
    if log.is_file():
        log_text = log.read_text(errors="replace")
        patterns = [r"Overfull \\[hv]box", r"Undefined control sequence",
                    r"(?:Reference|Citation).*undefined", r"undefined references",
                    r"multiply defined", r"Missing character:",
                    r"destination with the same identifier", r"Rerun to get"]
        for pattern in patterns:
            if re.search(pattern, log_text, re.I):
                errors.append(f"Build log needs attention: {pattern}")
    else:
        errors.append("Missing LOG file: source-build warnings are unverified")

    ledger = None
    if ledger_path:
        ledger = json.loads(ledger_path.read_text())
        main_end_label = ledger.get("main_end_label", main_end_label)
    if main_end_label in destinations:
        anchor = reader.get_destination_page_number(destinations[main_end_label]) + 1
        main_end = next((end for start, end in frames if start <= anchor <= end), anchor)
    else:
        errors.append(f"Missing main-end destination: {main_end_label}")
        main_end = count

    page_ids = {p.indirect_reference.idnum for p in reader.pages if p.indirect_reference}
    internal_links, external_links = 0, 0
    for number, page in enumerate(reader.pages, 1):
        for ref in page.get("/Annots", []):
            annotation = ref.get_object()
            action = annotation.get("/A", {})
            if action.get("/S") == "/URI":
                external_links += 1
            target = annotation.get("/Dest")
            if target is None and action.get("/S") == "/GoTo":
                target = action.get("/D")
            if target is None:
                continue
            internal_links += 1
            if isinstance(target, str):
                if target not in destinations:
                    errors.append(f"Page {number}: unknown destination {target}")
            elif isinstance(target, list) and target:
                page_ref = target[0]
                if hasattr(page_ref, "idnum"):
                    valid = page_ref.idnum in page_ids
                else:
                    valid = isinstance(page_ref, int) and 0 <= page_ref < count
                if not valid:
                    errors.append(f"Page {number}: invalid explicit page destination")
            else:
                errors.append(f"Page {number}: unsupported internal destination {target!r}")

    minutes, substantive, labels = 0.0, 0, set()
    if ledger is not None:
        for slide in ledger.get("slides", []):
            label = slide.get("label")
            if not label or label in labels:
                errors.append(f"Missing/duplicate ledger label: {label}")
            labels.add(label)
            if label not in destinations:
                errors.append(f"Ledger destination absent: {label}")
            for backup in slide.get("backup_labels", []):
                if backup not in destinations:
                    errors.append(f"Backup destination absent: {backup}")
            if slide.get("role", "main") != "main":
                continue
            substantive += 1
            duration = slide.get("minutes")
            if (isinstance(duration, bool) or not isinstance(duration, Real)
                    or not math.isfinite(duration) or duration <= 0):
                errors.append(f"Missing/invalid speaking time: {label}")
            else:
                minutes += duration
            if not slide.get("job") or not slide.get("sources"):
                errors.append(f"Main slide needs a job and source: {label}")
            if label in destinations:
                start = reader.get_destination_page_number(destinations[label]) + 1
                if start > main_end:
                    errors.append(f"Main ledger slide is after main end: {label}")
        if not substantive:
            errors.append("Ledger contains no substantive main slides")

    rows = []
    for i, (start, end) in enumerate(frames, 1):
        rows.append({"frame": i, "first_page": start, "last_page": end,
                     "reveals": end - start + 1, "section": "main" if end <= main_end else "backup"})
    report = {
        "pdf": str(pdf), "pdf_pages": count, "logical_frames": len(frames),
        "main_pdf_pages": main_end, "backup_pdf_pages": count - main_end,
        "main_logical_frames": sum(end <= main_end for _, end in frames),
        "substantive_main_slides_in_ledger": substantive if ledger is not None else None,
        "planned_minutes": minutes if ledger is not None else None,
        "internal_links": internal_links, "external_links": external_links,
        "errors": errors, "automated_checks_passed": not errors,
        "visual_review": "required; not certified by this script",
        "result_and_source_review": "required; not certified by this script",
    }
    return report, rows


def render(pdf, pages, out):
    from PIL import Image, ImageDraw
    executable = shutil.which("pdftoppm")
    if not executable:
        raise RuntimeError("pdftoppm is required for rendering")
    page_dir = out / "pages"
    page_dir.mkdir(parents=True, exist_ok=True)
    images = []
    for number in pages:
        prefix = page_dir / f"page-{number:03d}"
        subprocess.run([executable, "-f", str(number), "-l", str(number),
                        "-singlefile", "-scale-to", "1440", "-png", str(pdf), str(prefix)],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        images.append((number, prefix.with_suffix(".png")))
    sheets = []
    for offset in range(0, len(images), 12):
        batch = images[offset:offset + 12]
        canvas = Image.new("RGB", (1200, math.ceil(len(batch) / 3) * 250), "#eeeeee")
        draw = ImageDraw.Draw(canvas)
        for slot, (number, path) in enumerate(batch):
            x, y = (slot % 3) * 400, (slot // 3) * 250
            with Image.open(path) as source:
                thumb = source.convert("RGB")
                thumb.thumbnail((392, 221))
                canvas.paste(thumb, (x + 4, y + 4))
            draw.text((x + 6, y + 231), f"PDF page {number}", fill="black")
        path = out / f"contact-{offset // 12 + 1:03d}.png"
        canvas.save(path)
        sheets.append(str(path))
    return sheets


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--main-end-label", default="bq_main_end")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--render", choices=["none", "main", "finals", "all"], default="none")
    args = parser.parse_args()
    try:
        pdf = args.pdf.expanduser().resolve(strict=True)
        report, rows = check(pdf, args.ledger, args.main_end_label)
        args.out.mkdir(parents=True, exist_ok=True)
        if args.render != "none":
            if args.render == "main":
                pages = range(1, report["main_pdf_pages"] + 1)
            elif args.render == "all":
                pages = range(1, report["pdf_pages"] + 1)
            else:
                pages = [row["last_page"] for row in rows]
            report["contact_sheets"] = render(pdf, pages, args.out)
            report["rendered_pages"] = len(pages)
        with (args.out / "frames.csv").open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["frame", "first_page", "last_page", "reveals", "section"])
            writer.writeheader()
            writer.writerows(rows)
        (args.out / "audit.json").write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps(report, indent=2))
        return 1 if report["errors"] else 0
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"Audit failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
