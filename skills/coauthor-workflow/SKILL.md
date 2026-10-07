---
name: coauthor-workflow
description: Coordinate a research coauthor workflow spanning manuscript development, shared agent memory, Overleaf synchronization and GitHub publication. Route substantive writing to focused specialists; use for multi-stage collaboration rather than a single narrow prose edit.
---

# Coauthor Workflow

Use the smallest set of installed specialists needed for the request. A shared repository
does not confer account access or authorize external actions.

## Start

- Read the project's instructions and shared status. Use `agent-handoff` for catch up when shared
  memory exists; do not import another person's transcript stores or create memory silently.
- Identify authoritative manuscript sources, any Overleaf clone, the build command, and the
  requested output. Preserve dirty work and check for another active writer before editing.
- Set the current authority: review only, propose changes, local edits, or explicitly authorized
  publication. A review or writing request does not authorize synchronization or pushing.

## Route

| Requested work | Owning skill |
|---|---|
| Multi-stage writing or uncertain specialist | `econ-writing-suite` |
| Author-side argument or revision | `econ-write` |
| Theory exposition | `theory-writing-refinement` |
| Mathematical correctness | `audit-tex-math`, with `map-theory-dependencies` when needed |
| Spatial/trade/urban diction and corpus evidence | `corpus-econ-writing` |
| Build, conversion or rendered QA | `academic-draft-review`, `render-mathdown-tex` |
| Independent referee work | `referee-report` |
| Talk narrative and delivery | `design-econ-seminar`; `review-slide-deck` for review-only work |
| Overleaf drift or authorized synchronization | `overleaf-sync` |
| Local GitHub verification and authorized publication | `gh-local-first` |
| Cross-agent continuity | `agent-handoff` |

Read a specialist's instructions before using it, then only its task-relevant references. Do not
load every skill or every corpus edition at once. Do not substitute author-side editing for an
independent referee report or import private author judgments into a reviewer assessment.

## Sequence

For substantial revision: inventory → shared reasoning graph → diagnosis → authorized local
revision → mathematical audit where consequential → compilation/rendered QA → restrained prose
pass → handoff. A candidate derivation still needs verification; formatting cannot change claims.

Use corpus guidance when the topic or vocabulary request warrants it. Strict vocabulary checking
is not automatic, and an attested word is not evidence that a claim is correct. Preserve essential
technical meaning rather than rewriting to obtain a lexical pass.

For explicitly authorized publication, let `overleaf-sync` own its remote guard and `gh-local-first`
own the GitHub gate. Avoid two agents or services writing the same remote concurrently. Do not
force-push, expose tokens, or resolve genuine coauthor conflicts by choosing a side silently.

## Finish

Report substantive changes, checks, unresolved conflicts and publication state separately.
Record a concise project-local handoff when appropriate, without credentials or confidential
review text. Never claim that installation proves access, compilation proves correctness, or a
successful push proves that an external collaborator has reviewed the result.
