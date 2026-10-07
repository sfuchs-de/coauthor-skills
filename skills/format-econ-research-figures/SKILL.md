---
name: format-econ-research-figures
description: Standardize, redesign, and verify economics research figures, maps, tables, multi-panel exhibits, and their integration into TeX papers or slide decks. Use when Codex is asked to clean up plots, apply consistent figure conventions, make Python output look like restrained tidyverse graphics, harmonize map styling, repair panel layouts, standardize legends/captions/fonts/colors, trace generated assets, or conduct visual QA of research exhibits.
---

# Format Economics Research Figures

Apply a restrained, reproducible visual system to economics research exhibits. Preserve the underlying data and economic object unless the user separately asks for a new calculation.

## Workflow

1. **Locate the source of truth.** Find the script, input table, configuration, and generated output. Do not edit a PNG when a generating script exists.
2. **Read the surrounding document.** Determine the figure's economic role, units, sign convention, sample, scenario, and neighboring exhibits.
3. **Audit before editing.** Inspect the existing figure at native resolution and inside its compiled paper or slide. Record clipping, illegible text, inconsistent scales, misleading encodings, and stale assets.
4. **Declare a visual contract.** Reuse the project's established typography and semantic colors. If none exists, use the defaults in [visual-contract.md](references/visual-contract.md).
5. **Edit the generating source.** Keep changes scoped. Separate substantive recalculation from visual formatting and state clearly if both occur.
6. **Export for the destination.** Prefer vector PDF for line art, maps, and charts; use high-resolution PNG only when raster content requires it. Let TeX own figure titles, subtitles, panel labels, captions, and notes whenever possible.
7. **Compile and inspect.** Render the target TeX/PDF or slide deck. Inspect the exhibit at full page and presentation scale, not only as a standalone image.
8. **Verify provenance.** Check units, values, hashes, asset destinations, and references. Record any unsupported or diagnostic-only output.

## Core Conventions

- Give each main-text figure one economic job.
- State the displayed object and denominator exactly. Distinguish levels, shares, percentage changes, percentage points, elasticities, ranks, and model-implied quantities.
- Keep sign semantics fixed across the project. For welfare costs, positive means harm unless the document explicitly adopts another convention.
- Use color semantically, not decoratively. Reuse the same color for the same country, scenario, route, or mechanism across figures.
- Use a colorblind-safe palette. Avoid rainbow scales, saturated backgrounds, gradient decoration, and more than one visual emphasis hierarchy.
- Use shared axes, extents, breaks, and color limits for panels intended for comparison.
- Prefer direct labels and small legends. Do not repeat information in the title, subtitle, legend, caption, and note.
- Keep text horizontal where feasible. Use sentence case and zero letter spacing.
- Avoid chart borders, heavy gridlines, shadows, 3D effects, excessive annotations, and Python-default styling.
- Use `booktabs` tables with no vertical rules. Put units in headers and align numbers by decimal point.
- Never treat a presentation copy as the generated source of truth.

## Figure-Specific Guidance

- For map layers, route networks, closures, and geographic counterfactuals, read [maps.md](references/maps.md).
- For statistical charts, event studies, decompositions, heatmaps, and tables, read [charts-tables.md](references/charts-tables.md).
- For TeX typography, subfigures, captions, paper integration, and slide layouts, read [tex-slides.md](references/tex-slides.md).
- For render checks, numerical reconciliation, manifests, and delivery, read [qa-provenance.md](references/qa-provenance.md).

## Editing Rules

- Preserve the repository's plotting language and helper functions unless a change is necessary for correctness or consistency.
- Prefer a shared style helper over repeated local formatting once at least three figures use the same settings.
- Do not silently alter samples, weights, bins, truncation, winsorization, projections, route support, denominators, or model scenarios while restyling.
- If a requested visual change exposes a substantive data or model problem, stop presenting the output as a cosmetic fix. Report the problem and separate validated from diagnostic material.
- Keep unsupported scenarios and incomplete-support maps out of headline exhibits or label them explicitly.

## Completion Standard

Before reporting completion:

1. Rebuild the figure from source.
2. Compile the target paper or deck.
3. Inspect every changed page visually.
4. Check values against the generated table.
5. Check font size, panel alignment, land/sea contrast, legends, colorbars, clipping, and whitespace.
6. Run PDF integrity and repository whitespace checks where applicable.
7. Report the generating script, principal output, validation performed, and any remaining caveat.
