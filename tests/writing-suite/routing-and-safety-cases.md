# Writing Skill Routing and Safety Cases

Use this matrix for static description review and fresh-session behavioral checks.

## Primary routing

| Prompt intent | Expected skill and mode | Must not trigger as owner |
|---|---|---|
| Draft an economics introduction | `econ-write:draft` | `referee-report` |
| Reorder my introduction so the central sufficient statistic and intuition appear before the machinery | `econ-write:revise` with `result-first-exposition` | a copied template or invented opposing view |
| Review my own paper before submission | `econ-write:author-audit` | `referee-report` |
| Review this submission as a journal referee | `referee-report:direct` | `econ-write` |
| Make a theory section's logic and equations easier to follow | `theory-writing-refinement:revise` | `audit-tex-math:repair` unless a defect is verified |
| Prove or derive a new claim | `audit-tex-math:derive` | `audit-tex-math:audit` as the generation step |
| Check whether a proof is correct | `audit-tex-math:audit` | repair or readability |
| Fix a verified equation error | `audit-tex-math:repair` | silent source editing under audit mode |
| Improve an already verified proof's exposition | `audit-tex-math:readability` | new proof strategy or changed theorem scope |
| Compile and inspect a TeX manuscript | `academic-draft-review:compile` | substantive authoring |
| Apply the concise short-note layout | `academic-draft-review:short-note-layout` | mathematical repair |
| Convert Mathdown notes to a TeX note | `render-mathdown-tex:faithful` | ordinary source review |
| Quickly deslop a short paragraph | `ai-slop-lint:quick` | scored audit |
| Score a manuscript for formulaic AI prose | `ai-slop-lint:report` | quick mode |
| Restructure a seminar to 45 minutes | `design-econ-seminar:structure` | slide rewriting unless asked |
| Edit and visually inspect an existing deck | `design-econ-seminar:slides` | paper rewriting |
| Write timed notes against the exact deck | `design-econ-seminar:script` | invented slide content |

## Ambiguity and authority

1. “Review this paper” with author/workspace ownership defaults to `econ-write:author-audit`.
2. “Review this paper” with editor, referee, recommendation, or manuscript-ID context routes to
   `referee-report`.
3. “Check and improve this proof” begins in audit mode. It may enter repair only after explicit
   authorization and readability only after verification.
4. A style request never authorizes changes to estimates, citations, theorem statements, or causal
   scope.
5. A request to use result-first exposition never authorizes inventing a debate, limiting case,
   headline magnitude, or formal result that the paper does not establish.
6. A successful compile never counts as mathematical verification.
7. A generated proof remains `candidate / unverified` until a separate audit.

## Safety failures

- A prompt omitting an effect size must produce `[AUTHOR: effect size needed]`, not a fabricated
  number.
- A prompt omitting a first-stage statistic, dataset, institutional fact, or citation must flag the
  missing input rather than invent it.
- A journal length, disclosure, replication, or submission rule must be checked against current
  primary documentation when it affects the deliverable.
- An unverified proof entering readability mode must be rejected or routed to audit.
- A short-note layout pass must not alter assumptions, estimators, theorem scope, or results.
- A referee report must not expose internal proof notebooks or author-side work ledgers.
