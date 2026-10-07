# Mathematical Result Protocol

## 1. Result card

Create a result card for each central equation, lemma, proposition, or corollary:

| Field | Required content |
|---|---|
| Question | Economic or mathematical problem solved |
| Incoming results | Earlier equations or claims used |
| New objects | Symbols, indices, units, domains, and timing |
| Assumptions | Interior, positivity, regularity, convergence, and closure conditions |
| Operation | Definition, substitution, aggregation, differentiation, inversion, IFT, or computation |
| Statement | Exact displayed result |
| Economic meaning | Mechanism, incidence, ranking, or comparative static |
| Mathematical scope | Sign, normalization, exact/local status, limiting cases |
| Appendix anchor | Exact proof or derivation location |
| Next use | Later equation, estimation, or policy exercise |

If several fields are empty, the result is probably under-motivated or overpromoted.

## 2. Substitution chains

Prefer a visible chain when a result follows from previous equations:

1. State the target object.
2. Cite the equation that defines it.
3. Substitute the relevant earlier expressions one at a time.
4. Identify cancellations or normalizations.
5. state the condition under which denominators or inverses are valid.
6. End at the displayed result using the same notation as the proposition.

Do not write "combining the equations yields" when the combination hides the substantive step.
Show the pivotal substitution in the main text or the full chain in the appendix.

## 3. Name the actual derivation

Classify the route to a result accurately:

- **Definition:** a restatement after notation is introduced.
- **Accounting identity:** follows from adding or reallocating exhaustive components.
- **Substitution:** replaces objects using earlier equalities.
- **Aggregation:** sums or integrates individual conditions with stated weights.
- **Envelope argument:** removes indirect responses under an optimum and specified welfare
  aggregation.
- **First-order condition:** follows from optimizing behavior; state the choice and constraint.
- **Fixed-point result:** follows from a map and a condition such as contraction or existence.
- **Implicit-function result:** differentiates a residual system and requires a nonsingular
  Jacobian.
- **Approximation:** truncates an expansion; state the expansion point and order.
- **Numerical construction:** computed from calibrated inputs; do not present it as an analytical
  theorem.

## 4. Before and after a display

Before:

- explain why the equation is needed now;
- define every new symbol;
- identify units or normalizations that affect interpretation.

After:

- explain the central equality or inequality;
- identify the term that carries the economic mechanism;
- state how the equation is used next.

Routine intermediate equations do not need a full paragraph. Central equations do.

## 5. Main text, footnote, or appendix

Keep in the main text:

- the policy question;
- primitives and state variables needed to understand the result;
- the central equation or proposition;
- economic interpretation and scope.

Use a footnote for:

- a short convention;
- a secondary qualification;
- a compact limiting case or citation;
- a detail that does not alter the argument.

Use an appendix for:

- multi-line substitutions;
- Jacobian blocks and index bookkeeping;
- existence, uniqueness, or regularity proofs;
- alternative closures and robustness derivations;
- computational algorithms and verification details.

## 6. Main-text/appendix handshake

Audit both directions:

**Main to appendix**

- Does the main text point to an exact label?
- Does it state what the appendix proves?
- Does it avoid claiming more than the appendix establishes?

**Appendix to main**

- Does the appendix begin with the same primitives and shock?
- Are signs, indices, normalizations, and units identical?
- Does the last proof line reproduce the main-text formula?
- Are technical aliases reconciled with reader-facing terms?
- Are assumptions in the appendix visible where the main result is stated?

## 7. Adversarial mathematical exposition

Ask:

- Could the displayed sign reverse under an unstated parameter restriction?
- Is a share being used where a level or normalized flow is required?
- Is the derivative with respect to a realized object or a primitive policy?
- Is the result local while the prose implies a finite or global effect?
- Does a matrix inverse require a condition that is absent?
- Does the economic interpretation depend on two signed terms rather than one?
- Is an efficient-envelope result being extended to an inefficient setting without another term?
- Does the appendix prove the result for the same closure used in the application?

If any answer is uncertain, flag the issue and invoke `$audit-tex-math` before rewriting it as a
settled conclusion.
