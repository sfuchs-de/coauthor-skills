#!/usr/bin/env python3
"""Check a TeX note for short-note house-style formatting issues."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


BEGIN_LIST_RE = re.compile(r"\\begin\{(?P<env>itemize|enumerate|description)\}")
NOTATION_RE = re.compile(r"notation", re.IGNORECASE)
APPENDIX_RE = re.compile(r"\\appendix|\\section\*?\{Appendix\}", re.IGNORECASE)
ALGORITHM_RE = re.compile(r"\\begin\{algorithmblock\}|\\begin\{algorithm\}|\\begin\{algorithm2e\}")


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


def line_items(path: Path) -> list[tuple[int, str, str]]:
    rows: list[tuple[int, str, str]] = []
    for i, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        rows.append((i, raw, strip_comment(raw)))
    return rows


def find_table_spans(rows: list[tuple[int, str, str]]) -> list[dict[str, Any]]:
    spans: list[dict[str, Any]] = []
    start: int | None = None
    body: list[str] = []
    for line_no, raw, clean in rows:
        if "\\begin{table" in clean and start is None:
            start = line_no
            body = [clean]
        elif start is not None:
            body.append(clean)
            if "\\end{table" in clean:
                spans.append({"start": start, "end": line_no, "body": "\n".join(body)})
                start = None
                body = []
    return spans


def check(path: Path) -> dict[str, Any]:
    rows = line_items(path)
    appendix_line = next((line_no for line_no, _, clean in rows if APPENDIX_RE.search(clean)), None)

    active_lists = []
    for line_no, _, clean in rows:
        m = BEGIN_LIST_RE.search(clean)
        if m:
            active_lists.append({"line": line_no, "env": m.group("env")})

    tables = find_table_spans(rows)
    notation_tables_in_main = []
    notation_tables_in_appendix = []
    for table in tables:
        is_notation = bool(NOTATION_RE.search(table["body"]))
        if not is_notation:
            continue
        if appendix_line is not None and table["start"] > appendix_line:
            notation_tables_in_appendix.append({"start": table["start"], "end": table["end"]})
        else:
            notation_tables_in_main.append({"start": table["start"], "end": table["end"]})

    algorithm_blocks = [{"line": line_no} for line_no, _, clean in rows if ALGORITHM_RE.search(clean)]

    packages = {}
    for pkg in ["microtype", "setspace", "titlesec", "hyperref", "cleveref", "booktabs"]:
        packages[pkg] = any(f"\\usepackage{{{pkg}}}" in clean or f"\\usepackage[" in clean and f"]{{{pkg}}}" in clean for _, _, clean in rows)

    issues = []
    if active_lists:
        issues.append(
            {
                "severity": "S2",
                "kind": "active-list-environment",
                "message": "Active list environments are present; short notes should use prose or algorithm boxes.",
                "locations": active_lists,
            }
        )
    if notation_tables_in_main:
        issues.append(
            {
                "severity": "S2",
                "kind": "notation-table-main-text",
                "message": "Notation tables should be moved to the appendix.",
                "locations": notation_tables_in_main,
            }
        )
    if not algorithm_blocks:
        issues.append(
            {
                "severity": "Info",
                "kind": "missing-algorithm-box",
                "message": "No algorithm box found. Add one if the note has an iterative or procedural estimator.",
                "locations": [],
            }
        )

    return {
        "file": str(path),
        "appendix_line": appendix_line,
        "active_lists": active_lists,
        "notation_tables_in_main": notation_tables_in_main,
        "notation_tables_in_appendix": notation_tables_in_appendix,
        "algorithm_blocks": algorithm_blocks,
        "packages": packages,
        "issues": issues,
    }


def as_text(result: dict[str, Any]) -> str:
    lines = [f"Short-note format check: {result['file']}"]
    lines.append(f"Appendix line: {result['appendix_line'] or 'not found'}")
    lines.append(f"Active list environments: {len(result['active_lists'])}")
    for item in result["active_lists"]:
        lines.append(f"  - line {item['line']}: {item['env']}")
    lines.append(f"Notation tables in main text: {len(result['notation_tables_in_main'])}")
    for item in result["notation_tables_in_main"]:
        lines.append(f"  - lines {item['start']}-{item['end']}")
    lines.append(f"Notation tables in appendix: {len(result['notation_tables_in_appendix'])}")
    lines.append(f"Algorithm boxes/environments: {len(result['algorithm_blocks'])}")
    for item in result["algorithm_blocks"]:
        lines.append(f"  - line {item['line']}")
    if result["issues"]:
        lines.append("Issues:")
        for issue in result["issues"]:
            lines.append(f"  - [{issue['severity']}] {issue['kind']}: {issue['message']}")
    else:
        lines.append("Issues: none")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex_file", type=Path)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    result = check(args.tex_file)
    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(as_text(result), end="")
    return 1 if any(issue["severity"] != "Info" for issue in result["issues"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
