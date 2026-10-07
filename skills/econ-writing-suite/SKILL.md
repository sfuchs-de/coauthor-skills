---
name: econ-writing-suite
description: Coordinate the complete economics research writing suite across drafting, reasoning graphs, theory exposition, mathematical verification, TeX compilation, Markdown conversion, referee review, prose cleanup, and seminar design. Use when a request spans multiple writing stages, asks for an end-to-end paper or presentation workflow, asks which writing skill to use, or explicitly requests the writing suite. Route narrow single-stage requests directly to the specialized skill when its owner is clear.
---

# Economics Writing Suite

Act as a lightweight router and workflow coordinator. Select the smallest set of specialized skills
that can complete the request, apply them in dependency order, and preserve each skill's authority
boundary. Do not reproduce every specialist protocol in this umbrella.

## Establish the job

1. Identify the artifact, requested outcome, audience, scope, and binding deadline or length.
2. Determine whether the user wants review only, proposed text, direct edits, or a complete pipeline.
3. Separate supplied evidence from missing facts, estimates, citations, institutional details, and
   mathematical claims requiring verification.
4. If one specialist clearly owns the entire request, route directly to it. If the user explicitly
   invokes this umbrella, state the selected route before continuing.
5. Before using a selected specialist, read its sibling `SKILL.md` completely. Load only the
   references that specialist requires for the current mode.

For a graph-worthy task, read `references/reasoning-graph-integration.md`, initialize or reuse one
shared workspace, and require each selected specialist to update only its owned graph layer. Skip
the graph for narrow tasks where it would add ceremony without improving the result.

For an independent review that spans several specialists, read
`references/referee-report-workflow.md`. Keep `referee-report` as the sole owner of reviewer
judgment and deliverables; use the suite only to coordinate bounded supporting passes.

## Route to the subskills

| Need | Skill | Modes or focus |
|---|---|---|
| Economics drafting, revision, paper structure, reasoning graph, or author audit | `econ-write` | `draft`, `revise`, `author-audit`, `response`, `specialized` |
| Theory or quantitative-model exposition and dependency mapping | `theory-writing-refinement` | `map`, `audit-exposition`, `revise`, `full` |
| Proof derivation, correctness, authorized repair, or verified readability | `audit-tex-math` | `derive`, `audit`, `repair`, `readability` |
| TeX/source discovery, compilation, rendered inspection, or layout repair | `academic-draft-review` | `compile`, `repair`, `short-note-layout` |
| Markdown or Mathdown conversion to compilation-ready TeX | `render-mathdown-tex` | `faithful`, `curated`, `repair` |
| Independent reviewer-side assessment | `referee-report` | `direct`, `staged`, `evaluation` |
| Formulaic-prose diagnosis or cleanup | `ai-slop-lint` | `quick`, `report`, `rewrite` |
| Quick unscored prose cleanup | `stop-slop` | brief naturalization |
| Corpus-guided spatial/trade/urban writing | `corpus-econ-writing` | topical guidance and optional exact vocabulary checks |
| Talk narrative, slides, accessibility, timing, or speaker notes | `design-econ-seminar` | `structure`, `slides`, `script`, `full` |

Do not use `referee-report` for the author's own pre-submission audit. Do not treat successful
compilation as mathematical verification. Do not let a style, formatting, conversion, or
readability pass change claims, estimates, theorem scope, or model substance.

## Use dependency-ordered pipelines

### Full manuscript audit and revision

1. Initialize one reasoning-graph workspace and use `econ-write:author-audit` to reconstruct the
   paper spine and prioritize structural work.
2. Use `theory-writing-refinement:map` or `audit-exposition` to enrich theory dependencies.
3. Use `audit-tex-math:audit` to attach verification status to load-bearing mathematical claims.
4. Apply authorized repairs with the owning specialist and record the node or edge repaired.
5. Use `academic-draft-review` to attach source, build, cross-reference, and rendered-page status.
6. Rebuild or compare the graph after material edits; resolve stale anchors and new orphans.
7. Use `stop-slop` for quick cleanup or `ai-slop-lint:rewrite` for requested scored iteration only
   after the argument and mathematics stabilize. Use corpus guidance when topical or explicitly
   requested; strict vocabulary checks are a distinct gate, not a universal writing constraint.
8. Use `referee-report` only for a separate cold review with a temporary reviewer-side graph.

### Independent referee report

1. Route a report-only request directly to `referee-report`; use suite coordination only when the
   request also needs literature, theory, math, source-QA, archive, or prose work.
2. Reconstruct and audit the submitted record before importing outside literature.
3. Run only the supporting passes that can change the evaluation and return their verified findings
   to `referee-report` for consolidation.
4. Draft the author report and editor note as separate artifacts, then run evidence, fairness,
   confidentiality, length, and prose checks.
5. Archive the work only in an existing or explicitly requested private case structure.

The complete sequence and routing shortcuts are in
`references/referee-report-workflow.md`.

### New or substantially revised theory section

1. Use `theory-writing-refinement:map` to establish primitives, closure, dependencies, results, and
   appendix allocation.
2. Use `audit-tex-math:derive` for candidate derivations and then a separate `audit` before relying
   on them.
3. Use `econ-write:revise` for integration with the paper's economic question and contribution.
4. Compile and inspect through `academic-draft-review`.

### Mathdown-to-paper workflow

1. Use `render-mathdown-tex` in the requested authority mode.
2. Use `audit-tex-math:audit` when converted mathematics has not already been verified.
3. Use `theory-writing-refinement` for exposition and appendix integration.
4. Finish with `academic-draft-review`.

### Presentation workflow

Use `design-econ-seminar` in `structure`, then `slides`, then `script` mode. Use `full` only when the
user wants all three stages. Draw on `econ-write` for paper-to-talk compression and
`audit-tex-math` only when a displayed derivation needs correctness review.

## Reasoning graphs

For paper-level reasoning graphs, use `econ-write:author-audit`; for model dependencies, use
`theory-writing-refinement:map`. Use the shared contract to carry stable node IDs, specialist
findings, verification status, and handoffs across stages. Initialize and validate the workspace
with:

```bash
python3 "<skill-directory>/scripts/reasoning_graph_workspace.py" init <manuscript>
python3 "<skill-directory>/scripts/reasoning_graph_workspace.py" validate \
  writing-review/reasoning-graph
```

The deterministic skeleton does not establish argumentative or mathematical validity. The graph is
an audit instrument; never optimize connectivity at the expense of legitimate qualifications,
branches, alternative mechanisms, or mathematical complexity.

## Completion

Report the route used, graph layers completed when applicable, files reviewed or changed,
verification performed, handoffs, and residual issues. Validate a reused graph workspace before
delivery. Keep draft or derived results marked unverified until a separate audit establishes them.
Never invent missing evidence or present a specialist pass as certifying something outside its remit.
