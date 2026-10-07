#!/usr/bin/env python3
"""Install one or more skills from this repository into Codex's skill directory."""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = REPO_ROOT / "skills"


def default_target() -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
    return codex_home / "skills"


def skill_names() -> list[str]:
    return sorted(path.name for path in SOURCE_ROOT.iterdir() if (path / "SKILL.md").is_file())


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def same_install(source: Path, destination: Path, mode: str) -> bool:
    if destination.is_symlink():
        return mode == "symlink" and destination.resolve() == source.resolve()
    return mode == "copy" and destination.is_dir() and tree_digest(source) == tree_digest(destination)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=default_target())
    parser.add_argument("--mode", choices=("copy", "symlink"), default="copy")
    parser.add_argument("--skill", action="append", dest="skills", help="Install only this skill; repeat as needed")
    parser.add_argument("--force", action="store_true", help="Back up and replace differing installations")
    parser.add_argument("--dry-run", action="store_true", help="Describe changes without writing them")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    available = skill_names()
    selected = args.skills or available
    unknown = sorted(set(selected) - set(available))
    if unknown:
        print(f"Unknown skill(s): {', '.join(unknown)}", file=sys.stderr)
        print(f"Available: {', '.join(available)}", file=sys.stderr)
        return 2

    target = args.target.expanduser().resolve()
    actions: list[tuple[str, Path, Path]] = []
    conflicts: list[Path] = []
    for name in selected:
        source = SOURCE_ROOT / name
        destination = target / name
        if same_install(source, destination, args.mode):
            actions.append(("unchanged", source, destination))
        elif destination.exists() or destination.is_symlink():
            if args.force:
                actions.append(("replace", source, destination))
            else:
                conflicts.append(destination)
        else:
            actions.append(("install", source, destination))

    if conflicts:
        print("Refusing to replace differing installations:", file=sys.stderr)
        for path in conflicts:
            print(f"  {path}", file=sys.stderr)
        print("Review the differences, then rerun with --force if replacement is intended.", file=sys.stderr)
        return 1

    for action, source, destination in actions:
        print(f"{action}: {source.name} -> {destination}")
        if args.dry_run or action == "unchanged":
            continue
        target.mkdir(parents=True, exist_ok=True)
        if action == "replace":
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            backup_root = target.parent / "skill-backups" / stamp
            backup = backup_root / destination.name
            counter = 1
            while backup.exists() or backup.is_symlink():
                backup = backup_root.with_name(f"{stamp}-{counter}") / destination.name
                counter += 1
            backup.parent.mkdir(parents=True, exist_ok=True)
            destination.rename(backup)
            print(f"backup: {backup}")
        if args.mode == "copy":
            shutil.copytree(source, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            destination.symlink_to(source, target_is_directory=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
