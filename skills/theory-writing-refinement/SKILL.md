---
name: theory-writing-refinement
description: Structure, audit, and revise the exposition of economics theory, quantitative models, and mathematical manuscripts. Use when the user wants a reasoning map, clearer model setup, motivated notation, step-by-step derivations, proposition intuition, comparative statics exposition, main-text/appendix alignment, or a full theory-writing pass. This skill improves presentation but does not independently certify mathematical correctness; use `audit-tex-math` for proof or equation verification.
---

# Theory Writing Refinement

Make the paper's mathematical spine visible without changing the model or claiming that exposition
work constitutes proof verification.

## Select the mode

- **map**: reconstruct the question, primitives, equilibrium or solution concept, dependency graph,
  results, interpretation, and empirical or computational implications. Do not edit source.
- **audit-exposition**: identify missing motivation, undefined objects, compressed transitions,
  broken dependencies, appendix mismatches, and overclaims. Do not edit unless asked.
- **revise**: apply bounded author-side changes while preserving mathematical substance.
- **full**: map, audit, revise, compile through `academic-draft-review`, and report residual risks.

When mathematical correctness is uncertain, pause substantive revision of the affected result and
use `audit-tex-math` in audit mode. Apply a mathematical repair only when the user authorized repair.

## Operating contract

1. Treat the manuscript's definitions, assumptions, notation, and accepted results as authoritative
   unless a verified audit establishes a defect.
2. Distinguish exact results, approximations, numerical evidence, conjectures, and economic
   interpretations. Never promote one category into another through prose.
3. Preserve theorem scope, quantifiers, domains, signs, normalization, approximation order, and
   equilibrium closure.
4. Do not manufacture motivations, microfoundations, citations, comparative statics, or empirical
   implications. Label proposals as proposals.
5. For a review-only request, return evidence and repairs without modifying files.

## Workflow

### 1. Establish the mathematical spine

Read the complete governing context, including referenced appendices and definitions. Record:

- the economic question and mechanism;
- agents, timing, information, primitives, and constraints;
- equilibrium, optimization, fixed-point, or aggregation objects;
- assumptions and where each one is used;
- the dependency order of lemmas, propositions, comparative statics, welfare claims, and
  quantitative outputs; and
- the relationship between model objects and observables or counterfactuals.

Read `references/coherence-ledger.md` for section, subsection, paragraph, and sentence diagnostics.
For a full structural audit, also use the reasoning-graph protocol and reasoning-skeleton helper
bundled with `econ-write`. When a shared suite graph exists, read
`../econ-writing-suite/references/reasoning-graph-integration.md` and own its `theory` layer. Attach
primitives, assumptions, closure conditions, formal-result dependencies, interpretation, appendix
links, and model-to-observable mappings to stable manuscript nodes. Pass uncertain proof obligations
to `audit-tex-math`; do not label them verified through exposition review.

### 2. Repair hierarchy-wide flow

Give every section and subsection one job. Make each paragraph inherit a live question or object,
advance it, and hand the result forward. Move definitions before use; eliminate orphan results,
unmotivated detours, and duplicate statements. Preserve useful derivational detail even when moving
it to an appendix.

### 3. Present mathematical objects in a stable order

For each important display or result:

1. state why the object is needed;
2. define its domain, dimensions, indices, and dependencies;
3. name the derivation route;
4. show the nontrivial algebra or substitution chain;
5. state assumptions where they do work;
6. interpret the result mathematically and economically; and
7. explain what later result, computation, or empirical object it enables.

Read `references/math-result-protocol.md` for result cards and appendix handshakes. Read
`references/math-exposition-protocol.md` for a long derivation, theorem-condition mapping,
fixed-point argument, approximation, or spectral calculation.

### 4. Align main text and appendices

Keep the mechanism, scope, and decisive derivation steps in the main text. Put long proof algebra,
robustness, implementation detail, and supporting lemmas in the appendix, with explicit two-way
links. Read `references/appendix-integration.md` for the allocation protocol. Use
`references/network-theory-appendix.md` only for network, continuum, transport, welfare, or spectral
projects; it is a domain-specific option, not a universal outline.

### 5. Run adversarial and prose passes

Steelman the intended claim, then test whether the stated assumptions and displayed steps support
that claim at its advertised scope. Classify problems as exposition gaps, unverified mathematical
claims, missing closure, unsupported interpretation, or misplaced detail. Route correctness defects
to `audit-tex-math`. Use `ai-slop-lint` only for a requested scored style pass.

### 6. Verify delivery

Use `academic-draft-review` for compilation, cross-references, and rendered inspection. Confirm that
no symbol is undefined, no appendix result is orphaned, every formal statement has motivation and
interpretation, and every modification preserves the accepted mathematics. Update theory-layer
findings after revision and mark unmatched node anchors stale rather than silently remapping them.

## Output

Lead with the reconstructed argument and highest-priority breaks. For edits, identify changed files,
substantive choices, any audit invoked, compile status, and unresolved mathematical or expository
questions. In a shared graph workflow, include theory-layer status and handoffs. Do not bury the
central repair under exhaustive sentence-level notes.
