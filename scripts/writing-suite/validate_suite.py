#!/usr/bin/env python3
"""Run portable structural, safety, and helper checks for the writing suite."""

from __future__ import annotations

import csv
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"

EXPECTED = {
    "academic-draft-review": {"compile", "repair", "short-note-layout"},
    "ai-slop-lint": {"quick", "report", "rewrite"},
    "audit-tex-math": {"derive", "audit", "repair", "readability"},
    "design-econ-seminar": {"structure", "slides", "script", "full"},
    "econ-write": {"draft", "revise", "author-audit", "response", "specialized", "result-first"},
    "econ-writing-suite": {"author-audit", "map", "audit", "compile", "quick"},
    "referee-report": {"direct", "staged", "evaluation"},
    "render-mathdown-tex": {"faithful", "curated", "repair"},
    "theory-writing-refinement": {"map", "audit-exposition", "revise", "full"},
}

GRAPH_LAYERS = {
    "academic-draft-review": "source_qa",
    "ai-slop-lint": "prose",
    "audit-tex-math": "math",
    "design-econ-seminar": "presentation",
    "econ-write": "argument",
    "referee-report": "referee",
    "render-mathdown-tex": "conversion",
    "theory-writing-refinement": "theory",
}

RESOURCE_RE = re.compile(r"`((?:references|assets|scripts)/[A-Za-z0-9_.-]+)`")
SECRET_PATTERNS = {
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}
FORBIDDEN_PATH = re.compile(r"(?:/" + r"Users/[^/\s]+|[A-Za-z]:\\" + r"Users\\[^\\\s]+)")
TEXT_SUFFIXES = {"", ".md", ".py", ".tex", ".yaml", ".yml", ".json", ".txt"}


def frontmatter_keys(text: str) -> set[str]:
    lines = text.splitlines()
    assert lines and lines[0] == "---", "missing opening frontmatter delimiter"
    keys: set[str] = set()
    for line in lines[1:]:
        if line == "---":
            return keys
        match = re.match(r"^([A-Za-z0-9_-]+):", line)
        if match:
            keys.add(match.group(1))
    raise AssertionError("missing closing frontmatter delimiter")


def check_skill(name: str, required_terms: set[str]) -> None:
    root = SKILLS / name
    assert root.is_dir(), f"missing skill: {name}"
    skill_path = root / "SKILL.md"
    text = skill_path.read_text(encoding="utf-8")
    assert frontmatter_keys(text) == {"name", "description"}, f"bad frontmatter: {name}"
    assert len(text.splitlines()) <= 250, f"SKILL.md exceeds 250 lines: {name}"
    for term in required_terms:
        assert term in text, f"missing routing term {term}: {name}"
    for relative in RESOURCE_RE.findall(text):
        assert (root / relative).exists(), f"missing resource {name}/{relative}"
    metadata = (root / "agents" / "openai.yaml").read_text(encoding="utf-8")
    assert f"${name}" in metadata, f"metadata prompt omits ${name}"


def check_repository_text() -> None:
    paths = [path for name in EXPECTED for path in (SKILLS / name).rglob("*")]
    for path in paths:
        if not path.is_file() or ".git" in path.parts:
            continue
        assert "__pycache__" not in path.parts and path.suffix != ".pyc", f"cache file: {path}"
        is_license_notice = path.name.startswith("LICENSE")
        assert is_license_notice or path.suffix.lower() in TEXT_SUFFIXES, f"unexpected binary or document asset: {path}"
        text = path.read_text(encoding="utf-8")
        assert not FORBIDDEN_PATH.search(text), f"machine-specific absolute path: {path}"
        for label, pattern in SECRET_PATTERNS.items():
            assert not pattern.search(text), f"{label} shaped value: {path}"
        if path.suffix == ".py":
            compile(text, str(path), "exec")


