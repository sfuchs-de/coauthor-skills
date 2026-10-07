#!/usr/bin/env python3
"""Render Markdown as a reMarkable Paper Pro Move PDF and run lightweight QA."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CSS = SKILL_DIR / "assets" / "paper-pro-move.css"


def find_program(name: str, explicit: str | None = None) -> str | None:
    if explicit:
        path = Path(explicit).expanduser()
        if path.exists():
            return str(path)
        found = shutil.which(explicit)
        if found:
            return found
        raise FileNotFoundError(f"Cannot find {name}: {explicit}")
    return shutil.which(name)


def find_chrome(explicit: str | None = None) -> str:
    if explicit:
        return find_program("Chrome", explicit) or ""
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return found
    raise FileNotFoundError("Chrome or Chromium is required for PDF rendering")


def run(command: list[str], *, quiet: bool = False) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, text=True, capture_output=quiet)
    if result.returncode:
        if quiet:
            sys.stderr.write(result.stdout)
            sys.stderr.write(result.stderr)
        raise subprocess.CalledProcessError(result.returncode, command)
    return result


def build_css(base_css: Path, destination: Path, font_size: str | None, line_height: str | None) -> None:
    css = base_css.read_text(encoding="utf-8")
    overrides = []
    if font_size:
        overrides.append(f"font-size: {font_size};")
    if line_height:
        overrides.append(f"line-height: {line_height};")
    if overrides:
        css += "\n:root { " + " ".join(overrides) + " }\n"
    destination.write_text(css, encoding="utf-8")


def make_contact_sheet(page_files: list[Path], output: Path, thumb_width: int = 170) -> bool:
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return False

    thumbnails = []
    for number, page in enumerate(page_files, 1):
        image = Image.open(page).convert("RGB")
        height = round(image.height * thumb_width / image.width)
        image = image.resize((thumb_width, height))
        tile = Image.new("RGB", (thumb_width + 12, height + 28), "white")
        tile.paste(image, (6, 20))
        ImageDraw.Draw(tile).text((7, 3), str(number), fill="black")
        thumbnails.append(tile)

    if not thumbnails:
        return False
    columns = 5
    rows = (len(thumbnails) + columns - 1) // columns
    cell_width = max(image.width for image in thumbnails)
    cell_height = max(image.height for image in thumbnails)
    sheet = Image.new("RGB", (columns * cell_width, rows * cell_height), (225, 225, 225))
    for index, image in enumerate(thumbnails):
        sheet.paste(image, ((index % columns) * cell_width, (index // columns) * cell_height))
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)
    return True


def parse_page_count(pdfinfo_output: str) -> int | None:
    match = re.search(r"^Pages:\s+(\d+)", pdfinfo_output, re.MULTILINE)
    return int(match.group(1)) if match else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Markdown input")
    parser.add_argument("--output", "-o", type=Path, required=True, help="PDF output")
    parser.add_argument("--title", help="HTML/PDF metadata title; defaults to the input stem")
    parser.add_argument("--css", type=Path, default=DEFAULT_CSS, help="CSS stylesheet")
    parser.add_argument("--font-size", help="Body font-size override, for example 8.8pt")
    parser.add_argument("--line-height", help="Line-height override, for example 1.35")
    parser.add_argument("--chrome", help="Chrome or Chromium executable")
    parser.add_argument("--qa-dir", type=Path, help="Render page PNGs and a contact sheet here")
    parser.add_argument("--keep-html", action="store_true", help="Keep intermediate HTML beside the PDF")
    args = parser.parse_args()

    input_path = args.input.expanduser().resolve()
    output_path = args.output.expanduser().resolve()
    css_path = args.css.expanduser().resolve()
    if not input_path.is_file():
        parser.error(f"input does not exist: {input_path}")
    if not css_path.is_file():
        parser.error(f"CSS does not exist: {css_path}")

    pandoc = find_program("pandoc")
    if not pandoc:
        raise FileNotFoundError("Pandoc is required for Markdown conversion")
    chrome = find_chrome(args.chrome)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="remarkable-move-") as temp_name:
        temp_dir = Path(temp_name)
        effective_css = temp_dir / "move.css"
        build_css(css_path, effective_css, args.font_size, args.line_height)
        html_path = output_path.with_suffix(".html") if args.keep_html else temp_dir / "document.html"
        title = args.title or input_path.stem
        run([
            pandoc,
            str(input_path),
            "--standalone",
            "--mathml",
            "--embed-resources",
            f"--css={effective_css}",
            "--metadata",
            f"title={title}",
            "--output",
            str(html_path),
        ])
        run([
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={output_path}",
            html_path.resolve().as_uri(),
        ], quiet=True)

    if not output_path.is_file() or output_path.stat().st_size == 0:
        raise RuntimeError(f"Chrome did not create a PDF at {output_path}")

    qpdf = find_program("qpdf")
    if qpdf:
        run([qpdf, "--check", str(output_path)])
    else:
        print("warning: qpdf unavailable; skipped structural PDF check", file=sys.stderr)

    page_count = None
    pdfinfo = find_program("pdfinfo")
    if pdfinfo:
        result = subprocess.run([pdfinfo, str(output_path)], text=True, capture_output=True, check=True)
        page_count = parse_page_count(result.stdout)
        size_line = next((line for line in result.stdout.splitlines() if line.startswith("Page size:")), None)
        if size_line:
            print(size_line)
    else:
        print("warning: pdfinfo unavailable; skipped page metadata check", file=sys.stderr)

    if args.qa_dir:
        qa_dir = args.qa_dir.expanduser().resolve()
        qa_dir.mkdir(parents=True, exist_ok=True)
        pdftoppm = find_program("pdftoppm")
        if pdftoppm:
            prefix = qa_dir / "page"
            run([pdftoppm, "-png", "-r", "100", str(output_path), str(prefix)], quiet=True)
            pages = sorted(qa_dir.glob("page-*.png"))
            contact = qa_dir / "contact-sheet.png"
            if make_contact_sheet(pages, contact):
                print(f"Contact sheet: {contact}")
            else:
                print(f"Page renders: {qa_dir} (Pillow unavailable; no contact sheet)")
        else:
            print("warning: pdftoppm unavailable; skipped visual QA renders", file=sys.stderr)

    pages_text = f" ({page_count} pages)" if page_count is not None else ""
    print(f"PDF: {output_path}{pages_text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
