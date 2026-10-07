#!/usr/bin/env python3
"""Extract a lightweight mathematical index from a TeX file.

This is intentionally conservative: it is not a full TeX parser. It preserves line numbers
and finds the objects most useful for a math-audit proof notebook.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


SECTION_RE = re.compile(
    r"^\s*\\(?P<cmd>part|chapter|section|subsection|subsubsection|paragraph)\*?"
    r"(?:\[[^\]]*\])?\{(?P<title>.*)\}"
)
BEGIN_RE = re.compile(r"\\begin\{(?P<env>[A-Za-z*]+)\}(?:\[(?P<option>[^\]]*)\])?")
END_RE = re.compile(r"\\end\{(?P<env>[A-Za-z*]+)\}")
LABEL_RE = re.compile(r"\\label\{(?P<label>[^}]+)\}")
REF_RE = re.compile(r"\\(?:eqref|ref|cref|Cref|autoref)\{(?P<refs>[^}]+)\}")

THEOREM_ENVS = {
    "theorem",
    "proposition",
    "lemma",
    "corollary",
    "definition",
    "assumption",
    "axiom",
    "claim",
    "conjecture",
    "remark",
    "example",
    "proof",
}

MATH_ENVS = {
    "equation",
    "equation*",
    "align",
    "align*",
    "gather",
    "gather*",
    "multline",
    "multline*",
    "flalign",
    "flalign*",
}

CLAIM_RE = re.compile(
    r"\b("
    r"therefore|hence|thus|implies|follows|so that|we obtain|yields|"
    r"first[- ]order|second[- ]order|asymptotic|converges|consistent|unbiased|"
    r"unique|strictly|monotone|bounded away|without loss|if and only if|iff|"
    r"O\(|o\(|approximation|negligible|dominates"
    r")\b",
    re.IGNORECASE,
)

DEFINITION_RE = re.compile(
    r"(\\coloneqq|:=|\\equiv|\bdefine\b|\bdefined\b|\bdenote\b|\blet\b)",
    re.IGNORECASE,
)


def strip_comment(line: str) -> str:
    """Remove unescaped TeX comments from one line."""
    escaped = False
    for i, ch in enumerate(line):
        if ch == "\\":
            escaped = not escaped
            continue
        if ch == "%" and not escaped:
            return line[:i]
        escaped = False
    return line


def brace_title(raw: str) -> str:
    """Best-effort cleanup for section titles."""
    title = raw.strip()
    if title.endswith("}"):
        title = title[:-1]
    return re.sub(r"\s+", " ", title)


def labels_in(lines: list[str], start: int, end: int) -> list[str]:
    out: list[str] = []
    for line in lines[start - 1 : end]:
        out.extend(m.group("label") for m in LABEL_RE.finditer(strip_comment(line)))
    return out


def extract(path: Path) -> dict[str, Any]:
    raw_lines = path.read_text(encoding="utf-8").splitlines()
    clean_lines = [strip_comment(line) for line in raw_lines]

    sections: list[dict[str, Any]] = []
    labels: list[dict[str, Any]] = []
    refs: list[dict[str, Any]] = []
    theorem_envs: list[dict[str, Any]] = []
    equations: list[dict[str, Any]] = []
    claims: list[dict[str, Any]] = []
    definitions: list[dict[str, Any]] = []

    env_stack: list[dict[str, Any]] = []
    display_start: int | None = None

    for line_no, line in enumerate(clean_lines, start=1):
        if not line.strip():
            continue

        section = SECTION_RE.search(line)
        if section:
            sections.append(
                {
                    "line": line_no,
                    "level": section.group("cmd"),
                    "title": brace_title(section.group("title")),
                    "labels": labels_in(raw_lines, line_no, min(line_no + 2, len(raw_lines))),
                }
            )

        for m in LABEL_RE.finditer(line):
            labels.append({"line": line_no, "label": m.group("label")})

        for m in REF_RE.finditer(line):
            for ref in [r.strip() for r in m.group("refs").split(",") if r.strip()]:
                refs.append({"line": line_no, "ref": ref})

        for m in BEGIN_RE.finditer(line):
            env = m.group("env")
            env_stack.append({"env": env, "start": line_no, "option": m.group("option")})

        if "\\[" in line and display_start is None:
            display_start = line_no

        if CLAIM_RE.search(line):
            claims.append({"line": line_no, "text": line.strip()})

        if DEFINITION_RE.search(line):
            definitions.append({"line": line_no, "text": line.strip()})

        if "\\]" in line and display_start is not None:
            equations.append(
                {
                    "kind": "display",
                    "env": "\\[...\\]",
                    "start": display_start,
                    "end": line_no,
                    "labels": labels_in(raw_lines, display_start, line_no),
                }
            )
            display_start = None

        for m in END_RE.finditer(line):
            env = m.group("env")
            idx = next((i for i in range(len(env_stack) - 1, -1, -1) if env_stack[i]["env"] == env), None)
            if idx is None:
                continue
            start_info = env_stack.pop(idx)
            item = {
                "env": env,
                "start": start_info["start"],
                "end": line_no,
                "option": start_info.get("option"),
                "labels": labels_in(raw_lines, start_info["start"], line_no),
            }
            if env in THEOREM_ENVS:
                theorem_envs.append(item)
            if env in MATH_ENVS:
                item["kind"] = "environment"
                equations.append(item)

    return {
        "file": str(path),
        "line_count": len(raw_lines),
        "sections": sections,
        "theorem_like_environments": theorem_envs,
        "equations": equations,
        "labels": labels,
        "cross_references": refs,
        "definition_lines": definitions,
        "claim_like_lines": claims,
    }


def as_markdown(data: dict[str, Any]) -> str:
    def rows(items: list[dict[str, Any]], fields: list[str]) -> list[str]:
        if not items:
            return ["_None found._"]
        out = ["| " + " | ".join(fields) + " |", "| " + " | ".join(["---"] * len(fields)) + " |"]
        for item in items:
            out.append("| " + " | ".join(str(item.get(f, "")).replace("\n", " ") for f in fields) + " |")
        return out

    chunks = [f"# TeX Math Index\n\nFile: `{data['file']}`\n\nLines: {data['line_count']}\n"]
    chunks.append("\n## Sections\n" + "\n".join(rows(data["sections"], ["line", "level", "title", "labels"])))
    chunks.append(
        "\n## Theorem-Like Environments\n"
        + "\n".join(rows(data["theorem_like_environments"], ["env", "start", "end", "option", "labels"]))
    )
    chunks.append("\n## Equations\n" + "\n".join(rows(data["equations"], ["kind", "env", "start", "end", "labels"])))
    chunks.append("\n## Labels\n" + "\n".join(rows(data["labels"], ["line", "label"])))
    chunks.append("\n## Cross-References\n" + "\n".join(rows(data["cross_references"], ["line", "ref"])))
    chunks.append("\n## Definition-Like Lines\n" + "\n".join(rows(data["definition_lines"], ["line", "text"])))
    chunks.append("\n## Claim-Like Lines\n" + "\n".join(rows(data["claim_like_lines"], ["line", "text"])))
    return "\n".join(chunks) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex_file", type=Path)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    data = extract(args.tex_file)
    text = json.dumps(data, indent=2, ensure_ascii=False) if args.format == "json" else as_markdown(data)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
