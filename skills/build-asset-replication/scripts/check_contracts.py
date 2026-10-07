#!/usr/bin/env python3
"""Check replication metadata consistency; never certify scientific reproduction."""
from __future__ import annotations

import argparse
import json
import re
from collections import deque
from pathlib import Path, PurePosixPath

PROVENANCE = {"verified_exact", "verified_renamed", "producer_identified", "artifact_only", "manual_source", "unresolved"}
DATA_CLASSES = {"public-redistributable", "public-download-required", "restricted", "licensed", "author-created", "unknown"}
RESULT_KINDS = {"table-cell", "figure-series", "claim", "calibration", "ranking", "diagnostic", "external-statistic", "authored"}


def safe_path(value: object) -> bool:
    if not isinstance(value, str) or not value or any(c in value for c in ("\\", ":", "$", "\0")):
        return False
    path = PurePosixPath(value)
    return (bool(path.parts) and not path.is_absolute() and path.as_posix() == value
            and not any(p in {".", "..", ".git"} for p in path.parts)
            and not value.startswith("~"))


def check(spec: object) -> dict:
    errors, uncovered = [], []
    if not isinstance(spec, dict):
        return {"contract_errors": ["Root must be an object"], "uncovered": [], "certification": "not assessed"}
    if type(spec.get("schema_version")) is not int or spec["schema_version"] != 1:
        errors.append("Expected schema_version 1")
    target = spec.get("target", {})
    if not isinstance(target, dict) or not all(isinstance(target.get(k), str) and target[k].strip() for k in ("kind", "version")):
        errors.append("Target needs a kind and frozen version")

    tables = {}
    for name in ("inputs", "tasks", "assets", "results"):
        records = spec.get(name)
        if not isinstance(records, list):
            errors.append(f"{name}: expected a list")
            records = []
        index = {}
        for row in records:
            if not isinstance(row, dict):
                errors.append(f"{name}: non-object record")
                continue
            rid = row.get("id")
            if not isinstance(rid, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", rid):
                errors.append(f"{name}: invalid ID")
                continue
            if rid in index:
                errors.append(f"{name}: duplicate ID {rid}")
            else:
                index[rid] = row
        tables[name] = index
    if not tables["assets"] or not tables["results"]:
        uncovered.append("Target asset/result inventory is empty")

    def sequence(row, field, *, required=False):
        values = row.get(field)
        if not isinstance(values, list) or not all(isinstance(x, str) and x.strip() for x in values):
            errors.append(f"{row['id']}: {field} must be a list of nonempty strings")
            return []
        if len(values) != len(set(values)):
            errors.append(f"{row['id']}: duplicate {field}")
        if required and not values:
            uncovered.append(f"{row['id']}: missing {field}")
        return values

    def path(row, field="path"):
        value = row.get(field)
        if not safe_path(value):
            errors.append(f"{row['id']}: unsafe or missing {field}")
            return None
        return value

    input_paths = set()
    for row in tables["inputs"].values():
        value = path(row)
        if value in input_paths:
            errors.append(f"{row['id']}: duplicate input path")
        if value:
            input_paths.add(value)
        digest = row.get("sha256")
        if digest is None or digest == "":
            uncovered.append(f"{row['id']}: input hash not pinned")
        elif not isinstance(digest, str) or not re.fullmatch(r"[a-fA-F0-9]{64}", digest):
            errors.append(f"{row['id']}: malformed SHA-256")
        if not isinstance(row.get("data_class"), str) or row["data_class"] not in DATA_CLASSES:
            errors.append(f"{row['id']}: invalid data_class")
        elif row["data_class"] == "unknown":
            uncovered.append(f"{row['id']}: access/redistribution class unresolved")
        if not isinstance(row.get("source_level"), str) or row["source_level"] not in {"provider", "prepared", "derived"}:
            errors.append(f"{row['id']}: invalid source_level")

    graph, outputs = {}, {}
    for rid, row in tables["tasks"].items():
        for iid in sequence(row, "input_ids"):
            if iid not in tables["inputs"]:
                errors.append(f"{rid}: unknown input {iid}")
        dependencies = sequence(row, "dependencies")
        graph[rid] = dependencies
        for did in dependencies:
            if did not in tables["tasks"]:
                errors.append(f"{rid}: unknown dependency {did}")
        for p in sequence(row, "code_paths", required=True):
            if not safe_path(p):
                errors.append(f"{rid}: unsafe code path")
        for p in sequence(row, "output_paths", required=True):
            if not safe_path(p):
                errors.append(f"{rid}: unsafe output path")
            if p in input_paths:
                errors.append(f"{rid}: output overwrites a declared input")
            if p in outputs:
                errors.append(f"{rid}: output already owned by {outputs[p]}")
            outputs[p] = rid
        if not isinstance(row.get("command"), str) or not row["command"].strip():
            uncovered.append(f"{rid}: executable command unresolved")

    # Iterative topological check also handles long warm-start sequences.
    waiting = {rid: len(set(dep for dep in deps if dep in graph)) for rid, deps in graph.items()}
    consumers = {rid: [] for rid in graph}
    for rid, deps in graph.items():
        for dep in set(deps):
            if dep in consumers:
                consumers[dep].append(rid)
    queue = deque(rid for rid, count in waiting.items() if count == 0)
    while queue:
        rid = queue.popleft()
        for consumer in consumers[rid]:
            waiting[consumer] -= 1
            if waiting[consumer] == 0:
                queue.append(consumer)
    if any(waiting.values()):
        errors.append("Dependency cycle in task graph")

    for rid, row in tables["assets"].items():
        p = path(row)
        sequence(row, "anchors", required=True)
        kind = row.get("kind")
        producer = row.get("producer_task")
        if not isinstance(kind, str) or kind not in {"generated", "static", "authored"}:
            errors.append(f"{rid}: invalid asset kind")
        if not isinstance(row.get("provenance_status"), str) or row["provenance_status"] not in PROVENANCE:
            errors.append(f"{rid}: invalid provenance_status")
        elif row["provenance_status"] in {"unresolved", "artifact_only"}:
            uncovered.append(f"{rid}: source-to-output chain unresolved")
        if producer is not None and (not isinstance(producer, str) or producer not in tables["tasks"]):
            errors.append(f"{rid}: unknown producer")
        if kind == "generated":
            if producer is None:
                uncovered.append(f"{rid}: generated asset lacks producer")
            elif p and outputs.get(p) != producer:
                errors.append(f"{rid}: producer does not declare asset output")
        elif not isinstance(row.get("origin"), str) or not row["origin"].strip():
            uncovered.append(f"{rid}: static/authored origin undocumented")

    for rid, row in tables["results"].items():
        sequence(row, "anchors", required=True)
        for aid in sequence(row, "asset_ids"):
            if aid not in tables["assets"]:
                errors.append(f"{rid}: unknown asset {aid}")
        kind = row.get("kind")
        producer = row.get("producer_task")
        if not isinstance(kind, str) or kind not in RESULT_KINDS:
            errors.append(f"{rid}: invalid result kind")
        if producer is not None and (not isinstance(producer, str) or producer not in tables["tasks"]):
            errors.append(f"{rid}: unknown producer")
        if kind not in ("external-statistic", "authored") and producer is None:
            uncovered.append(f"{rid}: computational producer unresolved")
        comparison = row.get("comparison")
        if not isinstance(comparison, dict) or not all(isinstance(comparison.get(k), str) and comparison[k].strip() for k in ("method", "rule", "unit")):
            uncovered.append(f"{rid}: comparison contract incomplete")
        elif comparison['unit'].lower() == 'unknown':
            uncovered.append(f"{rid}: units unresolved")
        status = row.get("status")
        if not isinstance(status, str) or status not in {"pending", "verified", "discrepancy", "blocked", "documented-static"}:
            errors.append(f"{rid}: invalid result status")
        elif status == "verified":
            if not safe_path(row.get("receipt")):
                errors.append(f"{rid}: verified declaration lacks a safe receipt path")
        elif status == "documented-static":
            if kind not in ("external-statistic", "authored") or not isinstance(row.get("origin"), str) or not row["origin"].strip():
                errors.append(f"{rid}: undocumented or computational result labeled static")
        else:
            uncovered.append(f"{rid}: evidence status is {status}")

    return {"counts": {k: len(v) for k, v in tables.items()}, "contract_errors": sorted(set(errors)),
            "uncovered": sorted(set(uncovered)), "certification": "not assessed",
            "scope": "Metadata only; no file hashes, scientific results, or receipts were independently verified"}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key")
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--require-covered", action="store_true")
    args = parser.parse_args()
    try:
        spec = json.loads(args.manifest.read_text(), object_pairs_hook=unique_object)
        result = check(spec)
    except (OSError, ValueError) as error:
        parser.exit(2, f"Cannot read contracts: {type(error).__name__}\n")
    print(json.dumps(result, indent=2))
    if result["contract_errors"]:
        raise SystemExit(1)
    if args.require_covered and result["uncovered"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
