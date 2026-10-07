# Writing Library Review Report

## Delivery

**Vocabulary extension:** [the follow-up report](VOCABULARY_REVIEW.md) records the
exhaustive extraction inventory and adopted corpus-only default. The original
245-observation writing database is preserved; the extension has its own
word/compound database, source-page records, checker, and receipts. The current
combined test suite has 38 passing tests.

Completed a substantial, purposive study of writing in papers involving Dave
Donaldson, Treb Allen, Costas Arkolakis, and Stephen J. Redding. The outputs are a
comprehensive style guide, formatting guide, economic dictionary, reusable editing
instructions, ten worked exposition patterns, author/genre comparison, 23 paper
cards, evidence-linked rules, and a searchable analysis database.

This is a local writing resource. It does not revise the BCN manuscript, slides,
scientific assumptions, numerical outputs, or remote repositories.

## What Was Examined

| Measure | Scope |
|---|---|
| Distinct papers | 23 |
| Papers involving Donaldson / Allen / Arkolakis / Redding | 8 / 6 / 8 / 7; overlapping, not 29 independent papers |
| Raw downloaded PDF pages | 1,236 |
| Included PDF pages | 1,216 |
| Extracted word tokens | 466,239; approximate extraction count, not words manually reviewed |
| Pages containing manually reviewed passages | 311 |
| Individual rendered samples | 23, inspected in four contact sheets |
| Additional individual-image close inspections | A04, R03, R06 |
| Original page-linked observations | 245 |
| Evidence-linked recommendations | 45 |
| Dictionary entries | 185 across 14 categories |
| Approximate literal phrase/paper frequency records | 1,138 |

Every paper received selected substantive passage review. Samples cover openings,
theory definitions and results, data or empirical implementation, interpretation,
and concluding material as relevant to the paper. Several passages received fuller
follow-up reading. The record identifies the pages but does not claim that every
listed page, proof, or supplement was read in full. The visual review is a sample,
not a full-document layout audit.

The corpus includes eight empirical-model papers, five theory-quantitative papers,
four theory-method papers, four surveys, one empirical-method paper, and one
survey-theory paper. These are organizing categories, not author-approved labels.
The sample is deliberately varied rather than random or statistically representative.

## Findings Translated into Instructions

The strongest practical pattern is an economic dependency chain: question, choice,
relationship, information, recovery, evidence, and interpretation. The guides
recommend carrying its objects across sentence, paragraph, subsection, and section
boundaries. They preserve detailed explanation of timing, optimization, signs,
denominators, spatial mechanisms, and uncertainty rather than compressing the paper
into a summary.

Formal assumptions receive a reason before their statement and an interpretation
after their use. Valuation, identification, normalization, calibration, and
counterfactual computation remain separate. Results discussion distinguishes stable
patterns from stable magnitudes, fit from validation, and non-rejection from proof.
Data and maps receive economic interpretation without converting description into
a causal claim.

The dictionary includes technical distinctions and plain-language alternatives.
It is not a claim that all 185 terms occur in the sources. Literal occurrence
records are separate, approximate, and never used to infer individual authorship
or prescribe a frequent phrase.

Formatting recommendations distinguish observed layouts from house choices.
Publisher fonts and trim sizes are not author preferences. The 12-point XCharter
reading draft, 10-point captions/tables, 9-point notes, and paper-figure sizes are
explicit recommendations for the current project, not a purported shared format
used by all four authors.

## Source and Evidence Repairs

- A04's university bundle contains a cover and an unrelated article on pages 1-20.
  Only pages 21-46 support this study. Original PDF page numbering is retained.
- Several author-hosted manuscripts predate publication. Their exact versions,
  including Universal Gravity's May 2018 manuscript, are recorded separately from
  publication years.
- K02's appendix begins before its reference list. Its main-text computational
  sample stops at page 35 rather than treating the intervening appendix as prose.
- D06's author index has a bibliographic page-range discrepancy. The retrieved
  published PDF was used for page references; the discrepant range was not copied
  into the catalogue.
- The final pass corrected page mismatches in the worked-pattern draft and replaced
  two rule links that were less direct than available evidence. Envelope rule W013
  now cites D05's actual envelope discussion rather than an unrelated assumption.

All observation pages resolve to recorded manual-review pages. Every rule has an
existing observation link. These mechanical checks do not substitute for the
semantic second pass, which examined the links' relevance.

## Verification

The build checks all 23 original PDF hashes, 69 frozen extract/image hashes, visual
receipt hashes, page ranges, unique record IDs, and rule links. The database has
foreign-key checks, SQLite integrity checks, complete search coverage, and matched
JSON/CSV/SQLite record counts. Markdown evidence IDs and local links are checked.

The data-free unit suite includes rejection tests for duplicates, out-of-range or
unreviewed pages, incomplete manifests, changed/missing evidence, invalid source
hashes, empty assessments, broken rule links, and undeclared reproduced quotations.
It also checks literal matching and database search. The final receipts record
the executed checks, rather than treating configured checks as successful runs.

Evidence manifests are preservation records. Acquisition and extraction receipts
retain their event-time statuses; the current completed-review status is in the
database and paper cards. An old download-stage status is not the current analysis
status.

## Limitations and Appropriate Use

1. Coauthored prose and journal editing prevent attribution to a single writer.
2. Selected passages establish examples, not the prevalence of a habit in an
   author's whole output. No sentence-length or vocabulary ranking is claimed.
3. Font samples include text, mathematics, notes, and sometimes figure labels;
   representative sizes are not a full typographic census.
4. Phrase matching is literal after normalization; headers, formulas, extraction
   artifacts, and different meanings of the same term can remain.
5. No proof, estimate, identification claim, or numerical result was independently
   validated as part of this writing study.
6. Portability of analysis/search is distinct from reproduction of PDF extraction
   and rasterization under other software versions. The latter remains untested.
7. This is a local research library, not permission to redistribute downloaded
   copyrighted PDFs, extracted full text, or page images.

Use the evidence to learn explanatory operations, not to imitate signature wording.
Keep an author's fluid existing prose where it performs those operations well.
New scientific claims or changes still require separate review and authorization.
