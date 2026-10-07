# Spatial Economics Writing Library

An evidence-based study of papers by Dave Donaldson, Treb Allen, Costas Arkolakis,
and Stephen J. Redding, including their coauthors. Portable source-free edition. Start with [portable use](PORTABLE_USE.md);
no manuscript or slide is included or changed by this package.

## Completed Edition: October 3, 2026

Reviewed selected substantive passages from **23 distinct papers**, spanning
theory, empirical research, quantitative applications, and surveys. The manual
sample reaches **311 PDF pages**; this means passages on those pages, not a claim
that all 311 pages were read in full. All 23 papers received a rendered-page review.
Extraction covered 1,216 included pages, but extraction is not manual analysis.

The library contains **245 page-linked observations**, **185 dictionary entries**,
and **45 evidence-linked writing rules**. Exact source versions and SHA-256 hashes
distinguish author manuscripts from published texts. Shared papers count once.
See the [review report](REVIEW_REPORT.md) for coverage, checks, and limitations.

**Vocabulary extension:** the [exhaustive extraction inventory](vocabulary/README.md)
now records all recognized words and compounds from the included corpus, rather
than only the 185 curated entries. Future research writing follows the
[corpus-restricted vocabulary policy](VOCABULARY_POLICY.md), with necessary
exceptions explicitly justified. Existing papers and slides have not been rewritten.

## Start Here

| Need | Document |
|---|---|
| A comprehensive writing guide | [Writing spatial economics](STYLE_GUIDE.md) |
| Vocabulary, distinctions, and original examples | [Economic writing dictionary](DICTIONARY.md) |
| All attested word forms, compounds, and source pages | [Corpus vocabulary inventory](vocabulary/README.md) |
| Restrictions and necessary exceptions for future prose | [Vocabulary policy](VOCABULARY_POLICY.md) |
| Equations, typography, figures, tables, and placement | [Formatting guide](FORMATTING_GUIDE.md) |
| Instructions for a drafting or revision pass | [Reusable writing instructions](WRITING_INSTRUCTIONS.md) |
| Concrete reasoning and transition patterns | [Worked exposition patterns](EXPOSITION_PATTERNS.md) |
| Differences among samples and genres | [Author and genre comparison](AUTHOR_GENRE_COMPARISON.md) |
| Source versions and individual reviews | [Paper catalogue](catalogue.md) |
| Page-linked support for every rule | [Evidence-linked rule register](RULES.md) |
| Search, rebuild, and verification commands | [Setup and search](SETUP_AND_SEARCH.md) |

## Database

- [SQLite](database/writing_database.sqlite): searchable observations, dictionary,
  rules, and evidence relationships.
- [JSON](database/writing_database.json): complete original-analysis export.
- CSVs in `database/`: papers, observations, dictionary, rules, and approximate
  literal phrase counts.
- [Build receipt](database/BUILD_RECEIPT.json) and
  [quality receipt](database/QUALITY_RECEIPT.json): verified counts and checks.

Search example, run from this library's directory:

```sh
python3 scripts/study.py search '"fixed effects" OR normalization'
```

The curated dictionary is a precision aid, not a blanket vocabulary approval. The instructions
protect substantive detail and the author's voice; they do not authorize changes
to assumptions, results, or publication state.

## Evidence and Copyright

Full PDFs, extracted texts, and page images are retained locally for research,
not redistributed. Analysis uses original paraphrases; no source passages are
reproduced in the analytical exports. Original example sentences are hypothetical,
not new empirical findings. Coauthored wording cannot be attributed to one
individual's writing process. Writing observations do not certify a paper's proofs
or empirical claims. The local sample gallery and its page images are excluded from this
portable edition. No remote publication or synchronization was performed.
