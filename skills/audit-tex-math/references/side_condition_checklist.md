# Side-Condition Checklist

Use this reference when a proof invokes a theorem, asymptotic step, interchange operation,
convexity inequality, matrix fact, or stochastic convergence claim. The goal is to verify
the proof obligations that are often hidden by phrases like "standard arguments imply" or
"by regularity".

## Theorem Applications

For each theorem application, record:

| Field | Standard |
| --- | --- |
| Source lines | Tight line span of the invocation. |
| Theorem/rule used | Named theorem, lemma, inequality, or implicit rule. |
| Inputs | Objects to which the rule is applied. |
| Required hypotheses | Conditions needed by the rule. |
| Discharge status | `DISCHARGED`, `MISSING`, `PARTIAL`, or `NOT_APPLICABLE`. |
| Consequence | Exact statement obtained from the rule. |

## Common Side Conditions

| Step | Conditions to check |
| --- | --- |
| Dominated convergence | Pointwise convergence, measurable functions, integrable dominating function independent of limit index. |
| Monotone convergence | Nonnegative measurable functions and monotone sequence. |
| Fubini/Tonelli | Integrability for Fubini; nonnegativity or sigma-finiteness conditions for Tonelli. |
| Differentiating under integral/expectation | Differentiability, neighborhood domination of derivative, support not moving unless boundary terms are handled. |
| Taylor expansion | Expansion point, differentiability order, residual form, uniformity region, small parameter, bounded derivatives. |
| Implicit function theorem | Function class, zero condition, nonsingular Jacobian, neighborhood and uniqueness statement. |
| Jensen | Convexity/concavity direction, integrability, correct conditioning/sigma-field. |
| Cauchy-Schwarz/Holder | Correct norm space, integrability powers, nonnegative or absolute-value handling. |
| Matrix PSD/order | Symmetry, conformable dimensions, PSD assumptions, rank/invertibility, operator norm compatibility. |
| WLOG reduction | Symmetry or invariance that preserves all cases, and explicit map back to general case. |
| Big-O/little-o | Limit variable, deterministic versus stochastic order, pointwise versus uniform order, constants independent of required indices. |
| Stochastic convergence | Mode (`a.s.`, `p`, `d`, `L_p`), tightness/uniformity, generated-regressor and sample-splitting issues. |
| CLT/LLN | Independence/mixing, moment bounds, triangular-array conditions, normalization, variance nondegeneracy. |

## Limit and Order Map

For every proof with limits, asymptotics, or approximations, record:

| Field | Standard |
| --- | --- |
| Limit index | `n`, `T`, `h`, `\epsilon`, grid size, bandwidth, etc. |
| Object | Sequence, estimator, residual, approximation, or stochastic process. |
| Claimed order | `O`, `o`, `O_p`, `o_p`, convergence mode, or rate. |
| Uniformity | Pointwise, uniform over set, conditional, or unspecified. |
| Dependencies | Moment bounds, smoothness, compactness, positivity, rank, sparsity, or mixing. |
| Verified? | `Yes`, `Qualified`, `No`, or `Not checked`. |

## Acceptance Gate

Before marking a theorem or proof verified:

- Every named or implicit theorem application has a theorem-application ledger row.
- Every substantive verdict has evidence ledger support.
- Every nontrivial side condition is discharged, qualified, or listed as residual risk.
- Every hidden regularity condition needed for the conclusion appears in the statement,
  assumptions, or patch recommendation.
- Every limit/order claim identifies the limit index and uniformity level.
- Every verified theorem/equation has independent verification plus a reproducible check, or
  an explicit reason no tool check applies.
- Downstream conclusions are marked unsupported if an upstream obligation is missing.
