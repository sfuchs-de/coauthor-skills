# Slide Execution Protocol

## Contents

- Slide-level workflow and writing rules
- Anti-slop patterns and formatting hierarchy
- Figures, tables, TeX, Beamer, PowerPoint, and visual acceptance

## Objective

Turn a deck into slides that work in the room: one slide, one job; clear hierarchy; short but meaningful bullets; concrete titles; readable figures; no generic AI prose. Preserve the author's claims, quantitative content, equations, figures, tables, citations, slide order, and slide count unless the user explicitly asks for deeper restructuring.

## Workflow

1. **Find the deck root.** Identify the editable source (`.tex`, `.pptx`, `.md`, etc.) and the rendered output if available.
2. **Map the deck.** List slide titles and classify slides as main-deck or backup/appendix. Note dense slides, unclear titles, repeated language, and figures whose captions do not explain the object being shown.
3. **Review slide by slide.** For each slide, identify the slide's job in one sentence: setup, data, method, evidence, mechanism, scenario, result, implication, or backup detail.
4. **Edit locally.** Improve wording and formatting without changing the empirical/mathematical content. Keep edits slide-preserving unless the user asks for reordering or structural revision.
5. **Render and inspect.** For visual formats, compile/export/render to images and inspect affected pages for crowding, overlap, clipped text, broken links, missing figures, and title fit.
6. **Report succinctly.** Summarize the deck-level improvements and any residual risks, such as unverified citations or figures that depend on stale upstream data.

## Slide Writing Rules

- Put the main point first. Do not make the audience wait for the takeaway.
- As a planning diagnostic, budget roughly two minutes per substantive slide. Cut or move material when the implied talk exceeds the available time.
- Use slide titles as claims or clear objects, not vague section labels. Prefer "PSCPI Tracks the Benchmark and Decomposes the Signal" over "Results".
- Make every slide answer one question. If a slide tries to define data, show a result, explain a method, and give policy implications, split or move detail to backup.
- Use concrete verbs: `measures`, `decomposes`, `weights`, `maps`, `prices`, `tracks`, `estimates`, `compares`.
- Define technical notation the first time it appears. Add a plain-English scale when using standard deviations, elasticities, index points, log points, or normalized units.
- Add quick context reminders for historical episodes, institutions, or acronyms the audience may not remember.
- Do not overclaim. Use "event-time evidence", "suggests", "maps to", or "under this assumption" when the method is descriptive or heroic.
- Keep the author's voice. Do not replace specialist language with generic explainer prose when the audience is technical.

## Anti-Slop Rules

Remove or rewrite:

- Template headings such as "What we do / What we find / Takeaway" unless the user explicitly wants that structure.
- Generic phrases: "same message", "key insight", "robust takeaway", "important implications", "deep dive", "landscape", "leverage", "shed light on".
- "Not just X but Y" constructions unless they are genuinely the clearest contrast.
- Inflated claims: "explains", "proves", "demonstrates causally", "settles", "shows definitively" when the slide only measures, decomposes, correlates, or forecasts.
- Long paragraph bullets that read like paper prose. Convert them into short hierarchical points.

## Formatting Pattern

Use this default slide structure unless the existing deck has a stronger local convention:

```text
Title: clear object or claim

- Bold label
  - Short explanatory bullet.
  - Evidence, number, or source.
- Second bold label
  - Mechanism or interpretation.
  - Caveat if needed.

Figure/table
Caption: what is shown, unit, sample/date, data source.
Bottom line: one sentence only if it adds value.
```

Formatting conventions:

- Use hierarchical bullets: 2-4 top-level bullets, 1-3 nested bullets each.
- Bold the key label at the start of a top-level point: `\textbf{Data}`, `\textbf{Construction}`, `\textbf{Interpretation}`, `\textbf{Result}`.
- Keep nested bullets shorter than parent bullets where possible.
- Keep captions self-contained: object shown, unit/scale, time period or sample, data source.
- Put definitions near first use, not in a far-away appendix.
- Keep backup slides technical but still formatted consistently. Main slides should carry takeaways; backup slides should carry source detail, equations, diagnostics, and robustness.
- Avoid visible "how to read this slide" instruction text. Let labels, captions, and hierarchy do the work.

## Figures and Tables

- Explain what is being mapped or plotted before asking the audience to read the figure.
- Prefer a presentation-specific figure or table over a paper screenshot. Rebuild labels, precision, annotations, and aspect ratio for the room.
- Add source labels directly below figures or in captions.
- Make figure captions say the unit and scale. Example: "Index in standard deviations from normal" or "daily vessel transits, 7-day average".
- Move long data provenance, formulas, and method caveats to backup slides, but link or reference the backup when useful.
- For tables, make column headers conversational and comparable. Highlight the headline numbers; gray out secondary numbers only if the format supports it.
- Do not let a figure carry an unexplained acronym, notation, or episode label.

## TeX and Beamer Editing

When editing Beamer/LaTeX slides:

- Preserve labels, citations, equations, figure filenames, and backup navigation unless the user asks to change them.
- Prefer local prose edits over macro changes.
- Use existing list environments and color macros.
- Compile after edits with the project's existing build command.
- Render affected pages and inspect visually. Do not rely only on a successful LaTeX compile.
- Search the log for `Warning`, `Overfull`, `Underfull`, `undefined`, `Rerun`, `Too large`, `Float`, and `Missing character`.

## PowerPoint or Other Visual Decks

When editing `.pptx` or exported decks:

- Preserve layout theme, fonts, slide masters, and figure placements unless the user asks for redesign.
- Export or render changed slides for visual QA.
- Check text boxes for overflow, cropped text, inconsistent font sizes, and unaligned source notes.

## Acceptance Checklist

Before finishing, verify:

- Each edited slide has one clear job.
- Titles fit and are not generic.
- Main slides use short hierarchical bullets with bold labels.
- Technical notation and scales are defined at first use.
- Figure/table captions identify source, unit, and object shown.
- AI-ish phrasing and formulaic prose have been removed.
- Claims are calibrated to the evidence.
- Backup slides are consistent with main-slide language and source labels.
- The rendered deck has no visible overlap, clipping, unreadably small text, or broken figure/table placement.
