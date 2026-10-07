#!/usr/bin/env python3
"""Extract a line-anchored reasoning-ledger scaffold from authored TeX prose."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


SECTION_RE = re.compile(
    r"^\s*\\(?P<level>section|subsection|subsubsection)\*?"
    r"\{(?P<title>.*)\}\s*$"
)
DISPLAY_START_RE = re.compile(
    r"^\s*(?:\\\[|\\begin\{(?:equation\*?|align\*?|gather\*?|multline\*?|"
    r"theorem|proposition|lemma|corollary)\})"
)
DISPLAY_END_RE = re.compile(
    r"(?:\\\]|\\end\{(?:equation\*?|align\*?|gather\*?|multline\*?|"
    r"theorem|proposition|lemma|corollary)\})\s*$"
)
COMMAND_ONLY_RE = re.compile(
    r"^\s*\\(?:label|Needspace|vspace|smallskip|medskip|bigskip|"
    r"FloatBarrier|clearpage|newpage)\b"
)


@dataclass
class Unit:
    kind: str
    file: str
    start_line: int
    end_line: int
    section: str
    subsection: str
    text: str


def strip_comment(line: str) -> str:
    escaped = False
    out: list[str] = []
    for char in line:
        if char == "%" and not escaped:
            break
        out.append(char)
        escaped = char == "\\" and not escaped
        if char != "\\":
            escaped = False
    return "".join(out)


def clean_text(lines: list[str]) -> str:
    text = " ".join(line.strip() for line in lines)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract(path: Path) -> list[Unit]:
    raw_lines = path.read_text(encoding="utf-8").splitlines()
    units: list[Unit] = []
    paragraph: list[str] = []
    paragraph_start = 0
    section = ""
    subsection = ""
    in_display = False
    display: list[str] = []
    display_start = 0

    def flush_paragraph(end_line: int) -> None:
        nonlocal paragraph, paragraph_start
        text = clean_text(paragraph)
        if text:
            units.append(
                Unit(
                    kind="paragraph",
                    file=str(path),
                    start_line=paragraph_start,
                    end_line=end_line,
                    section=section,
                    subsection=subsection,
                    text=text,
                )
            )
        paragraph = []
        paragraph_start = 0

    for lineno, raw in enumerate(raw_lines, start=1):
        line = strip_comment(raw).rstrip()

        if in_display:
            display.append(line)
            if DISPLAY_END_RE.search(line):
                units.append(
                    Unit(
                        kind="display",
                        file=str(path),
                        start_line=display_start,
                        end_line=lineno,
                        section=section,
                        subsection=subsection,
                        text=clean_text(display),
                    )
                )
                in_display = False
                display = []
            continue

        heading = SECTION_RE.match(line)
        if heading:
            flush_paragraph(lineno - 1)
            level = heading.group("level")
            title = heading.group("title")
            if level == "section":
                section = title
                subsection = ""
            else:
                subsection = title
            units.append(
                Unit(
                    kind=level,
                    file=str(path),
                    start_line=lineno,
                    end_line=lineno,
                    section=section,
                    subsection=subsection,
                    text=title,
                )
            )
            continue

        if DISPLAY_START_RE.match(line):
            flush_paragraph(lineno - 1)
            in_display = True
            display_start = lineno
            display = [line]
            if DISPLAY_END_RE.search(line):
                units.append(
                    Unit(
                        kind="display",
                        file=str(path),
                        start_line=lineno,
                        end_line=lineno,
                        section=section,
                        subsection=subsection,
                        text=clean_text(display),
                    )
                )
                in_display = False
                display = []
            continue

        if not line.strip() or COMMAND_ONLY_RE.match(line):
            flush_paragraph(lineno - 1)
            continue

        if not paragraph:
            paragraph_start = lineno
        paragraph.append(line)

    flush_paragraph(len(raw_lines))
    if in_display:
        units.append(
            Unit(
                kind="display",
                file=str(path),
                start_line=display_start,
                end_line=len(raw_lines),
                section=section,
                subsection=subsection,
                text=clean_text(display),
            )
        )
    return units


def markdown(units: list[Unit]) -> str:
    out = [
        "# Reasoning Graph Scaffold",
        "",
        "Complete the editorial fields. Use sentence-relation labels "
        "`D/C/I/E/Q/X/T` from the coherence ledger.",
        "",
    ]
    paragraph_id = 0
    display_id = 0
    for unit in units:
        if unit.kind in {"section", "subsection", "subsubsection"}:
            out.extend(
                [
                    f"## {unit.kind.title()}: {unit.text}",
                    f"- Source: `{unit.file}:{unit.start_line}`",
                    "- Incoming object:",
                    "- Question:",
                    "- Output:",
                    "- Handoff:",
                    "- Risk:",
                    "",
                ]
            )
        elif unit.kind == "paragraph":
            paragraph_id += 1
            excerpt = unit.text[:500]
            out.extend(
                [
                    f"### P{paragraph_id:03d}",
                    f"- Source: `{unit.file}:{unit.start_line}-{unit.end_line}`",
                    f"- Context: `{unit.section}` / `{unit.subsection}`",
                    f"- Text: {excerpt}",
                    "- Role:",
                    "- Controlling claim:",
                    "- Sentence chain:",
                    "- Incoming edge:",
                    "- Outgoing edge:",
                    "- Orphan or repair:",
                    "",
                ]
            )
        elif unit.kind == "display":
            display_id += 1
            excerpt = unit.text[:500]
            out.extend(
                [
                    f"### M{display_id:03d}",
                    f"- Source: `{unit.file}:{unit.start_line}-{unit.end_line}`",
                    f"- Context: `{unit.section}` / `{unit.subsection}`",
                    f"- Display: `{excerpt}`",
                    "- Question:",
                    "- Incoming results:",
                    "- New objects:",
                    "- Assumptions:",
                    "- Operation:",
                    "- Economic meaning:",
                    "- Mathematical scope:",
                    "- Appendix anchor:",
                    "- Next use:",
                    "",
                ]
            )
    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    units: list[Unit] = []
    for path in args.files:
        units.extend(extract(path))

    if args.format == "json":
        rendered = json.dumps([asdict(unit) for unit in units], indent=2)
    else:
        rendered = markdown(units)

    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
