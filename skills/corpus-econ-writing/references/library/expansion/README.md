# Expanded Writing Edition 04

This edition adds eight public author-hosted papers to the frozen 23-paper library.
It adds study of longer arguments, original worked revisions, a usage supplement,
and four connected writing exercises. The previous sources, databases, policy,
packages, and evaluations remain recoverable and are not rewritten.

## Read Selectively

- [Argument and exposition](ARGUMENT_AND_EXPOSITION.md): sentence, paragraph,
  subsection, and section flow; assumptions, equations, interpretation, literature.
- [Worked revisions](WORKED_EXAMPLES.md): ten original contrasts, with explanations.
- [Usage supplement](USAGE_SUPPLEMENT.md): precise distinctions and examples;
  not a whitelist of new concepts.
- [Source study](SOURCE_STUDY.md): exact versions, selected passages, and page anchors.
- [Vocabulary policy](VOCABULARY_POLICY.md): the 31-paper edition and retained exceptions rule.
- [Evaluation](evaluation/REVIEW.md): connected exercises, findings, limits, and checks.
- [Connected examples](evaluation/SAMPLES.md) and their [argument maps](evaluation/ARGUMENT_MAPS.md).
- [Vocabulary additions](vocabulary/new_attestations.csv): new forms and source IDs.

Full source PDFs and extracted text are retained locally, not in the ZIP or skill.
Extraction covers all included pages, but manual reading covers only the passages
recorded in the source study. No BCN manuscript, slide, empirical result, or model
is changed by this resource update. Fictional examples are not publication results.

## Portable Commands

Run `scripts/edition.py` with Python 3.10+ from this edition's folder. It discovers
only its adjacent frozen base library, not personal skill or research paths.

```sh
python3 scripts/edition.py lookup afford
python3 scripts/edition.py check /absolute/path/section.tex --strict
python3 scripts/edition.py verify
python3 -m unittest discover -s tests -v
```

`verify --full`, `acquire`, `extract`, and `build` require the separate local sources.
Acquisition uses the declared public URLs; it is not part of ordinary writing or
portable verification. Never re-download into a frozen edition to update a source.

The original 23-paper checker remains available through the base library's
`scripts/vocabulary.py`. A report must state which edition it used.
