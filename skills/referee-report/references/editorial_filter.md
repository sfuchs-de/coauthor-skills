# Referee Report Editorial Filter

Use this filter before triage and final drafting. Read `comment_contract.md` first.

## 1. Section Coverage Harvest

Before choosing major comments, scan the manuscript by functional section:

- Introduction and contribution: novelty, closest predecessors, claimed contribution.
- Theory/framework: assumptions, comparative statics, mapping to observables.
- Data and measurement: sample, unit construction, outcome/proxy validity, missingness.
- Empirical design: estimand, identifying variation, assumptions, diagnostics.
- Results and robustness: main estimates, specification sensitivity, falsification checks.
- Mechanisms: whether mechanism evidence is local, contemporaneous, and uniquely supportive.
- Discussion/conclusion: whether extrapolation is warranted.

Create many candidate concerns internally, but keep only those that affect contribution, core validity, interpretation, external validity, measurement, mechanisms, theory closure, or quantification.

Before prioritizing, run one compact implementation sweep. Check the unit of observation and risk
set; geographic and temporal aggregation; category filters, duplicates, and missing values;
concordances and generated-variable construction; coefficient units and economically relevant
treatment movements; and whether a proposed mechanism is measured at the same level and is actually
a mediator rather than a parallel outcome. These details remain minor unless they change the
estimand, identifying variation, or interpretation of a headline result.

For empirical papers, complete `empirical_design_preflight.md` before scoring candidate concerns.
Do not allow a contribution discussion or a long robustness list to displace a more basic failure
to identify what the headline coefficient compares.

## 2. Scope And Comment Scoring

Apply the extension filter before scoring. Record whether an omission overturns the claim, changes
its material magnitude, limits interpretation, or is only an optional extension.

Score each candidate concern internally:

- `3`: central enough for a major comment and paired with a proportionate primary request.
- `2`: useful but secondary; consider minor comment or sentence inside a major comment.
- `1`: presentation-only or already addressed by the paper.
- `0`: generic, unsupported, or not suitable for a referee report.

Drop all `0` items. Do not include a concern merely because it is common in the literature; include it only if it applies to this manuscript or is a clear interpretive risk.

For each retained major concern, verify one primary request and one resolution threshold. Treat
alternative implementations as substitutes. A new-model or new-data request requires an explanation
of why a qualification or small check cannot resolve the problem.

## 3. Anchor Verification

Before final output:

- Verify every quoted phrase against the manuscript text.
- Verify every numerical claim against the manuscript table/figure/section.
- Replace excessive page anchors with section/table/figure anchors when the location is not the point.
- If a claim cannot be verified, remove it or label it as an uncertainty.

## 4. Editorial Deduplication

Merge comments that share the same underlying issue. Prefer one coherent major comment with several examples over three repetitive comments.

Delete a remedy from `Smaller comments` when it already appears in a major comment.

Drop comments that ask for:

- Generic robustness checks already reported in the manuscript.
- Simulations or worked examples unless they directly test the paper's identifying argument or model.
- Broad policy guidance beyond the paper's feasible scope.
- Heterogeneity analyses unless heterogeneity changes the paper's central contribution or interpretation.
- Optional model extensions that only broaden the paper's domain.
- Multiple robustness checks when one decisive diagnostic would resolve the concern.

## 5. Punchiness Pass

- State the concern in the first sentence of each major comment.
- Cut manuscript summary that the opening already covered.
- Keep one causal chain: assumption or design problem, implication, request.
- Prefer one decisive example to a list of related symptoms.
- End with one direct request in ordinary prose; do not expose the internal comment contract.
- Integrate the request into the final paragraph. Do not repeat a bold `Suggestion` block after
  every comment or force every remedy into the same sentence pattern.
- Allow comments to differ in length. Do not pad a secondary point to match the central one.

## 6. Anti-Slop Pass

Before delivery, remove:

- Formulaic preambles such as "Here are some overall reactions."
- Repeated "this matters because" scaffolding.
- Inflated but vague praise.
- Mechanical lists of generic issues.
- Dense page-reference strings that interrupt readability.

The final report should sound like a careful referee making a small number of high-value points.
