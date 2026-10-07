# Repository instructions

This is a public, code-and-instructions-only distribution. Do not add credentials, manuscript
sources, private referee cases, personal project registries, transcripts or source-paper downloads.

Preserve specialist authority and the developed referee-report workflow. Update shared contracts
deliberately; do not collapse independent referee work into author-side editing. Corpus output
hashes and source-evidence hashes must not be reset to make a changed inventory pass.

Validate locally before publishing. Installing live skills, changing other repositories or sending
messages requires a separate request. Do not overwrite unrelated installed skills.

Run `python3 scripts/validate.py` and `python3 -B -m unittest discover -s tests -v` after edits.
For corpus changes, also run its portable verifier. If an intended file changes, refresh the root
integrity manifest with `python3 scripts/build_manifest.py` only after reviewing the diff.
