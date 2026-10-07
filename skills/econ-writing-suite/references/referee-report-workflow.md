# Referee-Report Workflow

## Purpose and ownership

Use this workflow when an independent manuscript review spans several writing-suite skills. The
`referee-report` skill owns the review judgment, issue triage, author-facing report, revision
assessment, and confidential editor note. Supporting skills may supply bounded evidence or audits;
they do not independently add report comments or change the recommendation.

For a request that only asks for a referee report, invoke `referee-report` directly. Use the suite
as coordinator when the request also requires literature benchmarking, a serious theory or proof
audit, source reconstruction, archive integration, or a separate prose pass.

## Deliverable map

Keep distinct artifacts distinct:

| Artifact | Owner | Default location or treatment |
|---|---|---|
| Review log and verified notes | `referee-report` | Private working files |
| Author-facing report | `referee-report` | Markdown; no recommendation |
| Confidential editor note | `referee-report` | Separate file; only when requested |
| Literature review | `referee-report` with verified sources | Separate evidence note |
| Theory investigation | `audit-tex-math` or `map-theory-dependencies` supporting `referee-report` | Separate technical note |
| Source or rendering audit | `academic-draft-review` | Separate QA findings; no manuscript edits in reviewer mode |
| Prose cleanup | `ai-slop-lint` | Final pass that preserves the reviewer's voice |

Do not place confidential manuscripts, extracted full text, private recommendation reasoning, or
author-side strategy in a tracked skills repository or reasoning graph.

## End-to-end sequence

### 1. Intake and round classification

Inventory the manuscript, appendices, response letter, prior reports, user notes, annotations, and
requested outputs. Set `round_type`, `workflow_mode`, `report_kind`, journal target, and output
location. Verify that every referenced file is readable and report whether PDF annotations were
actually extracted.

For a revision, preserve the prior issue set and compare it against both the response and revised
text. Do not evaluate the revision as a new initial submission.

### 2. Manuscript-first reconstruction

Read the submitted record before searching outside literature. Reconstruct the paper's question,
answer, contribution claim, empirical design or equilibrium structure, data, and headline results.
Record manuscript anchors for load-bearing claims and separate what the manuscript establishes from
reviewer inference.

Use a temporary reviewer-side reasoning graph only when simultaneous equilibrium blocks, long
derivation chains, or several linked claims make it useful. Follow
`references/reasoning-graph-integration.md`; keep the graph internal.

### 3. Focused validity audit

Choose only the modules that can change the evaluation:

- contribution and journal calibration;
- identification and counterfactual variation;
- measurement and data construction;
- mechanism and mapping from theory to evidence;
- mathematical correctness, equilibrium closure, and computation;
- quantitative validation and external validity.

Use `audit-tex-math` in referee bridge mode for pivotal derivations. Use
`map-theory-dependencies` in referee bridge mode for timing, hidden assumptions, equilibrium
closure, comparative statics, or mappings to observables. Ask `academic-draft-review` only to
recover authoritative source, compile, or identify source/render discrepancies; reviewer mode does
not authorize manuscript patches.

### 4. External literature benchmark, when useful

Do this only when the user requests it or the contribution assessment genuinely depends on it.
Start with the manuscript's own cited predecessors, then search the Paperpile library, then verify
the closest papers through primary sources. Use the Paperpile ingest skill only for a separate,
explicit library-ingest request; never upload a confidential submission merely because it is under
review.

Compare the closest papers on the margin at issue: question, mechanism, data, identification,
equilibrium block, computation, or quantitative result. A title or citation match is not enough.
Keep the full comparison in the literature note and move only the decisive implication into the
report.

### 5. Concern consolidation and discussion

Convert findings into candidate concerns and classify each as fatal, materially addressable,
interpretive, optional, or presentational. Consolidate multiple symptoms of one underlying problem.
Apply the extension filter: an omitted feature is required only when it can overturn the claim or
materially change its quantitative content; otherwise it limits interpretation or belongs as an
optional extension.

Before drafting, identify the two to four issues that drive the evaluation. When the user wants to
discuss comments iteratively, retain their substantive framing and first-person language. Revise
for accuracy and structure without replacing personalized judgment with generic report prose.

### 6. Draft the requested outputs

Draft from scratch once the issue hierarchy is stable. The opening should state what the paper
does, what is genuinely appealing, and the overall assessment. Each major comment should begin
with the high-level problem and then move to manuscript-specific evidence, consequences, one
primary request, and a practical resolution threshold.

Keep the author report and editor note separate. Use the round-specific templates and word limits
owned by `referee-report`. Smaller comments should be first-person, concrete, and easy to act on;
avoid compressed specialist shorthand or a second list of robustness demands.

### 7. Verification and prose pass

Verify every number, quotation, anchor, and external comparison. Recheck each mathematical concern
against the technical note and each literature claim against the cited source. Run the
`referee-report` fairness and quality gates. Then use `ai-slop-lint` in referee context to remove
generic praise, repeated remedies, over-structured transitions, and machine-like phrasing while
preserving technical terms and the reviewer's established voice.

### 8. Archive and close

Write to the private referee archive only when the user supplies an existing case or asks to create
one. Keep review, literature, theory, decision, report, and editor-note files separate under the
case's round directory. Store only permitted Markdown, metadata, hashes, and private locators; do
not copy source PDFs or extracted text into Git.

Report the artifacts produced, supporting passes completed, validation performed, and remaining
uncertainties. A review is complete only when the requested deliverables pass their length,
evidence, fairness, confidentiality, and prose checks.

## Routing shortcuts

- `Review this paper`: `referee-report`, direct initial review.
- `Review the revision and response`: `referee-report`, direct revision protocol.
- `Check whether the model is correct, then write the report`: suite coordination with theory or
  math bridge, followed by `referee-report`.
- `Compare the contribution with my library`: suite coordination with manuscript references,
  Paperpile search, primary-source verification, then `referee-report`.
- `Help us revise our paper after a referee report`: `econ-write`; this is author-side work.
- `Compile or fix the submitted TeX`: `academic-draft-review`; this is source QA, not independent
  review judgment.
