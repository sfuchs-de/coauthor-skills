#!/usr/bin/env python3
"""Build a source-free theory release on the hash-pinned urban06 ZIP."""
import argparse
import importlib.util
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT.parents[1]
EDITION = "2026-10-04-theory-08"
PREVIOUS_HASH = "4317a8e34ef5a8fb8179cd0fce94578aafd3cdecd9d875d20af7c33ed7cd5ec8"
SOURCE = ROOT.parent / "2026-10-03-expanded-04/scripts/build_release.py"
SPEC = importlib.util.spec_from_file_location("theory08_archive_builder", SOURCE)
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)
if Path(helper.__file__).resolve() != SOURCE.resolve():
    raise ValueError("Wrong archive helper origin")
helper.PREVIOUS_HASH = PREVIOUS_HASH
helper.EDITION = EDITION


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--previous", type=Path, default=LIBRARY / "dist/2026-10-04-urban-06/corpus-econ-writing-2026-10-04-urban-06.zip")
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        parser.error("Choose a new release directory")
    output.mkdir(parents=True)
    helper.extract_previous(args.previous,output)
    skill = output / "corpus-econ-writing"
    library = skill / "references/library"
    extension = library / "expansion08"
    extension.mkdir()
    selected = list(ROOT.glob("*.md"))
    for folder in ("data","analysis","vocabulary","scripts","tests","evaluation"):
        selected.extend(p for p in (ROOT / folder).rglob("*") if p.is_file()
                        and "__pycache__" not in p.parts and p.suffix not in {".pyc",".pdf",".png"}
                        and p != ROOT / "data/extraction.json")
    for path in sorted(selected):
        if path.is_symlink():
            raise ValueError("No source symlinks")
        target = extension / path.relative_to(ROOT)
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(path,target)
    # The complete publication preservation map stays local, not in a writing skill.
    freeze = json.loads((ROOT / "data/PRESERVATION_FREEZE.json").read_text())
    helper.save(extension / "data/PRESERVATION_FREEZE.json", {
        "protocol_sha256": freeze["protocol_sha256"], "installed_manifest_sha256": freeze["installed_manifest_sha256"],
        "protected_files_count": len(freeze["files"]), "full_records_local_only": True})
    shutil.copyfile(ROOT / "packaging/verify_theory.py",library / "scripts/verify_theory.py")
    (library / "CURRENT_EDITION.md").write_text(
        "# Portable Writing Editions\n\nUse [theory08](expansion08/README.md), its "
        "[policy](expansion08/VOCABULARY_POLICY.md), and [guide](expansion08/THEORY_EXPOSITION.md) "
        "by default: 59 papers including the urban and transport extension. "
        "The [urban53](expansion06/README.md), [authors45](expansion05/README.md), "
        "[expanded31](expansion/README.md), and original23 inventories remain selectable.\n\n"
        "Run `python3 scripts/verify_theory.py` for offline verification. "
        "Source PDFs, full text, page images, and the full project-preservation map are excluded.\n")
    provenance = {"previous_skill_zip_sha256": PREVIOUS_HASH,
                  "theory_inventory_receipt_sha256": helper.digest(ROOT / "vocabulary/BUILD_RECEIPT.json"),
                  "study_receipt_sha256": helper.digest(ROOT / "analysis/STUDY_RECEIPT.json"),
                  "example_audit_sha256": helper.digest(ROOT / "evaluation/VERIFIED_AUDIT.json"),
                  "default_papers":59, "preserved_inventories":[23,31,45,53]}
    helper.manifest(library,"library",provenance)
    for source,target in (("SKILL.md","SKILL.md"), ("check_vocabulary.py","scripts/check_vocabulary.py"),
                          ("verify_theory.py","scripts/verify_package.py")):
        shutil.copyfile(ROOT / "packaging" / source,skill / target)
    helper.manifest(skill,"skill",{**provenance,"library_manifest_sha256":helper.digest(library / "PACKAGE_MANIFEST.json")})
    portable = output / "spatial-economics-writing-library"
    shutil.copytree(library,portable)
    archives = {}
    for folder in (skill,portable):
        archive = output / f"{folder.name}-{EDITION}.zip"
        helper.zip_tree(folder,archive)
        archives[archive.name] = {"sha256":helper.digest(archive), "size":archive.stat().st_size,
                                  "manifest_sha256":helper.digest(folder / "PACKAGE_MANIFEST.json")}
    helper.save(output / "RELEASE_RECEIPT.json", {"edition":EDITION,"archives":archives,
                "builder_sha256":helper.digest(Path(__file__)),"provenance":provenance,
                "verification":"Pending external offline, relocation, installation, and deterministic receipts",
                "excluded":helper.EXCLUDED})
    print(json.dumps(archives,indent=2))


if __name__ == "__main__":
    main()
