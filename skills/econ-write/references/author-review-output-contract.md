# Output Contract

## Contents

- Required author-side review deliverables
- Artifact structure and location standards
- Comment, rewrite, summary, and report templates

## General principle

The review must be actionable, location-specific, and ordered by dependency. Do not bury structural problems under hundreds of line edits. Do not give only high-level comments when exact repairs are possible.

## Required deliverables

### 1. Executive diagnosis

In one to three pages, state:

- the manuscript’s strongest existing reasoning spine;
- the two to five most consequential interruptions;
- whether the main problem is structure, mathematical exposition, interpretation, prose, appendix alignment, or a combination;
- the correct order of revision.

Avoid a long preamble of praise.

### 2. Paper-level reasoning spine

Give a compact directed chain from question to conclusion. Distinguish the main spine from secondary branches.

### 3. Section and subsection contracts

For every major section, and every consequential subsection, report:

| Unit | Inherited object/question | Task | Output | Handoff | Status |
|---|---|---|---|---|---|

Statuses: strong, adequate, weak, broken, duplicated, misplaced.

### 4. Connectivity ledger

Prioritize by severity:

| Priority | Location | From | To | Intended relation | Actual problem | Why it matters | Repair | Exact replacement or move |
|---|---|---|---|---|---|---|---|---|

Include section, subsection, paragraph, and sentence issues. For a long paper, report all blocking and major issues and representative moderate issues; save the complete ledger as an artifact.

### 5. Mathematical exposition audit

For each central result:

| Result | Motivation | Definitions | Derivation route | Interpretation | Mathematical discussion | Use | Scope | Status |
|---|---|---|---|---|---|---|---|---|

Then give exact repairs for deficient results.

### 6. Orphan audit

| Location | Orphan type | Why detached | Recommended action | Proposed integration |
|---|---|---|---|---|

### 7. Main-text, footnote, and appendix alignment

Provide the cross-reference matrix defined in `appendix-footnote-alignment.md`. Report notation and assumption mismatches separately.

### 8. AI-slop and prose audit

Group findings by pattern rather than dumping a phrase count:

- generic framing;
- vague transitions;
- repeated summaries;
- terminology drift;
- inflated or unsupported claims;
- excessive negative qualifications;
- abstract noun stacks;
- hedge stacking;
- choppy or overlong sentences;
- report-level slop.

Include representative before/after edits.

### 9. Adversarial review

List all blocking and major findings first. For each, include the strongest fair skeptical reading and a repair.

### 10. Ordered revision plan

Use dependency order:

1. structural moves;
2. result ownership;
3. main/appendix allocation;
4. section and subsection handoffs;
5. paragraph integration;
6. mathematical exposition;
7. sentence edits;
8. anti-slop pass;
9. validation.

Estimate effort or risk only when useful.

### 11. Exact edits or source changes

When review-only:

- give exact replacement transitions and representative paragraph rewrites;
- specify moves, merges, deletions, and additions.

When editing source:

- modify files;
- provide a unified diff or commit summary;
- list moved content and updated references;
- list all substantive or mathematical changes separately;
- compile or render when possible;
- report failed checks honestly.

### 12. Unresolved questions

List issues that require author judgment, additional data, mathematical proof, or a substantive modeling decision. Do not hide these in prose.

## Recommended artifact structure

For a comprehensive review, write to a review directory such as:

```text
review/
  00_executive_diagnosis.md
  01_reasoning_spine.md
  02_section_contracts.csv
  03_connectivity_ledger.csv
  04_math_exposition_audit.md
  05_orphan_audit.csv
  06_appendix_alignment.csv
  07_ai_slop_audit.md
  08_adversarial_review.md
  09_revision_plan.md
  10_change_log.md
  graph/
    reasoning_nodes.csv
    reasoning_edges.csv
    reasoning_graph.json
    reasoning_graph.graphml
    weak_edges.csv
    orphan_nodes.csv
```

Do not create every file for a short passage. Scale the deliverables to the manuscript.

## Location standard

Use the most precise stable location available:

- source file and line range;
- section/subsection and paragraph ID;
- compiled page;
- equation, theorem, figure, or table number.

Do not write “somewhere in Section 2.”

## Comment standard

Each criticism should answer:

1. What is the manuscript trying to do here?
2. What is missing, repeated, misplaced, or ambiguous?
3. Why does that interrupt the reasoning chain?
4. What exact change repairs it?

## Rewrite standard

A proposed replacement must:

- preserve the claim and conditions;
- use stable terminology;
- link backward;
- perform one advance;
- hand forward;
- avoid AI slop;
- avoid adding facts or citations;
- avoid stronger structural or causal language.

## Final summary standard

End the review with the ordered revision plan and unresolved questions. Do not end with “Overall, this is a strong paper” or another generic assessment.


## Report template

Use `assets/review-report-template.md` for a comprehensive report.
