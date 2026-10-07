#!/usr/bin/env python3
"""Verify and summarize iterative ai-slop-lint cleanup passes.

This script compares JSON outputs produced by ai_slop_lint.py. It is meant to
make cleanup loops auditable: initial scan, bounded rewrite, rescan, repeat,
then final strict gate.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


def load_scan(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"error: could not read scan JSON {path}: {exc}") from exc
    if not isinstance(payload, dict) or "gate" not in payload or "score" not in payload:
        raise SystemExit(f"error: {path} does not look like ai_slop_lint.py JSON output")
    return payload


def finding_signature(finding: dict[str, Any]) -> tuple[str, int, str, str]:
    return (
        str(finding.get("path", "")),
        int(finding.get("line", 0) or 0),
        str(finding.get("rule_id", "")),
        str(finding.get("match", "")).lower(),
    )


def summarize(path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    gate = payload.get("gate", {}) or {}
    findings = payload.get("findings", []) or []
    actionable = payload.get("actionable_findings", []) or []
    paragraphs = payload.get("paragraphs", []) or []
    categories = Counter(str(finding.get("category", "unknown")) for finding in actionable)
    priorities = Counter(str(finding.get("priority", "unknown")) for finding in actionable)
    return {
        "path": str(path),
        "score": int(payload.get("score", 0) or 0),
        "score_components": payload.get("score_components", {}) or {},
        "gate_passed": bool(gate.get("passed", False)),
        "actionable_count": int(gate.get("actionable_count", len(actionable)) or 0),
        "actionable_score": int(gate.get("actionable_score", 0) or 0),
        "p0": int(gate.get("p0", priorities.get("P0", 0)) or 0),
        "p1": int(gate.get("p1", priorities.get("P1", 0)) or 0),
        "p2": int(gate.get("p2", priorities.get("P2", 0)) or 0),
        "finding_count": len(findings),
        "paragraph_count": len(paragraphs),
        "categories": dict(categories),
        "actionable_signatures": {finding_signature(finding) for finding in actionable},
    }


def compute_deltas(summaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deltas = []
    for idx, (before, after) in enumerate(zip(summaries, summaries[1:]), start=1):
        before_sigs = before["actionable_signatures"]
        after_sigs = after["actionable_signatures"]
        deltas.append(
            {
                "step": idx,
                "from": before["path"],
                "to": after["path"],
                "score_delta": after["score"] - before["score"],
                "actionable_delta": after["actionable_count"] - before["actionable_count"],
                "actionable_score_delta": after["actionable_score"] - before["actionable_score"],
                "removed_actionable": len(before_sigs - after_sigs),
                "new_actionable": len(after_sigs - before_sigs),
            }
        )
    return deltas


def verify(summaries: list[dict[str, Any]], args: argparse.Namespace) -> tuple[bool, list[str]]:
    messages: list[str] = []
    if len(summaries) < args.min_scans:
        messages.append(f"expected at least {args.min_scans} scan snapshots, found {len(summaries)}")

    initial = summaries[0]
    final = summaries[-1]
    if args.allow_clean_initial and len(summaries) == 1 and initial["gate_passed"]:
        return not messages, messages

    if args.require_final_pass and not final["gate_passed"]:
        messages.append("final scan gate did not pass")

    if args.require_improvement:
        improved = (
            final["actionable_count"] < initial["actionable_count"]
            or final["actionable_score"] < initial["actionable_score"]
            or final["score"] < initial["score"]
        )
        if initial["gate_passed"] and not args.require_improvement_when_initial_passes:
            improved = True
        if not improved:
            messages.append("no improvement from first scan to final scan")

    if args.require_rescan_after_failure and not initial["gate_passed"] and len(summaries) < 2:
        messages.append("initial scan failed, but no rescan snapshot was provided")

    return not messages, messages


def render_markdown(summaries: list[dict[str, Any]], deltas: list[dict[str, Any]], ok: bool, messages: list[str]) -> str:
    lines: list[str] = []
    lines.append("# AI Slop Iteration Report")
    lines.append("")
    lines.append("This report verifies scan, rewrite, rescan evidence. It is still a style lint, not proof of authorship.")
    lines.append("")
    lines.append("## Passes")
    lines.append("")
    lines.append("| Pass | Gate | Score | Actionable | P0 | P1 | P2 | Paragraphs | File |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for idx, summary in enumerate(summaries):
        gate = "PASS" if summary["gate_passed"] else "FAIL"
        lines.append(
            "| "
            + " | ".join(
                [
                    str(idx),
                    gate,
                    str(summary["score"]),
                    str(summary["actionable_count"]),
                    str(summary["p0"]),
                    str(summary["p1"]),
                    str(summary["p2"]),
                    str(summary["paragraph_count"]),
                    f"`{summary['path']}`",
                ]
            )
            + " |"
        )
    lines.append("")
    lines.append("## Deltas")
    lines.append("")
    if not deltas:
        lines.append("- No pass-to-pass deltas available.")
    else:
        for delta in deltas:
            lines.append(
                "- Pass {step}: score {score_delta:+d}, actionable {actionable_delta:+d}, "
                "actionable score {actionable_score_delta:+d}, removed {removed_actionable}, new {new_actionable}.".format(**delta)
            )
    lines.append("")
    lines.append("## Verdict")
    lines.append("")
    lines.append(f"- Verification: {'PASS' if ok else 'FAIL'}")
    for message in messages:
        lines.append(f"- {message}")
    return "\n".join(lines)


def render_json(summaries: list[dict[str, Any]], deltas: list[dict[str, Any]], ok: bool, messages: list[str]) -> str:
    serializable = []
    for summary in summaries:
        item = dict(summary)
        item.pop("actionable_signatures", None)
        serializable.append(item)
    return json.dumps(
        {
            "ok": ok,
            "messages": messages,
            "passes": serializable,
            "deltas": deltas,
        },
        indent=2,
        sort_keys=True,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify iterative ai-slop-lint scan snapshots.")
    parser.add_argument("scans", nargs="+", help="ai_slop_lint.py JSON outputs in pass order.")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--min-scans", type=int, default=2, help="Minimum scan snapshots required.")
    parser.add_argument("--allow-clean-initial", action="store_true", help="Allow one passing initial scan.")
    parser.add_argument("--require-improvement", action="store_true", help="Require final scan to improve over initial scan.")
    parser.add_argument(
        "--require-improvement-when-initial-passes",
        action="store_true",
        help="Also require improvement when the first scan already passed.",
    )
    parser.add_argument("--require-final-pass", action="store_true", help="Require final scan gate to pass.")
    parser.add_argument(
        "--require-rescan-after-failure",
        action="store_true",
        help="Require at least one rescan when the first scan failed.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    paths = [Path(raw).expanduser() for raw in args.scans]
    summaries = [summarize(path, load_scan(path)) for path in paths]
    deltas = compute_deltas(summaries)
    ok, messages = verify(summaries, args)
    if args.format == "json":
        print(render_json(summaries, deltas, ok, messages))
    else:
        print(render_markdown(summaries, deltas, ok, messages))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
