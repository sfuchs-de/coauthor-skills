# Finding Severity

Use severity to rank mathematical risk, not prose style.

## Severity Levels

| Severity | Meaning | Typical action |
| --- | --- | --- |
| S0 Blocker | A central theorem, estimator, or conclusion is mathematically false as stated, or a proof relies on an invalid step that reverses the result. | Correct before relying on the note. |
| S1 Major | A derivation has a sign/coefficient/normalization/order error, a missing assumption needed for the result, or a strong inference claim not supported by the setup. | Patch or qualify before circulation. |
| S2 Moderate | The claim is likely correct under additional conditions, but the draft omits important domains, edge cases, boundedness, generated-regressor, or normalization details. | Add qualifications or proof detail. |
| S3 Minor | Local notation, wording, reference, or presentation could mislead a careful reader but does not change the mathematical conclusion. | Fix when editing. |
| Info | Useful observation, optional robustness check, or nonblocking clarification. | Optional. |

## Verdicts

Use exactly these verdict labels in the proof notebook:

- `Verified`: The claim follows under stated assumptions.
- `Verified with qualification`: The claim follows after adding explicit conditions or
  reading an implicit convention in a specific way.
- `Needs correction`: The statement or derivation is wrong as written.
- `Not established`: The statement may be true, but the provided assumptions/proof do not
  establish it.
- `Not checked`: The audit did not verify the claim; explain why.

## Reporting Standard

Every finding should include:

| Field | Standard |
| --- | --- |
| Severity | S0, S1, S2, S3, or Info. |
| Status | `INVALID`, `UNJUSTIFIED`, `UNDERSTATED`, `OVERSTATED`, or `UNCLEAR`. |
| Impact | `GLOBAL`, `LOCAL`, or `COSMETIC`. |
| Category | Algebra/sign, coefficient/power, indexing, normalization, approximation/order, side condition, theorem application, stochastic claim, statistical object, notation, or other precise class. |
| Evidence type | `explicit`, `inferred`, `contradicted`, `missing`, `ambiguous`, or `rejected-instruction`. |
| Source support | `source-supported`, `auditor-derived`, `unsupported`, or `not-applicable`. |
| Verification pass | Independent derivation, deterministic command, source match, side-condition discharge, or reason no tool check applies. |
| Residual uncertainty | Remaining ambiguity, author judgment, missing source, or `None`. |
| Source | File and line or line span. |
| Issue | The exact mathematical problem. |
| Why it matters | Consequence for the result, estimator, or reader interpretation. |
| Recommended correction | Minimal mathematical repair or qualification. |
| Patch? | `Yes`, `No`, or `Author judgment`. |

Do not inflate severity for missing exposition. Escalate severity when the missing condition
changes the truth of a theorem, the sign of a comparative static, the order of an
approximation, or the interpretation of an estimator.

## Status Labels

- `INVALID`: The statement is false as written or a proof step is mathematically invalid.
- `UNJUSTIFIED`: The statement may be true, but the assumptions or proof do not establish it.
- `UNDERSTATED`: The result needs stronger or more explicit assumptions, domains, or
  qualifications.
- `OVERSTATED`: The draft claims equality, exactness, generality, rate, or inference strength
  beyond what the derivation supports.
- `UNCLEAR`: Notation, quantification, object definition, or source scope is too ambiguous to
  classify without author input.

## Impact Labels

- `GLOBAL`: Affects a central theorem, estimator, conclusion, or downstream results.
- `LOCAL`: Affects a bounded derivation, lemma, equation, or explanatory claim.
- `COSMETIC`: Misleading notation or presentation with no apparent mathematical effect.
