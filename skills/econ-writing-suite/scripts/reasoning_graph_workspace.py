#!/usr/bin/env python3
"""Initialize and validate a shared reasoning-graph workspace."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET


SCHEMA_VERSION = "1.0"
SUITE_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = SUITE_ROOT.parent
BUILDER = SKILLS_ROOT / "econ-write" / "scripts" / "build_reasoning_skeleton.py"

STRUCTURAL_FILES = {
    "reasoning_nodes.csv",
    "reasoning_edges.csv",
    "reasoning_graph.json",
    "reasoning_graph.graphml",
    "summary.md",
}
ANNOTATION_FIELDS = [
    "node_id", "owner", "summary", "role", "inherits", "advance", "yield", "scope", "status", "confidence"
]
FINDING_FIELDS = [
    "finding_id", "owner", "node_ids", "source_node", "target_node", "severity", "category",
    "status", "evidence", "implication", "repair", "verification",
]
HANDOFF_FIELDS = [
    "handoff_id", "from_owner", "to_owner", "node_ids", "question", "evidence", "status", "close_when"
]
OWNERS = {
    "econ-write": "EW",
    "theory-writing-refinement": "TW",
    "audit-tex-math": "AM",
    "academic-draft-review": "AQ",
    "render-mathdown-tex": "RM",
    "referee-report": "RR",
    "ai-slop-lint": "AS",
    "design-econ-seminar": "DS",
}
LAYER_BY_OWNER = {
    "econ-write": "argument",
    "theory-writing-refinement": "theory",
    "audit-tex-math": "math",
    "academic-draft-review": "source_qa",
    "render-mathdown-tex": "conversion",
    "referee-report": "referee",
    "ai-slop-lint": "prose",
    "design-econ-seminar": "presentation",
}
LAYER_STATUSES = {"not_requested", "pending", "in_progress", "complete", "blocked", "stale"}
FINDING_STATUSES = {"candidate", "open", "verified", "repaired", "accepted-risk", "not-assessable", "stale"}
ANNOTATION_STATUSES = {"draft", "accepted", "stale"}
CONFIDENCE_LEVELS = {"", "high", "medium", "low"}
HANDOFF_STATUSES = {"open", "closed", "blocked", "stale"}
SEVERITIES = {"blocking", "major", "moderate", "minor", "informational"}
ABSOLUTE_PATH = re.compile(r"(?:/" + r"Users/[^/\s]+|[A-Za-z]:\\" + r"Users\\[^\\\s]+)")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_path(value: str | Path, project_root: Path) -> str:
    path = Path(value)
    if not path.is_absolute():
        return path.as_posix()
    return Path(os.path.relpath(path, project_root)).as_posix()


def normalize_structural_paths(workspace: Path, project_root: Path) -> list[dict[str, str]]:
    nodes_path = workspace / "reasoning_nodes.csv"
    nodes = read_csv(nodes_path)
    source_paths = sorted({Path(row["file"]) for row in nodes if row.get("file")})
    for row in nodes:
        if row.get("file"):
            row["file"] = relative_path(row["file"], project_root)
    write_csv(nodes_path, list(nodes[0].keys()) if nodes else [], nodes)

    graph_path = workspace / "reasoning_graph.json"
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    graph["metadata"]["input"] = relative_path(graph["metadata"]["input"], project_root)
    for node in graph["nodes"]:
        if node.get("file"):
            node["file"] = relative_path(node["file"], project_root)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    graphml_path = workspace / "reasoning_graph.graphml"
    namespace = "http://graphml.graphdrawing.org/xmlns"
    ET.register_namespace("", namespace)
    tree = ET.parse(graphml_path)
    for data in tree.findall(f".//{{{namespace}}}data[@key='d4']"):
        if data.text:
            data.text = relative_path(data.text, project_root)
    tree.write(graphml_path, encoding="utf-8", xml_declaration=True)

    summary_path = workspace / "summary.md"
    summary = summary_path.read_text(encoding="utf-8")
    for source_path in source_paths:
        summary = summary.replace(str(source_path), relative_path(source_path, project_root))
    summary_path.write_text(summary, encoding="utf-8")

    inputs: list[dict[str, str]] = []
    for source in source_paths:
        if source.is_file():
            inputs.append({"path": relative_path(source, project_root), "sha256": sha256(source)})
    return inputs


def init_workspace(args: argparse.Namespace) -> int:
    source = args.input.expanduser().resolve()
    if not source.is_file():
        raise ValueError(f"input does not exist: {source}")
    project_root = (args.project_root or source.parent).expanduser().resolve()
    workspace = args.output_dir.expanduser().resolve()
    if workspace.exists() and any(workspace.iterdir()):
        raise ValueError(f"workspace is not empty: {workspace}")
    workspace.mkdir(parents=True, exist_ok=True)

    command = [sys.executable, str(BUILDER), str(source), "--output-dir", str(workspace)]
    if args.no_sentences:
        command.append("--no-sentences")
    subprocess.run(command, check=True)
    inputs = normalize_structural_paths(workspace, project_root)

    write_csv(workspace / "reasoning_annotations.csv", ANNOTATION_FIELDS, [])
    write_csv(workspace / "reasoning_findings.csv", FINDING_FIELDS, [])
    write_csv(workspace / "reasoning_handoffs.csv", HANDOFF_FIELDS, [])
    layers = {layer: "pending" for layer in LAYER_BY_OWNER.values()}
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "source_root": relative_path(source, project_root),
        "source_inputs": inputs,
        "layers": layers,
        "artifacts": {
            "nodes": "reasoning_nodes.csv",
            "edges": "reasoning_edges.csv",
            "graph": "reasoning_graph.json",
            "graphml": "reasoning_graph.graphml",
            "annotations": "reasoning_annotations.csv",
            "findings": "reasoning_findings.csv",
            "handoffs": "reasoning_handoffs.csv",
            "map": "reasoning_map.md",
        },
    }
    (workspace / "reasoning_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    map_text = """# Reasoning Map

