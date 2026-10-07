#!/usr/bin/env python3
"""Default theory08; preserve explicit earlier inventories."""
import runpy
import sys
from pathlib import Path

library = Path(__file__).resolve().parents[1] / "references/library"
choices = {"--urban":"expansion06/scripts/edition.py", "--authors":"expansion05/scripts/edition.py",
           "--previous":"expansion/scripts/edition.py", "--base":"scripts/vocabulary.py"}
selected = [flag for flag in choices if flag in sys.argv[1:]]
if len(selected) > 1 or any(sys.argv[1:].count(flag) > 1 for flag in choices):
    raise SystemExit("Choose one inventory")
script = library / (choices[selected[0]] if selected else "expansion08/scripts/edition.py")
if selected:
    sys.argv.remove(selected[0])
sys.path.insert(0, str(script.parent))
runpy.run_path(str(script), run_name="__main__")
