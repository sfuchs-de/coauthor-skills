# Reasoning-Graph Integration Cases

Use these cases for fresh-session behavioral tests of the shared graph contract.

| Case | Expected behavior | Prohibited behavior |
|---|---|---|
| Full-paper author audit | Initialize one workspace; let `econ-write` own the argument layer; route theory, math, and source findings to their owners; return a compact integrated diagnosis | Eight independent inventories with unrelated IDs |
| Three-paragraph cleanup | Skip the graph and use `ai-slop-lint:quick` | Create a workspace for ceremonial compliance |
| Theory dependency gap | Attach primitives, assumptions, closure, and result edges in the theory layer; hand an uncertain proof obligation to math audit | Mark the theorem verified through exposition review |
| Candidate derivation | Add a math-layer finding with `candidate` status and require an independent audit | Treat generation, compilation, or readability as verification |
| Verified repair | Record the repaired obligation and hand scope or terminology propagation to theory and author-writing owners | Silently change other layers |
| Compile and render | Attach file, label, page, build, and visual status in `source_qa` | Infer argument or proof validity from a successful build |
| Mathdown conversion | Map each source-owner result to one TeX-owner node and flag lost scope or provenance | Declare a preserved equation independently verified |
| Independent referee report | Rebuild a minimal temporary reviewer graph from submitted materials; consolidate related symptoms into fair comments | Import private author judgments or expose the raw graph in the report |
| Whole-paper prose rewrite | Anchor style findings to paragraph or sentence nodes and hand substantive breaks to their owner | Rewrite claim scope to improve fluency |
| Paper-to-talk projection | Map slides to accepted source nodes and record cuts, omissions, and backup branches | Strengthen slide claims beyond the source graph |
| Post-revision comparison | Rebuild structural nodes, reconcile changed IDs, resolve repaired links, and mark ambiguous anchors stale | Reuse obsolete IDs by guesswork |
| Invalid graph row | Fail validation for an unknown node, owner, status, severity, absolute private path, or inconsistent JSON/CSV inventory | Accept malformed cross-skill state |

## End-to-end prompt

> Use `$econ-writing-suite` on `main.tex`. Review only. Initialize one reasoning-graph workspace,
> recover the paper spine, map the model dependencies, audit the two load-bearing propositions,
> compile and inspect the manuscript, and return the three highest-priority integrated findings.
> Keep specialist findings in their owned layers and do not edit until I approve repairs.

The successful route is `econ-write:author-audit` → `theory-writing-refinement:map` →
`audit-tex-math:audit` → `academic-draft-review:compile`, with explicit handoffs and no raw-ledger
dump in the final answer.
