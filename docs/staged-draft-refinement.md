# Staged Draft-Refinement Workflow

Use this workflow to refine a substantial economics draft in one Codex task while preserving the
same reasoning graph, source context, and author decisions from stage to stage. Codex should stop at
every checkpoint and wait for an explicit instruction to proceed.

This is an author-side process. Use `econ-write:author-audit` for the diagnosis and revision agenda;
reserve `referee-report` for an optional independent cold review after the author-side work is
complete.

## Governing instruction

Begin the task with this instruction:

> Never advance automatically. At the end of each stage, report the graph layers completed,
> decisions needed from me, unresolved handoffs, and the proposed next stage, then stop. Do not edit
> the manuscript until I approve a revision blueprint.

Keep the process in one Codex task unless context or confidentiality requires otherwise. A new task
should not be expected to recover unrecorded judgments from the earlier stages.

## Workflow at a glance

| Stage | Purpose | Editing authority | Checkpoint |
|---:|---|---|---|
| 1 | Identify the authoritative draft and initialize the graph | None | Confirm sources and scope |
| 2 | Recover and audit the paper's argument | None | Adjudicate the main findings |
| 3 | Run only the necessary specialist audits | None | Approve substantive repairs |
| 4 | Convert approved findings into a revision blueprint | None | Approve batches and protected content |
| 5 | Implement one coherent batch at a time | Approved batch only | Inspect each batch before continuing |
| 6 | Rebuild the graph, compile, and verify | Narrow repairs if authorized | Confirm structural readiness |
| 7 | Perform the final prose pass | Prose only | Confirm no substantive drift |
| 8 | Conduct an optional independent referee review | None unless separately requested | Keep reviewer inference independent |

## Stage 1: Intake and baseline

**Purpose:** Identify the authoritative draft and establish the review scope.

Prompt:

> Use `$econ-writing-suite` on `[path/main.tex]` as a staged author-side refinement workflow.
> Identify the authoritative manuscript root, included files, paper type, intended audience, and
> current build status. Initialize a private reasoning-graph workspace. Do not edit. Report any
> missing inputs and stop after Stage 1.

Expected output:

- manuscript root and source inventory;
- current question, answer, method or mechanism, and contribution;
- missing inputs or ambiguous authority;
- graph-workspace location; and
- proposed scope for the structural audit.

Confirm the authoritative source and requested scope before proceeding.

## Stage 2: Structural reasoning audit

**Purpose:** Determine whether the paper's argument works before editing prose.

Prompt:

> Proceed to Stage 2. Use `econ-write:author-audit` to reconstruct the shortest faithful argument
> spine. Map each section's incoming question, job, output, and handoff. Identify branches, repeated
> launches, orphan results, unsupported conclusions, and scope drift. Return only the five
> highest-value findings, with graph IDs, consequences, and candidate repairs. Do not edit.

At the checkpoint, classify every finding as:

- **Approve:** implement the proposed repair.
- **Modify:** accept the diagnosis but specify a different repair.
- **Defer:** preserve the finding for a later draft.
- **Reject:** retain the existing structure intentionally.
- **Specialist audit:** request theory, mathematical, empirical, or source verification before
  deciding.

Record these decisions in the graph. Do not proceed while a load-bearing finding lacks a disposition.

## Stage 3: Specialist audits

**Purpose:** Investigate only the substantive links that matter for the approved revision agenda.

### Theory or quantitative model

> Proceed to Stage 3A. Use `$theory-writing-refinement` in `map` or `audit-exposition` mode on the
> approved sections. Add primitives, assumptions, equilibrium closure, result dependencies,
> intuition, and appendix mappings to the existing graph. Do not edit or certify mathematical
> correctness.

### Mathematics

> Proceed to Stage 3B. Use `$audit-tex-math` in `audit` mode on the load-bearing propositions
> identified in Stage 2. Attach verification status and downstream consequences to the existing
> graph. Do not repair anything.

### Predominantly empirical paper

Use `econ-write` for a focused identification and evidence audit. Check:

- the estimand and identifying variation;
- the main identifying assumptions;
- the mapping from estimates to mechanisms;
- any step from local estimates to aggregate welfare or policy claims; and
- whether tables and figures support the prose claims attached to them.

Do not run specialist passes merely because they are available. At the checkpoint, decide which
verified substantive repairs to approve and which risks to accept, defer, or investigate further.

## Stage 4: Revision blueprint

