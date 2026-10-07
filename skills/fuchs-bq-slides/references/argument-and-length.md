# Argument, Length, and Reasoning Graph

## Similar Length Means Similar Explanatory Depth

The reference's 45 main content slides have 72.5 minutes in the saved slide map. It also has
title/agendas/boundary frames, 121 main PDF pages after reveals, and 112 logical backup frames
that expand to 155 more pages. The appendix reflects accumulated research, not a necessary
ratio. Do not aim for 276 pages by inserting pauses or copying tangential material.

Use about 45 main slides for comparably rich theory-plus-empirical material and a long seminar.
For a 45-minute slot, about 22--28 substantive slides will often be more honest. A sparse note
may support only 12--20; explain that and avoid invented exercises. User timing overrides all
default counts. Count explanation and discussion time, not just words.

## Flexible 45-Slide Spine

| Module | Starting budget | Audience question |
| --- | ---: | --- |
| Motivation, difficulty, answer/contributions, related literature | 4 | Why this question, what changes, and how does it relate to existing work? |
| Intuition, setup, core results, implementation handoff | 10 | Why does the method work? |
| Setting, sources, measurement/calibration, raw evidence | 5 | What is actually observed or maintained? |
| Design, estimation, main results, mechanisms, checks | 17 | What do we learn, and how credible is it? |
| Structural/alternative comparison, extension/policy | 8 | What does the extra structure add? |
| Conclusion | 1 | What should the audience retain? |

These are functions, not mandatory headings. Pure theory can replace empirical/calibration
modules with examples, comparative statics, applications, or tests of assumptions. Omit policy
when the material has none. Do not manufacture three theorems to imitate the reference.

## Opening Contribution and Literature Sequence

The default opening is motivation/question → **This paper** → optional headline findings →
**Related literature** → first substantive agenda or section. Keep the traditional “This paper”
title: it states what the paper does, while a separate findings slide states what it learns.
Combine the two only if the shorter format remains legible. Literature follows that block
immediately, so the audience knows the contribution before hearing its intellectual context.
User-requested orders and unusually short formats take precedence.

On contribution and findings slides, use 2–4 short parent claims or topic labels, each followed
by 1–2 genuine subitems explaining the operation, evidence, magnitude or qualification. Do not
simulate hierarchy with bold prefixes followed by paragraph-length text. Keep parent and child
on the same reveal and retain their positions in the final-state handout. Avoid repeating the
same prose on “This paper” and findings slides.

Give the literature slide 2–3 relevant strands when the paper supports them. For each, name
representative papers and explain the specific connection or distinction in a short subitem.
Use the supplied manuscript's verified references; do not invent citations or novelty claims.
A dense footer bibliography is not a substitute for explaining how the paper relates to the
literature. Keep detailed comparison and additional references in backup when needed.

## Reasoning Order

1. Open with the general question; retain a few concrete motivating examples as children.
   Reach the difficulty quickly instead of spending many slides on the setting first.
2. State the contribution as input -> operation -> output, with the answer/magnitude when
   supported. Weak assumptions for one theorem do not make the whole procedure assumption-free.
   Follow the opening sequence above, including related literature before technical development.
3. Introduce a concrete diagram or scalar example. Explain each point, axis, pivot, and shift.
4. Establish the necessary objects/restrictions before each theorem or mapping. State what the
   theorem identifies and what it leaves unknown. Separate economic identity from empirical fit.
5. End theory with the exact quantities the application must measure, estimate, or calibrate.
   Reuse those names as the empirical section's tasks.
6. Present source/calibration transparency before estimates that depend on it. Put intermediate
   price/elasticity estimates before downstream welfare or policy outcomes when needed.
7. Show the full intended specification. Restricted alternatives belong in named comparisons,
   not silently in place of the main result. Present validation and unresolved tensions openly.
8. Show robustness as overlays on the principal exhibit where that preserves scale and sample.
9. Put additional identifying/model assumptions immediately before the extension they enable.
   Show policy outcomes near the end only when supplied and validated.
10. Conclude with the method's output, the result, and the important limit or implication.

For each transition, ask: what does the previous slide establish that makes the next necessary?
If no dependency or useful contrast exists, reorder, cut, or move the slide to backup.

## Portable Planning Schema

Keep `reasoning-graph.json` and `slide-map.json` beside the deck. Use stable IDs, not PDF page
numbers. The graph need not mirror every paragraph in the paper. A small graph with genuine
dependencies is better than a large taxonomy.

```json
{
  "nodes": [
    {
      "id": "producer-envelope",
      "kind": "result",
      "claim": "The optimized value has a local price derivative.",
      "inputs": ["competitive optimum", "fixed technology"],
      "outputs": ["local derivative"],
      "assumptions": ["interior optimum"],
      "source": "paper.tex: proposition 2",
      "status": "verified"
    }
  ],
  "edges": [
    {"from": "firm-setup", "to": "producer-envelope", "type": "requires"}
  ]
}
```

This schema fragment is illustrative, not a complete valid graph: add every referenced node.
Use `defines`, `requires`, `feeds`, `supports`, `checks`, and `contrasts` as distinct edge types.
Check that the definition/requirement/feed subgraph is acyclic; equilibrium feedback can be
explicitly represented as feedback rather than falsely ordered as a proof dependency.

The companion slide map:

```json
{
  "main_end_label": "bq_main_end",
  "slides": [
    {
      "label": "main_result",
      "title": "A Claim the Evidence Supports",
      "role": "main",
      "job": "Explain one inference.",
      "node_ids": ["producer-envelope"],
      "sources": ["paper.tex: proposition 2"],
      "evidence": "One equation and its economic interpretation",
      "minutes": 2,
      "reveals": ["setup", "cancellation", "implication"],
      "handoff": "Which observed outcome supplies this derivative?",
      "cut": "keep",
      "backup_labels": ["backup_derivation"]
    }
  ]
}
```

Main `role` counts substantive frames; use `navigation`, `title`, or `backup` for other entries.
Define a `bq_main_end` destination on the final main frame, not the first technical backup.
List planned backup and navigation frames when useful. Scripts check what the ledger contains;
the author must confirm it is comprehensive and each source really supports the claim.

## Appendix Selection

Include the questions a demanding audience is likely to ask: proof/cancellation, normalization,
identification threats, sample construction, calibration source tables, full regression output,
alternative specifications, comparison alignment, inference, model closure, and optimizer
checks. Give each appendix slide a question/job and a return destination. Avoid generic
unreferenced appendices. Keep historical outputs explicitly separate from current results.

## Timing

Allow roughly 1 minute for a clean fact, 1.5--2 for a mechanism/result, and 2--3 for a new
derivation, diagram, or regression. Reveals share the parent slide's allocation. Mark optional
cuts that preserve the main argument, and reconcile total minutes before delivery. Do not
solve an overlong talk by shrinking fonts or accelerating the speaker.
