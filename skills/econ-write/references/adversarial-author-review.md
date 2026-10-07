# Adversarial Writing and Reasoning Review

## Contents

- Stance and claim ledger
- Adversarial questions and severity
- Repair standard and final red-team pass

## Stance

Use this as an internal author-side red team, not an independent publication recommendation. Read as
a skeptical but fair top-field-journal referee, seminar discussant, or mathematical reader. Do not
supply missing steps on the author's behalf. Do not manufacture objections for effect. Focus on
places where the manuscript's wording, ordering, or derivation invites a reasonable misreading or
fails to earn a claim.

## Claim ledger

For each central claim, record:

| Claim ID | Location | Exact claim | Premises | Derivation or evidence | Conditions | Strongest fair alternative reading | Severity | Repair |
|---|---|---|---|---|---|---|---|---|

Central claims include:

- contribution claims;
- theorem and proposition claims;
- identification claims;
- coefficient interpretations;
- welfare statements;
- calibration claims;
- robustness claims;
- policy conclusions;
- generality and external-validity claims.

## Adversarial questions

### Reasoning chain

- Does each conclusion follow from the immediately preceding premises?
- Is an essential intermediate object missing?
- Does “therefore” conceal an additional assumption?
- Does the paper use the same word for different objects?
- Does the argument change scale—from household to city, local to global, or partial to general equilibrium—without a bridge?
- Is the reader expected to recall an earlier condition that is no longer visible?
- Does a branch return to the headline argument?

### Mathematical exposition

- Is the result motivated before notation appears?
- Are all objects defined before use?
- Is the stated derivation route accurate?
- Does each equality have a justification?
- Are dimensions, signs, and normalizations consistent?
- Is a matrix result being reduced to a scalar without the required restrictions?
- Is an eigenmode or homogeneous special case carrying general rhetoric?
- Is a local derivative used for a large counterfactual?
- Is a stability, rank, or invertibility condition merely asserted?
- Does the appendix prove the same statement the main text claims?

### Empirical interpretation

- Is a fitted value called an income, price, or welfare response without the required mapping?
- Is a projection coefficient called a structural elasticity?
- Is shock exogeneity conflated with a response-span restriction?
- Is identification variation distinguished from the network mapping applied to that variation?
- Is a reduced form treated as observed realized spending when it is an instrument-based exposure?
- Are direct, zero-th-round, full-response, and tail regressors scaled consistently?
- Are standard errors, calibration uncertainty, and numerical uncertainty kept distinct?
- Are descriptive figures used as causal evidence?

### Model comparison and policy

- Does the quantitative model reproduce the empirical margins the policy argument relies on?
- If not, is the division of labor between reduced form and model stated positively and precisely?
- Are policy levels conditional on unestimated elasticities, ownership, or factor accounts?
- Does the policy result require curvature that the local model does not supply?
- Are welfare, revenue, tax-base expenditure, visitor counts, and gross tourist payments distinguished?
- Does a linear ranking get described as a feasible tax rate?

### Main text and appendix

- Is an essential assumption buried in a footnote?
- Does an appendix introduce stronger assumptions than the main text admits?
- Does the target appendix subsection actually deliver the promised derivation?
- Is notation translated?
- Is a substantial appendix branch absent from the paper’s framing?
- Is the same result duplicated in several places with slight differences?

### Prose and rhetoric

- Does the wording overclaim novelty, generality, exactness, causality, robustness, or structural interpretation?
- Is a caveat framed so defensively that the positive result disappears?
- Does the paper repeatedly restart its contribution?
- Are generic transitions standing in for missing logic?
- Are important results followed by mere paraphrase rather than interpretation?
- Does the conclusion introduce new claims?

## Severity

### Blocking

The paper’s stated reasoning does not establish the claim, a key derivation fails, or a main-text and appendix mismatch changes the result.

### Major

The claim may be correct, but an essential bridge, condition, definition, or interpretation is missing. A careful reader could reasonably reject or misread the claim.

### Moderate

The logic is recoverable, but ordering, terminology, repetition, or excessive technical detail obscures it.

### Minor

Local wording, transition, notation, formatting, or integration issue.

## Repair standard

Every adversarial finding must include:

1. exact location;
2. claim or transition under review;
3. missing premise, ambiguity, or overreach;
4. why a skeptical reader would object;
5. minimal repair;
6. stronger structural repair if the problem is not local;
7. whether the issue affects substance or only exposition.

Avoid comments such as “needs more intuition” or “unclear.” Specify which term lacks interpretation, which step is missing, and what sentence or derivation should be added.

## Final red-team pass after revision

Read only the revised text, not the revision memo, and ask:

- Can the central spine be stated without filling a gap?
- Does each section opening inherit a specific object?
- Does each central equation have motivation, definitions, derivation, interpretation, and use?
- Are all strong labels earned?
- Do the conclusion and abstract preserve scope?
- Are any essential caveats now hidden by smoother prose?
- Did moving detail to the appendix remove an indispensable premise?
- Did line editing introduce a change in meaning?
- Does any AI-like phrasing remain?

Report all remaining blocking and major issues. Do not declare the manuscript “fully coherent” unless the review actually supports that conclusion.
