# Corpus-Restricted Writing

## Adopted Rule

For future research prose, use words attested in the frozen Donaldson, Allen,
Arkolakis, and Redding paper corpus. Prefer plain words in the main text. Do not
introduce additional technical language merely to make the prose sound formal.

The scope is all 23 included source versions, not just the manually reviewed
passages. This applies to new or revised research prose; it is not an instruction
to rewrite the current manuscript automatically. Tool commands, mathematical
symbols, bibliographic keys, and private editing labels are not publication prose.

An unfamiliar word must either be replaced with an accurate attested expression
or retained through a recorded necessary exception. Do not weaken a definition,
assumption, proof, or estimand to satisfy the vocabulary check.

## What the Inventory Establishes

The [full inventory](vocabulary/README.md) records every recognized alphabetic form
on all 1,216 included extracted pages, with counts, spellings, source papers, PDF
pages, and approximate main-text versus other-page tags. It preserves both ordinary
forms and hyphenated compounds. It adds no free inflections or synonyms.

“Exhaustive” means exhaustive relative to the frozen text extraction and documented
tokenization. It does not mean perfect recognition of all printed text, a semantic
definition of every word, or manual approval of every occurrence. Math symbols,
names, reference entries, and extraction fragments are distinguished or flagged.
The unrelated A04 bundle pages remain excluded.

The 185-entry [usage dictionary](DICTIONARY.md) is separate: its definitions explain
economic distinctions. Its original examples are not source quotations and are
not automatically authorized publication vocabulary. The
[attestation report](vocabulary/curated_dictionary_attestation.csv) identifies
missing component words and phrases not found literally in the main-text sample.

## Editorial Procedure

1. Draft using familiar, attested economic language.
2. Check the prose against the inventory. Inspect every unfamiliar form in context.
3. Prefer an attested plain expression if it preserves the exact meaning.
4. Inspect appendix/reference-only words, single occurrences, acronyms, and names
   before treating them as ordinary prose. A bibliography entry is not evidence
   of an explanatory style.
5. Check any newly named technical concept or compound separately. Familiar
   component words do not authorize a new concept.
6. Record unavoidable exceptions and their reasons; report them with the writing
   changes. No automatic whitelist expansion.
7. Check sentence and paragraph flow. Passing a word-list check does not establish
   clear writing, scientific correctness, or an argument supported by evidence.

Only attested forms enter the normal vocabulary. Case, accents, apostrophe variants,
and ligatures are normalized for lookup. A new inflection or compound is still
flagged if its own form is absent. An unfamiliar spelling should not be approved
just because it resembles a source word.

## Necessary Exceptions

Exceptions are narrow, explicit, and based on meaning. Possible cases include an
official provider or place name, an essential measurement term, or an established
technical distinction that cannot be expressed accurately using the attested forms.
These categories are not blanket exemptions. Proper names can also be misspelled;
a technical-sounding term can also be unnecessary.

An exception record must contain:

- Exact term, including any compound spelling.
- Why the argument or source requires it.
- Why an attested alternative would change or obscure its meaning.
- Approval and status.

The machine-readable register is `data/vocabulary_policy.json`; it currently has
**no exceptions**. Record individual forms, not wildcard families. Pending terms
do not pass the strict check. A change introducing a new scientific assumption or
method still requires separate author authorization, regardless of word choice.

Do not replace a precise existing method name solely because this sample does not
contain it. Justify the necessary exception instead. Likewise, do not introduce a
new construct merely because its individual words already occur in the papers.

## Commands

Run from the writing library:

```sh
python3 scripts/vocabulary.py lookup heterogeneity
python3 scripts/vocabulary.py lookup first-order
python3 scripts/vocabulary.py check path/to/section.tex --strict
python3 scripts/vocabulary.py check path/to/draft.md --strict
python3 scripts/vocabulary.py build
python3 scripts/vocabulary.py verify
```

The checker reports missing words and compounds, counts, and line numbers. It also
reports context-review words and approved exceptions used. Strict mode exits with
an error for unapproved terms; context-review flags require editorial inspection.

The TeX checker is conservative target-file processing, not a complete TeX engine.
It does not expand input files or arbitrary macros. Math, citations, commands,
links, and comments are excluded; prose inside unusual macros or mathematical text
may need manual inspection. Use it on prose modules rather than expecting a
preamble or a compiled document to be fully understood.

## Scope of Enforcement

This portable edition applies the policy when the user invokes the companion
skill or adopts it for a project. It does not rewrite existing manuscripts or
change global agent instructions. Keep project-specific approved exceptions
outside the frozen library and pass their register explicitly with `--policy`.
Use `scripts/verify_package.py` for source-free integrity checks. The `build`
and full-source `verify` commands above require separately acquired inputs.
