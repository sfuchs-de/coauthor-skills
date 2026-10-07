# Dependency Extraction Playbook

## Contents

1. Corpus scan
2. Atomic extraction
3. Edge inference
4. Conflict reconciliation
5. Cycle audit
6. Module design
7. Review questions

## 1. Corpus scan

Search for:

- `Definition`, `Assumption`, `Lemma`, `Proposition`, `Theorem`, `Corollary`;
- equation labels and textual result IDs;
- phrases such as “given,” “conditional on,” “substituting,” “using,” “therefore,” and “closes”;
- registries, notation files, appendices, verification scripts, and reviews;
- duplicated equations with different notation or timing;
- statements downgraded or corrected by later audits.

Build a source ledger before choosing a graph. A polished exposition may not be the nearest proof authority.

## 2. Atomic extraction

For each formal block, answer:

1. What is newly defined or proved?
2. What named inputs appear on the right-hand side?
3. Which assumptions make the operation legal?
4. Is the conclusion exact, approximate, conditional, computational, or normative?
5. Which later blocks consume the output?

Split a source proposition if one conclusion is exact and another is conjectural, or if different conclusions have different dependencies.

Do not split a system whose equations have meaning only jointly, such as a KKT system or a fixed-point definition. Represent it as one node or a joint block.

## 3. Edge inference

Use three passes.

### Forward pass

Read in source order and add candidate edges when a statement invokes an earlier object.

### Reverse pass

For each output object, search all later and parallel sources for uses. This catches cross-file dependencies omitted by exposition.

### Counterfactual removal pass

Temporarily remove each candidate prerequisite. If the dependent statement remains definable and provable unchanged, remove the edge or reclassify it as `verifies`, `extends`, or shared notation.

Every retained ordering edge should name the transferred object in its reason.

## 4. Conflict reconciliation

Classify duplicates as:

- same result, same assumptions: one node with multiple anchors;
- same result, stronger assumptions: one node plus a `specializes` node when the restriction matters;
- different timing or solution concept: separate model nodes;
- correction or replacement: `supersedes` edge;
- unresolved inconsistency: `conflicts-with` edge and open issue.

Never create a blended formula that appears in no source unless the user explicitly makes the new derivation governing and it is independently audited.

## 5. Cycle audit

For every detected ordering cycle, ask:

1. Is one edge actually a citation, verification, or specialization?
2. Is one object dated and therefore lagged?
3. Are the nodes components of one simultaneous equilibrium?
4. Is a missing primitive or normalization causing apparent circularity?
5. Did two source versions get merged incorrectly?

If it is genuine same-period feedback, replace ordering edges inside the loop with `joint` edges and declare a joint block. Preserve all incoming prerequisites and outgoing equilibrium outputs.

## 6. Module design

Start from topological levels, then group by interfaces.

Good module boundaries occur where:

- a small set of inputs produces a stable reusable output;
- a formal result has one natural proof owner;
- a computational block has its own acceptance checks;
- an alternative model begins;
- status changes from closed to review or frontier.

Bad module boundaries occur where:

- a source file happens to end;
- two unrelated results share symbols;
- a long note is split without a mathematical interface;
- an equilibrium loop is arbitrarily sequenced.

## 7. Review questions

Before accepting the graph, ask:

- Can every formula in the proposed first module be written from its declared inputs?
- Does every result have one owner and at least one source anchor?
- Are all assumptions upstream of the claims they qualify?
- Are approximations separated from exact identities?
- Are alternatives prevented from silently feeding the governing chain?
- Does every equilibrium output come from a declared joint block or closure node?
- Does the proposed reading order preserve temporal timing?
- Can the synthesis follow the graph once without backtracking to introduce missing objects?
- Which edges are uncertain, and what source or calculation would resolve them?
