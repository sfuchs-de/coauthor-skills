---
name: econ-write
description: Draft, revise, structure, and audit author-side economics papers, sections, abstracts, introductions, conclusions, literature reviews, results, theory exposition, and responses to referees. Use for improving an author's own manuscript or response letter. Do not use for independent referee reports; use the `referee-report` skill for those.
---

# Economics Writing

## Modes and authority

- `draft`: write from supplied evidence, marking essential missing inputs explicitly.
- `revise`: edit the requested prose while preserving meaning and evidentiary scope.
- `author-audit`: diagnose the author's own paper and propose priorities; review-only by default.
- `response`: answer actual referee comments using actual revisions and manuscript anchors.
- `specialized`: use the relevant references for grants, surveys, policy or related author prose.
- `result-first`: clarify a sound technical argument using `references/result-first-exposition.md`;
  reorder rather than shortening away necessary reasoning.

Review requests do not authorize source edits. External publication, synchronization and messages
require separate authorization. Verify current journal requirements when consequential.

## Ownership Boundary

This skill owns author-side economics writing. It does not own independent referee reports,
confidential editor notes, or adjudication of reviewer concerns. Route those tasks to
`referee-report`.

Use supporting skills only when the task requires them:

- Use `academic-draft-review` for compilation and source-level draft correction.
- Use `audit-tex-math` for proof or derivation correctness.
- Use `theory-writing-refinement` for substantial theory exposition work.
- Use `ai-slop-lint` only for an explicit scored style audit.

## Core Rules

1. Put the main question, result, or mechanism before background.
2. Write for economists outside the paper's narrow subfield.
3. State findings and magnitudes rather than announcing activities or importance.
4. Use the simplest model, estimator, and prose that preserve the contribution.
5. Keep one central contribution visible throughout the paper.
6. Prefer active, concrete sentences, while retaining standard passive constructions when
   the actor is immaterial in methods or captions.
7. Preserve the author's meaning, voice, notation, citations, and evidentiary limits.
8. Never invent results, citations, sample details, institutional facts, or robustness checks.

## Workflow

### Drafting

1. Identify the target section, audience, paper type, and central contribution.
2. Inventory the facts, results, model claims, and citations that the draft may use.
3. Choose the section structure from the relevant reference below.
4. Draft from the strongest concrete claim outward.
5. Check that each paragraph has one job and that its first sentence signals that job.
6. Run a compression and citation-integrity pass before delivery.

### Rewriting

1. State the passage's intended claim in one sentence.
2. Preserve all supported technical content and qualifications.
3. Move the main claim forward, remove repetition, and replace abstract nouns with verbs
   where no technical distinction is lost.
4. Check notation, cross-references, citations, and numerical statements after editing.
5. Do not silently strengthen causal, welfare, policy, or generality claims.

### Author-Side Audit

When asked to review the author's own paper, assess contribution, organization, evidence,
interpretation, and prose. Give revision priorities rather than a simulated publication
recommendation. Read `references/review-checklist.md` for quick and deep audit modes.

For paper-level argument maps, read `references/reasoning-graph-protocol.md` and use
`scripts/build_reasoning_skeleton.py` when useful. For a shared specialist workflow, read
`../econ-writing-suite/references/reasoning-graph-integration.md` and own only the `argument` layer.
Reconstruct section contracts, paragraph handoffs, weak edges, orphans and claim scope. Reconcile
the graph after a material revision, leaving correctness and build judgments to their owners.

### Referee Response

For responses to referees, read `references/specialized-tasks.md`. Preserve the original
comment, identify the action taken, cite the revised manuscript location, and distinguish
implemented changes from respectful disagreement. Do not impersonate the referee or draft a
confidential recommendation.

## Reference Routing

Read only the material needed for the task:

- Section structure: `references/section-writing.md`.
- Empirical presentation: `references/empirical-writing.md`.
- Document genres: `references/paper-types.md`.
- Voice and sentence choices: `references/core-style.md`.
- Author-side adversarial review: `references/adversarial-author-review.md`.
- Result-led technical exposition: `references/result-first-exposition.md`.

- Full section and paper guidance: `references/authoring-guide.md`.
- Identification designs and design-specific exposition: `references/identification-strategies.md`.
- LaTeX, tables, figures, bibliography, and Beamer: `references/latex-tips.md`.
- Author-side paper audit and journal-fit checks: `references/review-checklist.md`.
- Referee responses, grants, surveys, policy writing, and other special tasks:
  `references/specialized-tasks.md`.

Useful search terms in `references/authoring-guide.md` include `WRITING THE INTRODUCTION`,
`WRITING THE MODEL SECTION`, `EMPIRICAL WORK RULES`, `PAPER TYPE`, and `TASK-SPECIFIC`.

## Final Gate

Before returning author-side prose, verify:

- The main claim appears early and is concrete.
- Every factual or numerical statement comes from supplied material or a verified source.
- Causal language matches the design.
- Model interpretation matches the assumptions and equilibrium concept.
- Literature comparisons are accurate and proportionate.
- Paragraphs do not repeat the same contribution or result.
- The prose sounds like the author's field and document type, not a generic assistant answer.
