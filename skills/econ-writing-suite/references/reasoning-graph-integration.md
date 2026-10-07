# Shared Reasoning-Graph Integration

## Contents

- Purpose and activation threshold
- Workspace artifacts and stable identity
- Layer ownership
- Status and finding contracts
- Lifecycle and cross-skill handoffs
- Privacy, authority, and acceptance rules

## Purpose

Use one reasoning graph to carry the manuscript's logical structure across writing stages. The graph
is a shared audit artifact, not a substitute for close reading and not a score to maximize. It should
answer four questions:

1. What does the paper claim?
2. What definitions, assumptions, derivations, evidence, and interpretations support each claim?
3. Which links have been verified, remain uncertain, or break under review?
4. How did a revision, conversion, review, or presentation preserve or alter those links?

Create a graph for full-paper audits, multi-section revisions, substantial theory work, proof audits
whose consequences propagate into prose, source conversions, revision rounds, and paper-to-talk
workflows. Skip it for a short paragraph, isolated formatting fix, single citation check, or other
task where the graph would cost more than it reveals.

## Workspace

Initialize a private or Git-ignored workspace with:

```bash
python3 "<suite-directory>/scripts/reasoning_graph_workspace.py" init <manuscript> \
  --output-dir writing-review/reasoning-graph
```

The workspace contains:

- `reasoning_nodes.csv`, `reasoning_edges.csv`, `reasoning_graph.json`, and
  `reasoning_graph.graphml`: deterministic structural skeleton;
- `reasoning_annotations.csv`: semantic inheritance, advance, yield, role, and scope by node and
  specialist;
- `reasoning_findings.csv`: anchored problems, implications, repairs, and verification status;
- `reasoning_handoffs.csv`: unresolved questions passed between specialists;
- `reasoning_manifest.json`: source hashes and layer status; and
- `reasoning_map.md`: concise human-readable spine, branches, weak links, and open obligations.

Use `validate`, `status`, `layer`, and `add-finding` subcommands for deterministic maintenance. Keep
the source manuscript authoritative. Rebuild structural files after source changes and treat stale
semantic rows as hypotheses until their node anchors are reconciled.

## Stable identity and paths

Use the node IDs emitted by the structural builder. Do not renumber a node merely to make a report
look cleaner. Join specialist findings to node IDs rather than copying manuscript text into every
ledger. Use source-relative paths in durable artifacts; never store private absolute paths, tokens,
or downloaded manuscript copies in a tracked graph.

When a revision changes node IDs, map old IDs to new IDs by source anchor and substantive object.
Mark an ambiguous mapping `stale` rather than guessing. Preserve one owner node for each definition,
assumption, result, table, figure, or headline claim and connect later uses to that owner.

## Layer ownership

| Layer | Owner | Contribution |
|---|---|---|
| `argument` | `econ-write` | Question, answer, contribution, section contracts, inheritance/advance/yield, main spine, branches, weak edges, and prose-level claim scope |
| `theory` | `theory-writing-refinement` | Primitives, timing, closure, assumptions, formal-result dependencies, intuition, main-text/appendix links, and model-to-observable mappings |
| `math` | `audit-tex-math` | Proof obligations, verification status, added conditions, counterexamples, repairs, and downstream consequences |
| `source_qa` | `academic-draft-review` | Authoritative roots, file/line/page anchors, cross-references, build state, and source/render mismatches |
| `conversion` | `render-mathdown-tex` | Source-owner to TeX-owner mappings, provenance, duplicate/specialization relations, and conversion-loss checks |
| `referee` | `referee-report` | Temporary reviewer inference and consolidation of decisive concerns; never an author-facing graph dump |
| `prose` | `ai-slop-lint` | Anchored style findings and rewrite status without changing logical dependencies or claim scope |
| `presentation` | `design-econ-seminar` | Projection from paper nodes to slide claims, timing, cuts, backup branches, and audience handoffs |

Each specialist may read every layer but may write only its own layer, except that `econ-write`
maintains the integrated human-readable map. A specialist may propose a change to another layer
through a handoff; it may not silently overwrite that layer's judgment.

## Annotation and finding contract

For a material node, record the minimum useful annotation:

- `owner` and stable `node_id`;
- one-sentence `summary` and primary `role`;
- `inherits`, `advance`, and `yield`;
- relevant `scope` and `status`; and
- confidence in the classification.

Use `draft`, `accepted`, or `stale` for annotation status and `high`, `medium`, or `low` for stated
confidence. One specialist may maintain one annotation per node; rerunning `annotate` replaces that
owner-node row rather than creating a duplicate.

For a material concern, record:

- owner and affected node IDs;
- source and target node when the concern is relational;
- severity and category;
- manuscript evidence;
- consequence for the paper or deliverable;
- smallest adequate repair; and
- verification status.

Use `candidate`, `open`, `verified`, `repaired`, `accepted-risk`, `not-assessable`, or `stale` for
finding status. A generated derivation begins `candidate`; only mathematical audit can set it to
`verified`. Use `open`, `closed`, `blocked`, or `stale` for handoff status. Compilation, prose
cleanup, conversion, or visual inspection cannot verify a mathematical finding.

## Lifecycle

### 1. Baseline

Build the structural skeleton, record source hashes, and identify the shortest faithful paper spine.
Populate semantic annotations only to the depth needed for the request.

### 2. Specialist enrichment

Run specialists in dependency order. Each reads the current graph, adds its annotations and
findings, updates its layer status, and leaves explicit handoffs for unresolved cross-domain issues.
Do not make every specialist repeat the whole-paper inventory.

### 3. Authorized revision

Approve repairs at the owning layer. Apply source edits through the appropriate specialist and
record which node or edge the edit was intended to repair. Preserve rejected recommendations as
`accepted-risk` only when the user explicitly chooses not to implement them.

### 4. Rebuild and compare

After material edits, rebuild the structural graph in a fresh workspace or reviewed refresh. Check
that repaired links close, branches return, owner nodes remain unique, source anchors resolve, and
no new orphan or scope drift appears. Compare severity and status, not a raw connectivity score.

### 5. Projection or independent review

Use the accepted graph as an input to a presentation or author-side response. For an independent
referee report, construct or copy only the minimum temporary graph needed for review; do not import
private author-side judgments, accepted-risk decisions, or hidden revision strategy.

## Handoff protocol

Every cross-skill handoff should name:

1. originating owner;
2. receiving owner;
3. affected node IDs;
4. the exact unresolved question;
5. evidence already checked;
6. the status that would close the handoff.

Examples include a prose claim whose theorem support is uncertain, a verified repair requiring
paper-wide terminology propagation, a conversion mapping that may change result scope, or a slide
claim stronger than the source result.

## Privacy and authority

- Keep full-text graph artifacts private or Git-ignored by default.
- Never store confidential referee materials or internal recommendation reasoning in a public or
  author-facing graph.
- Review-only work may enrich a private graph but may not edit manuscript source.
- A graph relation is an analytical claim requiring evidence; an automatically generated sequence
  edge is not proof of logical support.
- Do not manufacture a missing premise to repair connectivity. Flag it and route it to the owner.
- Preserve legitimate caveats, branches, and alternative mechanisms even when they make the graph
  less linear.

## Acceptance

For a graph-centered workflow, report the workspace used, layers completed, decisive open findings,
handoffs, source changes, rebuild status, and residual stale anchors. The graph is ready for reuse
only when the workspace validator passes and every load-bearing finding has an explicit status.
