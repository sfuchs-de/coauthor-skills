#!/usr/bin/env python3
"""Acquire public author-hosted papers and create page-addressable research text."""

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
import time
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def normalized(value):
    value = unicodedata.normalize("NFKD", value)
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.items = []
        self.anchor = None
        self.item = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "li":
            if self.item is not None:
                self.items.append(self.item)
            self.item = {"text": "", "links": []}
        if tag == "a" and "href" in attrs:
            self.anchor = {"href": attrs["href"], "text": ""}

    def handle_data(self, value):
        if self.anchor is not None:
            self.anchor["text"] += value
        if self.item is not None:
            self.item["text"] += value

    def handle_endtag(self, tag):
        if tag == "a" and self.anchor is not None:
            self.links.append(self.anchor)
            if self.item is not None:
                self.item["links"].append(self.anchor)
            self.anchor = None
        if tag == "li" and self.item is not None:
            self.items.append(self.item)
            self.item = None


def read_public(url, limit=35 * 1024 * 1024):
    request = Request(url, headers={"User-Agent": "AcademicWritingReview/1.0"})
    with urlopen(request, timeout=75) as response:
        raw = response.read(limit + 1)
        if len(raw) > limit:
            raise ValueError("Source exceeds bounded download size")
        return raw, response.geturl(), response.headers.get("Content-Type", "")


def resolve(paper, index_url):
    raw, final, _ = read_public(index_url)
    parser = Links()
    parser.feed(raw.decode("utf-8", errors="replace"))
    if parser.item is not None:
        parser.items.append(parser.item)
    title = normalized(paper["resolve_title"])
    if paper["index"] == "redding":
        matches = [link for item in parser.items if title in normalized(item["text"])
                   for link in item["links"] if "ungated pdf" in normalized(link["text"])]
    else:
        matches = [link for link in parser.links if normalized(link["text"]) == title]
    urls = {urljoin(final, item["href"]) for item in matches}
    if len(urls) != 1:
        raise ValueError(f"Expected one author PDF link, found {len(urls)}")
    url = urls.pop()
    if "dropbox.com" in urlsplit(url).netloc:
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query))
        query["dl"] = "1"
        url = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), ""))
    return url


def acquire(selected):
    config = json.loads((ROOT / "data/sources.json").read_text())
    source_dir = ROOT / "sources"
    source_dir.mkdir(exist_ok=True)
    receipt_path = ROOT / "data/acquisition.json"
    receipts = json.loads(receipt_path.read_text()) if receipt_path.exists() else {}
    for paper in config["papers"]:
        ident = paper["id"]
        if selected and ident not in selected:
            continue
        target = source_dir / f"{ident}.pdf"
        if target.exists():
            if ident not in receipts or hashlib.sha256(target.read_bytes()).hexdigest() != receipts[ident]["sha256"]:
                raise ValueError(f"Unrecorded or changed existing PDF: {ident}")
            print(f"{ident}: verified existing source", flush=True)
            continue
        try:
            url = paper.get("pdf_url") or resolve(paper, config["author_indexes"][paper["index"]])
            raw, final, content_type = read_public(url)
            if not raw.startswith(b"%PDF-"):
                raise ValueError(f"Not a PDF ({content_type})")
            with target.open("xb") as output:
                output.write(raw)
            receipts[ident] = {"id": ident, "requested_url": url, "resolved_url": final,
                               "author_index": config["author_indexes"][paper["index"]],
                               "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                               "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                               "status": "downloaded_not_yet_reviewed"}
            receipt_path.write_text(json.dumps(receipts, indent=2) + "\n")
            print(f"{ident}: acquired {len(raw):,} bytes", flush=True)
        except Exception as error:
            print(f"{ident}: acquisition failed: {type(error).__name__}: {error}", flush=True)
        time.sleep(0.15)


def extract(selected):
    from pypdf import PdfReader
    import pdfplumber
    config = json.loads((ROOT / "data/sources.json").read_text())
    output = ROOT / "extracted"
    output.mkdir(exist_ok=True)
    metrics = {}
    for paper in config["papers"]:
        ident = paper["id"]
        if selected and ident not in selected:
            continue
        source = ROOT / "sources" / f"{ident}.pdf"
        if not source.exists():
            continue
        reader = PdfReader(source)
        with tempfile.TemporaryDirectory() as temporary:
            text_path = Path(temporary) / "text.txt"
            subprocess.run(["pdftotext", "-layout", str(source), str(text_path)], check=True)
            pages = text_path.read_text(errors="replace").split("\f")
        if pages and not pages[-1].strip():
            pages.pop()
        if len(pages) != len(reader.pages):
            raise ValueError(f"Page extraction mismatch: {ident}")
        first, last = paper.get("source_page_range", [1, len(pages)])
        if not 1 <= first <= last <= len(pages):
            raise ValueError(f"Invalid declared source page range: {ident}")
        page_records = []
        for index, text in enumerate(pages, start=1):
            if not first <= index <= last:
                continue
            page_records.append({"pdf_page": index, "text": text,
                                 "word_count": len(re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", text))})
        (output / f"{ident}.pages.json").write_text(json.dumps(page_records, indent=2) + "\n")
        (output / f"{ident}.txt").write_text("\n".join(
            f"\n===== PDF PAGE {page['pdf_page']} =====\n{page['text']}" for page in page_records))
        # Inspect representative pages only; typography is not inferred from text extraction.
        inspected = sorted(set([first-1, min(first+1, last-1), (first+last)//2-1, max(first-1, last-4)]))
        geometry = []
        with pdfplumber.open(source) as pdf:
            for index in inspected:
                page = pdf.pages[index]
                chars = [char for char in page.chars if char.get("text", "").strip()]
                fonts = Counter((char.get("fontname", ""), round(char["size"], 1)) for char in chars)
                geometry.append({"pdf_page": index+1, "width_pt": page.width, "height_pt": page.height,
                                 "dominant_fonts": [{"font": name, "size_pt": size, "characters": count}
                                                    for (name, size), count in fonts.most_common(7)]})
        metrics[ident] = {"pdf_pages": len(pages), "included_pages": [first,last],
                          "analyzable_pages": len(page_records),
                          "extracted_words": sum(p["word_count"] for p in page_records),
                          "pdf_metadata": {str(k): str(v) for k, v in (reader.metadata or {}).items()},
                          "sampled_typography": geometry,
                          "review_status": "extracted_not_yet_reviewed"}
        print(f"{ident}: {len(pages)} pages extracted", flush=True)
    target = ROOT / "data/extraction.json"
    previous = json.loads(target.read_text()) if target.exists() else {}
    previous.update(metrics)
    target.write_text(json.dumps(previous, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["acquire", "extract"])
    parser.add_argument("--papers", nargs="*")
    args = parser.parse_args()
    if args.mode == "acquire":
        acquire(set(args.papers or []))
    else:
        extract(set(args.papers or []))


if __name__ == "__main__":
    main()
