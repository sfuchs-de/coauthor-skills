# Main Text, Footnote, and Appendix Alignment

## Contents

- Allocation rules for main text, footnotes, and appendices
- Cross-reference, notation, assumption, and duplication audits
- Orphan detection, relocation tests, and mathematical-correctness routing

## Principle

Technical detail should be allocated by its role in the reader’s reasoning chain, not by length alone.

- The main text must contain what the reader needs to understand the claim and why it matters.
- A footnote may carry a local qualification or compact technical aside.
- An appendix may carry a substantial derivation, proof, robustness exercise, alternate closure, or computational implementation.

The main text must not outsource its logic.

## Main-text requirements

Keep in the main text:

- the question a result answers;
- the economically or scientifically essential setup;
- all objects required to parse the central formula;
- assumptions that materially affect interpretation;
- the central result;
- the mechanism or intuition;
- the use of the result in the next stage of the paper;
- a precise statement of what the appendix supplies.

A main-text appendix reference should be informative:

Weak:

> See Appendix B.

Stronger:

> Appendix B.7 converts the destination coefficient into sales units, restores the origin price-index term, and states the additional matched-variation condition required for the retention interpretation.

## Footnote requirements

A footnote is suitable for:

- a citation or nomenclature point;
- a brief edge case;
- a short alternative normalization;
- a one- or two-step algebraic aside;
- a local qualification that does not change the main result;
- a pointer to an appendix or robustness exercise.

A footnote is not suitable for:

- a premise required for the displayed result;
- the only definition of a recurring object;
- an assumption that changes the sign or scope of the claim;
- a contradiction or correction to the main prose;
- a multi-paragraph derivation;
- a qualification that most readers would need to interpret the headline estimate.

Review footnote placement. A footnote marker should follow the precise claim it qualifies, not an entire paragraph when the target is ambiguous.

## Appendix requirements

For each appendix subsection, require a five-part contract:

1. **Main-text target**: identify the exact result, equation, estimate, or claim being supported.
2. **Purpose**: state what additional material is supplied.
3. **Notation and assumptions**: match the main text or provide an explicit dictionary.
4. **Derivation or evidence**: deliver the promised proof, detail, or robustness exercise.
5. **Return**: state what has been established and how it maps back to the main text.

Suggested opening:

> This subsection derives equation (2.10) from the bilateral spending identity and the propagation operator. It first states the exact response, then projects that response onto the observable direct and network-tail exposure basis used in the empirical specification.

Suggested closing:

> Combining the two projections yields equation (2.10). Exact recovery requires the common response-span and rank conditions stated above; otherwise the coefficients are pooled projection loadings.

## Cross-reference matrix

Build this table for every substantive reference:

| Main-text location | Claim or promise | Target | Target location | Delivered content | Same notation? | Same assumptions? | Returns to main text? | Status |
|---|---|---|---|---|---|---|---|---|

Statuses:

- `aligned`;
- `partial`;
- `notation drift`;
- `assumption mismatch`;
- `dangling reference`;
- `appendix orphan`;
- `duplicate`;
- `misallocated`.

## Notation alignment audit

Check:

- identical symbols denote identical objects;
- origin and destination indices retain the same orientation;
- transposes and matrix dimensions agree;
- baseline, fitted, exact, and counterfactual objects retain their adornments;
- hats, tildes, bars, and superscripts are used consistently;
- the appendix does not introduce a new normalization without translating it;
- theorem numbering and equation references are correct;
- a symbol is not reused for a different parameter in another appendix without warning.

When notation must differ, provide a dictionary near the beginning of the appendix.

## Assumption alignment audit

Identify every assumption used in the appendix proof and classify it:

- stated in main text;
- stronger than main text;
- special-case restriction;
- technical regularity condition;
- implementation assumption;
- previously unstated.

Flag any previously unstated assumption that does substantive work. Either move it to the main text, weaken the appendix result, or narrow the main-text claim.

## Duplication audit

Duplication is justified only when the main text gives a short, readable derivation and the appendix supplies the complete proof. Flag:

- two appendices deriving the same result with no difference in purpose;
- a main-text subsection repeating appendix algebra at nearly full length;
- a result restated several times with slightly different notation;
- robustness details repeated in both notes and prose;
- alternate closures interleaved with the headline derivation rather than collected.

Recommend a single authoritative owner and cross-reference it.

## Appendix orphan audit

An appendix subsection may be orphaned if:

- no main-text claim cites or uses it;
- its purpose is not stated;
- it introduces a substantial extension absent from the paper’s framing;
- it proves a result that is never invoked;
- it uses incompatible notation;
- it reads like an abandoned branch from an earlier draft.

Recommend:

- integrate into the main text;
- connect with an explicit main-text reference;
- merge with another appendix subsection;
- move to an online supplement;
- remove.

## Technical-detail relocation test

Move material out of the main text when all are true:

1. the result can be understood and used without the full derivation;
2. the detail interrupts the main spine;
3. the detail is multi-step, special-case, or robustness-oriented;
4. a precise main-text summary and appendix reference can preserve interpretation.

Keep or restore material to the main text when any are true:

1. it motivates the central result;
2. it defines an object used repeatedly;
3. it states an assumption that changes interpretation;
4. it explains the mechanism;
5. the result otherwise appears unsupported;
6. a reader would need the detail to distinguish fitted, causal, structural, or calibrated objects.

## Mathematical correctness in appendices

For each appendix derivation:

- trace the starting equation;
- check each substitution or theorem invocation;
- verify dimensions and signs;
- identify regularity conditions;
- check numbering and cross-references;
- compare the endpoint with the main-text formula;
- test special cases or numerical examples when useful;
- verify computational formulas against code when available.

Do not certify the entire appendix as correct merely because the endpoint resembles the main-text equation. Report the level of verification performed.
