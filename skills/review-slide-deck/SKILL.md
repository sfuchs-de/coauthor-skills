---
name: review-slide-deck
description: Review academic, economics, policy, seminar, conference, and job-talk slide decks for audience comprehension, argument order, slide focus, visual accessibility, timing, delivery readiness, and question handling. Use when the user asks to critique, audit, red-team, score, or give slide-by-slide feedback on a PDF, PPTX, Beamer deck, Google Slides deck, or rendered presentation. Default to read-only review; use design-econ-seminar when the user asks to implement revisions or write a speaker script.
---

# Review Slide Deck

Review the talk the audience will experience, not merely the extracted text. Inspect every rendered slide, reconstruct the presentation's argument, and prioritize changes by their effect on comprehension and delivery.

## Choose the review mode

- `rapid`: inspect the complete deck, then report the overall diagnosis, the three to five highest-value changes, and critical slide-level failures.
- `full`: add the complete scorecard, section and timing map, actionable slide ledger, cut plan, backup-slide plan, and likely questions.
- `rehearsal`: focus on spoken flow, transitions, timing, interruption handling, questions, and which slides should be skipped under time pressure. Request or infer the allotted time and audience.

If the user does not specify a mode, use `full` for a manageable deck and `rapid` for a large deck or a quick-review request.

## Establish scope and authority

1. Identify the exact deck version and presentation type.
2. Determine the audience, allotted talk time, expected question culture, and the presenter's objective when available.
3. Treat the task as read-only unless the user explicitly asks for edits. Recommendations do not authorize source changes.
4. If material context is missing, proceed with labeled assumptions unless a wrong assumption would materially change the review.

Do not invent claims, results, citations, institutional facts, or timing observations. Distinguish a problem visible in the deck from one that depends on the speaker's delivery.

## Inspect the rendered deck

Use the relevant file-handling skill for the source format. For a PDF, use the PDF workflow; for PowerPoint or Google Slides, use the presentation workflow. Compile source when necessary and inspect the rendered result.

Review every slide at readable resolution. Also use a contact sheet or sorter view to assess pacing, repetition, visual rhythm, and section balance. Do not rely on text extraction alone.

For each slide, capture only what is needed for the audit:

- slide number and title;
- intended audience takeaway;
- role in the argument;
- principal visual, equation, or table;
- likely time cost and dependency on earlier material;
- any visible legibility, overflow, contrast, citation, or alignment problem.

## Reconstruct the talk before scoring it

Write a compact argument map:

1. question or problem;
2. answer or central claim;
3. mechanism or logic;
4. evidence or quantitative result;
5. contribution and implication.

Then map the deck's actual order onto that chain. Prefer answer-first ordering: state the main point, explain the main steps, then supply details. Flag openings that delay the question or answer behind biography, literature, institutional history, or apologies.

Test whether the talk is recursively cuttable. A shorter version should preserve the question, answer, evidence, and implication by removing later detail rather than breaking the logical chain.

## Apply the review rubric

Read [references/review-rubric.md](references/review-rubric.md) before performing a review. Evaluate:

- audience goal and opening;
- argument order and section transitions;
- one-message discipline and claim-style titles;
- text, notation, equations, figures, and tables;
- terminology and conceptual consistency;
- accessibility and rendered visual quality;
- timing, cutability, and backup material;
- closing, delivery cues, and question readiness.

Treat numeric rules as diagnostics, not laws. For example, slide counts and minutes-per-slide depend on complexity, interruptions, and speaker style. Never solve density by shrinking fonts or hiding essential assumptions.

## Classify findings

Use three priorities:

- `blocking`: the audience is unlikely to understand, trust, or finish the central argument within the allotted time;
- `material`: the issue impairs comprehension, credibility, pacing, or question handling but does not destroy the talk;
- `polish`: a worthwhile improvement after blocking and material issues are fixed.

Every finding must name the affected slide or section, explain the audience consequence, and propose a concrete remedy. Avoid generic advice such as “simplify” or “add intuition” without specifying what to cut, state, show, or move.

## Calibrate timing

Estimate time from slide complexity, not slide count alone. Allow more time for unfamiliar equations, dense tables, transitions, audience questions, and live demonstrations. Separate:

- core presentation time;
- expected interruption allowance;
- closing buffer;
- optional or backup material.

Produce a cut order for talks that run long. Preserve the main answer and evidence; move robustness, derivations, literature detail, and secondary extensions to backup unless they are central to the audience's trust.

## Produce the review

Use [references/report-template.md](references/report-template.md), scaling it to the requested mode. Lead with the outcome:

1. one-paragraph diagnosis;
2. the talk's argument in one sentence;
3. the highest-priority changes;
4. a compact evidence-backed scorecard;
5. section and timing map;
6. slide-level ledger only where action is needed;
7. cut and backup plan;
8. likely audience questions and missing defenses.

Separate deck changes from rehearsal changes. If the deck is already strong, say so and focus the report on the few remaining constraints.

## Route follow-on work

- Use `design-econ-seminar` in `slides` or `full` mode to implement approved deck revisions.
- Use `design-econ-seminar` in `script` mode for a timed speaker script.
- Use `academic-draft-review` only when a TeX build or source-repair loop is required beyond ordinary deck rendering.
- Consult the underlying paper when the deck's claims, notation, or contribution cannot be verified from the presentation alone.

Do not turn a review request into an unsolicited redesign.

## Source and adaptation

The core audience-centered principles are adapted and extended from Berthold Herrendorf, *How to Make Academic Presentations* (2021), available at <https://roozbeh-hosseini.github.io/PresentationTips.pdf>. The rubric paraphrases rather than reproduces the source and adds contemporary checks for accessibility, citations, mathematical slides, hybrid viewing, and rendered-file quality.
