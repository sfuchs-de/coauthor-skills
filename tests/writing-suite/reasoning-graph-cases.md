# Evaluation Prompts

Use these prompts to test trigger behavior and output quality.

## Should trigger

### 1. Full-paper audit

> Review `main.tex` for section-to-section, subsection-to-subsection, paragraph-to-paragraph, and sentence-to-sentence continuity. Build a reasoning graph, audit mathematical exposition and appendix alignment, identify AI-like prose, and perform an adversarial review. Do not edit yet.

Expected behavior:

- routes through `econ-writing-suite` to `econ-write:author-audit`, then the requested specialist audits;
- reads root and included files;
- creates paper spine, contracts, graph, and prioritized issues;
- does not modify source.

### 2. Theory-section revision

> Revise Section 2 so that every equation is motivated, all new objects are defined, derivations refer back to previous numbered results, and important results receive economic intuition. Move excessive algebra to the appendix but keep the main text self-contained.

Expected behavior:

- routes to `theory-writing-refinement:revise` and invokes mathematical audit where needed;
- preserves mathematical meaning;
- uses explicit substitution or named derivation routes;
- updates appendix references and provides a diff.

### 3. Anti-AI-slop pass

> The structure is now fixed. Remove AI slop from the introduction without flattening the author’s voice. Preserve every factual and contribution claim.

Expected behavior:

- routes to `ai-slop-lint:quick`;
- does not reorder sections or alter claims;
- identifies functional slop rather than deleting from a banned-word list;
- provides before/after edits.

### 4. Appendix audit

> Audit Appendices A–D against every main-text citation. Check notation, assumptions, equation labels, and whether each appendix proves what the main text says it proves.

Expected behavior:

- routes to `theory-writing-refinement:audit-exposition` and `audit-tex-math:audit`;
- creates a two-way crosswalk;
- flags notation and assumption mismatches;
- checks for appendix orphans and dangling references.

### 5. Adversarial review

> Read this as a skeptical top-journal referee. Identify the strongest fair objections to the reasoning chain, especially any jump from fitted coefficients to structural welfare or from local derivatives to nonlinear policy.

Expected behavior:

- steelmans before attacking;
- labels severity and confidence;
- distinguishes exposition from substantive identification or model issues;
- gives repairs.

### 6. Paragraph-level chain

> For every paragraph in Section 3.2, reconstruct the sentence chain and identify exact broken sentence edges or orphan sentences. Propose integrated rewrites.

Expected behavior:

- provides sentence tables for every paragraph in scope;
- does not give only global comments;
- preserves technical content.

## Should not trigger implicitly

### 7. Citation formatting only

> Convert the bibliography to APA style.

Expected behavior: do not invoke this full skill unless explicitly requested.

### 8. Standalone proof solving

> Prove that every compact metric space is complete.

Expected behavior: do not invoke the manuscript-review workflow.

### 9. Ordinary business copyediting

> Make this customer-support email friendlier.

Expected behavior: do not invoke unless the user explicitly asks for the academic reasoning workflow.

## Dry-run fixture

Use the following passage for validation:

> A demand shock raises sales in the treated location. Let \(M\) be the network matrix. Therefore, welfare rises.
>
> \[
> y=(I-M)^{-1}g.
> \]
>
> This is important.¹
>
> ¹Appendix A proves the result under homogeneous ownership.
>
> **Appendix A.** Suppose ownership is homogeneous. Differentiating market clearing yields the displayed activity response.

A successful dry run should identify at least:

- the missing bridge from sales/activity to welfare;
- the unmotivated and underdefined matrix \(M\);
- the unsupported “therefore”;
- the empty sentence “This is important”;
- the mismatch between an activity response and a welfare claim;
- the appendix’s stronger ownership assumption;
- the missing mapping from the appendix result back to the main-text welfare statement.
