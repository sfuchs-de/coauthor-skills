#!/usr/bin/env python3
"""Verify the opt-in urban extension and all preserved inventories offline."""
import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def run(args,expected=0):
    result=subprocess.run([sys.executable,"-B",*map(str,args)],capture_output=True,text=True,timeout=240)
    if result.returncode!=expected:
        raise ValueError(f"Unexpected exit {result.returncode}: {result.stderr[-2000:]}")
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    library=root / "references/library" if (root / "SKILL.md").is_file() else root
    if args.output and (args.output.exists() or args.output.resolve().is_relative_to(root)):
        parser.error("Write a new receipt outside the frozen package")
    spec=importlib.util.spec_from_file_location("base_verifier",library / "scripts/verify_package.py")
    verifier=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    manifest=verifier.verify_manifest(root)
    prior=json.loads(run([library / "scripts/verify_authors.py"]).stdout)
    links=verifier.verify_links(root)
    urban=library / "expansion06"
    checked=json.loads(run([urban / "scripts/edition.py","verify"]).stdout)
    result=run(["-m","unittest","discover","-s",urban / "tests","-v"])
    count=re.search(r"Ran (\d+) tests",result.stderr)
    if not count or int(count[1])!=20: raise ValueError("Incomplete urban tests")
    examples=json.loads(run([urban / "scripts/audit_examples.py"]).stdout)
    if examples["lexical_passes"]!=6: raise ValueError("Unchecked urban repairs")
    if root!=library:
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary) / "test.tex"
            wrapper=root / "scripts/check_vocabulary.py"
            path.write_text("The model explains rents and income.")
            run([wrapper,"--urban","check",path,"--strict"])
            path.write_text("zzzznewunattestedword")
            run([wrapper,"--urban","check",path,"--strict"],1)
            run([wrapper,"--urban","--base","lookup","rents"],1)
            run([wrapper,"--urban","--previous","lookup","rents"],1)
            run([wrapper,"--urban","--urban","lookup","rents"],1)
            lookup=json.loads(run([wrapper,"lookup","rents"]).stdout)
            if not lookup["record"]: raise ValueError("Missing default45 lookup")
            selected=json.loads(run([wrapper,"--urban","lookup","neighborhood"]).stdout)
            if not selected["record"]: raise ValueError("Missing urban lookup")
    summary={"package_verified":True,"kind":manifest["kind"],
        "manifest_sha256":hashlib.sha256((root / "PACKAGE_MANIFEST.json").read_bytes()).hexdigest(),
        "packaged_files_checked":len(manifest["files"]),"local_links_checked":links,
        "base_tests":prior["base_tests"],"previous_expansion_tests":prior["previous_expansion_tests"],
        "author_extension_tests":prior["author_extension_tests"],"urban_extension_tests":20,
        "total_tests":prior["base_tests"]+prior["previous_expansion_tests"]+prior["author_extension_tests"]+20,
        "expanded_counts":checked["counts"],"general_default_papers":45,"urban_opt_in_papers":53,
        "source_screen_rerun":False,"source_pdfs_included":False,"network_required":False,
        "independent_writing_validation":False,"previous_examples_preserved":True}
    value=json.dumps(summary,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(value)
    print(value,end="")


if __name__=="__main__": main()
