# Formatting Economics Research

## Evidence versus House Choices

The sample spans published AER, QJE, Econometrica, JEP, and Annual Review articles
and author manuscripts. Publisher typefaces, trim sizes, headers, and copyediting
are not evidence of an author's preferred submission format. The table below
reports representative body/footnote sizes observed in embedded PDF font samples;
it is not a specification for submission. Fonts in math and illustrations can
have other sizes. Four pages per source were sampled computationally; one selected
page per source was inspected visually, with additional close inspection of maps,
diagrams, and a wide table.

| Sample/version family | Page size, PDF points | Representative body / notes | Embedded text family |
|---|---|---|---|
| AER published: D01, D03, R03 | 504 x 720 | 11 / 8 pt | Times LT |
| QJE published: D02, D04, D06, R02, R04, R07 | about 431 x 649 | 10 / 8 pt | New Century Schoolbook or corresponding publisher font |
| Econometrica published: A05, R01 | 486 x 702 | 10.5 / 8.5 pt | Dutch 801 |
| JEP published: D05, A04, R06 | 504 x 720 | 10 / 8 pt | New Baskerville |
| Annual Review: R05 | 612 x 792 | 9 / 7 pt | Janson Text |
| Author manuscripts: A01-A03, A06, K01-K03 | 612 x 792 | typically 12 / 10 pt | Computer Modern family or related TeX encoding |
| Author manuscript: K04 | 612 x 792 | 12 / 9-10 pt | Palladio |

Version dates and sample pages are in the database. A04's university file contains
an unrelated article before the requested paper; only PDF pages 21-46 enter this
study. No appearance from the unrelated pages supports a recommendation.

### Recommended Reading Draft

Retain the project's established 12-point XCharter body text rather than adopting
a publisher's trim size. Use letter paper, approximately one-inch margins, and a
consistent modest line spread suited to coauthor reading. This is a house choice,
not a finding that these authors use XCharter. Follow journal requirements for
submission. Do not change page geometry merely to reduce page count.

Keep one hierarchy of section, subsection, and subsubsection. Use sentence-case
descriptive headings; do not put complete claims into very long headings. Headings
should have text beneath them before the next heading unless the hierarchy
genuinely requires otherwise. Reserve bold for structure or occasional key terms,
not whole paragraphs. Avoid decorative boxes around theory or results.

## Equations and Formal Statements

### Displays

- Display a central definition, optimization problem, estimating equation, or result.
- Keep small relationships inline when their appearance would otherwise interrupt prose.
- Number displays that are cited; leave incidental substitutions unnumbered.
- Use `align` or `aligned` for related derivation steps, not repeated independent display blocks.
- Treat punctuation after a display as part of its sentence.
- Give a long expression an economic explanation before adding more displays.
- Use semantic labels and automatic numbering; never repair references by manual tags.

An optimization problem should distinguish the value function from the optimizer.
Use `max` for the value and `arg max` for the choice. State the feasible set or
budget constraint. Do not abbreviate the budget in words if that hides the income
or price object central to the argument.

### Assumptions and Results

Use named, numbered theorem environments. Label both assumptions and results.
Introduce the reason for an assumption in ordinary prose; state its mathematical
content without mixing in a literature survey. Name the conditions in the result,
then explain it in ordinary prose. Avoid using italics as the only difference
between several long adjacent formal blocks.

For several cases, use numbered clauses with parallel grammar. Break long
parameter conditions into readable lines. A02's rendered theorem illustrates how
compact conditions can become dense even on an author-manuscript page; compactness
alone is not a readability goal. A01 and K01 provide useful examples of explanatory
prose before and after formal material.

Use `\ref` or an appropriate typed reference for an assumption/proposition; reserve
`\eqref` for an equation. Attach a label only to a genuinely equivalent statement
after consolidation. Do not retain an obsolete label by pointing it at an unrelated
new result. Core and online appendices need distinct numbering and reliable
cross-document references.

### Notation

Maintain a notation dictionary: object, dimension, units, index orientation,
normalization, and first definition. Use consistent origin/destination indices.
Do not overload the same letter for a share, a price, and a matrix without a clear
reason. Distinguish gross from net values, nominal from real quantities, and
baseline shares from derivatives.

Notation should save repetition rather than create a symbol for every phrase.
Introduce the general economic object in words before its abbreviation. Explain
new composite indices and normalized variables at first use.

## Tables

### House Standard

Use 10-point table text and captions, with single-spaced 9-point notes. A final
included table should never have text below 9 points. These are recommendations
for the project's reading draft, not measurements inferred from every published
article. Avoid stacking `\small`, `\footnotesize`, and `\resizebox` reductions.

Use booktabs-style rules and no vertical lines. Decimal-align numerical columns
with a structured number formatter such as `siunitx` where compatible with the
project. Preserve declared precision; changing the displayed digits is not a
formatting-only edit if it affects interpretation. Keep estimates and standard
errors in a consistent arrangement, usually estimates above parenthesized errors.

Place the table caption above. Recommended style: bold number, short sentence-case
title. Published articles often use capitals or small capitals; that is not a
requirement for a local manuscript. Use panel headings to separate different
outcomes, units, or scenarios. Define symbols or codes in readable labels or notes.

### Notes Checklist

One left-aligned block below the exhibit should identify:

1. The dependent variable or measured object and its units.
2. The observation unit, geography, dates, and sample restrictions.
3. Any normalization, trimming, weighting, or scaling.
4. Which columns change controls, assumptions, or estimators.
5. The uncertainty definition, clustering level, and significance conventions if used.
6. Source attribution and qualifications for conditional or simulated results.

