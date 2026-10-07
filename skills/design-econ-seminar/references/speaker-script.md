# Speaker Script Protocol

Create notes that sound spoken, remain faithful to the deck, and explain rather than recite the slides.

## Workflow

1. Identify the exact deck version and the requested scope: main deck, short deck, backup, or all slides.
2. Read the slide source when available. Compile or render the deck if page order, overlays, figures, or navigation are uncertain.
3. Build a slide inventory containing title, job, key claims, equations, figures, overlays, citations, and backup buttons.
4. Inspect relevant papers, notes, code, and data documentation. Use primary construction code for data definitions when prose and code disagree.
5. Draft one Markdown section per main slide using the structure in `references/script-template.md`.
6. Cross-check every section against the rendered slide and source.
7. Run a prose pass for accessibility and AI-style residue. Preserve technical meaning, citations, numbers, and notation.
8. Render the Markdown when requested and inspect page breaks, equations, and dense sections.

## Writing Rules

- Give each slide one speaking job.
- Use developed bullets rather than a wall of prose or a verbatim slide transcript.
- State the claim first, then explain the visual or equation, then give the handoff.
- Explain equations in words. Do not read symbols aloud or introduce notation absent from the deck without a clear reason.
- Mark click or reveal instructions in italics, for example `*Advance to the ratio.*`.
- Keep transitions specific. Avoid repeated phrases such as “This slide shows,” “We now turn,” “The key insight,” and “The next slide.”
- Distinguish facts, model implications, descriptive correspondences, and causal claims.
- Do not infer data construction from filenames or captions when code is available.
- Use the speaker's preferred vocabulary consistently across slides.
- Keep backup explanations short enough to use in a question period.

## Timing

- Add independent and cumulative time to each slide.
- Estimate at roughly 115--135 spoken words per minute, then add time for equations, reveals, and visual inspection.
- Reconcile cumulative times exactly; do not round each slide independently and leave an inconsistent total.
- Add a short list of optional cuts when the user wants multiple talk lengths.

## Source-Fidelity Audit

Check the final script against the deck for:

- slide order and exact titles;
- equations, signs, indices, units, and approximation language;
- figure objects, colors, panels, samples, and numerical results;
- experiment versus result versus interpretation;
- data construction and normalization;
- citations and qualifications;
- overlay order and reveal cues;
- exact backup-button labels and destinations.

If a statement cannot be established from the deck or supporting material, flag it rather than smoothing over the uncertainty.

## Backup Slides

- Mention optional backup slides on the page where the related main slide is discussed.
- Use the exact visible clicker label and identify the source slide carrying the button.
- Say explicitly when a main slide has no button.
- Add a compact backup-explainer section at the end only when it improves Q&A preparation.

## Final QA

- Run `ai-slop-lint` when available and iterate until no actionable findings remain.
- Read the script aloud mentally for rhythm and plausible spoken syntax.
- Verify that shortened transitions still preserve the argument.
- Confirm that source and delivered copies match when the project keeps multiple copies.
- If a PDF is produced, inspect the opening, densest theory slide, densest data slide, a result slide, and the backup section.
