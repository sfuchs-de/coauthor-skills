#!/usr/bin/env python3
"""Verify the 45-paper edition and both preserved inventories without source files."""
import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def run(arguments, expected=0):
    result = subprocess.run([sys.executable,"-B",*map(str,arguments)], capture_output=True,
                            text=True,timeout=240)
    if result.returncode != expected:
        raise ValueError(f"Unexpected exit {result.returncode}: {result.stderr[-2000:]}")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    library = root / "references/library" if (root / "SKILL.md").is_file() else root
    if args.output and (args.output.resolve().is_relative_to(root) or args.output.exists()):
        parser.error("Write a new receipt outside the frozen package")
    spec = importlib.util.spec_from_file_location("base_verifier",library / "scripts/verify_package.py")
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    manifest = verifier.verify_manifest(root)
    previous = json.loads(run([library / "scripts/verify_expansion.py"]).stdout)
    links = verifier.verify_links(root)
    extension = library / "expansion05"
    checked = json.loads(run([extension / "scripts/edition.py","verify"]).stdout)
    tests = run(["-m","unittest","discover","-s",extension / "tests","-v"])
    count = re.search(r"Ran (\d+) tests",tests.stderr)
    if not count or int(count[1]) != 24:
        raise ValueError("Incomplete author-extension tests")
    examples = json.loads(run([extension / "scripts/audit_examples.py"]).stdout)
    if examples["lexical_passes"] != 6:
        raise ValueError("Unchecked revised examples")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "example.tex"
        for value,code in (("The model explains income and prices.",0),("zzzznewunattestedword",1)):
            path.write_text(value)
            run([extension / "scripts/edition.py","check",path,"--strict"],code)
        if library != root:
            lookup = json.loads(run([root / "scripts/check_vocabulary.py","lookup","working"] ).stdout)
            if lookup["word"] != "working" or not lookup["record"]:
                raise ValueError("Wrong default inventory")
            run([root / "scripts/check_vocabulary.py","--previous","lookup","afford"])
            run([root / "scripts/check_vocabulary.py","--base","lookup","heterogeneity"])
            run([root / "scripts/check_vocabulary.py","--base","--previous","lookup","working"],1)
    summary = {"package_verified":True,"kind":manifest["kind"],
        "manifest_sha256":hashlib.sha256((root / "PACKAGE_MANIFEST.json").read_bytes()).hexdigest(),
        "packaged_files_checked":len(manifest["files"]),"local_links_checked":links,
        "base_tests":previous["base_tests"],"previous_expansion_tests":previous["expanded_tests"],
        "author_extension_tests":int(count[1]),"expanded_counts":checked["counts"],
        "six_new_examples_lexically_replayed":True,"source_screen_rerun":False,
        "previous_examples_preserved":True,"source_pdfs_included":False,"network_required":False,
        "independent_writing_validation":False,
        "limits":"Offline artifact checks, not a fresh source review or independent quality evaluation"}
    value = json.dumps(summary,indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(value)
    print(value,end="")


if __name__ == "__main__":
    main()
