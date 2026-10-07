#!/usr/bin/env python3
"""Print tight line-context windows for TeX audit citations."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


LABEL_RE = re.compile(r"\\label\{(?P<label>[^}]+)\}")


def strip_comment(line: str) -> str:
    escaped = False
    for i, ch in enumerate(line):
        if ch == "\\":
            escaped = not escaped
            continue
        if ch == "%" and not escaped:
            return line[:i]
        escaped = False
    return line


def label_lines(lines: list[str], wanted: str) -> list[int]:
    out: list[int] = []
    for i, line in enumerate(lines, start=1):
        for m in LABEL_RE.finditer(strip_comment(line)):
            if m.group("label") == wanted:
                out.append(i)
    return out


def context(lines: list[str], center: int, window: int) -> dict[str, object]:
    start = max(1, center - window)
    end = min(len(lines), center + window)
    return {
        "center": center,
        "start": start,
        "end": end,
        "lines": [{"line": i, "text": lines[i - 1]} for i in range(start, end + 1)],
    }


def render_text(path: Path, blocks: list[dict[str, object]]) -> str:
    chunks: list[str] = []
    for block in blocks:
        chunks.append(f"{path}:{block['start']}-{block['end']} (center {block['center']})")
        chunks.append("```tex")
        for row in block["lines"]:  # type: ignore[index]
            marker = ">" if row["line"] == block["center"] else " "
            chunks.append(f"{marker} {row['line']:5d}: {row['text']}")
        chunks.append("```")
    return "\n".join(chunks) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex_file", type=Path)
    parser.add_argument("--line", type=int, action="append", default=[])
    parser.add_argument("--label", action="append", default=[])
    parser.add_argument("--window", type=int, default=4)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    lines = args.tex_file.read_text(encoding="utf-8").splitlines()
    centers = list(args.line)
    missing: list[str] = []
    for label in args.label:
        hits = label_lines(lines, label)
        if hits:
            centers.extend(hits)
        else:
            missing.append(label)

    if not centers and not missing:
        parser.error("provide at least one --line or --label")

    blocks = [context(lines, center, args.window) for center in centers]
    payload = {"file": str(args.tex_file), "missing_labels": missing, "contexts": blocks}
    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        if missing:
            print("Missing labels: " + ", ".join(missing))
        print(render_text(args.tex_file, blocks), end="")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
