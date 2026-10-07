#!/usr/bin/env python3
"""Copy the portable worked starter without overwriting existing work."""
import argparse
from pathlib import Path
import shutil


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    destination = args.destination.expanduser().absolute()
    if destination.exists() or destination.is_symlink():
        parser.error(f"Destination already exists; choose a new directory: {destination}")
    source = Path(__file__).resolve().parents[1] / "assets" / "deck"
    if not (source / "deck.tex").is_file():
        parser.error(f"Skill starter is missing: {source}")
    shutil.copytree(source, destination)
    print(f"Created {destination}")
    print("Replace the illustrative content and slide map with the supplied research.")
    print("Build in that directory: latexmk -pdf -halt-on-error deck.tex")
    print("Then: latexmk -pdf -halt-on-error handout.tex")


if __name__ == "__main__":
    main()
