---
name: fuchs-bq-slides
description: Create or substantially revise research seminar decks from papers, notes, results, or existing slides in Simon Fuchs's minimalist McGill BQ/Baqaee-style Beamer format. Use for this specific white-and-blue, item-by-item reasoning style, normally about 45 substantive slides with stepped reveals and linked technical backup. Not the older NBER/Cowles house style or a review-only workflow.
---

# Fuchs BQ Research Slides

Turn supplied material into an argument the audience can follow one step at a time. Reproduce
the current McGill BQ deck's visual grammar, reasoning hierarchy, generous spacing, large
exhibits, restrained emphasis, and contextual backup. Do not reproduce its research claims.

This is a Beamer authoring skill, not a PowerPoint Template Gallery artifact. The portable
starter has no dependency on the original project or its SimplePlus theme.

## Choose the Scope

- New deck: use the starter below and build from the supplied evidence.
- Restyling or successor: preserve authoritative claims and create the requested version;
  do not rewrite a predecessor or replace numerical results merely to match the example.
- Local revision: apply the relevant style rules and check affected reveals, not the full
  creation procedure unless the changes alter the argument.
- If the user requests a different style, format, duration, or audience, that request wins.
  Do not force an economics-policy arc on a pure theory paper.

Do not synchronize to Overleaf, send files, run costly new estimation, or create a speaker
script merely because a deck was requested. These are separate tasks. Flag a result needing
recalculation; a styling task is not permission to silently recalibrate the research.

## Establish the Contract

Identify the supplied material, authoritative version, audience, available duration, required
outputs, and source/result gaps. Ask only about consequential missing choices; otherwise state
reasonable defaults and proceed. Read the actual paper, notes, tables, and figure generators,
not just an abstract or filenames. Existing source restrictions still apply.

Default for a full seminar comparable to the reference:

- 40--50 substantive main slides, centered on 45; title and agendas excluded.
- About 70--75 planned speaking minutes; allow roughly 90 minutes with discussion.
- Usually 2--4 meaningful reveals per main slide; static evidence may need one.
- A source-driven technical appendix. The reference's 112 backup frames are an accumulated
  research archive, not a quota. Never pad material to reach a PDF-page count.
- Deliver stepped Beamer source/PDF and a compact final-state reading PDF from the same source.
  Existing-deck revisions retain the existing version set unless a new one is requested.

The measured reference has 45 substantive main slides, 51 main frames including navigation,
121 main PDF pages, and 276 total pages. Report substantive slides, logical frames, PDF pages,
and planned minutes separately. When material or time cannot support the default, shorten and
explain the tradeoff; do not invent findings or generate empty slide slots.

## Read the Relevant References

1. Read [references/design-system.md](references/design-system.md) before slide authoring.
2. Read [references/argument-and-length.md](references/argument-and-length.md) before a full
   deck or substantial restructuring. It defines the reasoning graph and slide map.
3. Read [references/evidence-and-qa.md](references/evidence-and-qa.md) before presenting
   empirical/model results or declaring a build complete.
4. For visual calibration, inspect [references/public-calibration.md](references/public-calibration.md). Private manuscript screenshots are not distributed. Screenshots
   are design precedents only; they are not source material for a new paper.

## Build the Argument Before the Slides

Write one sentence connecting the question, mechanism or method, evidence, and answer.
Build a compact reasoning graph and slide map using the schema in the argument reference.
Each slide owns one question, claim, derivation step, evidence exhibit, or handoff. Map it to
sources and dependencies, and record its reveal sequence and speaking time.

Introduce intuition before formal results, scalar objects before matrices, and restrictions
before conclusions that need them. For each contribution explain what it takes as input and
what it delivers. Link the end of theory to the empirical tasks in the same vocabulary.

### Standard Seminar Opening

Unless the user requests another order, use: motivation/question, an explicit **This paper**
slide, an optional separate headline-findings slide, then **Related literature**, before the
first model/data agenda. Related literature immediately follows the contribution/findings
block; citations in a footer do not replace this slide. On contribution and findings slides,
use short top-level labels with one level of actual nested explanatory bullets, not long
inline paragraphs after bold labels. Reveal each parent together with its supporting children.
See the argument reference for the literature slide's job and how to avoid repetition.

Read the figures and numerical outputs before writing result headlines. Results do not become
current because their source file was modified recently. Establish which run, calibration,
sample, and specification actually governs each result.

## Start a Portable Deck

Resolve this skill's directory, then run with an available Python 3 interpreter:

```bash
python3 /path/to/fuchs-bq-slides/scripts/init_deck.py /absolute/path/new-deck
```

The initializer refuses to overwrite an existing destination. It copies `assets/deck/`:
`deck.tex`, `handout.tex`, `bq-theme.sty`, and a worked `slide-map.json`.
Replace the short, explicitly illustrative worked example with the supplied material. Its
economics is not a template for the new paper's results. Grow into section files when useful;
keep one source for numerical macros and one shared theme across versions.

For an existing project, reuse its build system and packages; import only the relevant theme
and layout conventions. Do not discard working bibliographies or replace figure pipelines.

## Author Item by Item

- Lead with a concrete question or finding, not a generic topic slogan.
- Use 2--4 top-level reasoning steps, with one level of nested reasons, definitions, or
  implications when useful. Do not nest merely to fit more prose.
- One main equation or a short derivation at a time. Define symbols in neighboring text and
  use the same sparse semantic color for an object in equations and prose.
- Reveal premise, construction, result, and interpretation in causal order. Keep all earlier
  needed premises visible. Reserve geometry so later reveals do not move earlier content.
- Keep emphasis selective: one short bold phrase for the key operation or contrast, not
  whole sentences or every bullet label. Blue titles and triangle bullets already provide
  hierarchy. Red is an optional second semantic accent.
- Put material identifying assumptions in the items. Footnotes carry sources, units,
  uncertainty details, and limits, not a hidden assumption that reverses the conclusion.
- Let plots use the available body area; keep a histogram compact enough to retain its
  shape. Prefer comparable overlays and matched panels over repeated full slides.
- Use underlined textual backup links at the end of the relevant item or bottom-right.
  Provide contextual return links. No button-shaped navigation chrome.

The design reference contains exact spacing, color, font, figure, table, and layout defaults.
It also explains handout-safe replacement reveals; ordinary `only` commands can superimpose
in handout mode unless the desired final state is specified.

## Verify and Deliver

Compile both requested versions with `latexmk -pdf -interaction=nonstopmode -halt-on-error`.
Run the bundled audit (requires `pypdf`; rendering also needs Poppler and Pillow):

```bash
python3 /path/to/fuchs-bq-slides/scripts/audit_deck.py deck.pdf \
  --ledger slide-map.json --out qa --render main
python3 /path/to/fuchs-bq-slides/scripts/audit_deck.py handout.pdf \
  --out qa-handout --render all
```

This checks build warnings, frame/page counts, 16:9 geometry, internal destinations, and ledger
coverage, then renders pages/contact sheets when requested. It cannot certify visual quality,
economic validity, or result freshness. Inspect every main reveal, every appendix final state,
and changed replacement states. Open dense pages at full size. Verify final-state handouts do
not stack mutually exclusive panels. Re-render after fixes.

Deliver editable source, compiled PDFs, required assets, slide map, reasoning graph, result
provenance where relevant, and a short QA summary. State the count/time, what was omitted,
unresolved source or assumption gaps, and checks actually performed. Keep the close-out brief.

For speaker notes or external synchronization, use the corresponding available workflow only
when requested. Do not infer permission from a historic request embedded in source documents.
