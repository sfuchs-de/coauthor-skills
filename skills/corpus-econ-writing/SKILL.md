---
name: corpus-econ-writing
description: Draft, revise, or review economics prose with a versioned spatial, trade, urban, transport, and theory corpus. Use for argument flow, mathematical exposition, interpretation, literature comparisons, and exact vocabulary audits; not for changing methods or results.
---

# Corpus Economics Writing

Preserve the author's voice, substantive detail, and scientific meaning. The
default theory08 inventory contains 59 pinned papers, including the earlier
urban and transport extension. Previous inventories remain selectable. Selected
reading and word attestation are not full manual review or scientific validation.

## Choose Relevant Guidance

- For assumptions, propositions, derivation depth, envelope intuition, and
  policy feedback, read the [theory guide](references/library/expansion08/THEORY_EXPOSITION.md).
  Use its [four connected examples](references/library/expansion08/WORKED_EXAMPLES.md)
  and [source cards](references/library/expansion08/SOURCE_STUDY.md) selectively.
- For housing, sorting, commuting, congestion, or urban policy, use the retained
  [urban guide](references/library/expansion06/URBAN_EXPOSITION.md) and
  [urban source cards](references/library/expansion06/SOURCE_STUDY.md).
- For argument structure, use the [argument guide](references/library/expansion/ARGUMENT_AND_EXPOSITION.md).
  Add the [author and genre guide](references/library/expansion05/AUTHOR_AND_GENRE_GUIDE.md)
  for dynamics, measurement, identification, and aggregation.
- For task-specific depth, read [exposition by task](references/calibrated-exposition.md).
  Do not impose a structural-paper outline on a descriptive request.
- For wording and mathematical presentation, consult the
  [dictionary](references/library/DICTIONARY.md),
  [theory usage distinctions](references/library/expansion08/USAGE_SUPPLEMENT.md),
  [patterns](references/library/EXPOSITION_PATTERNS.md), and
  [formatting guide](references/library/FORMATTING_GUIDE.md).

## Preserve And Complete The Argument

Check whether each sentence inherits an economic object, each paragraph uses the
preceding conclusion, and each section supplies an input to the next. Prefer a
relationship between economic objects to generic signposting. Do not shorten
away useful derivation or interpretation merely to make prose smoother.

Explain the question before a consequential condition. Introduce assumptions
where used: primitives, valuation conditions, then stronger recovery or finite
change restrictions. Name the relevant conditions in a proposition, show its
decisive step, and interpret what it establishes and leaves unresolved. Avoid
an early assumption inventory repeated later. Keep necessary conditions visible;
secondary proof navigation and literature ancestry can go in footnotes.

Define choices, timing, units, normalization, and fixed arguments before math.
Distinguish input-price changes from optimized input quantities, marginal from
average shares, and partial from total policy derivatives. Include direct policy
dependence when present, and count equilibrium and transfer feedback once.
Do not silently strengthen a local result into a finite or global conclusion.

Separate observed outcomes, constructed exposure, assigned income, and model
predictions. State denominators, weights, and the role of fitted targets versus
external checks. Keep adverse sensitivity beside the conclusion it qualifies.
In urban work, distinguish stocks from flows, rents from asset values, residents
from workplaces, and sorting from causal effects when consequential.

Organize literature around the economic task and the restrictions that change
what can be inferred, rather than one summary per study. A precedent does not
validate the current design. Remove writer-facing editing commands from
publication prose; keep their substantive explanation.

A writing pass does not authorize estimation, calibration, new findings, model
solutions, publication, or adoption of a new method. A review-only request does
not authorize edits. Preserve versions and unrelated coauthor changes.

## Apply Exact Vocabulary Evidence

Use the [theory08 policy](references/library/expansion08/VOCABULARY_POLICY.md)
and record that choice before drafting. The inventory has 23,211 recognized
attested forms, not 23,211 manually approved meanings. Do not change inventories
solely to make a passage pass. No stemming, automatic compounds, or newly
approved exceptions are allowed. Inspect rare and extraction-flagged evidence.

The checker separately reports single uppercase statement labels in recognized
contexts, without exempting arbitrary symbols or new prose. A journal
abbreviation does not attest a currency meaning. Unsupported compounds remain
flagged even when their components occur.

Use Python 3.10+ with SQLite FTS5; substitute the installed path for `<skill>`:

```sh
python3 <skill>/scripts/check_vocabulary.py lookup basket
python3 <skill>/scripts/check_vocabulary.py check /absolute/path/section.tex --strict
python3 <skill>/scripts/check_vocabulary.py --urban lookup neighborhood
python3 <skill>/scripts/check_vocabulary.py --authors lookup working
python3 <skill>/scripts/check_vocabulary.py --previous lookup afford
python3 <skill>/scripts/check_vocabulary.py --base lookup heterogeneity
```

Check changed modules, not just drivers. The checker does not traverse arbitrary
TeX dependencies or macros; never hide prose in math. Preserve an essential term
when an alternative would change the claim, record its justification, and obtain
an explicitly approved exception. See [exceptions](references/exception-handling.md).

## Verify And Report

Run `python3 <skill>/scripts/verify_package.py` for offline verification of all
five inventories, hashes, links, examples, negative tests, and routing. Source
PDFs, full text, and page images are excluded. Source reading and overlap screens
are recorded, not rerun offline.

Report mathematical and editorial checks separately from vocabulary status.
The [theory08 review](references/library/expansion08/evaluation/REVIEW.md) retains
first drafts, repairs, found errors, and unresolved old-sample flags. These are
same-context tests, not independent validation or reliable first-pass claims.