## Paper spine

[Recover the shortest faithful question-to-conclusion chain and cite node IDs.]

## Section contracts

[Record incoming object, section task, output, and outgoing handoff.]

## Branches and returns

[Identify each material branch, its output, and return node.]

## Weak links and open obligations

[Summarize load-bearing findings from reasoning_findings.csv.]

## Revision comparison

[After revision, record repaired links, new orphans, stale anchors, and residual risks.]
"""
    (workspace / "reasoning_map.md").write_text(map_text, encoding="utf-8")
    return validate_workspace(workspace)


def required_files() -> set[str]:
    return STRUCTURAL_FILES | {
        "reasoning_annotations.csv", "reasoning_findings.csv", "reasoning_handoffs.csv",
        "reasoning_manifest.json", "reasoning_map.md",
    }


def split_ids(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def validate_headers(path: Path, expected: list[str]) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != expected:
            raise ValueError(f"unexpected header in {path.name}: {reader.fieldnames}")
        return list(reader)


def validate_workspace(workspace: Path) -> int:
    workspace = workspace.expanduser().resolve()
    missing = sorted(required_files() - {path.name for path in workspace.iterdir() if path.is_file()})
    if missing:
        raise ValueError(f"missing workspace files: {', '.join(missing)}")

    nodes = read_csv(workspace / "reasoning_nodes.csv")
    edges = read_csv(workspace / "reasoning_edges.csv")
    node_ids = {row["id"] for row in nodes}
    if len(node_ids) != len(nodes):
        raise ValueError("duplicate node IDs")
    for edge in edges:
        if edge["source"] not in node_ids or edge["target"] not in node_ids:
            raise ValueError(f"edge references missing node: {edge}")

    annotations = validate_headers(workspace / "reasoning_annotations.csv", ANNOTATION_FIELDS)
    findings = validate_headers(workspace / "reasoning_findings.csv", FINDING_FIELDS)
    handoffs = validate_headers(workspace / "reasoning_handoffs.csv", HANDOFF_FIELDS)
    for row in annotations:
        if row["node_id"] not in node_ids or row["owner"] not in OWNERS:
            raise ValueError(f"invalid annotation anchor or owner: {row}")
        if row["status"] not in ANNOTATION_STATUSES or row["confidence"] not in CONFIDENCE_LEVELS:
            raise ValueError(f"invalid annotation status or confidence: {row}")
    for row in findings:
        if row["owner"] not in OWNERS or row["status"] not in FINDING_STATUSES:
            raise ValueError(f"invalid finding owner or status: {row}")
        if row["severity"] not in SEVERITIES:
            raise ValueError(f"invalid finding severity: {row}")
        anchors = split_ids(row["node_ids"]) + split_ids(row["source_node"]) + split_ids(row["target_node"])
        if any(anchor not in node_ids for anchor in anchors):
            raise ValueError(f"finding references missing node: {row['finding_id']}")
    for row in handoffs:
        if row["from_owner"] not in OWNERS or row["to_owner"] not in OWNERS:
            raise ValueError(f"invalid handoff owner: {row}")
        if row["status"] not in HANDOFF_STATUSES:
            raise ValueError(f"invalid handoff status: {row}")
        if any(anchor not in node_ids for anchor in split_ids(row["node_ids"])):
            raise ValueError(f"handoff references missing node: {row['handoff_id']}")

    manifest = json.loads((workspace / "reasoning_manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"unsupported schema version: {manifest.get('schema_version')}")
    if set(manifest.get("layers", {})) != set(LAYER_BY_OWNER.values()):
        raise ValueError("manifest layer inventory is incomplete")
    if any(status not in LAYER_STATUSES for status in manifest["layers"].values()):
        raise ValueError("manifest contains invalid layer status")

    graph = json.loads((workspace / "reasoning_graph.json").read_text(encoding="utf-8"))
    if {node["id"] for node in graph["nodes"]} != node_ids:
        raise ValueError("JSON and CSV node inventories differ")
    for path in workspace.iterdir():
        if path.is_file() and path.suffix in {".csv", ".json", ".md", ".graphml"}:
            if ABSOLUTE_PATH.search(path.read_text(encoding="utf-8")):
                raise ValueError(f"private absolute path in {path.name}")

    print(
        f"PASS: nodes={len(nodes)} edges={len(edges)} annotations={len(annotations)} "
        f"findings={len(findings)} handoffs={len(handoffs)}"
    )
    return 0


def update_layer(args: argparse.Namespace) -> int:
    workspace = args.workspace.expanduser().resolve()
    manifest_path = workspace / "reasoning_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    layer = LAYER_BY_OWNER[args.owner]
    manifest["layers"][layer] = args.status
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return validate_workspace(workspace)


def add_finding(args: argparse.Namespace) -> int:
    workspace = args.workspace.expanduser().resolve()
    validate_workspace(workspace)
    nodes = {row["id"] for row in read_csv(workspace / "reasoning_nodes.csv")}
    anchors = args.node or []
    optional = [value for value in (args.source_node, args.target_node) if value]
    if any(anchor not in nodes for anchor in anchors + optional):
        raise ValueError("finding contains an unknown node ID")
    path = workspace / "reasoning_findings.csv"
    rows = validate_headers(path, FINDING_FIELDS)
    prefix = f"RG-{OWNERS[args.owner]}-"
    numbers = [int(row["finding_id"].removeprefix(prefix)) for row in rows if row["finding_id"].startswith(prefix)]
    finding_id = f"{prefix}{max(numbers, default=0) + 1:04d}"
    row = {
        "finding_id": finding_id,
        "owner": args.owner,
        "node_ids": ";".join(anchors),
        "source_node": args.source_node or "",
        "target_node": args.target_node or "",
        "severity": args.severity,
        "category": args.category,
        "status": args.status,
        "evidence": args.evidence,
        "implication": args.implication,
        "repair": args.repair,
        "verification": args.verification,
    }
    rows.append(row)
    write_csv(path, FINDING_FIELDS, rows)
    print(f"Added {finding_id}")
    return validate_workspace(workspace)


def add_annotation(args: argparse.Namespace) -> int:
    workspace = args.workspace.expanduser().resolve()
    validate_workspace(workspace)
    nodes = {row["id"] for row in read_csv(workspace / "reasoning_nodes.csv")}
    if args.node not in nodes:
        raise ValueError("annotation contains an unknown node ID")
    path = workspace / "reasoning_annotations.csv"
    rows = validate_headers(path, ANNOTATION_FIELDS)
    row = {
        "node_id": args.node,
        "owner": args.owner,
        "summary": args.summary,
        "role": args.role,
        "inherits": args.inherits,
        "advance": args.advance,
        "yield": args.yield_value,
        "scope": args.scope,
        "status": args.status,
        "confidence": args.confidence,
    }
    replaced = False
    for index, existing in enumerate(rows):
        if existing["node_id"] == args.node and existing["owner"] == args.owner:
            rows[index] = row
            replaced = True
            break
    if not replaced:
        rows.append(row)
    write_csv(path, ANNOTATION_FIELDS, rows)
    print(f"{'Updated' if replaced else 'Added'} annotation {args.owner}/{args.node}")
    return validate_workspace(workspace)


def add_handoff(args: argparse.Namespace) -> int:
    workspace = args.workspace.expanduser().resolve()
    validate_workspace(workspace)
    nodes = {row["id"] for row in read_csv(workspace / "reasoning_nodes.csv")}
    anchors = args.node or []
    if any(anchor not in nodes for anchor in anchors):
        raise ValueError("handoff contains an unknown node ID")
    path = workspace / "reasoning_handoffs.csv"
    rows = validate_headers(path, HANDOFF_FIELDS)
    prefix = f"RH-{OWNERS[args.from_owner]}-{OWNERS[args.to_owner]}-"
    numbers = [int(row["handoff_id"].removeprefix(prefix)) for row in rows if row["handoff_id"].startswith(prefix)]
    handoff_id = f"{prefix}{max(numbers, default=0) + 1:04d}"
    rows.append(
        {
            "handoff_id": handoff_id,
            "from_owner": args.from_owner,
            "to_owner": args.to_owner,
            "node_ids": ";".join(anchors),
            "question": args.question,
            "evidence": args.evidence,
            "status": args.status,
            "close_when": args.close_when,
        }
    )
    write_csv(path, HANDOFF_FIELDS, rows)
    print(f"Added {handoff_id}")
    return validate_workspace(workspace)


def status_workspace(workspace: Path) -> int:
    workspace = workspace.expanduser().resolve()
    validate_workspace(workspace)
    manifest = json.loads((workspace / "reasoning_manifest.json").read_text(encoding="utf-8"))
    findings = read_csv(workspace / "reasoning_findings.csv")
    handoffs = read_csv(workspace / "reasoning_handoffs.csv")
    print("Layers:")
    for layer, status in manifest["layers"].items():
        print(f"  {layer}: {status}")
    print("Findings:")
    counts: dict[str, int] = {}
    for row in findings:
        key = f"{row['severity']}/{row['status']}"
        counts[key] = counts.get(key, 0) + 1
    if not counts:
        print("  none")
    for key in sorted(counts):
        print(f"  {key}: {counts[key]}")
    handoff_counts: dict[str, int] = {}
    for row in handoffs:
        handoff_counts[row["status"]] = handoff_counts.get(row["status"], 0) + 1
    print("Handoffs:")
    if not handoff_counts:
        print("  none")
    for key in sorted(handoff_counts):
        print(f"  {key}: {handoff_counts[key]}")
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="Create a new layered graph workspace")
    init.add_argument("input", type=Path)
    init.add_argument("--output-dir", type=Path, default=Path("writing-review/reasoning-graph"))
    init.add_argument("--project-root", type=Path)
    init.add_argument("--no-sentences", action="store_true")

    validate = commands.add_parser("validate", help="Validate graph structure and specialist layers")
    validate.add_argument("workspace", type=Path)

    status = commands.add_parser("status", help="Show layer and finding status")
    status.add_argument("workspace", type=Path)

    layer = commands.add_parser("layer", help="Update one specialist layer status")
    layer.add_argument("workspace", type=Path)
    layer.add_argument("--owner", choices=sorted(OWNERS), required=True)
    layer.add_argument("--status", choices=sorted(LAYER_STATUSES), required=True)

    finding = commands.add_parser("add-finding", help="Append one validated specialist finding")
    finding.add_argument("workspace", type=Path)
    finding.add_argument("--owner", choices=sorted(OWNERS), required=True)
    finding.add_argument("--node", action="append")
    finding.add_argument("--source-node")
    finding.add_argument("--target-node")
    finding.add_argument("--severity", choices=sorted(SEVERITIES), required=True)
    finding.add_argument("--category", required=True)
    finding.add_argument("--status", choices=sorted(FINDING_STATUSES), default="open")
    finding.add_argument("--evidence", required=True)
    finding.add_argument("--implication", default="")
    finding.add_argument("--repair", default="")
    finding.add_argument("--verification", default="")

    annotation = commands.add_parser("annotate", help="Add or replace one specialist node annotation")
    annotation.add_argument("workspace", type=Path)
    annotation.add_argument("--owner", choices=sorted(OWNERS), required=True)
    annotation.add_argument("--node", required=True)
    annotation.add_argument("--summary", default="")
    annotation.add_argument("--role", default="")
    annotation.add_argument("--inherits", default="")
    annotation.add_argument("--advance", default="")
    annotation.add_argument("--yield", dest="yield_value", default="")
    annotation.add_argument("--scope", default="")
    annotation.add_argument("--status", choices=sorted(ANNOTATION_STATUSES), default="draft")
    annotation.add_argument("--confidence", choices=sorted(CONFIDENCE_LEVELS - {""}), default="")

    handoff = commands.add_parser("add-handoff", help="Append one validated cross-skill handoff")
    handoff.add_argument("workspace", type=Path)
    handoff.add_argument("--from-owner", choices=sorted(OWNERS), required=True)
    handoff.add_argument("--to-owner", choices=sorted(OWNERS), required=True)
    handoff.add_argument("--node", action="append")
    handoff.add_argument("--question", required=True)
    handoff.add_argument("--evidence", default="")
    handoff.add_argument("--status", choices=sorted(HANDOFF_STATUSES), default="open")
    handoff.add_argument("--close-when", required=True)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "init":
            return init_workspace(args)
        if args.command == "validate":
            return validate_workspace(args.workspace)
        if args.command == "status":
            return status_workspace(args.workspace)
        if args.command == "layer":
            return update_layer(args)
        if args.command == "add-finding":
            return add_finding(args)
        if args.command == "annotate":
            return add_annotation(args)
        if args.command == "add-handoff":
            return add_handoff(args)
    except (OSError, ValueError, KeyError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
