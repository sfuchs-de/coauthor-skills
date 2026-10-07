#!/usr/bin/env python3
"""Summarize recent GitHub Actions run frequency and wall time for one repository."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path


FIELDS = (
    "databaseId,workflowName,event,conclusion,status,createdAt,updatedAt,"
    "headBranch,displayTitle"
)


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def rounded(value: float) -> float:
    return round(value, 1)


def load_runs(repo: Path, limit: int, repository: str | None) -> list[dict[str, object]]:
    command = ["gh", "run", "list", "--limit", str(limit), "--json", FIELDS]
    if repository:
        command.extend(["--repo", repository])
    result = subprocess.run(
        command,
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown gh error"
        raise RuntimeError(detail)
    return json.loads(result.stdout)


def aggregate(runs: list[dict[str, object]], cutoff: datetime) -> dict[str, object]:
    selected = [run for run in runs if parse_time(str(run["createdAt"])) >= cutoff]
    by_event: dict[str, dict[str, float | int]] = defaultdict(
        lambda: {"runs": 0, "wall_minutes": 0.0, "failures": 0}
    )
    by_workflow: dict[str, dict[str, float | int]] = defaultdict(
        lambda: {"runs": 0, "wall_minutes": 0.0, "failures": 0}
    )
    total_minutes = 0.0

    for run in selected:
        created = parse_time(str(run["createdAt"]))
        updated = parse_time(str(run["updatedAt"]))
        minutes = max(0.0, (updated - created).total_seconds() / 60)
        total_minutes += minutes
        event = str(run.get("event") or "unknown")
        workflow = str(run.get("workflowName") or "unknown")
        failed = run.get("conclusion") == "failure"
        for bucket, key in ((by_event, event), (by_workflow, workflow)):
            bucket[key]["runs"] = int(bucket[key]["runs"]) + 1
            bucket[key]["wall_minutes"] = float(bucket[key]["wall_minutes"]) + minutes
            if failed:
                bucket[key]["failures"] = int(bucket[key]["failures"]) + 1

    def normalize(values: dict[str, dict[str, float | int]]) -> dict[str, dict[str, float | int]]:
        return {
            key: {
                "runs": int(value["runs"]),
                "wall_minutes": rounded(float(value["wall_minutes"])),
                "failures": int(value["failures"]),
            }
            for key, value in sorted(values.items())
        }

    return {
        "runs": len(selected),
        "wall_minutes": rounded(total_minutes),
        "failures": sum(run.get("conclusion") == "failure" for run in selected),
        "by_event": normalize(by_event),
        "by_workflow": normalize(by_workflow),
    }


def recommendations(summary: dict[str, object]) -> list[str]:
    notes: list[str] = []
    by_event = summary["by_event"]
    assert isinstance(by_event, dict)
    if "pull_request" in by_event and "push" in by_event:
        notes.append(
            "Both pull-request and push runs are present; check whether merged PRs repeat the same full gate on main."
        )
    if int(summary["failures"]) > 0:
        notes.append(
            "Failed runs consumed time; inspect logs before rerunning and reproduce failures locally first."
        )
    if float(summary["wall_minutes"]) and int(summary["runs"]):
        average = float(summary["wall_minutes"]) / int(summary["runs"])
        if average >= 2:
            notes.append(
                "Average run duration exceeds two minutes; condition builds, browser installation, and E2E on relevant paths."
            )
    return notes


def print_text(repo: Path, days: int, summary: dict[str, object], workflows: list[str]) -> None:
    print(f"Repository: {repo}")
    print(f"Window: last {days} days")
    print(f"Runs: {summary['runs']}")
    print(f"Observed workflow wall time: {summary['wall_minutes']} minutes")
    print(f"Failures: {summary['failures']}")
    print("Events:")
    for name, values in summary["by_event"].items():
        print(
            f"  {name}: {values['runs']} runs, {values['wall_minutes']} minutes, "
            f"{values['failures']} failures"
        )
    print("Workflows:")
    for name, values in summary["by_workflow"].items():
        print(
            f"  {name}: {values['runs']} runs, {values['wall_minutes']} minutes, "
            f"{values['failures']} failures"
        )
    print("Workflow files:")
    for workflow in workflows or ["(none found)"]:
        print(f"  {workflow}")
    notes = recommendations(summary)
    if notes:
        print("Review opportunities:")
        for note in notes:
            print(f"  - {note}")
    print("Note: wall time is diagnostic and may differ from billed GitHub Actions usage.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Local repository path")
    parser.add_argument("--repository", help="Optional OWNER/REPO override for gh")
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    if args.days <= 0 or args.limit <= 0:
        parser.error("--days and --limit must be positive")
    if not shutil.which("gh"):
        print("error: GitHub CLI (gh) is required", file=sys.stderr)
        return 2

    repo = Path(args.repo).expanduser().resolve()
    if not repo.is_dir():
        print(f"error: repository path does not exist: {repo}", file=sys.stderr)
        return 2

    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
    try:
        summary = aggregate(load_runs(repo, args.limit, args.repository), cutoff)
    except (RuntimeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    workflows = [
        str(path.relative_to(repo))
        for path in sorted((repo / ".github" / "workflows").glob("*.y*ml"))
    ]
    payload = {
        "repository_path": str(repo),
        "period_days": args.days,
        **summary,
        "workflow_files": workflows,
        "recommendations": recommendations(summary),
        "measurement_note": "Observed workflow wall time; not exact billed usage.",
    }
    if args.as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print_text(repo, args.days, summary, workflows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

