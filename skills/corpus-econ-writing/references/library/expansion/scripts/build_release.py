#!/usr/bin/env python3
"""Overlay source-free edition 04 on the preserved Candidate03 ZIP."""
import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parents[1]
EDITION = "2026-10-03-expanded-04"
PREVIOUS_HASH = "93d8cc6dbf81259164ac5a51c01a851888adbfdce7478cac36ee7be10c4022ed"
EXCLUDED = ["sources/", "extracted/", "visual_review/", "data/extraction.json", "__pycache__/", "packaging/", "*.pdf", "*.png"]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n")


def manifest(root, kind, provenance):
    files = {p.relative_to(root).as_posix(): {"sha256": digest(p), "size": p.stat().st_size}
             for p in sorted(root.rglob("*")) if p.is_file() and "__pycache__" not in p.parts
             and p != root / "PACKAGE_MANIFEST.json"}
    save(root / "PACKAGE_MANIFEST.json", {"schema_version": 1, "kind": kind,
         "edition": EDITION, "provenance": provenance, "excluded": EXCLUDED,
         "source_review_rerun_by_package": False, "files": files})


def extract_previous(archive, destination):
    if digest(archive) != PREVIOUS_HASH:
        raise ValueError("Changed preserved Candidate03 ZIP")
    with zipfile.ZipFile(archive) as zipped:
        names = zipped.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Duplicate ZIP member")
        for info in zipped.infolist():
            relative = Path(info.filename)
            if relative.is_absolute() or ".." in relative.parts or "\\" in info.filename or relative.parts[0] != "corpus-econ-writing":
                raise ValueError("Unsafe ZIP member")
            if (info.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError("ZIP symlink")
        zipped.extractall(destination)


def zip_tree(root, destination):
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(root.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            info = zipfile.ZipInfo((Path(root.name) / path.relative_to(root)).as_posix(), (2026, 10, 3, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--previous", type=Path, default=BASE / "dist/2026-10-03-candidate-03/corpus-econ-writing-2026-10-03.zip")
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        parser.error("Use a new release directory; earlier releases stay unchanged")
    output.mkdir(parents=True)
    extract_previous(args.previous, output)
    skill = output / "corpus-econ-writing"
    library = skill / "references/library"
    expansion = library / "expansion"
    expansion.mkdir()
    selected = list(ROOT.glob("*.md"))
    for folder in ("data", "analysis", "vocabulary", "scripts", "tests", "evaluation"):
        selected.extend(p for p in (ROOT / folder).rglob("*") if p.is_file()
                        and "__pycache__" not in p.parts and p.suffix not in {".pyc", ".pdf", ".png"}
                        and p != ROOT / "data/extraction.json")
    for path in sorted(selected):
        if path.is_symlink():
            raise ValueError("Refuse source symlinks")
        target = expansion / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    shutil.copyfile(ROOT / "packaging/verify_expansion.py", library / "scripts/verify_expansion.py")
    (library / "CURRENT_EDITION.md").write_text(
        "# Current Portable Edition\n\n"
        "Use [expanded edition 04](expansion/README.md), its [policy](expansion/VOCABULARY_POLICY.md), "
        "and [argument guide](expansion/ARGUMENT_AND_EXPOSITION.md) for the 31-paper edition. "
        "The original README, database, and 23-paper checker remain frozen as the base.\n\n"
        "Run `python3 scripts/verify_expansion.py` to verify both inventories offline. "
        "Use `expansion/scripts/edition.py` for the expanded vocabulary; "
        "use `scripts/vocabulary.py` explicitly for the original inventory. "
        "Sources, full text, and rendered pages are excluded.\n")
    previous = {"previous_skill_zip_sha256": PREVIOUS_HASH,
                "expanded_source_receipt_sha256": digest(ROOT / "vocabulary/BUILD_RECEIPT.json"),
                "study_receipt_sha256": digest(ROOT / "analysis/BUILD_RECEIPT.json")}
    manifest(library, "library", previous)
    for source, target in (("SKILL.md", "SKILL.md"), ("check_vocabulary.py", "scripts/check_vocabulary.py"),
                           ("verify_expansion.py", "scripts/verify_package.py")):
        shutil.copyfile(ROOT / "packaging" / source, skill / target)
    manifest(skill, "skill", {**previous, "library_manifest_sha256": digest(library / "PACKAGE_MANIFEST.json")})
    portable = output / "spatial-economics-writing-library"
    shutil.copytree(library, portable)
    archives = {}
    for folder in (skill, portable):
        archive = output / f"{folder.name}-{EDITION}.zip"
        zip_tree(folder, archive)
        archives[archive.name] = {"sha256": digest(archive), "size": archive.stat().st_size,
                                 "manifest_sha256": digest(folder / "PACKAGE_MANIFEST.json")}
    save(output / "RELEASE_RECEIPT.json", {"edition": EDITION, "archives": archives,
        "builder_sha256": digest(Path(__file__)), "provenance": previous,
        "verification": "Pending separate offline, relocation, and installation checks", "excluded": EXCLUDED})
    print(json.dumps(archives, indent=2))


if __name__ == "__main__":
    main()
