# Comment Fairness Audit

Use this pass when evaluating a generated referee report, comparing it to another system, or checking whether comments are fair to the manuscript.

## Unit Of Review

Score each substantive report comment separately:

- Overall evaluation claims that make a judgment about the paper.
- Each major comment.
- Each minor comment, except purely mechanical typo lists if they were already exact-quote verified.

## Scoring Scale

- `5`: Accurate, manuscript-supported, important, and phrased at the right level.
- `4`: Fair and useful, but lower priority or requiring some nuance.
- `3`: Plausible but under-supported, overstated, or too generic.
- `2`: Weak fit to the manuscript.
- `1`: Unfair, contradicted by the paper, or based on invented information.

## Required Checks

For every comment, record:

1. `Restatement`: one sentence describing the criticism.
2. `Score`: 1-5.
3. `Verdict`: keep, revise, demote to minor, defer for verification, or drop.
4. `Manuscript support`: compact section/table/figure/appendix anchor; use page numbers only when necessary.
5. `Fairness assessment`: explain whether the comment accurately reflects what the paper does and does not do.
6. `Revision needed`: exact edit if the comment is overstated or under-anchored.
7. `Primary request`: the single action required from the authors.
8. `Resolution threshold`: the evidence or qualification that would close the concern.
9. `Burden`: text-only, small-check, new-analysis, new-data, or new-model.

## Rules

- Do not reward a comment merely because it is conceptually plausible. It must fairly apply to the manuscript.
- Penalize comments that ask for analyses the paper already provides, unless the criticism is that the analysis is hard to find or under-integrated.
- Penalize comments that rely on exact quotes or numerical claims that have not been verified.
- Penalize comments that are generic robustness requests rather than targeted fixes.
- Prefer revising an overstated but useful comment over dropping it.
- Score below 4 if a comment bundles cumulative requests, lacks a resolution threshold, or treats an
  optional extension as necessary without showing that the paper's claim fails.
- For revision rounds, penalize reopening a resolved concern unless the revision created a new
  problem or the concern is necessary to evaluate a still-open claim.
- After revisions, re-score the report against `report_quality_rubric.md` and compare the score with the benchmark output.

## Output

Save the audit as a Markdown table with columns:

`Report comment | Score | Verdict | Manuscript support | Fairness assessment | Primary request | Resolution threshold | Burden | Revision needed`

End with:

- Mean score for major comments.
- Mean score for minor comments.
- Overall mean score.
- List of comments revised or dropped.
- Whether the report remains stronger than the benchmark comparator.
- Whether every retained major comment scores at least 4/5.
