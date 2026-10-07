---
name: fuchs-econ-slides
description: Create or substantially revise economics and academic Beamer presentations in Simon Fuchs's standard NBER/Cowles format. Use when building a new research deck, converting a paper into slides, creating long/short/stepped versions, or standardizing an existing deck to the house style.
---

# Fuchs Economics Slides

Create research presentations that inherit the mature NBER short-v3 visual system and argument structure. The deck must work in the room: one job per slide, claim-based titles, readable evidence, restrained semantic color, deliberate reveals, and linked technical backup.

Do not use this skill merely to review an unrelated deck without restyling it. For review-only work, use the general slide-review workflow. Do not push to Overleaf unless the user separately requests synchronization.

## Read Before Building

- Read [references/style-guide.md](references/style-guide.md) for visual, typography, layout, figure, and navigation conventions.
- Read [references/deck-architecture.md](references/deck-architecture.md) to choose the argument spine and slide jobs.
- Read [references/source-decks.md](references/source-decks.md) only when the original NBER/Cowles sources are locally available and inspecting a precedent would resolve a design choice.

Use [assets/standard-deck.tex](assets/standard-deck.tex) and [assets/beamerthemeSimplePlus.sty](assets/beamerthemeSimplePlus.sty) as the default starting point for a new Beamer deck. Preserve a project's established bibliography and figure paths when revising an existing deck.

## Establish Authority

Before editing, identify:

- the exact paper, note, results, and data documentation that govern claims;
- the target audience, talk length, interruption norm, and required output versions;
- the authoritative deck source and rendered PDF, if one exists;
- the figure and table assets that are current;
- whether the task is a new deck, a versioned successor, or an in-place revision.

Never infer units, sample definitions, equations, or empirical results from filenames alone. Do not update a slide claim unless the paper, code output, or documented result supports it.

## Build the Slide Map

Write a compact internal slide map before authoring. For each substantive slide record:

- claim-title;
- one-sentence job;
- evidence object or equation;
- source location;
- estimated speaking time;
- reveal plan;
- main, optional, or backup status.

Budget roughly 1.5--2 minutes per substantive slide, with more time for equations and audience discussion. Section dividers and title slides do not count as substantive slides.

## Author in the House Style

Apply these defaults unless the user or an existing deck requires otherwise:

- 16:9 Beamer, `SimplePlus`, white canvas, dark-blue title rule, minimal page number.
- One question or economic claim per slide.
- Claim-based title, then a thin progress strip when the section has a meaningful internal sequence.
- Two to four top-level ideas, normally introduced by bold topic markers.
- Semantic colors stay fixed across equations, prose, figures, and tabs.
- Most body content is `\footnotesize`; never solve crowding by shrinking an entire slide below readable size.
- Use section dividers for major argument transitions, not for every subsection.

### Standard slide forms

- **Motivation:** setting, economic tension, then the paper's question.
- **Contribution:** object, method/data, quantitative evaluation, and headline findings; avoid a generic feature list.
- **Theory or framework:** define the economic environment, develop equations in logical order, and explain each object in prose.
- **Measurement or stylized fact:** construction on the left, principal evidence on the right, and a restrained stylized-fact box when useful.
- **Quantitative result:** `Experiment` first, then the principal figure or table, then `Results` with economic magnitudes and interpretation.
- **Conclusion:** nested hierarchy for framework, measurement, quantitative findings, and the central distinction or implication.
- **Backup:** self-contained technical detail with a roadmap and contextual return link.

Do not put a figure on screen before the experiment or construction needed to interpret it, unless the figure itself is the motivating fact.

## Figures and Tables

Prefer presentation-specific exports. Remove internal titles that duplicate the slide title. Keep figure dimensions stable across reveals and use `keepaspectratio`. Every figure note should state:

1. the object and unit or scale;
2. the sample, period, or scenario when needed;
3. a concise `Data:` or `Model:` provenance tag.

Use direct labels, consistent map projections, comparable scales, and economically meaningful precision. Avoid screenshots of paper figures, nested cards, decorative boxes, and legends that require the audience to decode many unrelated colors.

## Reveals and Versions

Use no more reveal steps than the logic requires. A standard sequence is:

1. question or experiment;
2. evidence or equation;
3. interpretation.

Create a stepped version only when the delivery benefits from revealing bullets, equations, or maps separately. Keep positions fixed across overlays. Derive short versions from the accepted long-deck narrative rather than independently rewriting them.

For a versioned request, leave the predecessor untouched and create the requested successor. Keep long, short, and stepped sources synchronized in terminology, notation, figures, and results.

## Compile and Visual QA

Compile with the project's existing command or:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error <deck>.tex
```

Then:

- inspect the log for missing figures, undefined references/citations, duplicate labels, missing characters, and material overfull boxes;
- run `qpdf --check` and `pdfinfo`;
- render every main-deck page, including all meaningful overlay states;
- inspect title fit, vertical centering, text hierarchy, figure legibility, clipping, overlap, progress-strip placement, and backup links;
- test links from main slides to backup and return links back to context.

A successful compile is not completion. Correct visible problems and re-render until the deck is clean.

## Deliverables

For a full creation task, provide:

- editable `.tex` source and `beamerthemeSimplePlus.sty`;
- compiled PDF;
- any new presentation-specific assets;
- a concise slide inventory with substantive-slide count and estimated talk time;
- a speaker script only when requested;
- a note identifying deliberate omissions, optional cuts, and remaining source uncertainty.

Report the source used as authority, versions created, compile status, pages visually inspected, and residual warnings. Synchronize with Overleaf only after the user asks for it and the guarded Overleaf workflow is applied.
