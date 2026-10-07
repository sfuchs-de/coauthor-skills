# Workflow patterns

Use these as starting points, not blind templates. Inspect current branch protection and verify current GitHub documentation before changing a live workflow.

## PR-only gate with manual fallback

```yaml
name: QA

on:
  pull_request:
  workflow_dispatch:

concurrency:
  group: ${{ github.workflow }}-${{ github.head_ref || github.ref }}
  cancel-in-progress: true
```

This is the preferred solo-repository pattern when the pull-request event tests the proposed change against its current base and a main-branch push does not deploy anything. Keep `push: main` when it performs a distinct deployment, release, migration, or post-merge security action.

## One gate, conditional expensive steps

Prefer one required job that always exists and determines whether expensive stages are necessary. This avoids a required workflow remaining pending because the entire workflow was filtered out.

1. Fetch enough history to compare the pull request with its base.
2. Compute changed paths with repository-owned code or shell commands.
3. Export booleans such as `backend_changed`, `frontend_changed`, and `full_ci`.
4. Always run cheap invariant checks.
5. Guard dependency installation, builds, and E2E stages with those outputs.

Treat workflow files, lockfiles, security code, deployment code, and the change-detection logic itself as `full_ci`.

## Local verification contract

Expose one repository command such as `make qa`, `./scripts/qa`, or `pm.py qa` that Codex can run before publication. It should be deterministic and should not require GitHub credentials. Add narrower commands for rapid iteration, but keep one acceptance command that approximates the remote gate.

Generated artifacts require a two-pass test:

1. generate or render with any required pinned clock;
2. record the resulting diff or hash;
3. generate again;
4. confirm the diff or hash is unchanged.

## Caching

Use the official setup actions' package-manager caches when available. Key caches from lockfiles and runtime versions. Do not cache generated research outputs, secrets, mutable vault state, or files whose provenance would become ambiguous.

## Manual full CI

Keep `workflow_dispatch` for a complete remote run before an important release or after changing workflow logic. Do not schedule full CI merely to consume minutes regularly; schedule only when unattended regression detection has material value.

## Self-hosted runners

Use only with explicit authorization. Prefer a dedicated, disposable, least-privilege machine or VM for private repositories. Do not expose a personal workstation or NAS to workflows from untrusted forks. Restrict repository access, credentials, network reach, and runner labels; document shutdown and removal procedures.

## Billing and measurement

- Workflow wall time from `gh run list` is a diagnostic approximation, not the billing ledger.
- Exact usage may depend on plan allowances, runner type, rounding, retries, storage, and account ownership.
- For exact numbers, use the GitHub billing dashboard or authenticated billing API and state the reporting period.
- Set budgets and alerts independently of workflow optimization.

