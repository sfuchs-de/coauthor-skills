---
name: research-note-tex
description: Create, refactor, and compile self-contained economics research notes in TeX/PDF that summarize recent theory, computational, empirical, or mixed results. Use when Codex is asked to turn discussion, notes, derivations, model results, simulations, regressions, or research fragments into a polished standalone LaTeX write-up matching Simon's compact house-note format, including economics-style step-by-step derivations and compiled output.
---

# Research Note TeX

## Core Workflow

1. Identify the note type: theory, computational, empirical, or mixed.
2. Inspect the available source material: conversation context, attached text, TeX, Markdown, code output, tables, figures, or logs.
3. Create a self-contained `.tex` document from `assets/research-note-template.tex` unless the user supplies a stricter template.
4. Preserve the house layout: compact article note, clear title/subtitle, section-level equation numbering, short sections, run-in paragraphs, theorem environments, and appendices for long derivations.
5. Present derivations in economics style: define the economic object, state the margin, show line-by-line algebra, then interpret the final terms.
6. Compile the `.tex` to PDF, inspect the log, and fix serious compile errors, undefined references, missing citations, and material overfull boxes.
7. In the final response, provide the `.tex` path, PDF path, compilation status, and remaining material warnings.

Use `scripts/compile_tex_note.sh <path/to/file.tex>` when a normal LaTeX build is appropriate. If the project already has a build system, use the project build system instead.

## Output Format Contract

Write a research note, not a chat transcript. Do not include conversational framing inside the TeX.

Follow this house format unless the user provides a different template:

- Use `article`, `11pt`, 1-inch margins, `microtype`, and `\setstretch{1.15}`.
- Use section-level equation numbering with `\numberwithin{equation}{section}`.
- Use compact `titlesec` styling: large bold sections, normal-size bold subsections, and bold run-in paragraphs.
- Use black internal links and blue URLs via `hyperref`.
- Use an empty author unless specified.
- Use a bold title and optional subtitle:
  `\title{\textbf{...}\\[0.5em]\large ...}`.
- Include theorem, lemma, proposition, corollary, assumption, definition, and remark environments.
- Keep general macros in the template and add project-specific macros in the marked project-macro block.
- Use explicit dates for archival/reproducible notes; use `\today` only for working notes.

Default section skeleton:

1. `Summary of Main Results` or `Introduction`
2. `Setup and Notation`
3. `Main Results`
4. `Interpretation`
5. `Implementation`, `Empirical Specification`, or `Computational Details` when relevant
6. `Checks, Limitations, and Open Issues`
7. Appendices for derivations, proofs, robustness checks, algorithms, and additional tables

Use boxed displays sparingly for final formulas, implementation recipes, or benchmark decompositions. Prefer short run-in `\paragraph{...}` labels for local exposition.

## Note-Type Guidance

For theory notes, state assumptions before results, use theorem-like environments only for verified claims, and put longer algebra in appendices.

For computational notes, include the problem, algorithm, inputs or calibration, diagnostics, numerical checks, results, and reproducibility details.

For empirical notes, include the question, data/sample, estimating equation, identifying variation, coefficient interpretation, robustness, and caveats.

For mixed notes, put the economic model or result first, then show how the computational or empirical object maps to it.

## Derivation Style

Read `references/derivation-patterns.md` before writing substantial derivations, appendices, welfare decompositions, FOCs, elasticity systems, envelope arguments, hat-algebra mappings, comparative statics, or regression microfoundations.

Required derivation discipline:

- State the economic object before the algebra: FOC, envelope condition, elasticity, welfare derivative, estimating equation, decomposition, or equilibrium mapping.
- Define primitives, controls, states, prices, shocks, constraints, and equilibrium objects before using them.
- State the margin being varied: tax, price, productivity, transport shock, policy counterfactual, parameter perturbation, or equilibrium shock.
- Use `align` or `aligned` for line-by-line algebra. Do not skip substitutions, chain-rule steps, normalizations, sign changes, or fixed-effect residualizations.
- Explain each final term economically after the display.
- Include checks: units, signs, row/column sums, limiting cases, logit/Cobb-Douglas/partial-equilibrium benchmarks, or zero-shock cases when relevant.
- If a step depends on an unproved condition, label it as an assumption, sufficient condition, maintained approximation, or conjecture.

Do not write "clearly", "obviously", or "it follows" for load-bearing steps. Replace those phrases with the missing algebra or the identity being used.

## Verification

Compile before finishing. Prefer:

```bash
path/to/research-note-tex/scripts/compile_tex_note.sh path/to/note.tex
```

If the build fails, inspect the first real LaTeX error and patch the source. Run at least two LaTeX passes when `latexmk` is unavailable.

Treat these as material warnings to report or fix:

- Undefined references or citations.
- Missing figures, tables, or input files.
- Package errors.
- Serious overfull boxes in visible text or equations.
- Unnumbered equations referenced later.

Warnings about reruns, benign font substitutions, or minor overfull boxes can be left if the final PDF is otherwise clean.

## Final Response

After compiling, respond with:

- path to the `.tex`
- path to the `.pdf`
- whether compilation succeeded
- any remaining material warnings

Do not paste the full TeX into chat unless the user explicitly asks for inline source.
