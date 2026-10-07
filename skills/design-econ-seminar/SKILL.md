---
name: design-econ-seminar
description: Design, revise, and verify economics research presentations from narrative through delivery. Use for seminar, conference, lunch-talk, job-talk, policy, or discussant decks; restructuring a talk, cutting it to time, editing slides for clarity and accessibility, rendering and inspecting slides, or producing a slide-aligned timed speaker script. Select `structure`, `slides`, `script`, or `full` mode.
---

# Economics Presentation Design

Make the audience understand the question, answer, evidence, and economic contribution before
technical detail accumulates.

## Select the mode

- **structure**: audit the talk's argument, evidence order, section jobs, timing, cuts, and likely
  questions without performing slide-level edits unless requested.
- **slides**: revise wording, hierarchy, figures, tables, captions, and layout slide by slide;
  compile or export and inspect the rendered deck.
- **script**: create or audit slide-aligned Markdown speaker notes with per-slide and cumulative
  timing, reveal cues, transitions, and backup links.
- **full**: establish the narrative, revise the deck, render and inspect it, then write the script.

## Intake and authority

Identify the exact deck version, paper or supporting sources, format, total time, audience,
interruption norm, and requested scope. Treat the deck and underlying paper, code, or data
documentation as authority for claims, equations, units, samples, and figures. Do not infer a data
construction from a filename when source documentation is available.

Preserve claims, citations, equations, numerical results, labels, and slide navigation unless the
user explicitly authorizes substantive changes. For a review-only request, report recommendations
without modifying source.

## Structure mode

1. Write the one-sentence talk argument: question, answer, evidence or mechanism, and contribution.
2. Give each section and slide one job. Put the headline answer and magnitude before literature or
   machinery.
3. For empirical work, name the identifying variation and main threat. For theory or quantitative
   work, show what the model adds, which mechanisms drive the result, and what disciplines them.
4. Order evidence from setting and raw patterns to direct effects, mechanisms, validation,
   extensions, and policy or welfare implications.
5. Budget roughly two minutes per substantive slide, then adjust for equations, reveals,
   interruptions, and discussion. Maintain explicit cut and backup lists; do not solve timing by
   shrinking text or speaking faster.
6. For a discussant presentation, summarize the paper in one or two slides and spend the remaining
   time on value added and two or three constructive comments.

Maintain a slide map with: number, claim-title, job, evidence object, time, dependency, and
cut/backup status. When a paper reasoning graph exists, also record the source node IDs projected
onto each slide.

## Reasoning-graph projection

For a graph-centered paper-to-talk workflow, read
`../econ-writing-suite/references/reasoning-graph-integration.md` and own the `presentation` layer.
Treat the deck as a projection of the accepted paper spine: map each substantive slide to its source
claim, evidence, or mechanism nodes; record deliberate omissions, cuts, and backup branches; and
flag any slide claim that outruns its source scope. Do not edit the paper graph merely to simplify
the talk.

## Slides mode

Read `references/slide-execution.md`. Put the main point first, use claim titles, keep one question
per slide, define notation and units at first use, and calibrate claims to the evidence. Prefer
presentation-specific figures and tables over paper screenshots.

Compile or export after edits and inspect affected slides for overflow, clipping, unreadable text,
broken figures, title fit, inconsistent hierarchy, color dependence, and source/caption clarity.
Visual inspection is required; a successful build is insufficient.

## Script mode

Read `references/speaker-script.md` and use `assets/speaker-script-template.md`. Build an inventory of
exact titles, claims, equations, figures, overlays, citations, and backup buttons. For each slide,
state the claim, explain the evidence or equation, and provide a specific handoff rather than
reciting slide text.

Estimate delivery at roughly 115–135 spoken words per minute, with extra time for equations,
reveals, and visual inspection. Reconcile cumulative timing exactly and list optional cuts for
shorter versions. Use exact visible labels for backup links.

## Economics checks

- Identification: variation, relevance, exclusion logic, comparison group, and main threat.
- Quantitative model: primitives, estimated or calibrated objects, fit, benchmark, mechanism,
  validation, and counterfactual scope.
- Results: uncertainty and economically interpretable magnitudes, not significance alone.
- Figures and tables: readable labels, comparable scales, relevant precision, source, unit, sample,
  and date.
- Notation: define every acronym and symbol at first use and retain a running example when useful.

Read `references/econ-writing-presentation-guidance.md` for the imported result-first economics
heuristics. Read `references/sources.md` only when source-specific presentation guidance is useful.

## Completion

Report the selected mode, one-sentence argument, timing total, major moves or edits, cuts and backup
plan, rendered pages inspected, residual source uncertainty, and likely audience questions. In a
shared graph workflow, report presentation-layer coverage and deliberate omissions. In full mode,
confirm that deck and script use identical slide order, titles, numbers, notation, and timing.
