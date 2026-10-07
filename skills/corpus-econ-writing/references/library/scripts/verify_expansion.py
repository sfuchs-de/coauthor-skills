#!/usr/bin/env python3
"""Offline verification of the frozen base plus its separately versioned extension."""
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
    result = subprocess.run([sys.executable, "-B", *map(str, arguments)],
                            capture_output=True, text=True, timeout=180)
    if result.returncode != expected:
        raise ValueError(f"Unexpected exit {result.returncode}: {result.stderr[-2000:]}")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    library = root / "references/library" if (root / "SKILL.md").is_file() else root
    if args.output and args.output.resolve().is_relative_to(root):
        parser.error("Write receipts outside the frozen package")
    spec = importlib.util.spec_from_file_location("base_verifier", library / "scripts/verify_package.py")
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    manifest = verifier.verify_manifest(root)
    base = json.loads(run([library / "scripts/verify_package.py"]).stdout)
    links = verifier.verify_links(root)
    extension = library / "expansion"
    expanded = json.loads(run([extension / "scripts/edition.py", "verify"]).stdout)
    tests = run(["-m", "unittest", "discover", "-s", extension / "tests", "-v"])
    count = re.search(r"Ran (\d+) tests", tests.stderr)
    if not count or int(count[1]) != 20:
        raise ValueError("Incomplete extension tests")
    checked = json.loads((extension / "evaluation/SUMMARY.json").read_text())
    fixtures = {}
    with tempfile.TemporaryDirectory() as temporary:
        for name, text, code in (("pass", "The model explains income and prices.", 0),
                                 ("fail", "zzzznewunattestedword", 1)):
            path = Path(temporary) / f"{name}.tex"
            path.write_text(text)
            result = run([extension / "scripts/edition.py", "check", path, "--strict"], code)
            report = json.loads(result.stdout)
            if report["lexical_gate_passed"] != (code == 0):
                raise ValueError("Invalid strict checker result")
            fixtures[name] = code
        if library != root:
            lookup = run([root / "scripts/check_vocabulary.py", "lookup", "afford"])
            if '"afford"' not in lookup.stdout or '"main_text_attested"' not in lookup.stdout:
                raise ValueError("Expanded wrapper did not use the new inventory")
            legacy = run([root / "scripts/check_vocabulary.py", "--base", "lookup", "heterogeneity"])
            if '"word": "heterogeneity"' not in legacy.stdout:
                raise ValueError("Base wrapper is unavailable")
    summary = {"package_verified": True, "kind": manifest["kind"],
        "manifest_sha256": hashlib.sha256((root / "PACKAGE_MANIFEST.json").read_bytes()).hexdigest(),
        "packaged_files_checked": len(manifest["files"]), "local_links_checked": links,
        "base_tests": base["unit_tests_passed"], "expanded_tests": int(count[1]),
        "expanded_counts": expanded["counts"], "strict_fixtures": fixtures,
        "same_context_long_examples": len(checked["cases"]),
        "source_pdfs_included": False, "source_screen_rerun": False,
        "network_required": False, "independent_writing_validation": False,
        "limits": "Artifact and behavior checks; neither a fresh source review nor independent writing-quality validation"}
    text = json.dumps(summary, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
