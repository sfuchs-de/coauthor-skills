# Additional Authors: Edition 05

This edition extends the preserved 31-paper library to **45 exact source versions**.
It adds four papers with Myrto Kalouptsidi, four with Woan Foong Wong, four with
Fernando Leibovici, and two with Stephen Redding. Redding already had ten papers
in the preceding edition. Coauthors are recorded for every paper; these are
observations about papers, not an attribution of their prose to one coauthor.

## Use

- [Author and genre guide](AUTHOR_AND_GENRE_GUIDE.md): mechanism, sequence,
  identification, aggregation, mathematical presentation, and literature comparison.
- [Source study](SOURCE_STUDY.md): 56 observations anchored to selected excerpts
  on 83 PDF pages. This is not a claim to have manually read every page.
- [Usage supplement](USAGE_SUPPLEMENT.md): 28 economic distinctions.
- [Worked examples](WORKED_EXAMPLES.md): six original fictional repairs and
  explicit argument/fidelity checks, not research findings.
- [Vocabulary policy](VOCABULARY_POLICY.md): exact-form evidence and exceptions.

The combined extraction has 2,417 included pages and 445,232 source-page records.
The inventory contains 21,265 normalized forms, of which 19,854 satisfy the
checker’s attestation rule. The 4,002 newly attested forms are relative to
edition04, not the original 23-paper base. Normalized forms, source-page records,
and meaningful dictionary entries are different counts.

Use `python3 scripts/edition.py lookup WORD` or
`python3 scripts/edition.py check /absolute/path/file.tex --strict`.
Use `python3 scripts/edition.py verify` for the source-free artifacts, or add
`--full` in the local research tree for the additional source hash checks.
The installed wrapper defaults to this edition and retains explicit `--previous`
and `--base` modes.

## Evidence And Limits

All 14 additional PDFs were obtained through public author links. Version dates,
publication information, acquisition hashes, and approximate main-text page ranges
are in [the source registry](data/sources.json). Do not infer that an author-linked
manuscript is the latest or identical to a subsequently published article.

The English inventory excludes two declared French-abstract spans in L04 while
preserving the raw extraction. Extraction artifacts, names, reference-page usage,
and page-level main-text classifications still require contextual judgment. A
word’s appearance is neither concept approval nor evidence that its meaning fits
the passage being edited. The dictionary is selective, not exhaustive semantic
annotation of all 19,854 forms.

Fourteen selected source pages were rendered and inspected. The
[inspection notes](data/visual_observations.json) are separate from rendering
receipts. Published typography and preliminary manuscript typography are examples,
not rules imposed on another author.

Full-text PDFs, extracted text, and page images remain local and are excluded from
the portable library and skill. The source-free package can verify recorded
evidence and run lexical checks, but cannot repeat source reading or the local
source-overlap screen. The worked repairs are same-context examples; independent
generation and blinded writing-quality evaluation remain pending.
