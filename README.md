# Coauthor Skills

A portable collection of research-writing and collaboration skills for Codex and Claude Code.
It brings writing, reasoning graphs, mathematical audits, presentations, corpus-based vocabulary,
Overleaf synchronization, local-first GitHub work, and cross-agent handoffs into one repository.

Skills are instructions and tools—not account access. Every collaborator supplies their own
credentials and project permissions. This package contains no manuscripts, private review cases,
personal project registries, tokens, or downloaded source-paper text.

## Install

Clone this repository and use Python 3.10 or newer:

```sh
git clone https://github.com/sfuchs-de/coauthor-skills.git
cd coauthor-skills
python3 scripts/install.py --agent codex --dry-run
python3 scripts/install.py --agent codex
# Or install the same packages for Claude Code:
python3 scripts/install.py --agent claude
```

The installer copies skills, leaves unrelated installations alone, and refuses to replace a
different existing skill. `--replace` explicitly authorizes replacing selected skills, with a
timestamped backup outside active discovery. Restart or refresh your agent session after install.
Installing this repository does not automatically replace either older repository on GitHub.

Install a smaller group or an individual skill:

```sh
python3 scripts/install.py --agent codex --profile collaboration
python3 scripts/install.py --agent codex --profile writing
python3 scripts/install.py --agent codex --skill referee-report
python3 scripts/install.py --target-dir /path/to/isolated/skills --profile writing
```

Dependencies on other bundled skills are included automatically. The corpus package is substantial
because it preserves five verified inventories; use `--profile collaboration` if you only want sync
and handoff tools. Do not install duplicate copies under different folder names.

## Choose the right skill

| Area | Skills |
|---|---|
| Coordinate a coauthor workflow | `coauthor-workflow` |
| Coordinate writing stages | `econ-writing-suite` |
| Drafting and author-side review | `econ-write`, `theory-writing-refinement` |
| Mathematical checking and dependency graphs | `audit-tex-math`, `map-theory-dependencies` |
| Compile, inspect, convert and format | `academic-draft-review`, `render-mathdown-tex`, `research-note-tex`, `remarkable-move-render` |
| Independent referee work | `referee-report` |
| Style and spatial/trade/urban vocabulary | `stop-slop`, `ai-slop-lint`, `corpus-econ-writing` |
| Presentations and figures | `design-econ-seminar`, `review-slide-deck`, `fuchs-econ-slides`, `fuchs-bq-slides`, `format-econ-research-figures` |
| Overleaf | `overleaf-sync` |
| GitHub | `gh-local-first` |
| Switch between Codex and Claude | `agent-handoff` |

The 22 skills remain separate so the agent loads only the protocols needed for the current task.
The referee-report package retains its developed direct/staged workflows, revision rounds,
comment contract, empirical and quantitative-model preflights, fairness gates, and editor notes.
No confidential review reports are bundled.

## Everyday examples

**Review first, then revise:**

> Use coauthor-workflow on this paper. Catch up, then use econ-writing-suite to build the reasoning
> graph and propose a revision plan. Review only; do not edit or publish.

After reviewing the plan:

> Revise the introduction and model exposition. Preserve claims and estimates. Audit the affected
> derivations, compile and inspect the result, then record a handoff. Do not push.

**Use the spatial vocabulary library:**

> Use corpus-econ-writing on Section 2. Preserve technical meaning and my voice; use the urban
> exposition guidance and report unfamiliar terms. Do not replace an essential term just to pass.

Vocabulary attestation is not proof of semantic correctness. Strict checking is a distinct requested
gate, not a universal writing restriction. Source PDFs and extracted passages are not included.

**Safely work with coauthors on Overleaf:**

> Use overleaf-sync to fetch and compare this authenticated clone with my working copy. Report
> drift and conflicts. Do not edit, commit or push.

**Publish only when asked:**

> Use gh-local-first to run the relevant checks locally and prepare a coherent diff. Do not push.

Then separately authorize the commit/push or PR. Neither installing a skill nor approving a writing
plan authorizes publication, messages, bookings, account changes or additional tool access.

## Setup and detailed guides

- [Account and collaboration setup](docs/collaboration-setup.md): GitHub, Overleaf tokens, local
  LaTeX, project authority, and shared agent memory.
- [Staged draft refinement](docs/staged-draft-refinement.md): reasoning graph, diagnosis, revision,
  mathematical audit, compilation, prose cleanup and handoff.
- [Packaging and audit](docs/publication-audit.md): preserved resources, public-copy adaptations,
  excluded material and verification limits.
- [Third-party notices](THIRD_PARTY_NOTICES.md): retained licenses and source attribution.

Codex examples can use `$skill-name`; Claude Code can invoke the installed skill by its name or
slash command when supported. Product-specific connectors are not interchangeable: check available
tools instead of assuming that a skill gives either agent access to GitHub, Paperpile or Overleaf.

## Verify the package

```sh
python3 scripts/validate.py
python3 -B -m unittest discover -s tests -v
python3 -B skills/corpus-econ-writing/scripts/verify_package.py
```

Validation checks the manifest, skill metadata, bundled Markdown links, Python syntax, private
paths and credential-shaped content, including text stored in SQLite. It does not verify every
external link or prove mathematical/editorial correctness. Portable checker tests are separate
from evaluations of an agent's judgments. No paid API or GitHub Actions run is needed for these
local checks.

Updates are local-first. This repository is the new distribution collection; existing installed
skills and the earlier repositories are not changed automatically. Preserve an installation backup
and review package differences before choosing `--replace`.

## License

Original toolkit code and instructions are MIT licensed. Incorporated MIT notices remain beside
the relevant packages. Paper titles, bibliographic metadata and vocabulary evidence do not transfer
rights to the source papers; obtain those sources separately under their own terms.
