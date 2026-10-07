#!/usr/bin/env python3
"""Create a deterministic structural inventory of Markdown/Mathdown sources."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
CITATION_RE = re.compile(r"(?<!\w)@([A-Za-z0-9_:.+-]+)")
MARKER_RE = re.compile(
    r"mathdown-(claim|derivation)\s*:\s*([A-Za-z0-9][A-Za-z0-9_.:-]*)",
    re.IGNORECASE,
)
RESULT_TOKEN_RE = re.compile(r"\b(?:R|MV-R|SOW-R|SS-R|CP-R|UB-R)-[A-Z0-9][A-Z0-9-]*\b")
DISPLAY_DOLLAR_RE = re.compile(r"(?ms)^\s*\$\$(.*?)\$\$\s*$")
DISPLAY_BRACKET_RE = re.compile(r"(?ms)\\\[(.*?)\\\]")
BEGIN_DISPLAY_RE = re.compile(r"\\begin\{(equation\*?|align\*?|gather\*?|multline\*?)\}")
THEOREM_WORD_RE = re.compile(
    r"(?im)^\s*(?:#{1,6}\s*)?(theorem|lemma|proposition|corollary|assumption|definition|remark)\b"
)


def split_frontmatter(text: str) -> tuple[str, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return "", text
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "".join(lines[1:index]), "".join(lines[index + 1 :])
    return "", text


def explicit_markers(text: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {"claim": [], "derivation": []}
    for kind, result_id in MARKER_RE.findall(text):
        key = kind.lower()
        if result_id not in result[key]:
            result[key].append(result_id)
    return result


def inventory_file(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    frontmatter, body = split_frontmatter(text)
    headings = []
    for line_number, line in enumerate(body.splitlines(), start=1):
        match = HEADING_RE.match(line)
        if match:
            headings.append(
                {"level": len(match.group(1)), "title": match.group(2), "line": line_number}
            )

    markers = explicit_markers(text)
    result_tokens = sorted(set(RESULT_TOKEN_RE.findall(text)))
    links = [{"text": label, "target": target} for label, target in LINK_RE.findall(body)]
    wikilinks = sorted(set(WIKILINK_RE.findall(body)))
    citations = sorted(set(CITATION_RE.findall(body)))
    display_count = (
        len(DISPLAY_DOLLAR_RE.findall(body))
        + len(DISPLAY_BRACKET_RE.findall(body))
        + len(BEGIN_DISPLAY_RE.findall(body))
    )

    return {
        "path": str(path.resolve()),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "lines": len(text.splitlines()),
        "has_frontmatter": bool(frontmatter),
        "frontmatter": frontmatter.strip(),
        "headings": headings,
        "explicit_markers": markers,
        "result_ids": result_tokens,
        "display_math_blocks": display_count,
        "theorem_like_headings": THEOREM_WORD_RE.findall(body),
        "links": links,
        "wikilinks": wikilinks,
        "citations": citations,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inventory Markdown structure, result markers, math, links, and hashes."
    )
    parser.add_argument("paths", nargs="+", type=Path, help="Markdown or Mathdown source files")
    parser.add_argument("--output", "-o", type=Path, help="Write JSON to this path")
    args = parser.parse_args()

    missing = [str(path) for path in args.paths if not path.is_file()]
    if missing:
        parser.error("not a file: " + ", ".join(missing))

    files = [inventory_file(path) for path in args.paths]
    all_result_ids = sorted({result_id for item in files for result_id in item["result_ids"]})
    all_marker_ids = sorted(
        {
            result_id
            for item in files
            for values in item["explicit_markers"].values()
            for result_id in values
        }
    )
    payload = {
        "schema": "render-mathdown-tex-inventory/v1",
        "files": files,
        "summary": {
            "file_count": len(files),
            "result_ids": all_result_ids,
            "explicit_marker_ids": all_marker_ids,
            "display_math_blocks": sum(item["display_math_blocks"] for item in files),
        },
    }
    rendered = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
