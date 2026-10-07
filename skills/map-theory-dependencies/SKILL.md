---
name: map-theory-dependencies
description: Build and audit mathematical dependency graphs from TeX, Markdown, proof notes, result registries, and theory repositories. Use for full theory architecture, equilibrium closure, hidden circularity, ownership, and topological ordering. For independent referee reports, use `referee-report`; enter compact referee bridge mode here only when joint equilibrium or hidden dependencies are pivotal.
---

# Map Theory Dependencies

## Referee Bridge Mode

When supporting `referee-report`, do not deliver the full graph. Inspect only the model block that
carries the disputed claim and return:

- the relevant primitives, decisions, and outputs;
- the simultaneous equilibrium block and closure conditions;
- hidden assumptions, circularity, or missing interfaces;
- the comparative static or data mapping affected;
- a compact source anchor and smallest repair.

Separate genuine closure failures from omitted extensions. Let `referee-report` translate no more
than one or two verified findings into author-facing comments.

## Core rule

Build the atomic mathematical graph before grouping material into notes or sections. Source-file order, equation proximity, and citation order are evidence, not dependency tests.

Keep four structures distinct:

1. **Authority graph:** which source or review controls each statement.
2. **Derivation graph:** which definitions, assumptions, and results are logical prerequisites.
3. **Equilibrium graph:** which objects are jointly solved through same-period feedback.
4. **Exposition graph:** how atomic nodes are grouped into modules and presented to readers.

Read [references/graph-contract.md](references/graph-contract.md) before creating a machine-readable graph. Read [references/extraction-playbook.md](references/extraction-playbook.md) when the corpus is large, duplicated, or mathematically inconsistent.

## Workflow

### 1. Freeze the corpus and authority

Inventory source files, result registries, notation contracts, review documents, tests, and superseded versions. Record the nearest authority for each block.

Do not treat two versions of the same equation as two required nodes. Mark one governing, one superseded, or both as explicit alternatives. Record unresolved conflicts instead of merging them.

### 2. Extract atomic nodes

Create one node for each object that has an independent mathematical role:

- primitive or state;
- definition or normalization;
- assumption or domain condition;
- lemma or identity;
- formal result;
- equilibrium or closure condition;
- computational or estimation result;
- benchmark, extension, or frontier claim.

For each node record:

- stable ID and title;
- kind and status;
- inputs and outputs;
- assumptions;
- source anchors and authority;
- primary owner if already known;
- verification evidence and open issue.

Split compound source propositions when their conclusions have different prerequisites or statuses. Keep tightly inseparable equations in one node.

### 3. Apply the dependency test

For candidate prerequisite $A$ and statement $B$, ask:

> If $A$ were removed or changed, could $B$ still be defined, proved, or computed as stated?

Add an ordering edge only when the answer is no. Write a reason that names the object transferred across the edge.

Orient ordering edges from prerequisite to dependent:

$$
A\longrightarrow B.
$$

Use the edge vocabulary in the graph contract. Do not convert the following into prerequisite edges:

- a source merely cites another source;
- two results share notation but neither needs the other;
- one result verifies another;
- one model is an alternative or extension;
- two equations are solved simultaneously in equilibrium.

### 4. Expose interfaces

For every result, list exactly which upstream outputs it consumes and which downstream objects it produces. Check units, timing, indexing, normalization, and status at each interface.

Reverse-audit outputs: for every produced object, search the corpus for downstream uses. Missing reverse edges often reveal an omitted closure, duplicated formula, or silently imported assumption.

### 5. Separate feedback from circular proof

Run cycle detection on ordering edges.

- Treat a cycle in definitions, assumptions, or proofs as an error until resolved.
- Represent legitimate same-period feedback with `joint` edges and a named `joint_blocks` entry.
- Give the joint block incoming prerequisite edges and outgoing equilibrium-result edges.
- Represent temporal recursion with dated nodes or an explicit lag; do not confuse $t\to t+1$ with same-period circularity.

Never break an equilibrium loop by imposing an arbitrary sequential timing. If timing is a substantive alternative, create a separate model node.

### 6. Reconcile claims and ownership

Give every formal result exactly one primary owner. Supporting notes may reference it but may not redefine it. When several source files derive the same result, choose ownership by the nearest complete derivation and retain the others as source anchors.

Do not mechanically propagate status by taking the weakest upstream label. Instead, state whether the downstream result is unconditional, conditional on a review-status input, or independently closed under explicit assumptions.

### 7. Topologically layer the theory

Topologically sort only the ordering edges. Use the resulting levels to identify a natural reading sequence. A common pattern is primitives and notation, local behavior, aggregation, equilibrium closure, dynamics, counterfactuals, analytic companions, and identification, but follow the actual graph rather than forcing this template.

Nodes connected only by `specializes`, `extends`, `verifies`, or `conflicts-with` do not determine the canonical reading order.

### 8. Group nodes into modules

Create a module when a set of nodes has a coherent input-output contract and can support one substantive derivation note. Prefer mathematical ownership to source-file boundaries.

For each module provide:

- incoming objects;
- outgoing objects;
- owned claims;
- source anchors;
- assumptions and status boundary;
- upstream and downstream modules;
- verification obligations.

Create a central integration note for the governing joint block when the equilibrium architecture is dispersed across source files. Keep alternatives, timing variants, and frontier material outside the canonical chain unless they feed it explicitly.

### 9. Deliver the graph

Provide, at minimum:

1. node ledger;
2. typed edge ledger with reasons;
3. joint-block ledger;
4. topological levels;
5. module ownership table;
6. unresolved ambiguities, conflicts, and missing proofs;
7. a dependency table suitable for the project overview.

Create JSON only when it will be retained or used for validation. Otherwise keep the graph in the implementation plan and persist ownership in the claim manifest and overview.

Validate retained JSON with:

```bash
node "<skill-directory>"/scripts/validate_dependency_graph.mjs \
  --graph /path/to/dependency-graph.json \
  --require-owners \
  --require-sources \
  --require-reasons \
  --print-order
```

Use `--mermaid` to emit a visual graph after validation.

## Acceptance gate

Do not call the dependency graph complete until:

- every formal claim has one owner;
- every ordering edge has a mathematical reason;
- all edge endpoints resolve;
- ordering edges are acyclic;
- every legitimate feedback loop is represented as a joint block;
- alternatives and extensions are not silently placed in the governing chain;
- source conflicts and superseded versions are recorded;
- each module has explicit incoming and outgoing objects;
- the topological order reproduces the intended derivation without importing undeclared objects;
- independent reviewers can trace every graph decision back to source evidence.
