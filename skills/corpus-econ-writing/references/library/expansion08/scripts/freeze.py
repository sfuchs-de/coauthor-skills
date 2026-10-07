#!/usr/bin/env python3
"""Freeze prior resources and publication sources before the resource update."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT.parents[1]
PROJECT = LIBRARY.parent


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def selected():
    for folder in ("sources", "extracted", "database", "vocabulary", "scripts", "data",
                   "editions/2026-10-03-expanded-04", "editions/2026-10-04-authors-05",
                   "editions/2026-10-04-urban-06", "evaluation/2026-10-04/theory-07"):
        for path in (LIBRARY / folder).rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
                yield path
    for folder in ("paper", "presentation"):
        for path in (PROJECT / folder).rglob("*"):
            if path.is_file() and path.suffix in {".tex", ".bib", ".sty", ".cls", ".pdf"}:
                yield path


def main():
    target = ROOT / "data/PRESERVATION_FREEZE.json"
    if target.exists():
        raise SystemExit("Preserve the existing freeze")
    files = {p.relative_to(PROJECT).as_posix(): digest(p) for p in sorted(set(selected()))}
    manifest = Path.home() / ".codex/skills/corpus-econ-writing/PACKAGE_MANIFEST.json"
    protocol = ROOT / "evaluation/PROTOCOL.md"
    receipt = {"files": files, "installed_manifest_sha256": digest(manifest),
               "protocol_sha256": digest(protocol), "scope": "No publication edits authorized"}
    target.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"frozen_files": len(files), "protocol_sha256": receipt["protocol_sha256"]}))


if __name__ == "__main__":
    main()
