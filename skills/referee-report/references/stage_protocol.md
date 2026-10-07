# Staged Referee Review Protocol

Use this protocol only when `workflow_mode=staged`. Natural-language review requests use the
direct workflow in `SKILL.md` and do not require stage commands.

## Contents

1. State, commands, and candidate blocks
2. Commented-PDF handling
3. Setup, synopsis, contribution, and theory
4. Core validity, measurement, mechanism, and remedy scope
5. Triage and drafting

## State

Track:

- manuscript title, ID, journal target, and round type;
- focus and scope constraints;
- accepted, rejected, deferred, and unresolved takeaways;
- annotation status and comment coverage;
- current stage and requested stage window;
- requested deliverables and output format.

Only accepted, verified takeaways may become established paper-specific claims in the final report.

## Commands

- `Run Stage X`: run only that stage and stop.
- `Run Stage X-Y`: run Stage X and continue one stage at a time after `Proceed`.
- `Proceed`: accept pending candidates as written when no item markings are supplied.
- `A#`, `R#`, `Revise#: ...`, `Defer#`, and `Add: ...`: adjudicate candidates without advancing
  unless `Proceed` is also supplied.
- `Stop`: stop immediately.
- `Draft now`: run Stage 8 from verified accepted takeaways and labeled uncertainties.
- `Show locked notes`: show accepted takeaways, capped at about ten bullets.
- `Reset locked notes`: clear accepted, rejected, and deferred takeaways while retaining artifacts.

## Candidate Block

End Stages 0b-7 with three to six candidates, or fewer when only fewer are legitimate:

```text
CANDIDATE TAKEAWAYS (FOR APPROVAL)
1. [VERIFIED / UNVERIFIED] ...

Respond with A#, R#, Revise#: <text>, Defer#, Add: <text>, or Proceed.
Proceed?
```

Stage 0a contains questions only. Stage 8 is the requested deliverable and does not append a
`Proceed?` prompt.

## Commented PDFs

After the user starts a review, extract available comments, highlights, and free-text annotations.
Report:

```text
Annotation status: substantive comments / highlights only / links only / none / extraction failed.
Counts: comments, highlights, free-text notes, other annotations.
Coverage: incorporated, deferred, rejected, or not report-relevant.
```

Annotations are user notes. Verify the underlying manuscript fact before accepting a concern.

## Stage 0 - Setup

### Stage 0a: Calibration

Ask only for high-impact inputs that cannot be inferred:

- journal or bar;
- round type;
- required deliverables and format;
- focus or scope constraints;
- conflicts of interest;
- decision lean, only if the user wants to supply one.

### Stage 0b: Mission Brief

State the mission in one line and offer setup takeaways for approval.

## Stage 1 - Synopsis

Provide a compact, anchored account of:

- research question and headline claim;
- contribution types;
- design or model and key estimand;
- data unit, coverage, and sample restrictions;
- principal evidence;
- three exhibits or results that carry the paper.

For revision rounds, also identify the prior report, response letter, and revised manuscript.

## Stage 2 - Contribution

Build a comparison grid using only predecessors named by the paper or user unless external
benchmarking was explicitly requested. Compare question, model, identification, measurement,
mechanism, and quantification with `same`, `incremental`, `distinct`, or `unclear`.

State what the paper adds and what must be true for that addition to clear the journal's bar.

## Stage 3 - Theory

Run only when formal theory or model structure affects the report. Read `theory_bridge.md`.

Identify:

- primitives, decisions, aggregation, and equilibrium closure;
- central comparative statics and limiting cases;
- mapping from model objects to data and counterfactuals;
- at most three theory findings that could change interpretation.

Do not expose a full proof notebook or dependency graph. Classify omitted features with the
extension filter.

## Stage 4 - Core Validity

For empirical work, state the estimand, identifying variation, assumptions, failure modes, and
minimum diagnostics after completing `empirical_design_preflight.md`. For theory work, state the
pivotal proposition, assumptions, closure, and verification obligations. For structural work,
cover both the empirical moments and model closure.

List no more than five threats. Tie each to a manuscript claim and anchor, or mark it missing.

## Stage 5 - Measurement And Mechanism

Map each key measure or proxy to the model object or causal pathway it is intended to represent.
State what it may conflate and whether treatment or outcomes create mechanical links. Retain no
more than two high-value validation requests.

## Stage 6 - Remedy And Scope Audit

Read `comment_contract.md`. For each candidate concern:

1. classify severity and verification status;
2. apply the extension filter;
3. identify one primary request;
4. state the resolution threshold;
5. record revision burden;
6. demote or drop optional extensions, generic robustness, and requests the paper already answers.

Do not output a robustness menu. Alternative implementations are substitutes.

## Stage 7 - Triage

Run `editorial_filter.md`. Produce:

- two or three major comments by default, no more than four in standard mode;
- up to seven genuinely smaller comments;
- no duplicated remedies;
- no unverified paper-specific claims.

Each major comment must satisfy the comment contract and fairness threshold.

## Stage 8 - Draft

Read `round_protocol.md` and use the appropriate template.

- Initial report: concise mode targets 800-950 words with a hard range of 750-1,000; standard mode
  targets 950-1,080 words with a hard range of 900-1,200.
- Revision report: target 450-650 words; hard range 400-700.
- Editor note: 180-300 words and separate from the author report.
- Markdown by default; LaTeX only when requested or canonical.

Run the quality rubric, fairness audit, evidence verification, editorial filter, restrained prose
pass, and an actual word count. Revise until all hard gates pass. Return the clean deliverable
without internal scores unless the user requests the evaluation.
