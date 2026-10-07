---
name: gh-local-first
description: Minimize GitHub Actions consumption while preserving safe repository publication. Use whenever Codex implements repository changes that may later be committed, pushed, reviewed, or merged; prepares or publishes a pull request; chooses local versus remote verification; batches iterative agent work; audits excessive Actions usage; or redesigns CI for a smaller GitHub footprint. Especially useful for private repositories and repeated Codex edits. Coordinate publication with github:yeet and failing checks with github:gh-fix-ci when those skills are available.
---

# GitHub Local-First

Treat the local workspace as the iteration and verification surface. Use GitHub for durable publication, review, and the smallest independent release gate that matches the risk.

## Authority and routing

- For explanation, review, audit, or diagnosis, remain read-only apart from disposable local diagnostics.
- Local implementation does not authorize a push, PR, merge, workflow edit, runner registration, or billing change.
- Publish only when the user explicitly asks to commit, push, open a PR, merge, deploy, or otherwise update GitHub.
- Do not weaken required checks, change branch protection, use CI-skip markers, register a self-hosted runner, or make a private repository public without explicit authorization.
- If `github:yeet` is available, use it for the final commit/push/PR sequence after this skill's local gate.
- If a GitHub Actions check fails, use `github:gh-fix-ci`: inspect logs, report the root cause, propose a focused fix, and obtain approval before repair.
- Preserve dirty user work. Use a clean integration worktree rather than rebasing, stashing, resetting, or bulk-committing an unrelated working tree.

## Operating modes

1. **Work locally** — implement and verify without generating remote runs.
2. **Publish once** — create one coherent remote branch and one PR after local acceptance.
3. **Audit footprint** — quantify run frequency and duration, then recommend proportional changes.
4. **Design CI** — reduce redundant triggers and expensive stages without eroding the release gate.

## Local-first workflow

### 1. Resolve scope and repository rules

- Read applicable `AGENTS.md` files and repository instructions.
- Inspect `git status -sb`, remotes, branch/worktree state, and `.github/workflows/`.
- Separate requested files from unrelated user changes before editing or staging.
- For a usage audit, run:

  ```bash
  python <skill-dir>/scripts/audit_actions_usage.py --repo <repo> --days 30
  ```

  Treat the reported duration as observed workflow wall time, not an exact billing statement. Use GitHub's billing report when exact billed usage is required.

### 2. Classify change risk

Choose the smallest verification tier that would catch a plausible defect:

| Change class | Default local gate | Remote gate |
|---|---|---|
| Prose or documentation only | link/schema/format checks that exist | optional or lightweight |
| Vault, task, date, or generated-view change | schema, privacy, sync/render, deterministic diff | lightweight consistency gate |
| Backend or library code | targeted tests, then full relevant test suite | unit/integration gate |
| Frontend code | unit tests and production build | unit/build gate |
| Server, workflow, security, release, or broad UI change | full suite, build, and relevant E2E | full independent gate |

Repository-specific instructions and risk override this table.

### 3. Iterate without remote runs

- Start from a clean branch or clean integration worktree based on current `origin/main`.
- Keep intermediate fixes local. Do not push merely to save progress or ask GitHub to discover errors that local tools can detect.
- Run targeted checks while editing; run the selected acceptance gate once the coherent change is complete.
- Batch related changes into one publication unit. Split genuinely independent or high-risk changes into separate PRs.
- Before publication, inspect the complete diff, run `git diff --check`, and verify generated files deterministically when applicable.

### 4. Publish once

- Fetch the remote and confirm the branch still has the intended base.
- Resolve base movement locally before publishing; never rebase a dirty user worktree.
- Stage explicit paths and commit intentionally.
- Push once after local acceptance, then open one ready PR unless a draft is requested or review is genuinely incomplete.
- Avoid follow-up pushes for formatting, generated artifacts, or predictable test failures: catch those locally first.
- Wait for the required remote gate. Merge only when authorized and green.
- After merge, update the clean local `main`, remove the merged feature branch when safe, and verify `HEAD == origin/main` with a clean status.

## Designing a smaller workflow

Apply reductions in this order:

1. Add branch-scoped concurrency with `cancel-in-progress: true` so superseded pushes stop consuming minutes.
2. Eliminate duplicate full PR and post-merge runs when the PR gate already tests the merge result and no deployment follows the main push.
3. Keep an always-available `workflow_dispatch` full suite for exceptional verification.
4. Make expensive steps conditional on changed components. Content-only changes should not install browsers or build unrelated applications.
5. Cache dependencies with the official setup actions when the cache is safe and useful.
6. Keep one job when splitting would only duplicate setup and billing overhead; split only for meaningful parallelism or independent required gates.
7. Consider a self-hosted runner only after simpler reductions, and only with explicit approval and an isolated security design.

Do not naively attach path filters or skip markers to a required workflow: skipped required checks can remain pending. Prefer an always-created lightweight gate with conditional expensive steps, or update branch-protection requirements together with the workflow.

Read [references/workflow-patterns.md](references/workflow-patterns.md) before editing a workflow, configuring branch protection, or proposing a self-hosted runner.

## Completion standard

Report:

- local checks run and their results;
- number of pushes and remote runs created;
- PR and merge status when publication was authorized;
- whether clean local `main` matches `origin/main`;
- any preserved dirty checkout or unverified billing assumption;
- any non-blocking CI warning that remains.

