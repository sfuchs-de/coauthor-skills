#!/usr/bin/env python3
"""Build a conservative proof-obligation skeleton from TeX source.

This is not a full TeX parser. It preserves line numbers and extracts the audit cues needed
to build proof-obligation ledgers: theorem/proof blocks, dependencies, assumptions,
theorem-application lines, asymptotic/limit claims, interchange cues, and micro-claims.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


BEGIN_RE = re.compile(r"\\begin\{(?P<env>[A-Za-z*]+)\}(?:\[(?P<option>[^\]]*)\])?")
END_RE = re.compile(r"\\end\{(?P<env>[A-Za-z*]+)\}")
LABEL_RE = re.compile(r"\\label\{(?P<label>[^}]+)\}")
REF_RE = re.compile(r"\\(?:eqref|ref|cref|Cref|autoref)\{(?P<refs>[^}]+)\}")
SECTION_RE = re.compile(
    r"^\s*\\(?P<cmd>part|chapter|section|subsection|subsubsection|paragraph)\*?"
    r"(?:\[[^\]]*\])?\{(?P<title>.*)\}"
)

THEOREM_ENVS = {
    "theorem",
    "proposition",
    "lemma",
    "corollary",
    "claim",
    "conjecture",
    "definition",
    "assumption",
    "axiom",
    "remark",
    "example",
}
PROOF_ENVS = {"proof"}

ASSUMPTION_RE = re.compile(
    r"\b(assume|suppose|let|if|provided|under|whenever|where|for all|there exists|"
    r"bounded|compact|continuous|differentiable|smooth|integrable|measurable|"
    r"independent|i\.i\.d\.|iid|finite|positive|nonzero|nonsingular|invertible|"
    r"rank|regularity|uniform|bounded away)\b",
    re.IGNORECASE,
)

APPLICATION_RE = re.compile(
    r"\b(by|using|apply|applying|invoke|invoking|follows from|"
    r"from (?:lemma|proposition|theorem|corollary|assumption|\\ref|\\cref|\\Cref)|"
    r"by (?:lemma|proposition|theorem|corollary|assumption)|"
    r"(?:lemma|proposition|theorem|corollary|assumption)\s*\\ref)\b",
    re.IGNORECASE,
)

MICRO_CLAIM_RE = re.compile(
    r"\b(therefore|hence|thus|so|so that|it follows|follows|implies|we have|"
    r"we obtain|this yields|it remains|suffices|enough to show|without loss|wlog|"
    r"equivalently|consequently|as desired)\b",
    re.IGNORECASE,
)

ASYMPTOTIC_RE = re.compile(
    r"(\\to|\\rightarrow|\\xrightarrow|\\lim|\\limsup|\\liminf|\\infty|"
    r"\\sqrt|\\asymp|\\sim|\\Theta|\\Omega|\\mathcal\{O\}|\\operatorname\{O\}|"
    r"(?<![A-Za-z])O_p?\s*\(|(?<![A-Za-z])o_p?\s*\()"
)

INTERCHANGE_RE = re.compile(
    r"\b(dominated convergence|monotone convergence|fubini|tonelli|interchange|"
    r"exchange|differentiat(?:e|ing) under|leibniz|swap|uniform integrability|"
    r"pass(?:ing)? (?:the )?limit|limit and (?:expectation|integral|sum)|"
    r"expectation and (?:derivative|limit)|integral and (?:derivative|limit))\b",
    re.IGNORECASE,
)

SIDE_CONDITION_RE = re.compile(
    r"\b(jensen|cauchy[- ]schwarz|holder|hoelder|taylor|implicit function|"
    r"mean value|central limit|law of large numbers|clt|lln|martingale|"
    r"positive semidefinite|psd|operator norm|rank|invertible|nonsingular)\b",
    re.IGNORECASE,
)


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


def clean_text(line: str) -> str:
    return re.sub(r"\s+", " ", strip_comment(line)).strip()


def labels_in(lines: list[str], start: int, end: int) -> list[str]:
    out: list[str] = []
    for line in lines[start - 1 : end]:
        out.extend(m.group("label") for m in LABEL_RE.finditer(strip_comment(line)))
    return out


def refs_in_text(text: str) -> list[str]:
    refs: list[str] = []
    for m in REF_RE.finditer(text):
        refs.extend(ref.strip() for ref in m.group("refs").split(",") if ref.strip())
    return refs


def line_hit(line_no: int, line: str, kind: str, pattern: re.Pattern[str]) -> dict[str, Any] | None:
    text = clean_text(line)
    detection_text = LABEL_RE.sub("", text)
    if not text or not pattern.search(detection_text):
        return None
    return {"line": line_no, "kind": kind, "text": text, "refs": refs_in_text(text)}


def block_text(lines: list[str], start: int, end: int, max_lines: int = 8) -> str:
    chosen = [clean_text(line) for line in lines[start - 1 : min(end, start + max_lines - 1)]]
    return " ".join(part for part in chosen if part)


def extract(path: Path) -> dict[str, Any]:
    raw_lines = path.read_text(encoding="utf-8").splitlines()
    clean_lines = [strip_comment(line) for line in raw_lines]

    sections: list[dict[str, Any]] = []
    blocks: list[dict[str, Any]] = []
    labels: list[dict[str, Any]] = []
    refs: list[dict[str, Any]] = []
    cues: list[dict[str, Any]] = []
    env_stack: list[dict[str, Any]] = []

    for line_no, line in enumerate(clean_lines, start=1):
        if not line.strip():
            continue

        section = SECTION_RE.search(line)
        if section:
            sections.append(
                {
                    "line": line_no,
                    "level": section.group("cmd"),
                    "title": re.sub(r"\s+", " ", section.group("title").rstrip("}")).strip(),
                }
            )

        for m in LABEL_RE.finditer(line):
            labels.append({"line": line_no, "label": m.group("label")})

        for m in REF_RE.finditer(line):
            for ref in [r.strip() for r in m.group("refs").split(",") if r.strip()]:
                refs.append({"line": line_no, "ref": ref})

        for kind, pattern in [
            ("assumption_or_hypothesis", ASSUMPTION_RE),
            ("theorem_application", APPLICATION_RE),
            ("micro_claim", MICRO_CLAIM_RE),
            ("asymptotic_or_limit", ASYMPTOTIC_RE),
            ("interchange_step", INTERCHANGE_RE),
            ("side_condition_cue", SIDE_CONDITION_RE),
        ]:
            hit = line_hit(line_no, line, kind, pattern)
            if hit:
                cues.append(hit)

        for m in BEGIN_RE.finditer(line):
            env_stack.append({"env": m.group("env"), "start": line_no, "option": m.group("option")})

        for m in END_RE.finditer(line):
            env = m.group("env")
            idx = next((i for i in range(len(env_stack) - 1, -1, -1) if env_stack[i]["env"] == env), None)
            if idx is None:
                continue
            start_info = env_stack.pop(idx)
            if env not in THEOREM_ENVS and env not in PROOF_ENVS:
                continue
            start = start_info["start"]
            end = line_no
            local_cues = [cue for cue in cues if start <= cue["line"] <= end]
            blocks.append(
                {
                    "env": env,
                    "role": "proof" if env in PROOF_ENVS else "statement",
                    "start": start,
                    "end": end,
                    "option": start_info.get("option"),
                    "labels": labels_in(raw_lines, start, end),
                    "refs": sorted({ref for cue in local_cues for ref in cue["refs"]}),
                    "preview": block_text(raw_lines, start, end),
                    "cues": local_cues,
                }
            )

    edges = []
    for block in blocks:
        source = block["labels"][0] if block["labels"] else f"{block['env']}-L{block['start']}"
        for ref in block["refs"]:
            edges.append({"from": source, "to": ref, "source_lines": f"{block['start']}-{block['end']}"})

    return {
        "file": str(path),
        "line_count": len(raw_lines),
        "sections": sections,
        "blocks": blocks,
        "labels": labels,
        "cross_references": refs,
        "dependency_edges": edges,
        "global_cues": cues,
    }


def rows(items: list[dict[str, Any]], fields: list[str]) -> list[str]:
    if not items:
        return ["_None found._"]
    out = ["| " + " | ".join(fields) + " |", "| " + " | ".join(["---"] * len(fields)) + " |"]
    for item in items:
        vals = []
        for field in fields:
            val = item.get(field, "")
            if isinstance(val, (list, dict)):
                val = json.dumps(val, ensure_ascii=False)
            vals.append(str(val).replace("\n", " "))
        out.append("| " + " | ".join(vals) + " |")
    return out


def as_markdown(data: dict[str, Any]) -> str:
    chunks = [f"# Proof Obligation Index\n\nFile: `{data['file']}`\n\nLines: {data['line_count']}\n"]
    chunks.append("\n## Theorem and Proof Blocks\n")
    block_rows = []
    for block in data["blocks"]:
        cue_kinds = sorted({cue["kind"] for cue in block["cues"]})
        block_rows.append(
            {
                "env": block["env"],
                "role": block["role"],
                "start": block["start"],
                "end": block["end"],
                "labels": block["labels"],
                "refs": block["refs"],
                "cue_kinds": cue_kinds,
                "preview": block["preview"],
            }
        )
    chunks.append("\n".join(rows(block_rows, ["env", "role", "start", "end", "labels", "refs", "cue_kinds", "preview"])))

    chunks.append("\n\n## Dependency DAG Edges\n")
    chunks.append("\n".join(rows(data["dependency_edges"], ["from", "to", "source_lines"])))

    for kind, title in [
        ("assumption_or_hypothesis", "Assumption and Hypothesis Cues"),
        ("theorem_application", "Theorem Application Cues"),
        ("micro_claim", "Micro-Claim Cues"),
        ("asymptotic_or_limit", "Asymptotic and Limit Cues"),
        ("interchange_step", "Interchange Cues"),
        ("side_condition_cue", "Side-Condition Cues"),
    ]:
        hits = [cue for cue in data["global_cues"] if cue["kind"] == kind]
        chunks.append(f"\n\n## {title}\n")
        chunks.append("\n".join(rows(hits, ["line", "kind", "refs", "text"])))

    chunks.append(
        "\n\n## Audit Skeleton\n"
        "\nUse this skeleton as a starting point, then fill it by reading the proof.\n\n"
        "### Proof Obligation Ledger\n\n"
        "| ID | Source lines | Canonical statement | Required assumptions | Discharge status | Dependencies | Notes |\n"
        "| --- | --- | --- | --- | --- | --- | --- |\n\n"
        "### Theorem Application Ledger\n\n"
        "| ID | Source lines | Rule/theorem used | Inputs | Required side conditions | Discharge status | Consequence |\n"
        "| --- | --- | --- | --- | --- | --- | --- |\n\n"
        "### Limit-Order Map\n\n"
        "| ID | Source lines | Limit index | Object | Claimed order/mode | Uniformity | Dependencies | Verified? |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- |\n\n"
        "### Acceptance Gate\n\n"
        "| Claim/proof | Status | Blocking obligations | Residual risk |\n"
        "| --- | --- | --- | --- |\n"
    )
    return "".join(chunks) + "\n"


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
