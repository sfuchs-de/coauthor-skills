# Proof and Derivation Protocol

## Purpose

Construct a complete candidate argument whose assumptions, dependencies, and nontrivial steps are
visible enough for independent verification. Calibrate elementary detail to the audience rather
than mechanically expanding every operation.

## Workflow

1. Restate exactly what must be shown, including domain, quantifiers, parameter restrictions, and
   local/global or exact/approximate scope.
2. Inventory definitions and prior results. Verify that each cited result is available and that its
   conditions match the current setting.
3. Name a proof strategy and list the obligations it creates before beginning algebra.
4. Proceed in dependency order. Define intermediate objects before use and keep indices,
   dimensions, conditioning sets, and normalization visible.
5. Justify each nontrivial equality, inequality, sign, limit, derivative, inversion, fixed-point
   step, or theorem application. Show intermediate algebra when omitting it would force the target
   reader to reconstruct the argument.
6. Separate cases explicitly and check boundary, degenerate, and limiting configurations.
7. Add intuition after the formal step it explains. Keep the intuition literally consistent with
   the proof; do not use “dominates,” “clearly,” or a monotonicity claim without support.
8. Verify the conclusion against the original target and list any condition not supplied by the
   source.

## Common patterns

- For ratios or logs, state positivity and nonzero-denominator conditions before differentiation.
- For chains through distributions, state continuity, differentiability, support, and density
  conditions actually used.
- For inequalities, record sign conditions before multiplying, dividing, or reversing order.
- For induction, state the base case, induction hypothesis, and exact induction step.
- For discrete and continuous formulations, do not transfer derivatives, sums, or measure-zero
  claims without a separate argument.
- For examples or numerical checks, state that they are diagnostics rather than a general proof.

## Deliverable

Give the proof or derivation in the source's native notation and format. End with assumptions used,
edge cases checked, unresolved obligations, and the label `candidate / unverified` until a separate
audit closes the argument.
