#!/usr/bin/env python3
"""Check structural preservation and common TeX build failures."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TOKEN_RE = re.compile(r"@@[A-Z0-9][A-Z0-9-]*@@")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\(?:eqref|ref|autoref|cref|Cref)\{([^}]+)\}")
RESULT_MARKER_RE = re.compile(
    r"^\s*%\s*mathdown-result\s*:\s*([A-Za-z0-9][A-Za-z0-9_.:-]*)\s*$",
    re.MULTILINE | re.IGNORECASE,
)
FATAL_LOG_PATTERNS = {
    "TeX error": re.compile(r"(?m)^! "),
    "undefined references": re.compile(r"undefined references?|Reference .* undefined", re.IGNORECASE),
    "undefined citations": re.compile(r"undefined citations?|Citation .* undefined", re.IGNORECASE),
    "multiply-defined labels": re.compile(r"multiply defined|multiply-defined", re.IGNORECASE),
}
WARNING_LOG_PATTERNS = {
    "overfull boxes": re.compile(r"Overfull \\[hv]box"),
    "underfull boxes": re.compile(r"Underfull \\[hv]box"),
    "rerun requested": re.compile(r"Rerun to get|Label\(s\) may have changed", re.IGNORECASE),
}


def load_inventory(path: Path, require_all_result_tokens: bool) -> tuple[set[str], bool]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "render-mathdown-tex-inventory/v1":
        raise ValueError(f"unsupported inventory schema in {path}")
    summary = data.get("summary", {})
    explicit_ids = set(summary.get("explicit_marker_ids", []))
    if require_all_result_tokens:
        explicit_ids.update(summary.get("result_ids", []))
    return explicit_ids, bool(summary.get("result_ids", []))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check a generated TeX note for source coverage and build failures."
    )
    parser.add_argument("tex", type=Path, help="Generated TeX root")
    parser.add_argument("--inventory", type=Path, help="JSON from inventory_markdown.py")
    parser.add_argument(
        "--require-all-result-tokens",
        action="store_true",
        help="Require every result-like token in the source, including cross-references",
    )
    parser.add_argument("--log", type=Path, help="LaTeX build log")
    parser.add_argument(
        "--strict-log",
        action="store_true",
        help="Treat overfull/underfull boxes and rerun requests as failures",
    )
    args = parser.parse_args()

    if not args.tex.is_file():
        parser.error(f"not a file: {args.tex}")

    text = args.tex.read_text(encoding="utf-8")
    failures: list[str] = []
    warnings: list[str] = []
    strict_log_warnings: list[str] = []

    tokens = sorted(set(TOKEN_RE.findall(text)))
    if tokens:
        failures.append("unresolved template tokens: " + ", ".join(tokens))

    labels = LABEL_RE.findall(text)
    duplicate_labels = sorted({label for label in labels if labels.count(label) > 1})
    if duplicate_labels:
        failures.append("duplicate labels: " + ", ".join(duplicate_labels))

    label_set = set(labels)
    missing_refs = sorted({ref for ref in REF_RE.findall(text) if ref not in label_set})
    if missing_refs:
        failures.append("references without local labels: " + ", ".join(missing_refs))

    tex_result_ids = set(RESULT_MARKER_RE.findall(text))
    if args.inventory:
        try:
            source_result_ids, inventory_has_result_tokens = load_inventory(
                args.inventory, args.require_all_result_tokens
            )
        except (OSError, ValueError, json.JSONDecodeError) as error:
            failures.append(f"could not load inventory: {error}")
        else:
            missing_results = sorted(source_result_ids - tex_result_ids)
            if missing_results:
                failures.append("source result IDs missing TeX markers: " + ", ".join(missing_results))
            if inventory_has_result_tokens and not source_result_ids:
                warnings.append(
                    "inventory has result-like tokens but no explicit source markers; "
                    "verify owner coverage from the result registry"
                )

    if args.log:
        if not args.log.is_file():
            failures.append(f"log file not found: {args.log}")
        else:
            log_text = args.log.read_text(encoding="utf-8", errors="replace")
            for name, pattern in FATAL_LOG_PATTERNS.items():
                if pattern.search(log_text):
                    failures.append(f"build log reports {name}")
            for name, pattern in WARNING_LOG_PATTERNS.items():
                if pattern.search(log_text):
                    warning = f"build log reports {name}"
                    warnings.append(warning)
                    strict_log_warnings.append(warning)

    print(f"TeX: {args.tex.resolve()}")
    print(f"Labels: {len(labels)}; result markers: {len(tex_result_ids)}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for failure in failures:
        print(f"ERROR: {failure}")

    if failures or (args.strict_log and strict_log_warnings):
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
