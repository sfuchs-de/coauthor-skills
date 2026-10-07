# Core Connectivity Rubric

## Contents

- Governing continuity tests and relation types
- Document, section, subsection, paragraph, and sentence contracts
- Introduction, results, and conclusion audits
- Severity, repairs, graph nodes, edges, branches, orphans, and outputs

## Governing test

For every unit, answer:

1. **Inheritance:** What live question, object, claim, or result does this unit receive?
2. **Advance:** What one identifiable piece of reasoning does it perform?
3. **Yield:** What usable object, conclusion, or unresolved task does it pass forward?

A transition word cannot substitute for one of these links.

## Relations that create continuity

Classify the relation between units as one or more of:

- motivates;
- poses a problem for;
- defines;
- assumes;
- derives;
- substitutes into;
- differentiates;
- aggregates;
- decomposes;
- specializes;
- generalizes;
- interprets;
- qualifies;
- contrasts;
- tests;
- validates;
- applies;
- resolves;
- hands off to.

“Next,” “moreover,” and “finally” mark order but do not identify the logical relation.

## Document-level review

Recover the shortest faithful argument from the research question to the conclusion. Distinguish the central spine from secondary branches.

Flag:

- repeated launches in the introduction;
- theory, empirics, or quantitative sections that read as parallel papers;
- an extension or caveat that captures the main narrative;
- a branch with no explicit return to the spine;
- two sections claiming ownership of the same result;
- a later section using an object that no earlier section produced;
- a conclusion stronger or broader than the body;
- abstract, introduction, and conclusion using different object language.

## Section contract

For each section, record:

| Incoming object/question | Section task | Output | Outgoing handoff | Status |
|---|---|---|---|---|

A strong section opening inherits a specific unresolved object. A strong close states what has been established and why the next section is needed.

Weak:

> This section presents the data.

Stronger:

> The theory requires a shock vector, an income network, a spending network, and a bilateral outcome. This section constructs those four objects.

## Subsection contract and ownership

Assign each subsection one controlling role: setup, motivation, definition, derivation, interpretation, identification, estimation, validation, application, robustness, extension, policy, or synthesis.

For every important result or object, identify one owner subsection. The owner should motivate, define, derive or estimate, interpret, and hand off the object. Later subsections should use it rather than partially restarting its derivation.

## Paragraph contract

For each paragraph, record:

- topic object already active;
- primary function;
- main claim or operation;
- evidence or derivation;
- closing yield.

Common paragraph failures:

- detail before a topic sentence;
- several unrelated jobs without hierarchy;
- premise supplied after conclusion;
- caveat interrupts the claim and never returns;
- table or figure reported without inference;
- inference stated without evidence;
- summary loop with no new reasoning;
- silent shift from individual to aggregate, local to global, benchmark to general, descriptive to causal, or fitted to structural;
- terminology changes without a transformation;
- short transition paragraph that says only that the next topic matters.

A paragraph should normally be merged, split, moved, expanded, or deleted only after its intended function is identified.

## Sentence chain

Within each paragraph, record:

| Sentence | Old information | New information | Relation to prior sentence | Function | What the next sentence needs |
|---|---|---|---|---|---|

Flag:

- a new subject with no bridge;
- ambiguous “this,” “that,” “these,” “it,” or “they”;
- unsupported “therefore,” “thus,” “hence,” or “equivalently”;
- premise introduced after its conclusion;
- scope condition dropped;
- technical object renamed without explanation;
- sentence that merely paraphrases its predecessor;
- sentence containing several hidden logical operations;
- sentence that belongs in another paragraph.

Use old-to-new ordering. Begin with the object already active and end with the new information the next sentence can use.

## Introduction audit

A coherent introduction normally has one controlling sequence:

`question -> obstacle -> conceptual solution -> method -> data/identification -> findings -> policy or broader use -> contributions -> roadmap`.

The order may vary, but the introduction should not restart under several competing schemes such as “two observations,” “three steps,” a second roadmap, and a separate contribution list that retells the paper.

Check that:

