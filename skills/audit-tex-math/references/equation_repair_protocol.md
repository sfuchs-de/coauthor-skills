# Equation Repair Protocol

## Contents

1. Localize the defect and establish authority
2. Build and verify repair candidates
3. Patch rules and deep-repair planning
4. Unrecoverable proofs and second-pass review
5. Patch report

Use this only in patch mode, after the audit has identified a concrete mathematical defect
or a user has explicitly asked for equation fixes. The goal is not to make the equation look
plausible; it is to replace the wrong statement with the nearest correct statement supported
by the document's definitions and assumptions.

## 1. Localize the Defect

Classify the issue before proposing a correction:

| Type | Common symptoms |
| --- | --- |
| Algebra/sign | Wrong sign, missing minus, bad expansion, invalid cancellation. |
| Coefficient/power | Missing factor of 2, wrong exponent, lost denominator, transpose error. |
| Indexing/summation | Wrong index set, double-counting, missing diagonal exclusion, inconsistent time index. |
| Normalization/unit | Share versus level, probability versus count, per-period versus total, normalized utility. |
| Approximation/order | Expansion around wrong point, missing remainder, first-order claim is only heuristic. |
| Domain/assumption | Division by possibly zero term, log of nonpositive value, inverse without rank condition. |
| Statistical object | Population moment, sample analog, estimator, and asymptotic target are conflated. |

If the defect cannot be localized, do not patch. Record the ambiguity and give alternative
candidate repairs.

## 2. Establish the Source of Truth

Before editing, identify the authoritative inputs:

- Definitions and assumptions that determine the equation.
- Earlier equations or labels the expression depends on.
- The object being solved for, differentiated, approximated, estimated, or normalized.
- Which symbols are fixed with respect to the relevant derivative, limit, expectation, or
  summation.
- Whether nearby prose claims exact equality, approximation, asymptotic equivalence, or a
  heuristic relationship.

When definitions conflict, repair the later equation to match the main definition only if
the conflict is local and clear. Otherwise flag author judgment instead of silently choosing.

## 3. Build Repair Candidates

For every proposed equation fix, write a repair candidate before touching the TeX:

| Field | Standard |
| --- | --- |
| Source | File and tight line span. |
| Evidence | Evidence ledger IDs supporting the defect and repair. |
| Current claim | Plain-language statement of the existing equation. |
| Defect | The precise sign/coefficient/index/order/domain problem. |
| Corrected TeX | Minimal replacement TeX, preserving style and labels where possible. |
| Derivation basis | Definitions, assumptions, and equations used to derive the correction. |
| Prose changes | Nearby sentences, theorem statements, or assumptions that must change too. |
| Verification | Symbolic, numerical, limit, dimension, or edge-case check distinguishing old from new. |
| Closure tests | Checks that patched assumptions, theorem statement, downstream labels, and algebra/type sanity all close. |
| Verification loop | Draft repair, independent verification, deterministic check or reason omitted, revised verdict, and residual uncertainty. |
| Confidence | `Patch`, `Patch with qualification`, or `Author judgment`. |

Only apply candidates with confidence `Patch` or `Patch with qualification`. For `Patch with
qualification`, patch the qualification together with the equation.

Use these repair statuses only:

- `PATCHED_VERIFIED`: Edited and independently rechecked.
- `PATCHED_WITH_QUALIFICATION`: Edited with an explicit assumption, approximation, or scope
  qualification.
- `NOT_PATCHED_AMBIGUOUS`: Multiple mathematically plausible repairs remain.
- `NOT_PATCHED_NEEDS_SOURCE`: The document lacks a definition, data source, or assumption
  needed to choose a correction.

## 4. Verify Before Patching

Each patched equation should pass at least one independent check that would fail or differ
for the old equation:

- Re-derive the expression from definitions line by line.
- Simplify both sides symbolically for a small local identity.
- Compare exact and proposed approximate formulas numerically over controlled inputs.
- Check boundary cases such as zero weights, equal shares, inactive edges, singular limits,
  or scalar special cases of matrix formulas.
- Check units/dimensions and adding-up restrictions.
- Compare analytic derivatives to finite differences.
- Confirm approximation order by shrinking the perturbation parameter.

