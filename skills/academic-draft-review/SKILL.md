---
name: academic-draft-review
description: Compile, inspect, and correct an author's academic TeX, Markdown, LyX, theory, appendix, or manuscript source. Use for author-side build and source-repair loops. Do not use for independent referee reports; use `referee-report`. Use `audit-tex-math` when proof or derivation correctness is the primary task.
---

# Academic Draft Review

## Modes and authority

- `compile`: discover the root, build and inspect the rendered output without changing source.
- `repair`: make narrowly authorized source corrections and repeat the build/inspection loop.
- `short-note-layout`: apply `references/short-note-style.md` while preserving claims and math.

Review and compilation alone do not authorize edits. Do not change statements, assumptions,
estimates or causal language as formatting. Route consequential mathematical changes to
`audit-tex-math` and require explicit repair authority.

## Overview

Use this skill for paper-quality review loops: find the manuscript root, compile when possible, audit the math and exposition, make narrow corrections, and verify the PDF/log state.

## Ownership Boundary

This is an author-side source and compilation skill. Route independent reviewer judgments,
publication-bar assessments, referee reports, and editor notes to `referee-report`. Route a focused
proof or derivation audit to `audit-tex-math`. When both compilation and mathematics matter, compile
here and use the math audit only on the pivotal claims.

## Root Discovery

1. Prefer the file named by the user.
2. Otherwise look for `0_main.tex`, `main.tex`, `paper.tex`, `*.lyx`, `latexmkrc`, `Makefile`, or manuscript-specific docs.
3. Inspect `\input`, `\include`, bibliography files, figures, custom class/style files, and generated outputs before editing.
4. Preserve the existing one-file or multi-file structure unless the user asks for reorganization.

## Compile Loop

- Use the project command if documented. Otherwise start with:
  `latexmk -pdf -interaction=nonstopmode -halt-on-error <root.tex>`
- If `latexmk` is unavailable, fall back to the minimal `pdflatex`/`bibtex` or `biber` sequence implied by the project.
- Read the `.log`, `.blg`, `.bbl`, `.out`, and console output for real blockers first: undefined control sequences, missing files, undefined references/citations, bibliography failures, hyperref bookmark warnings, and serious overfull boxes.
- Cosmetic underfull bibliography URL warnings can be reported without blocking unless the user asks for production polish.

## Math And Theory Review

Audit for correctness, not just grammar:

- Match theorem claims to assumptions, domains, positivity restrictions, boundary cases, and proof logic.
- Check dimensions, signs, notation conflicts, overloaded symbols, equilibrium objects, fixed-point maps, convergence claims, and comparative-static derivatives.
- Flag overclaims such as "sharp", "iff", "unique", "global", "trichotomy", or "without loss" unless the draft proves them under stated assumptions.
- For generated or revised theory text, search for stale terms after edits and confirm cross-references still point to the right claims.

## Correction Rules

- Apply these corrections only when edits are authorized. Flag apparent substantive defects in
  review-only mode, and route mathematical or argument changes to their owning specialists.
- Make source edits narrowly and in the author's style.
- Prefer weakening or conditioning claims over inventing new results.
- Preserve citation style and avoid adding external citations unless the user asks or local files already support them.
- Recompile after changes and rerun targeted searches for stale notation, labels, and old terminology.

## Short-note and graph protocols

For `short-note-layout`, read `references/short-note-style.md` and run
`python3 <skill-directory>/scripts/check_short_note_format.py <root.tex>`.
Preserve project-specific formatting unless the user requests the house style. Visually inspect
affected pages, dense equations/tables, appendices and bibliography; a clean build is not visual QA.

For shared graph workflows, read
`../econ-writing-suite/references/reasoning-graph-integration.md` and own the `source_qa` layer.
Record authoritative file/line/label/page anchors and source/render mismatches. Flag moved anchors
as stale for their semantic owner; build success establishes neither argument nor math validity.

## Final Response

Report the root file, compile command, PDF/output path, issues fixed, remaining warnings, and any residual math risks that require author judgment.
