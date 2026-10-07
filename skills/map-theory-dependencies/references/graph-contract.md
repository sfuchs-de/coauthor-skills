# Theory Dependency Graph Contract

## Contents

1. Graph layers
2. Node schema
3. Edge schema
4. Joint blocks
5. Module schema
6. Minimal JSON example
7. Interpretation rules

## 1. Graph layers

The machine-readable graph represents mathematical dependencies and equilibrium structure. Keep authority details on nodes and source anchors; do not encode source citations as ordering edges.

The ordering graph consists only of `defines`, `requires`, and `feeds` edges. It must be a directed acyclic graph.

Same-period mutual determination uses `joint` edges and `joint_blocks`. Alternative, audit, and conflict relationships are nonordering.

## 2. Node schema

Required fields:

```json
{
  "id": "stable-node-id",
  "title": "Human-readable title",
  "kind": "result"
}
```

Recommended fields:

```json
{
  "status": "review",
  "owner": "target-note-id",
  "inputs": ["named input object"],
  "outputs": ["named output object"],
  "assumptions": ["assumption ID or concise statement"],
  "source_anchors": ["path:line or stable equation name"],
  "authority": "source-governed",
  "verification": ["symbolic check"],
  "open_issues": ["unverified domain condition"]
}
```

Suggested `kind` values:

- `primitive`
- `state`
- `definition`
- `assumption`
- `lemma`
- `identity`
- `result`
- `equilibrium`
- `computation`
- `estimation`
- `benchmark`
- `extension`
- `frontier`

Use `final`, `review`, `draft`, or `unknown` for status unless the target project defines another vocabulary.

## 3. Edge schema

Every edge is directed from `from` to `to`:

```json
{
  "from": "prerequisite-node",
  "to": "dependent-node",
  "type": "requires",
  "reason": "The dependent result uses the prerequisite's output object."
}
```

Edge types:

| Type | Ordering? | Meaning |
| --- | --- | --- |
| `defines` | yes | Upstream node defines an object used by the downstream node |
| `requires` | yes | Downstream statement cannot be proved or stated as written without upstream |
| `feeds` | yes | Upstream computed output is an input to downstream computation |
| `joint` | no | Nodes are mutually determined inside one declared joint block |
| `specializes` | no | Downstream is a parameter or domain restriction of upstream |
| `extends` | no | Downstream adds structure without governing the upstream result |
| `verifies` | no | Upstream evidence checks downstream or vice versa |
| `conflicts-with` | no | Statements cannot both govern the same scope |
| `supersedes` | no | One statement replaces an older formulation |

Do not use `requires` merely because two nodes appear in the same source section.

## 4. Joint blocks

Declare simultaneous feedback explicitly:

```json
{
  "id": "monthly-fixed-point",
  "title": "Monthly equilibrium block",
  "members": ["policy-system", "aggregate-field", "market-clearing"],
  "reason": "Each member is evaluated conditional on the others and solved jointly.",
  "outputs": ["equilibrium allocation"]
}
```

A node may belong to at most one joint block at a given modeling level. Nested games should use separate levels or separate graph files rather than ambiguous overlapping blocks.

Represent member feedback with `joint` edges. Do not include those edges in the topological sort.

## 5. Module schema

Modules group atomic nodes for exposition:

```json
{
  "id": "local-behavior-note",
  "title": "Local behavior",
  "nodes": ["local-problem", "local-policy-result"],
  "inputs": ["state", "primitive cost"],
  "outputs": ["policy", "continuation value"],
  "owned_claims": ["local-policy-result"],
  "status": "final"
}
```

Every formal result should appear in one primary module. Definitions and assumptions may be shared through links but should still have a canonical home.

## 6. Minimal JSON example

```json
{
  "graph_version": 1,
  "project_key": "example-project",
  "nodes": [
    {
      "id": "primitive-state",
      "title": "Primitive state and costs",
      "kind": "primitive",
      "status": "final",
      "source_anchors": ["source.tex: primitives"]
    },
    {
      "id": "local-policy",
      "title": "Local policy rule",
      "kind": "result",
      "status": "final",
      "owner": "local-behavior-note",
      "source_anchors": ["source.tex: Proposition 1"]
    },
    {
      "id": "aggregate-field",
      "title": "Aggregate field",
      "kind": "result",
      "status": "review",
      "owner": "aggregation-note",
      "source_anchors": ["source.tex: Equation 8"]
    },
    {
      "id": "equilibrium-result",
      "title": "Equilibrium allocation",
      "kind": "equilibrium",
      "status": "review",
      "owner": "equilibrium-note",
      "source_anchors": ["source.tex: Theorem 2"]
    }
  ],
  "edges": [
    {
      "from": "primitive-state",
      "to": "local-policy",
      "type": "requires",
      "reason": "The local objective is defined from the primitive state and costs."
    },
    {
      "from": "local-policy",
      "to": "aggregate-field",
      "type": "feeds",
      "reason": "The aggregation map integrates the local policy."
    },
    {
      "from": "aggregate-field",
      "to": "equilibrium-result",
      "type": "feeds",
      "reason": "The equilibrium closure uses the aggregate field."
    }
  ],
  "joint_blocks": [],
  "modules": [
    {
      "id": "local-behavior-note",
      "title": "Local behavior",
      "nodes": ["primitive-state", "local-policy"],
      "owned_claims": ["local-policy"]
    },
    {
      "id": "aggregation-note",
      "title": "Aggregation",
      "nodes": ["aggregate-field"],
      "owned_claims": ["aggregate-field"]
    },
    {
      "id": "equilibrium-note",
      "title": "Equilibrium",
      "nodes": ["equilibrium-result"],
      "owned_claims": ["equilibrium-result"]
    }
  ]
}
```

## 7. Interpretation rules

- `inputs` and `outputs` are interface descriptions; edges carry graph semantics.
- A missing source anchor is an evidence gap, not proof that a claim is new.
- A node can be final conditional on explicit assumptions even when a quantitative calibration remains review; record the boundary.
- A topological level is not necessarily one note. Group only when the input-output contract is coherent.
- Mermaid diagrams are views of the ledger. The typed node and edge tables remain authoritative.