- the opening poses the actual problem;
- the obstacle is precise;
- the method is presented as a solution to that obstacle;
- theory and empirics are connected;
- results use the same object language as the body;
- caveats sit near the claims they limit;
- literature discussion explains the difference rather than listing papers;
- the roadmap adds information rather than repeating prior pages.

## Results-section audit

Prefer this order unless the design requires otherwise:

`estimand/object -> identification or design -> baseline result -> interpretation -> diagnostics -> robustness -> implication`.

Evidence that defends a result should usually follow the result. For each figure or table:

1. state why it enters;
2. identify the comparison;
3. report the central pattern;
4. state what it supports;
5. state what it does not establish when necessary;
6. connect it to the next result.

## Conclusion audit

The conclusion should:

- answer the opening question;
- restate the mechanism rather than the table of contents;
- distinguish headline findings from conditional extensions;
- preserve scope;
- end with the most general earned lesson.

Do not introduce a new result or literature at the end. Do not let a list of defensive qualifications erase the positive conclusion.

## Severity

- **Blocking:** premises do not establish a headline claim.
- **Major:** an essential bridge, condition, definition, or object mapping is missing.
- **Moderate:** the chain is recoverable but obscured by order, repetition, branches, or terminology.
- **Minor:** local transition, referent, rhythm, or integration problem.

## Repair taxonomy

Recommend concrete actions:

- add a dependency statement;
- move motivation before a result;
- assign one subsection ownership of an object;
- split a multi-job paragraph;
- merge or relocate an orphan;
- move substantial technical detail to an appendix;
- restore an essential premise to the main text;
- delete repeated setup;
- standardize terminology;
- add a closing handoff;
- reorder diagnostics after the baseline result;
- mark benchmark/general or fitted/structural distinctions;
- add the exact cross-reference to the prior result used.


---

# Directed Reasoning Graph Schema

## Purpose

Use the graph to represent how the manuscript reasons, not merely how it is formatted. The graph should make it possible to detect:

- weak transitions;
- missing premises;
- repeated restarts;
- branches that never rejoin the main argument;
- orphaned paragraphs, sentences, equations, figures, footnotes, or appendices;
- duplicated derivations;
- notation or scope drift;
- main-text and appendix mismatches.

## Node levels

Create nodes for:

- `document`;
- `section`;
- `subsection`;
- `subsubsection`;
- `run_in_heading`;
- `paragraph`;
- `sentence`;
- `equation`;
- `assumption`;
- `definition`;
- `lemma`;
- `proposition`;
- `theorem`;
- `corollary`;
- `proof`;
- `figure`;
- `table`;
- `footnote`;
- `appendix_section`;
- `algorithm` or `computational_step`.

## Node fields

Each node should contain, when available:

| Field | Meaning |
|---|---|
| `id` | Stable identifier such as `S2.3-P04-S02` |
| `level` | Node type |
| `parent_id` | Containing unit |
| `order` | Order within parent |
| `file` | Source file |
| `start_line` / `end_line` | Source range |
| `page` | Compiled page when available |
| `text` | Full text or display |
| `summary` | One-sentence substantive summary |
| `role` | Primary rhetorical role |
| `inherits` | Object, question, or claim taken as given |
| `advance` | New reasoning performed |
| `yield` | Object or conclusion handed forward |
| `claims` | Claims made |
| `definitions` | New objects introduced |
| `assumptions` | Conditions used or stated |
| `formal_objects` | Equations, operators, estimands, variables |
| `terminology` | Key terms |
| `scope` | Local/global, benchmark/general, fitted/structural, etc. |
| `confidence` | Confidence in semantic classification |
| `flags` | Potential issues |

## Primary rhetorical roles

Use one primary role and optional secondary roles:

- `problem`;
- `motivation`;
- `roadmap`;
- `setup`;
- `definition`;
- `assumption`;
- `derivation`;
- `formal_result`;
- `interpretation`;
- `evidence`;
- `identification`;
- `estimation`;
- `validation`;
- `qualification`;
- `comparison`;
- `application`;
- `robustness`;
- `extension`;
- `synthesis`;
- `transition`;
- `conclusion`.

