# Vocabulary Extension Review

## Completed Scope

Extended the curated dictionary with a full inventory from all 23 frozen papers'
included extracts, not just the manually reviewed passages. The original writing
analysis database remains unchanged. No manuscript, slide, source PDF, research
result, or remote repository was changed.

| Object | Count |
|---|---:|
| Included extracted pages | 1,216 |
| Normalized recognized forms | 13,904 |
| Word forms | 12,800 |
| Hyphenated compound forms | 1,104 |
| Forms with main-range attestation | 10,937 |
| Forms attested only elsewhere | 2,206 |
| Symbol/non-English forms, not automatically licensed | 650 |
| Unverified line-break fragments, not licensed | 111 |
| Source-page/evidence-kind occurrence records | 225,204 |

There are 13,143 mechanically eligible attested forms; eligibility is not semantic
approval. Names, bibliography words, rare forms, and acronyms still need context
review. Appendix, reference, and main-range tags are based on recorded boundaries
and reference headings, not a perfect classification of every prose line.

The inventory folds case and accents and preserves recorded spellings. It does not
add inflections automatically. Verified broken-line words are rejoined only when
the unbroken form is independently attested; unresolved fragments remain visible
but cannot license new words.

## Curated Dictionary Reconciliation

All 185 curated entries have an attestation report. Twenty-two entries contain at
least one unattested component word, and 49 lack the exact literal phrase in the
main-text sample. These counts describe different checks and overlap.

For example, “handoff” is an editing label, not corpus publication vocabulary.
“Estimand” and “smearing” can be necessary technical terms, but their inclusion in
the usage dictionary does not establish that they appear in this corpus. A future
writing pass must use an accurate attested expression or explain the necessary
exception. No exceptions have been preapproved.

## Implemented Default

The [policy](VOCABULARY_POLICY.md), project `AGENTS.md`, reusable writing instructions,
and shared feedback memory now require corpus vocabulary by default. New technical
wording must be necessary and justified. New concepts are not authorized merely
because their component words appear in the corpus. This applies to future research
prose, not to silently revising existing manuscripts or policing tool commands.

## Executed Checks

- All 23 PDF hashes and all frozen extract/image hashes verified.
- Vocabulary output and producing-input hashes verified.
- SQLite integrity and foreign keys pass.
- Every word's full, main, solid, standalone, and paper counts reconcile with its
  page-level records.
- CSV counts match the database; all 185 curated entries are covered.
- The strict CLI accepts the attested-word fixture and rejects the unfamiliar-word
  fixture at line 2, with the expected exit codes.
- 38 data-free tests cover the original library and the vocabulary extension.
- The original writing-analysis JSON and SQLite hashes are unchanged.

Receipts are in [vocabulary](vocabulary/README.md) and
[the library quality receipt](database/QUALITY_RECEIPT.json). A strict lexical pass
is not a semantic, mathematical, or full-TeX validation. The corpus is exhaustive
relative to this extraction; unrecognized printed text and unusual macros remain
limitations. Necessary distinctions should be justified, not erased.
