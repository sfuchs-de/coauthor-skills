# Portable Writing Library

This package contains the original analytical guides, 23 paper cards, 245
observations, 185 usage entries, 45 writing rules, and the 13,904-form vocabulary
inventory with 225,204 source-page records. The inventory covers 1,216 extracted
pages; the original manual review sampled selected passages on 311 pages.

## Start and Check

Run from this library's directory, using Python 3.10+ and SQLite with FTS5:

```sh
python3 scripts/verify_package.py
python3 scripts/study.py search '"fixed effects" OR normalization' --limit 15
python3 scripts/vocabulary.py lookup heterogeneity
python3 scripts/vocabulary.py check /absolute/path/section.tex --strict
python3 -m unittest discover -s tests -v
```

These operations use the packaged databases, not downloaded papers, research
data, a paid API, a TeX compiler, or a personal skill installation. Python 3.14.6
was tested for this edition; Python 3.10 is the minimum syntax requirement, not
a separately tested environment.

The checker prints JSON with unfamiliar forms, line numbers, context-review
flags, and hashes. Strict mode returns 1 for unapproved words. Review flags
still require editorial judgment. Check changed prose modules separately:
TeX inputs and arbitrary macros are not expanded. Preserve necessary scientific
terms through explicit project-specific exceptions, not automatic whitelisting.

## Install the Companion Skill

The companion ZIP contains one folder, `corpus-econ-writing`. Extract it into
`~/.codex/skills/` (or your chosen `CODEX_HOME/skills`) without overwriting an
existing installation. For Claude Code, use the same folder through a dedicated
symlink under `~/.claude/skills/`, or install a copy there. Do not replace an
existing skills directory. Refresh the agent session if discovery is cached.

Invoke it as `$corpus-econ-writing`, or request an economics writing revision
with corpus vocabulary checks. The skill includes this entire portable library;
the standalone library ZIP is not required for skill operation.

## Verification Boundaries

`PACKAGE_MANIFEST.json` records the SHA-256 and size of every packaged file,
source hashes for borrowed files, and explicit documentation adaptations.
`verify_package.py` checks those artifacts, SQLite integrity and evidence links,
JSON/CSV counts, frozen vocabulary output hashes, the unit tests, and positive
and negative strict-check fixtures. It rejects unsafe manifest paths, duplicate
keys, missing/changed files, unexpected files, and symlinks.

The manifest is an integrity record, not a cryptographic signature proving
authorship. Compare its archive hash with the separately delivered release
receipt when transporting the ZIP.

The original build, quality, and vocabulary receipts are preserved as records
of the earlier local source review. A portable check does **not** repeat the
source-PDF, full-text, or rendered-page hash checks: those inputs are excluded.
It also cannot establish that an editorial interpretation or economic claim is
correct. No independent collaborator test is claimed.

## Included and Excluded

Included: original paraphrased analysis, hypothetical usage examples, isolated
word-form inventories and page locations, source metadata/URLs, provenance
receipts, checker/search code, and tests.

Excluded: `sources/`, `extracted/`, `visual_review/`, the image-dependent gallery,
raw extraction metadata (which can embed source abstracts), bytecode, caches,
private research inputs, and manuscript/slide files. No source passages or
source-page images are included. Acquire the papers separately under their
applicable terms to inspect exact passages. Public author links may change;
matching a title is not sufficient to recover the frozen source version.

Full-source acquisition/build/verification scripts are retained for provenance,
but their source-dependent commands require separately acquired frozen inputs
and the optional PDF dependencies. Use `verify_package.py` for ordinary portable
verification; do not reset frozen evidence hashes to accommodate missing inputs.

The [original review report](REVIEW_REPORT.md) and
[vocabulary review](VOCABULARY_REVIEW.md) describe earlier coverage and limits.
The [style guide](STYLE_GUIDE.md), [policy](VOCABULARY_POLICY.md), and
[writing instructions](WRITING_INSTRUCTIONS.md) are the working entry points.
