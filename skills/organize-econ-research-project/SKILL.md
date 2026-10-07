---
name: organize-econ-research-project
description: Audit, initialize, or refactor an economics research project into a task-based, reproducible, portable, modular, dependency-aware, and version-controlled workflow. Use when the user asks to organize a research folder, onboard a coauthor or RA, build a Make/targets pipeline, separate raw and derived data, add a logbook or task structure, trace which code creates each result, or make an economics replication package easier to run. Use reproducible-data-pipeline for executing data jobs and repo-intake-cleanup for general repository cleanup.
---

# Organize an Economics Research Project

## Evaluation Standard

Audit the project on five dimensions:

1. **Replicability:** Can final results be rebuilt from documented inputs?
2. **Portability:** Can a new machine or collaborator start without hidden local state?
3. **Modularity:** Can one task run from declared inputs without understanding the whole project?
4. **Dependencies:** Is the order from raw data to paper output explicit and automated?
5. **History:** Can one explain when, why, and by whom a result changed?

## Workflow

1. **Inventory without moving files.** Identify raw data, external inputs, code, intermediate products, final outputs, paper/slides, environments, secrets, and generated artifacts. Check Git state first and preserve user changes.
2. **Map result ownership.** For every paper table, figure, statistic, and model output, identify the task and command that produces it. Mark orphaned outputs and manual steps.
3. **Define tasks.** Give each task declared inputs, code, outputs, parameters, validation checks, and a responsible owner. Prefer task boundaries that allow parallel work.
4. **Build the dependency graph.** Use Make, targets, Snakemake, a project CLI, or the existing build system. Avoid a monolithic master script when distinct tasks have distinct inputs.
5. **Separate states.** Keep immutable/raw inputs, cleaned data, intermediate data, final results, and presentation artifacts distinct. Never edit raw data in place.
6. **Record provenance.** Pin external versions or hashes, capture environment requirements, keep sanitized query metadata, and document exact commands.
7. **Test from a clean state.** Run the cheapest end-to-end path in a temporary or clean checkout. Verify schemas, keys, aggregates, figures, and manuscript links.
8. **Support collaboration.** Use issues/tasks for assignment, small reviewable changes, pull requests when appropriate, and a concise logbook of designs, decisions, failures, and results.

## Recommended Task Contract

```yaml
task: build_trade_panel
inputs:
  - data/raw/census/*.csv.gz
code:
  - code/build_trade_panel.py
outputs:
  - data/derived/trade_panel.parquet
checks:
  - unique: [month, port, country]
  - coverage_min: 0.95
command: make trade-panel
owner: initials
```

## Guardrails

- Do not reorganize a dirty project before mapping current ownership and dependencies.
- Do not commit credentials, machine-specific paths, large licensed data, or disposable build files.
- Do not treat notebooks with hidden execution order as the only production pipeline.
- Do not claim reproducibility after running only the final script on prebuilt intermediates.
- Preserve licenses and source attribution for templates, code, and data.

## Deliverable

Provide a current-state map, severity-ranked gaps, proposed task graph, conservative migration sequence, build commands, validation gates, and onboarding instructions. Implement only after identifying canonical files and preserving existing work.

Read `references/sources.md` for the Dingel/Gentzkow-Shapiro provenance of this workflow.

