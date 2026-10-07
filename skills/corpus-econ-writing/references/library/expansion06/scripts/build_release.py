#!/usr/bin/env python3
"""Add the source-free opt-in urban extension to the frozen authors05 release."""
import argparse
import importlib.util
import json
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parents[1]
EDITION="2026-10-04-urban-06"
PREVIOUS_HASH="197338126183a43e7b1ac8eb083d8974b49289978b738a3142aaa6f3d92459f6"
spec=importlib.util.spec_from_file_location("prior_builder",ROOT.parent / "2026-10-04-authors-05/scripts/build_release.py")
prior=importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
helpers=prior.previous
helpers.PREVIOUS_HASH=PREVIOUS_HASH
helpers.EDITION=EDITION


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--previous",type=Path,default=BASE / "dist/2026-10-04-authors-05/corpus-econ-writing-2026-10-04-authors-05.zip")
    args=parser.parse_args()
    output=args.output.resolve()
    if output.exists(): parser.error("Choose a new release directory")
    output.mkdir(parents=True)
    helpers.extract_previous(args.previous,output)
    skill=output / "corpus-econ-writing"
    library=skill / "references/library"
    extension=library / "expansion06"
    extension.mkdir()
    selected=list(ROOT.glob("*.md"))
    for folder in ("data","analysis","vocabulary","scripts","tests","evaluation"):
        selected.extend(p for p in (ROOT / folder).rglob("*") if p.is_file()
            and "__pycache__" not in p.parts and p.suffix not in {".pyc",".pdf",".png"}
            and p!=ROOT / "data/extraction.json")
    for path in sorted(selected):
        if path.is_symlink(): raise ValueError("No source symlinks")
        target=extension / path.relative_to(ROOT)
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(path,target)
    shutil.copyfile(ROOT / "packaging/verify_urban.py",library / "scripts/verify_urban.py")
    (library / "CURRENT_EDITION.md").write_text(
        "# Portable Writing Editions\n\nThe general default remains [authors05](expansion05/README.md), with 45 papers. "
        "For urban writing, select [urban06](expansion06/README.md), its [guide](expansion06/URBAN_EXPOSITION.md), "
        "and [policy](expansion06/VOCABULARY_POLICY.md): 53 papers. The 31- and 23-paper inventories remain frozen.\n\n"
        "Run `python3 scripts/verify_urban.py` for offline checks. Use `expansion06/scripts/edition.py` for the urban inventory "
        "and `expansion05/scripts/edition.py` for the general default. Source PDFs, full extracted text, and page images are excluded.\n")
    provenance={"previous_skill_zip_sha256":PREVIOUS_HASH,
        "urban_source_receipt_sha256":helpers.digest(ROOT / "vocabulary/BUILD_RECEIPT.json"),
        "study_receipt_sha256":helpers.digest(ROOT / "analysis/BUILD_RECEIPT.json"),
        "example_audit_sha256":helpers.digest(ROOT / "evaluation/CHECKED_AUDIT.json"),
        "general_default_papers":45,"urban_opt_in_papers":53}
    helpers.manifest(library,"library",provenance)
    for source,target in (("SKILL.md","SKILL.md"),("check_vocabulary.py","scripts/check_vocabulary.py"),
                          ("verify_urban.py","scripts/verify_package.py")):
        shutil.copyfile(ROOT / "packaging" / source,skill / target)
    helpers.manifest(skill,"skill",{**provenance,"library_manifest_sha256":helpers.digest(library / "PACKAGE_MANIFEST.json")})
    portable=output / "spatial-economics-writing-library"
    shutil.copytree(library,portable)
    archives={}
    for folder in (skill,portable):
        archive=output / f"{folder.name}-{EDITION}.zip"
        prior.zip_tree(folder,archive)
        archives[archive.name]={"sha256":helpers.digest(archive),"size":archive.stat().st_size,
                               "manifest_sha256":helpers.digest(folder / "PACKAGE_MANIFEST.json")}
    helpers.save(output / "RELEASE_RECEIPT.json",{"edition":EDITION,"archives":archives,
        "builder_sha256":helpers.digest(Path(__file__)),"provenance":provenance,
        "verification":"Pending offline, relocation, installation and deterministic checks","excluded":helpers.EXCLUDED})
    print(json.dumps(archives,indent=2))


if __name__=="__main__": main()