**Purpose:** Translate approved findings into an editing plan without editing yet.

Prompt:

> Proceed to Stage 4. Convert the approved findings into a dependency-ordered revision blueprint.
> For every proposed change, give the graph finding, source location, intended repair, protected
> content, downstream sections affected, and verification required afterward. Divide implementation
> into small batches. Do not edit.

A sensible batch order is:

1. headline question, answer, and contribution;
2. introduction and paper roadmap;
3. model, design, or empirical setup;
4. main results and interpretation;
5. appendices and cross-references;
6. conclusion; and
7. surface prose.

Approve or alter the batches before implementation. Identify content that must not change, including
estimates, citations, equations, theorem scope, samples, or established terminology.

## Stage 5: Controlled implementation

**Purpose:** Revise one coherent batch at a time.

Prompt:

> Proceed to Stage 5, Batch 1 only. Implement the approved findings `[IDs]`. Preserve all estimates,
> citations, equations, theorem scope, sample definitions, and established terminology except where
> an approved repair explicitly requires a change. Record which finding each edit addresses. Compile
> affected source when appropriate. Stop after this batch and show the substantive changes and
> unresolved handoffs.

Inspect the result before continuing:

> Proceed to Stage 5, Batch 2.

For every batch, Codex should report:

- files and locations changed;
- approved findings addressed;
- substantive choices made;
- compile or audit status;
- new or unresolved handoffs; and
- the next proposed batch.

Do not combine unrelated batches to save time. Small checkpoints prevent one repair from silently
changing downstream sections or protected claims.

## Stage 6: Rebuild and verify

**Purpose:** Test whether the revisions actually improved the reasoning chain.

Prompt:

> Proceed to Stage 6. Rebuild the reasoning graph from the revised manuscript and compare it with
> the baseline. Determine which findings are repaired, which remain open, whether any node anchors
> became stale, and whether the edits created new orphans, broken handoffs, duplicated ownership, or
> scope drift. Compile and visually inspect the manuscript through `$academic-draft-review`. Do not
> perform general copyediting.

The manuscript is structurally ready when:

- headline claims have visible support;
- important branches return to the central argument;
- definitions and results have unique owners;
- theory or empirical claims retain their conditions;
- main-text and appendix statements agree;
- source anchors and cross-references resolve; and
- no blocking or major graph finding remains unresolved.

Do not use a raw connectivity count as the acceptance criterion. Legitimate caveats, alternative
mechanisms, and technical branches may make a sound paper less linear.

## Stage 7: Final prose pass

**Purpose:** Improve readability after the substance stabilizes.

Prompt:

> Proceed to Stage 7. Use `$ai-slop-lint` in `quick` mode on the abstract, introduction, section
> openings, and conclusion. Remove formulaic language, repetition, vague referents, and inflated
> transitions while preserving every substantive and quantitative claim. If a prose problem reveals
> a substantive reasoning break, create a handoff rather than silently repairing the argument.

Then rebuild only the affected graph regions, compile once more, and confirm that the prose pass did
not alter estimates, citations, theorem statements, identifying assumptions, or claim scope.

## Stage 8: Optional cold referee review

Run this separately after the author-side process is complete:

> Use `$referee-report` for an independent cold review of the revised submission. Reconstruct a
> temporary reviewer-side graph from the submitted manuscript. Do not import the author-side graph,
> revision decisions, or internal accepted-risk judgments.

This preserves genuine reviewer independence. The referee workflow may use a graph internally to
consolidate related concerns, but the author-facing report remains governed by its evidence,
fairness, length, and quality contracts.

## Adjusting the depth

For an **early draft**, prioritize Stages 1, 2, 4, and 5. Map sections and important paragraphs;
avoid sentence-level annotation except in the abstract or introduction.

For a **mature draft**, include specialist audits, a complete rebuild, rendered inspection, and a
final prose pass. Audit only load-bearing proofs or identification links rather than every equation
or robustness result.

For a **short section or isolated passage**, skip the shared graph and invoke the owning specialist
directly. A graph should reduce repeated work and reveal dependencies, not become procedural overhead.

## Completion record

At the end of the process, retain a compact record of:

- baseline and revised graph locations;
- findings implemented, deferred, rejected, or accepted as risks;
- completed specialist layers;
- verified mathematical or empirical obligations;
- files changed and builds inspected;
- unresolved handoffs and stale anchors; and
- the manuscript version used for any subsequent cold review.