Do not repeat all coefficient values in notes. Do not refer the reader to the main
text for the dependent variable's unit. D06's fit table, A05's trade regressions,
and R07's model/data comparison illustrate different note tasks. Their scientific
claims remain the authors' claims; this study is about presentation.

### Wide Tables

Before reducing type, remove duplicated columns, shorten labels without losing
meaning, split panels, or separate headline and additional specifications. If a
wide table remains essential, use a landscape page or a larger figure-only space.
Do not convert a table to a raster screenshot. A mathematically labeled row may
need an economic description alongside it; a dense expression alone can obstruct
comparison, as the wide R03 sample illustrates.

## Figures, Maps, and Diagrams

### Size and Typography

Generate at the intended inclusion dimensions. Preserve aspect ratios. For the
paper-specific output, target 8.5-point ticks, legends, and annotations, 9.5-point
axis titles, and 10-point panel headings at final inclusion. Use the manuscript
font where feasible and embed it. These are house specifications, not a claim
about a universal author practice.

If an exhibit cannot fit legibly, restructure it rather than shrinking a slide
export. Do not mistake file-canvas font sizes for final included sizes. Audit
embedded fonts after scaling and visually inspect the rendered manuscript.

### Empirical Comparisons

State the observed and predicted objects, transformations, residualization, support,
weights, and fitted relation. For a gravity scatter or smoother, label whether
origin/destination effects are removed, which points are present, and which sample
or bins determine the curve. Name the smoothing method and uncertainty procedure.
Do not imply a confidence band is prediction uncertainty. A 45-degree line is a
level/slope benchmark, not a causal validation test.

When there are many points, use restrained transparency, density shading, or
explicit bins; export the underlying observations. A smoother must not conceal
empty support, outliers, or reversal. A raw-point plot and a binned summary answer
different visual questions. D02's rendered local-polynomial figure is a useful
example of a clearly stated fitted relationship and band, not a command to use
that method for every network exhibit.

### Maps

Use the economic variable's appropriate scale, and retain classifications needed
for comparison. State whether bins are fixed, quantile-based, or independently
defined by panel. Identify missing observations separately from zero and water.
Show the denominator: totals, per person, per area, or shares are not interchangeable.
Use shared legends only when both scale and economic meaning match.

Place geographic examples in the discussion, not only in labels on the map. Keep
labels sparse, legible, and connected to the locations they name. Dense tract
boundaries may be needed for geography but should not overpower the plotted object.
R06's three-map sample demonstrates explicit units, missingness, and normalization;
its many categories need not be copied for a smaller paper exhibit.

### Theory Diagrams

Define axes and initial equilibrium, then show the changed object and adjustment.
Link the movement at the relevant initial basket or allocation to the equation in
the text. Use consistent labels across the discussion and the drawing. Distinguish
an illustration from a quantitative calibration.

The A04 sample uses color and arrows to distinguish local and global adjustments.
That carries an argument, but the many labels illustrate the cost of adding every
step to a single static panel. A sequence of simpler panels or stepped slides can
be clearer. Do not rely on color alone: use labels, line patterns, and markers.

### Color and Accessibility

Use a restrained palette with stable scenario meanings. Preserve existing
economic channel conventions where they matter. Add line or marker distinctions
for grayscale and color-vision accessibility. Sequential scales suit magnitudes;
diverging scales require a meaningful center. A color shared by two figures should
not silently change from scenario identity to sign. Avoid decorative gradients.

## Placement and Flow

Default to `tbp`, with top placement preferred. Introduce an exhibit before its
discussion and keep it near the relevant text. Do not place `\clearpage` after
every exhibit or insert barriers after every paragraph. Use a barrier when a float
would otherwise cross into unrelated material, not to force a desired page count.

Reserve figure-only pages for genuinely large exhibits. Avoid a short text fragment
stranded before a full-page figure. Keep a caption and notes with the exhibit.
After repagination, inspect section openings, formal statements, table starts, and
the paragraphs on both sides of each large float. A clean build log does not
establish good flow.

Author manuscripts in the sample sometimes put exhibits after the main text or
references. That can suit a submission requirement; it is not the preferred layout
for an integrated reading draft.

## Citations, Footnotes, and Navigation

Use the project's citation system consistently. Cite specific propositions,
measurements, or empirical precedents rather than whole topics by association.
Move incidental comparisons and proof navigation to footnotes where helpful.
Retain references essential to an identifying assumption or headline limitation
in the main argument.

Number footnotes automatically. A footnote should belong to a specific sentence
and add useful content. Avoid footnotes that introduce a new central object, or
long collections of appendix labels without explaining their relevance. Dense
colored links in D04 and K04 are publisher/manuscript navigation choices, not an
instruction to color every reference. Prefer restrained links for a reading draft.

Maintain an exhibit ledger: semantic label, caption, main callout, discussion,
source, sample, units, and output hash. Use distinct appendix prefixes. Verify
external references from a clean build, not only from existing auxiliary files.

## Rendered Quality Gate

Before considering formatting finished:

- Compile all active manuscript variants and the online appendix.
- Check undefined references/citations, duplicate labels, and material overflows.
- Render changed exhibits and all repaginated transitions.
- Inspect at ordinary reading size and zoom small notes or labels.
- Check clipping, panel alignment, whitespace, grayscale distinctions, and font embedding.
- Verify that numerical values, bins, samples, and transformations did not change.
- Record irreproducible historical assets as exceptions; do not silently replace their data.

This guide does not modify the BCN manuscript, decks, or their existing style
helpers. Applying it is a separate, scoped revision.