def check_umbrella() -> None:
    text = (SKILLS / "econ-writing-suite" / "SKILL.md").read_text(encoding="utf-8")
    for name in EXPECTED:
        if name != "econ-writing-suite":
            assert f"`{name}`" in text, f"umbrella omits {name}"
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for name in EXPECTED:
        assert f"`{name}`" in readme, f"README omits {name}"
    for name, layer in GRAPH_LAYERS.items():
        specialist = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
        assert "reasoning-graph-integration.md" in specialist, f"graph contract omitted by {name}"
        assert f"`{layer}`" in specialist, f"graph layer {layer} omitted by {name}"


def smoke_reasoning_graph() -> None:
    helper = SKILLS / "econ-writing-suite" / "scripts" / "reasoning_graph_workspace.py"
    fixture = """# A Small Paper\n\n## Model\n\nDemand rises. Therefore welfare rises.\n\n## Appendix\n\nA condition is imposed.\n"""
    with tempfile.TemporaryDirectory() as temp:
        temp_root = Path(temp)
        source = temp_root / "fixture.md"
        output = temp_root / "graph"
        source.write_text(fixture, encoding="utf-8")
        subprocess.run(
            [
                sys.executable, str(helper), "init", str(source), "--output-dir", str(output),
                "--project-root", str(temp_root), "--no-sentences",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        required = {
            "reasoning_nodes.csv",
            "reasoning_edges.csv",
            "reasoning_graph.json",
            "reasoning_graph.graphml",
            "reasoning_annotations.csv",
            "reasoning_findings.csv",
            "reasoning_handoffs.csv",
            "reasoning_manifest.json",
            "reasoning_map.md",
        }
        produced = {path.name for path in output.iterdir() if path.is_file()}
        assert required <= produced, f"reasoning helper omitted: {sorted(required - produced)}"
        with (output / "reasoning_nodes.csv").open(encoding="utf-8", newline="") as handle:
            node_id = next(csv.DictReader(handle))["id"]
        subprocess.run(
            [
                sys.executable, str(helper), "annotate", str(output), "--owner", "econ-write",
                "--node", node_id, "--summary", "The paper's root argument.", "--role", "problem",
                "--status", "accepted", "--confidence", "high",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [
                sys.executable, str(helper), "add-finding", str(output), "--owner", "econ-write",
                "--node", node_id, "--severity", "major", "--category", "missing-bridge",
                "--evidence", "The conclusion lacks a stated supporting edge.",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [
                sys.executable, str(helper), "layer", str(output), "--owner", "econ-write",
                "--status", "complete",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [
                sys.executable, str(helper), "add-handoff", str(output), "--from-owner", "econ-write",
                "--to-owner", "audit-tex-math", "--node", node_id,
                "--question", "Does the stated condition establish the headline claim?",
                "--close-when", "The load-bearing implication is audited.",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [sys.executable, str(helper), "validate", str(output)],
            check=True,
            capture_output=True,
            text=True,
        )
        invalid = subprocess.run(
            [
                sys.executable, str(helper), "add-finding", str(output), "--owner", "econ-write",
                "--node", "UNKNOWN-NODE", "--severity", "major", "--category", "bad-anchor",
                "--evidence", "Synthetic invalid case.",
            ],
            capture_output=True,
            text=True,
        )
        assert invalid.returncode != 0, "reasoning helper accepted an unknown node"
        for path in output.iterdir():
            if path.is_file() and path.suffix in {".csv", ".json", ".md", ".graphml"}:
                private_prefix = "/" + "Users/"
                assert private_prefix not in path.read_text(encoding="utf-8"), f"absolute path leaked: {path.name}"


def main() -> None:
    found = {path.name for path in SKILLS.iterdir() if (path / "SKILL.md").is_file()}
    assert set(EXPECTED) <= found, f"missing writing skills: {sorted(set(EXPECTED) - found)}"
    for name, terms in EXPECTED.items():
        check_skill(name, terms)
    check_umbrella()
    check_repository_text()
    smoke_reasoning_graph()
    print("PASS: 9 skills, routing contracts, repository safety, Python syntax, and graph helper")


if __name__ == "__main__":
    main()