Report checks as diagnostics, not as substitutes for proof.

For any non-trivial arithmetic, symbolic simplification, numerical comparison, derivative
check, or approximation-order check, use Python, SymPy, a spreadsheet formula, or another
reproducible tool. Record the exact command, script path, seed/input values, tolerance, and
result in the audit notebook. Prefer `scripts/math_check.py` for scalar numerical equality
checks, finite-difference derivative checks, and optional SymPy identities. Do not mark a
repair verified from mental arithmetic alone.

## 5. Patch Rules

- Make the smallest TeX edit that fixes the mathematics.
- Preserve equation labels and cross-references unless the label points to the wrong object.
- Patch dependent prose, assumptions, theorem statements, and later references in the same
  pass when they would otherwise become false.
- Keep exact equalities, approximations, and asymptotic notation distinct. Do not turn an
  unsupported equality into another unsupported equality; use `\approx`, `= ... + O(...)`,
  `o_p(...)`, or a qualified statement when that is the true claim.
- Do not hide uncertainty in wording. If multiple repairs are mathematically plausible, list
  them and leave the TeX unchanged unless the user chooses one.
- Re-run the TeX build when possible and check for broken labels, syntax errors, and serious
  warnings introduced by the patch.

## 6. Deep Repair Plan

For theorem/proof repairs or central equation repairs, write a deep repair plan before
editing:

| Field | Standard |
| --- | --- |
| Corrected statement | Exact revised theorem, lemma, proposition, or equation in mathematical prose. |
| Before/after equations | Current TeX and replacement TeX for every changed display. |
| Added/changed assumptions | Minimal assumptions required and where they will be inserted. |
| Downstream labels | Labels, references, and later claims affected by the repair. |
| Minimal TeX patch plan | File/line targets and the smallest coherent set of edits. |
| Closure tests | Independent derivation, `math_check.py` command, side-condition discharge, and downstream-reference review. |
| Algebra/type sanity | Dimensional compatibility, domains, positivity/rank conditions, and quantifier scope. |

Only implement the repair if the closure tests are concrete enough to distinguish a real
fix from a cosmetic rewrite.

## 7. Unrecoverable-Proof Protocol

If no repair can honestly close the proof under the available assumptions, do not force a
patch. Report:

| Field | Standard |
| --- | --- |
| Blocking issue | The false statement, missing assumption, circular dependency, or invalid theorem application. |
| Failed repair attempts | Candidate repairs considered and why they fail or require author judgment. |
| Salvage options | Weaker theorem, local lemma, conditional result, numerical diagnostic, or removal path. |
| Reusable parts | Definitions, derivation fragments, lemmas, or checks that remain valid. |
| Author decisions needed | New assumption, theorem weakening, model change, empirical caveat, or proof rewrite. |

Mark the repair status `NOT_PATCHED_AMBIGUOUS` or `NOT_PATCHED_NEEDS_SOURCE`, and mark
downstream dependent claims as residual risk.

## 8. Second-Pass Review

After patching, re-audit the edited equation as if it were new:

- Re-run `scripts/extract_tex_math.py` on every touched TeX file.
- Check that the patched equation still matches its source definitions and assumptions.
- Check downstream equations and prose that reference the patched label.
- Re-run the distinguishing verification check against the patched TeX.
- Confirm the final statement is exact, approximate, asymptotic, or qualified in the correct
  way.

If the second pass changes the repair, patch again and repeat this review for that equation.

## 9. Patch Report

After editing, report:

| Field | Standard |
| --- | --- |
| Patched lines | File and line span after the edit. |
| Mathematical change | What changed in the equation and why. |
| Evidence | Source evidence and evidence type supporting the change. |
| Verification used | Independent derivation or diagnostic check. |
| Commands/scripts | Exact commands, scripts, seeds, inputs, and tolerances used for verification. |
| Dependent edits | Assumptions, prose, labels, or later equations updated. |
| Second-pass status | `PATCHED_VERIFIED`, `PATCHED_WITH_QUALIFICATION`, `NOT_PATCHED_AMBIGUOUS`, or `NOT_PATCHED_NEEDS_SOURCE`. |
| Residual risk | Any remaining ambiguity or author judgment. |
