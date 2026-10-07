# Theory-note presentation contract

This contract distills the layout and presentation of the user-supplied example while deliberately
excluding its substantive model, notation, and equations.

## Page and typography

- Use an 11-point `article`, one-inch margins, microtypography, and 1.15 line spacing.
- Use compact, numbered section and subsection headings and run-in bold paragraph headings.
- Number equations within sections. Number theorem-like environments within sections.
- Use black internal and citation links and blue external URLs.
- Keep the page visually quiet: no colored theorem boxes, decorative rules, or oversized headings.
- Use a bold title, optional explanatory subtitle, restrained author block, and a real date supplied
  by the user or `\today`.

The neutral asset uses widely available packages. Add specialist packages only when the source
actually needs their commands. Prefer `mathtools`'s `\coloneqq` over a dedicated package and prefer
`\mathbf{1}` over loading multiple indicator-font packages.

## Information architecture

Open with `Summary of Main Results`. Its job is to make the complete argument legible before the
technical material. A useful order is:

1. **Goal.** State the question and what is unified, derived, or characterized.
2. **Objects and instrument.** Define only the primitives required to read the summary.
3. **Logic box.** Show the main causal or mathematical chain when it has at least three links.
4. **Intuition ladder.** Move from a scalar or one-block case to a two-block or low-dimensional case,
   then to the full matrix, operator, or equilibrium system.
5. **Headline result.** State the exact result with its assumptions and explain each term.
6. **Benchmarks and approximations.** Separate exact identities from local rules and computational
   characterizations.
7. **Implementation and diagnostics.** Include only when the note contains an algorithm or empirical
   interface.

Do not force this ladder when the source has no meaningful scalar specialization. A presentation
device must clarify the mathematics, not invent it.

After the summary, use either a conventional main exposition or a clearly marked technical appendix.
The example's appendix grammar is especially useful for a self-contained memo:

- setup, notation, and roadmap;
- primitive blocks and equilibrium or operator mapping;
- derivation of the key elasticity, Jacobian, transform, or sufficient statistic;
- formal theorem/proposition and proof;
- closed-form benchmarks and approximations;
- computation, verification, boundary cases, and limitations.

## Prose and displays

Use the recurring rhythm:

1. a sentence that names the operation or purpose;
2. the displayed equation;
3. a sentence that interprets the terms and states the condition under which the display is valid.

Use `align` when successive lines perform distinct algebraic operations. Use one equation label for
one referenced mathematical object. Avoid chains of unlabeled displays with no prose between them.

Use bold run-in paragraphs such as `Goal.`, `Normalization.`, `Unknowns.`, `Sanity check.`, and
`Failure conditions.` to orient the reader. Do not turn every sentence into a heading.

## Formal environments and boxes

- Use assumptions before results that need them.
- Put definitions before propositions and remarks after the formal claim.
- Use theorem environments sparingly; an identity need not be called a theorem.
- Use a plain framed minipage only for the central logic chain or a compact algorithm.
- Reserve boxed equations for at most the principal result or decision rule. Ordinary intermediate
  equations should not be boxed.
- Use lists only for assumptions, a genuinely parallel comparison, or a short algorithm. Prefer
  connected prose elsewhere.

## Notation and appendices

Introduce objects locally in the main text. Put a full notation table, dimensions, normalizations,
and raw-versus-transformed distinctions in an appendix. Keep detailed proof algebra in the appendix
only if the main text retains the operation, conditions, and conclusion needed to understand it.

## Content-neutrality guardrail

Never copy the example's tourist-tax primitives, economic claims, matrices, keywords, PDF metadata,
or subject-specific macros into an unrelated note. Match its hierarchy, spacing, theorem grammar,
summary-to-appendix architecture, and exposition rhythm—not its content.
