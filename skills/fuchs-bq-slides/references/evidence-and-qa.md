# Evidence and Verification

## Authoritative Inputs

Maintain a small result/source ledger for quantitative decks. Record the result ID, source
file or run manifest, scenario/specification, sample/period/support, units, weights,
normalization, parameters, inference scope, figure/table path, and consuming slide labels.
Hash inputs or use a saved run ID when the workflow already supports that. Do not pick the
newest filename without checking what it contains.

Keep source numbers in shared generated TeX macros when available. Do not manually repeat a
number across intro, results, conclusion, backup, and alternate versions. Do not convert an
unresolved source gap into a fabricated citation. Cite linked official tables with agency and
observation year; distinguish observation year from publication/revision year.

## Assumptions Across Results

For an empirical-model-policy comparison, write a compact consistency matrix before slides:

| Dimension | Empirical calculation | Model benchmark | Policy variant |
| --- | --- | --- | --- |
| Outcome and units | ... | ... | ... |
| Shock, period, support, weights | ... | ... | ... |
| Budget/import/outside shares | ... | ... | ... |
| Ownership/trade/income balance | ... | ... | ... |
| Local slopes and finite-change rules | ... | ... | ... |
| Labor/factor mobility and capacity | ... | ... | ... |
| Housing, amenities, externalities | ... | ... | ... |
| Inference and conditioning | ... | ... | ... |

Only include relevant rows. Do not import these specific economic assumptions into unrelated
work. Mark differences as deliberate, unresolved, or erroneous. "Same calibration" is not
just matching a few parameter names. Distinguish geographic imports from model-outside inputs,
and share levels from marginal responses. Never claim a model matches estimated local slopes
because it reproduces the baseline account.

When a mismatch is intentional, name the variant on slides and explain which comparison remains
valid. If it is an error, separate the proposed computation fix from presentation cleanup.

## Estimation and Results

- Define dependent variable, exposure/treatment, identifying variation, fixed effects, controls,
  sample, weights, and uncertainty before interpreting slopes.
- Explain what is measured, calibrated, assumed, predicted, and recovered. Exposure is not a
  fitted outcome merely because it uses an equilibrium inverse.
- State the conditional nature of inference. Coefficient-only intervals are not full-pipeline
  uncertainty. No detected pre-trend is not proof of exogeneity.
- Show the actual intended outcome comparison. Do not carry fit statistics from a bilateral
  spending regression to an origin-income or price-index comparison.
- Confirm signs, scales, percentages versus percentage points, and total versus component
  indices. Present residual components before labeling an unexplained difference an externality.
- Do not use old tax/model results under a new calibration caption. Optimizer boundaries,
  constraints, convergence, rebate budget, and income balance matter when such results exist.

## Build and Link Checks

The bundled `audit_deck.py` reads `.nav`, `.log`, and the PDF next to the requested deck.
It checks 16:9 pages, frame coverage, internal named/numeric destinations, material build
warnings, and (when supplied) ledger labels/timing. It writes a JSON audit and a frame CSV.
Treat missing build files as incomplete QA, not proof the source is clean.

It renders all main PDF pages for `--render main`, one final page per logical frame for
`--render finals`, or every page for `--render all`. Contact sheets group the rendered pages.
It does not detect all overlaps or validate equations/results. It never substitutes for reading
the material or inspecting the images. It flags review status as required, not passed.

## Visual Review

1. Inspect a representative title, reasoning slide, derivation, figure, table, and backup early.
2. For a full build render every main reveal and every appendix final state. Inspect all changed
   intermediate figure states. Use contact sheets for order, then full-size pages for text.
3. Check title wrapping, formula widths, visual balance, readable source notes, and ample item
   gaps. A dense backup still must fit above or clear of its return link.
4. Verify figures occupy useful space, not giant invisible margins; plot labels are legible;
   legends do not crush maps; comparable exhibits have fixed scales.
5. Follow main-to-backup and contextual return links. Check source hyperlinks in the PDF.
6. Compile the reading handout. Compare every final state with the intended reveal: no stacked
   replacement figures, missing interpretation, or meaningful comparison lost.
7. Check numerical statements against their authoritative artifacts, including conclusions and
   backup. Report what cannot be verified, not an unqualified "all results current".

For revision tasks, compare before/after page text or rendered pages outside the intended scope
when feasible. Preserve unrelated source edits and numerical outputs.

## Delivery

Keep the source editable and portable, with relative paths. Exclude restricted raw datasets
from slide packages. Deliver figures and generated value files actually needed to compile, not
private credentials, caches, entire replication trees, or unnecessary local absolute paths.
Do not upload or publish the deck unless explicitly requested. The original McGill reference
contact sheet stays in the personal skill; it is not automatically included in a new deck.
