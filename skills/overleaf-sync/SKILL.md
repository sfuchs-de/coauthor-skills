---
name: overleaf-sync
description: Safely audit, pull, merge, compile, commit, push, and verify Overleaf Git projects when local and online coauthor edits may coexist. Use for Overleaf synchronization, drift checks, project migration, or confirming that local and remote copies match.
---

# Overleaf Sync

Synchronize Overleaf projects without overwriting local work or coauthor changes. An Overleaf sync is a merge operation, not a file upload.

## Invariants

- Prefer an existing authenticated clone. Never print, persist in source files, commit, or place an Overleaf token in a command-line URL.
- Never force-push, reset a worktree destructively, or replace the remote tree with a broad copy.
- Fetch before classifying changes and fetch again immediately before pushing.
- Preserve unrelated dirty files. Stage only the sources and assets intended for the requested sync.
- Do not commit TeX build artifacts unless they are already tracked or the user explicitly requests them.
- Treat remote renames and archival moves as intentional until inspection shows otherwise.

For authentication failures or a new clone, read [references/authentication.md](references/authentication.md). Configure paths in that project's local instructions; personal project registries are intentionally not distributed.

## Orient the Project

Identify:

1. the local editing copy, if distinct;
2. the Overleaf Git clone used for synchronization;
3. the remote branch;
4. the authoritative TeX root and bibliography;
5. any local deliverable copies outside the clone.

Some projects use the clone itself as the working copy. Others keep a separate local folder and copy selected files between it and the clone. Do not assume either layout. Check `README.md`, `.latexmkrc`, recent commits, and the root's `\input` or `\include` statements.

## Choose the Operation

- **Audit:** fetch, report divergence and dirty state, compare relevant files, and make no mutations.
- **Pull/merge:** incorporate remote changes into the working copy without pushing.
- **Full sync:** reconcile both sides, compile, commit selected changes, push, and verify.
- **New project or migration:** establish an authenticated clone first, then use the same guarded workflow.

If the user asks whether a project is synced, perform an audit at minimum. If the user asks to sync, carry the work through verification unless a genuine conflict requires their decision.

## Guarded Preflight

Run the bundled preflight helper or the equivalent commands:

```bash
bash <skill-directory>/scripts/overleaf_preflight.sh "<clone>" [branch]
```

The helper fetches the remote without printing its URL or credentials and reports `ahead`, `behind`, and worktree state. Interpret `HEAD...FETCH_HEAD` as follows:

| Ahead | Behind | Meaning | Action |
|---:|---:|---|---|
| 0 | 0 | Git histories aligned | Compare uncommitted/local-copy changes. |
| positive | 0 | Local commits only | Compile and re-fetch before push. |
| 0 | positive | Remote commits only | Inspect, then fast-forward or merge them locally. |
| positive | positive | Diverged histories | Inspect both ranges and merge; never force-push. |

Inspect remote movement before changing files:

```bash
git log --oneline --format="%h %an %s" HEAD..FETCH_HEAD
git diff --name-status HEAD FETCH_HEAD
git status --short
```

## Reconcile Changes

### Working directly in the clone

- Remote ahead and worktree clean: fast-forward when possible.
- Local ahead: retain the local commits, compile, re-fetch, then push.
- Diverged: inspect file-level changes and merge the remote branch explicitly.
- Dirty worktree plus remote movement: do not auto-stash. Classify the dirty paths first and preserve unrelated work.

### Separate local copy and clone

Compare only live source paths and required assets. For each path:

- remote changed, local unchanged since the last sync: copy remote to local;
- local changed, remote unchanged: copy local to clone;
- both changed: merge the changes by hand against a common base;
- remote renamed, moved, or archived: mirror that decision locally unless the user directs otherwise.

Use `git show <base>:<path>` for the common-base version. Compare binary assets with checksums. Avoid recursive copy commands that can resurrect archived sources or delete coauthor files.

## Compile and Inspect

Compile the live root locally before pushing. Prefer the project's existing build command; otherwise use:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error <root>.tex
```

If bibliography processing is not configured automatically, run the required BibTeX or Biber cycle. Check for:

- fatal errors or missing inputs;
- undefined citations or references;
- duplicate labels;
- materially overfull boxes;
- missing or stale figures.

For important paper or slide deliveries, also run `qpdf --check` and `pdfinfo`. An Overleaf compile timeout does not invalidate a successful local build; report the distinction.

## Commit and Push

1. Review `git status --short`.
2. Stage only intended paths.
3. Review `git diff --cached --stat` and, for text, `git diff --cached`.
4. Commit with a substantive message and `commit.gpgsign=false` when the environment lacks the user's signing key.
5. Re-run the guarded preflight immediately before push.
6. If the remote moved, stop and reconcile it. Otherwise push the current branch to the detected remote branch.
7. Fetch again and require zero divergence.

Do not use `git add -A` by default. Do not push generated PDFs unless they are deliberately tracked.

## Verification Report

Report:

- audit, pull-only, or full-sync mode;
- remote project and branch, without credentials;
- files moved in each direction or merged;
- commit hash and push result, if applicable;
- compile root, status, and page count;
- final ahead/behind counts;
- warnings or intentionally uncommitted files.

If nothing changed, say that the fetched remote, clone, and any separate local copies are aligned as of the reported commit.
