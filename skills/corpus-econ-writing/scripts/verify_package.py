#!/usr/bin/env python3
"""Verify preserved inventories and the theory extension without source downloads."""
import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def run(args, expected=0):
    result = subprocess.run([sys.executable, "-B", *map(str,args)], capture_output=True, text=True, timeout=240)
    if result.returncode != expected:
        raise ValueError(f"Unexpected exit {result.returncode}: {result.stderr[-3000:]}")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    library = root / "references/library" if (root / "SKILL.md").is_file() else root
    if args.output and (args.output.exists() or args.output.resolve().is_relative_to(root)):
        parser.error("Save a new receipt outside the frozen package")
    source = library / "scripts/verify_package.py"
    spec = importlib.util.spec_from_file_location("theory08_base_verifier", source)
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    if Path(verifier.__file__).resolve() != source.resolve():
        raise ValueError("Wrong verifier origin")
    manifest = verifier.verify_manifest(root)
    prior = json.loads(run([library / "scripts/verify_urban.py"]).stdout)
    links = verifier.verify_links(root)
    theory = library / "expansion08"
    checked = json.loads(run([theory / "scripts/edition.py", "verify"]).stdout)
    result = run(["-m", "unittest", "discover", "-s", theory / "tests", "-v"])
    count = re.search(r"Ran (\d+) tests", result.stderr)
    if not count or int(count[1]) != 30:
        raise ValueError("Incomplete new test suite")
    examples = json.loads(run([theory / "scripts/audit_examples.py", "--json"]).stdout)
    recorded = json.loads((theory / "evaluation/VERIFIED_AUDIT.json").read_text())
    if examples["lexical_passes"] != 4 or examples["length_passes"] != 4:
        raise ValueError("Unchecked final examples")
    if [(r["id"],r["sha256"]) for r in examples["samples"]] != [(r["id"],r["sha256"]) for r in recorded["samples"]]:
        raise ValueError("Changed screened examples")
    if root != library:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test.tex"
            wrapper = root / "scripts/check_vocabulary.py"
            path.write_text("The model explains income.")
            default = json.loads(run([wrapper,"check",path,"--strict"]).stdout)
            if default["edition"] != "2026-10-04-theory-08":
                raise ValueError("Wrong default")
            for flag, expected in (("--urban","2026-10-04-urban-06"), ("--authors","2026-10-04-authors-05"),
                                   ("--previous","2026-10-03-expanded-04")):
                value = json.loads(run([wrapper,flag,"check",path,"--strict"]).stdout)
                if value["edition"] != expected:
                    raise ValueError("Wrong explicit inventory")
            run([wrapper,"--base","check",path,"--strict"])
            run([wrapper,"--urban","--authors","lookup","income"],1)
            run([wrapper,"--authors","--authors","lookup","income"],1)
            path.write_text("Assumption H holds. Study B explains income.")
            value = json.loads(run([wrapper,"check",path,"--strict"]).stdout)
            if len(value["classified_labels"]) != 2:
                raise ValueError("Missing contextual label receipt")
            for text in ("zzzzunattestedword", "feasible-direction", "Income is one euro.", "Assumption H-income holds."):
                path.write_text(text)
                run([wrapper,"check",path,"--strict"],1)
    summary = {"package_verified": True, "kind": manifest["kind"],
               "manifest_sha256": hashlib.sha256((root / "PACKAGE_MANIFEST.json").read_bytes()).hexdigest(),
               "packaged_files_checked": len(manifest["files"]), "local_links_checked": links,
               "preserved_inventory_tests": prior["total_tests"], "theory_extension_tests": 30,
               "total_tests": prior["total_tests"]+30, "expanded_counts": checked["counts"],
               "default_papers": 59, "previous_inventories": [23,31,45,53],
               "example_lexical_passes": 4, "example_length_passes": 4,
               "recorded_source_screen_papers": recorded["overlap_papers"], "source_screen_rerun": False,
               "source_pdfs_included": False, "network_required": False, "independent_writing_validation": False}
    value = json.dumps(summary,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(value)
    print(value,end="")


if __name__ == "__main__":
    main()
