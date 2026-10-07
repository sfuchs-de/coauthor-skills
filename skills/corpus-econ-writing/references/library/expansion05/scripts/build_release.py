#!/usr/bin/env python3
"""Overlay the source-free author extension on the preserved edition04 skill ZIP."""
import argparse
import importlib.util
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parents[1]
EDITION = "2026-10-04-authors-05"
PREVIOUS_HASH = "ba0e1e393d927d9649e68f60c461070a308c5dde4d3e1796c69f51e509025a16"
spec = importlib.util.spec_from_file_location("previous_builder",ROOT.parent / "2026-10-03-expanded-04/scripts/build_release.py")
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)
previous.PREVIOUS_HASH = PREVIOUS_HASH
previous.EDITION = EDITION


def zip_tree(root,destination):
    with zipfile.ZipFile(destination,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for path in sorted(root.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                info=zipfile.ZipInfo((Path(root.name) / path.relative_to(root)).as_posix(),(2026,10,4,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED
                info.create_system=3
                info.external_attr=0o100644 << 16
                archive.writestr(info,path.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--previous",type=Path,default=BASE / "dist/2026-10-03-expanded-04/corpus-econ-writing-2026-10-03-expanded-04.zip")
    args=parser.parse_args()
    output=args.output.resolve()
    if output.exists():
        parser.error("Preserve prior releases: choose a new directory")
    output.mkdir(parents=True)
    previous.extract_previous(args.previous,output)
    skill=output / "corpus-econ-writing"
    library=skill / "references/library"
    expansion=library / "expansion05"
    expansion.mkdir()
    selected=list(ROOT.glob("*.md"))
    for folder in ("data","analysis","vocabulary","scripts","tests","evaluation"):
        selected.extend(p for p in (ROOT / folder).rglob("*") if p.is_file()
            and "__pycache__" not in p.parts and p.suffix not in {".pyc",".pdf",".png"}
            and p != ROOT / "data/extraction.json")
    for path in sorted(selected):
        if path.is_symlink():
            raise ValueError("No source symlinks")
        target=expansion / path.relative_to(ROOT)
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(path,target)
    shutil.copyfile(ROOT / "packaging/verify_authors.py",library / "scripts/verify_authors.py")
    (library / "CURRENT_EDITION.md").write_text(
        "# Current Portable Edition\n\nUse [edition05](expansion05/README.md) and its [policy](expansion05/VOCABULARY_POLICY.md) "
        "for the 45-paper inventory. The [new guide](expansion05/AUTHOR_AND_GENRE_GUIDE.md) supplements "
        "the [preceding argument guide](expansion/ARGUMENT_AND_EXPOSITION.md). The 31-paper expansion and original "
        "23-paper base are preserved.\n\nRun `python3 scripts/verify_authors.py` to verify all inventories offline. "
        "Use `expansion05/scripts/edition.py` for current vocabulary. Source PDFs, full extracted text, and images are excluded.\n")
    provenance={"previous_skill_zip_sha256":PREVIOUS_HASH,
        "expanded_source_receipt_sha256":previous.digest(ROOT / "vocabulary/BUILD_RECEIPT.json"),
        "study_receipt_sha256":previous.digest(ROOT / "analysis/BUILD_RECEIPT.json"),
        "example_audit_sha256":previous.digest(ROOT / "evaluation/CHECKED_AUDIT.json")}
    previous.manifest(library,"library",provenance)
    for source,target in (("SKILL.md","SKILL.md"),("check_vocabulary.py","scripts/check_vocabulary.py"),
                          ("verify_authors.py","scripts/verify_package.py")):
        shutil.copyfile(ROOT / "packaging" / source,skill / target)
    previous.manifest(skill,"skill",{**provenance,"library_manifest_sha256":previous.digest(library / "PACKAGE_MANIFEST.json")})
    portable=output / "spatial-economics-writing-library"
    shutil.copytree(library,portable)
    archives={}
    for folder in (skill,portable):
        target=output / f"{folder.name}-{EDITION}.zip"
        zip_tree(folder,target)
        archives[target.name]={"sha256":previous.digest(target),"size":target.stat().st_size,
                              "manifest_sha256":previous.digest(folder / "PACKAGE_MANIFEST.json")}
    previous.save(output / "RELEASE_RECEIPT.json",{"edition":EDITION,"archives":archives,
        "builder_sha256":previous.digest(Path(__file__)),"provenance":provenance,
        "verification":"Pending separate offline, relocation, and installation checks","excluded":previous.EXCLUDED})
    print(json.dumps(archives,indent=2))


if __name__=="__main__":
    main()