## Edge classes

### Structural edges

- `contains`: parent contains child;
- `sequence`: adjacent units at the same level;
- `cross_reference`: explicit equation, section, figure, table, footnote, or appendix reference;
- `citation_support`: literature reference supporting a claim.

### Argument edges

- `motivates`;
- `poses_problem_for`;
- `defines_for`;
- `assumes_for`;
- `derives`;
- `substitutes_into`;
- `differentiates_to`;
- `aggregates_to`;
- `projects_onto`;
- `specializes`;
- `generalizes`;
- `decomposes`;
- `interprets`;
- `qualifies`;
- `contrasts_with`;
- `validates`;
- `tests`;
- `applies`;
- `uses`;
- `supports`;
- `resolves`;
- `hands_off_to`;
- `returns_to`;
- `duplicates`;
- `interrupts`.

## Edge fields

| Field | Meaning |
|---|---|
| `source` | Source node ID |
| `target` | Target node ID |
| `edge_class` | Structural or argument |
| `relation` | Relation label |
| `explicitness` | `explicit`, `implicit`, or `absent` |
| `evidence` | Short text explaining the relation |
| `shared_object` | Object carried across the edge |
| `condition_preserved` | Yes, no, or uncertain |
| `terminology_preserved` | Yes, no, or uncertain |
| `strength` | Strong, adequate, weak, broken |
| `confidence` | Classification confidence |
| `issue` | Reason for weakness |
| `repair` | Proposed transition or structural move |

## Sequence-edge audit

For every sequential edge, answer:

1. What is the source node’s yield?
2. Does the target node inherit that yield?
3. If not, does the target state a legitimate reason for changing topic?
4. What exact relation links the nodes?
5. Is the relation linguistically marked?
6. Are conditions and terminology preserved?
7. Does the target advance rather than repeat?

## Weak-edge criteria

Flag an edge as weak or broken when one or more hold:

- target introduces a new object without motivation;
- source raises a question that target ignores;
- target uses a result not produced by source or another visible dependency;
- connective word overstates the logical relation;
- a scope condition disappears;
- terminology changes without transformation;
- the target repeats setup instead of using the source result;
- a branch begins without a return path;
- a figure, table, or appendix appears without integration;
- a paragraph’s opening has no clear backward referent;
- a sentence’s conclusion requires an unstated premise.

## Orphan criteria

Potential orphan nodes include:

- no incoming argument edge other than containment;
- no outgoing argument edge and no legitimate terminal role;
- very short paragraph with weak sequence edges on both sides;
- equation or theorem never interpreted or used;
- appendix section not cited or connected to a main-text claim;
- footnote containing an essential premise;
- figure or table not used to support an inference.

Do not classify an abstract, title, standalone transition, or genuine concluding sentence as an orphan merely because it has low degree.

## Branch analysis

Identify the paper’s main spine, then classify secondary paths:

- necessary derivation branch;
- interpretation branch;
- robustness branch;
- special-case branch;
- literature branch;
- policy branch;
- obsolete or disconnected branch.

For every branch, identify:

- entry node;
- reason for branching;
- branch output;
- return node;
- whether the return changes the main argument.

A branch without a clear return is a priority review target.

## Recommended outputs

For long manuscripts, create:

- `reasoning_nodes.csv`;
- `reasoning_edges.csv`;
- `reasoning_graph.json`;
- `reasoning_graph.graphml`;
- `reasoning_map.md`;
- `weak_edges.csv`;
- `orphan_nodes.csv`.

The human-readable review should summarize:

- paper-level spine;
- section contracts;
- highest-priority weak edges;
- repeated subgraphs;
- orphan nodes;
- branches that displace the central argument.

## Graph use after revision

After editing:

1. rebuild or update the graph;
2. compare weak-edge count and severity;
3. ensure moved nodes have updated parents and references;
4. check that branches now return;
5. check that no edit created a new orphan;
6. verify that the central spine remains faithful to the manuscript’s substantive claims.

Do not optimize a numeric connectivity score at the expense of legitimate complexity. The graph is an audit instrument, not the objective function.
