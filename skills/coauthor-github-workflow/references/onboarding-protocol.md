# Coauthor onboarding: one stage at a time

Use this with Claude Code or Codex in the collaborator's own local workspace. Paste one prompt,
review the result, then proceed. Do not paste the entire sequence as an unattended setup job.
Project instructions take precedence over these examples. Replace placeholders with confirmed
values before running commands; the agent should ask rather than invent a missing value.

Skills supply instructions, not authentication, data rights, dependencies or another person's
connectors. No stage authorizes account sharing, invitations, paid services, remote uploads,
commits, pushes, merges or manuscript synchronization. Installations and local file changes are
limited to the stage explicitly requested. Do not weaken permissions to make setup succeed.

## Owner's setup card

Fill this in and keep the completed version in the private project's existing documentation:

| Item | Agreed value |
|---|---|
| Project repository and visibility | `<PROJECT_REPO_URL>`; private/public |
| Default branch, reviewer and merge authority | `<DEFAULT_BRANCH>`; `<REVIEWER>` |
| Code authority | Repository and current version to use; preserved legacy copies |
| Manuscript authority | GitHub / Overleaf / other; file ownership and agreed entry points |
| Data access | Approved shared area; rights contact; exact snapshot IDs and manifest paths |
| First pilot | `<SMALL_TASK>`; expected output, checks, disk/time budget |
| Environment | Lockfiles, supported platforms, optional licensed tools |
| Readiness limits | Missing inputs, unpublished repairs, untested platforms or upstream steps |
| Daily agreement | Branch naming, checks, handoff location, output policy and AI permissions |

No tokens, authenticated URLs or personal machine paths belong in this public protocol. A private
project card may record useful access pointers, but never secrets or copied account sessions.

## Stage 1 — inspect the machine and existing folder

```text
Help me onboard to this research project using the setup card below. Inspect first; do not
install, move, delete, overwrite or publish anything. Identify my operating system, current
folder, existing Git checkout and common Git directory, dirty/untracked files, available tools
and known Dropbox/iCloud/OneDrive roots. Read applicable project instructions and shared memory.

Preserve existing work. Recommend a local checkout, environments, caches and run directory
outside all synchronized folders, with authorized data separate. A worktree is not isolated if
its common Git directory remains in a sync folder. On Windows, assess the project's supported
native/WSL setup rather than claiming an untested platform works.

Give me a short path/access plan, questions that block it, and the smallest next setup stage.
Do not display secrets, raw credential-bearing remotes or whole environment dumps.
[Paste the completed setup card here.]
```

**Continue when:** the working location is agreed and existing work is accounted for. Never erase
an old folder merely because a clean clone exists elsewhere.

## Stage 2 — install the small collaboration toolkit

```text
Set up the public sfuchs-de/coauthor-skills toolkit in its own tools folder, separate from the
research checkout and outside synchronized folders. Clone https://github.com/sfuchs-de/coauthor-skills
if needed; preserve any existing copy. Record the checked-out commit, read its README, AGENTS.md
and installer, and validate the package locally before executing its installer. Use Python 3.10
or newer. Do not add account permissions or install the entire writing library.

For Claude Code, preview with:
python3 scripts/install.py --agent claude --profile collaboration --dry-run
Then install that same profile without --replace. For Codex, use --agent codex instead.
If an existing skill differs, stop and show the conflict; do not overwrite it, delete it or
install a second discovery copy under a new name. Report the destination and installed skills.
Tell me to restart/refresh the agent session, then verify the skills are discoverable in the
new session. Do not change global permission settings, hooks or project files.
```

The profile includes seven skills: `coauthor-workflow`, `coauthor-github-workflow`, `overleaf-sync`,
`gh-local-first`, `agent-handoff`, `organize-econ-research-project`, `build-asset-replication`.
The installer copies their resources too. Do not combine the profile with an explicit `--skill`
list expecting a union: explicit selections replace the profile selection. Add writing skills
only when a later task needs them. Installation is distinct from discovery in a running session.

## Stage 3 — connect your own GitHub account and clone the project

```text
Use coauthor-github-workflow to connect my own GitHub account to the repository in the setup
card. Check whether I have accepted its private-repository invitation and which permissions I
actually have. Use an existing secure credential manager or guide me through the provider's
own authentication screen; never request a token in chat or embed one in a remote URL.

Clone the agreed repository into the agreed local location if absent. If a checkout already
exists, inspect it and fetch safely; preserve dirty and untracked work and stop on divergence.
Do not silently reset, stash, rebase or substitute an older fork. Read README, AGENTS.md,
CLAUDE.md, the current coauthor guide, data instructions and shared memory when present.
Report the branch/commit, default branch, reviewer, manuscript authority and project-local
skills. Do not edit research, commit, push, request access or invite anyone.
```

**Continue when:** the intended repository is authenticated and reachable. Public toolkit access
does not establish private project access, write permission or the coauthor's Dropbox access.

## Stage 4 — select and verify authorized Dropbox inputs

```text
Use the project's data-access guide and manifests to find the inputs for the first small pilot.
Confirm my own Dropbox access, the exact snapshot IDs and their licensing/sharing permissions
before copying restricted files. A shared-folder invitation does not establish redistribution
rights. Download or make available offline only the authorized, task-relevant subset after
estimating disk use; do not fetch a full vendor archive or restructure the shared folder.

Keep source and frozen derived inputs immutable, including folders named output_generated or
results_saved when the manifests classify them as inputs. Verify readable bytes against the
existing trusted file sizes and SHA-256 hashes. A cloud listing or offline icon is not a hash
check. Dropbox content_hash and ordinary SHA-256 are different algorithms.

Report missing, changed or unauthorized inputs separately. Never pin the observed hash merely
to make verification pass, substitute another vintage or upload data/results into GitHub.
Do not change snapshot manifests, access permissions or anyone else's data.
```

## Stage 5 — configure only the required local runtimes

```text
Set up the runtimes needed for the agreed first pilot from the project's existing lockfiles
and documented commands. Use isolated local environments outside sync folders. Inspect setup
scripts before running them; do not upgrade all packages, change locks, install paid tools or
alter model parameters as an installation workaround. Optional Stata/TeX/R/Julia tools are
needed only for tasks that use them. Package downloads belong in environment setup, not runs.

Create/update only the project's ignored local configuration with my resolved data, work,
cache and runtime paths. Verify it is ignored and not already tracked before saving absolute
paths. Check physical paths, symlink escapes and all known sync roots. Keep credentials in
secure stores, not configuration files. Preserve existing local settings and report conflicts.

Run the documented read-only preflight or doctor after inspecting its behavior. Report what
is configured versus actually tested, and list unsupported platforms or missing dependencies.
Do not launch a model, rewrite scientific settings, commit or publish.
```

A preflight check is not a sandbox. Inspect actual generators' write paths; a declared environment
variable cannot redirect a hard-coded path that the program does not read.

## Stage 6 — a cheap test, then an agreed reproduction pilot

```text
Inspect the documented cheap smoke test and its outputs/network behavior, then run it in a
fresh local destination within the agreed budget. Preserve failures and logs. Report exactly
whether it is synthetic/unit testing, saved-result rendering or real prepared-input computation.
Do not label setup as full replication.

Next propose one substantive figure/table task using the verified inputs: exact command,
code revision, snapshot IDs, environment, new run path, expected checks, runtime and disk
estimate. Wait for my approval before that data-backed or expensive computation. Do not run
a full rebuild, start unattended jobs or use a paid API fallback. Do not loosen checks, tune
parameters or overwrite failed runs to obtain expected numbers.
```

After approving the pilot, retain its code identity, input hashes, settings, environment, command,
diagnostics and output checks in the project's existing run records. A saved-data comparison
does not establish reconstruction from raw sources; an independent coauthor pilot is its own gate.

## Stage 7 — optional manuscript/Overleaf access

Skip this if the collaborator only works on code or data.

```text
Use overleaf-sync to set up my own access to the agreed manuscript project. Confirm the live
manuscript authority and current entry points; distinguish it from frozen replication snapshots.
Check whether my account/project supports Git integration, without starting a paid subscription.
Use my own securely stored token through the provider authentication prompt, never in chat,
source files or a credential-bearing remote URL. Use a separate local clone outside sync folders.

Fetch and compare only; do not edit, commit, push or upload broad directories. Preserve existing
local changes and coauthor markup. If compilation is wanted, first identify the build commands
and required inputs. Access, compilation, scientific validation and successful synchronization
are different states. Do not turn an immutable paper snapshot into a competing editing copy.
```

## Stage 8 — agree the daily workflow and finish the handoff

```text
Summarize our ready-to-use workflow using coauthor-github-workflow and agent-handoff. At session
start, inspect the actual checkout, current instructions, shared memory and other active writers;
fetch safely and explain drift before integrating it. Use a short-lived working branch from the
agreed current base, never someone else's unfinished branch without permission.

For each task, save locally, test the affected code/results and keep runs separate from inputs.
At session end, review staged/unstaged/untracked changes and update existing shared memory and
the handoff log. If none exists, offer a setup; do not create an alternative memory system silently.

Prepare a concise readiness report: repo/branch/commit, account reachability, data rights and
hash verification, runtimes, checks actually run, known gaps and the next pilot. Do not commit,
push, merge, upload results or sync Overleaf. State saved, committed, pushed, merged and deployed
separately. Never claim the next collaborator has access just because my machine does.
```

See the [daily GitHub/Dropbox handbook](coauthor-handbook.md) for GitHub Desktop and command-line
routines. Decide the team's policy explicitly; an AI editing request alone is not publication authority.

## Readiness checklist

- Intended repository, current base and preserved existing work identified.
- Own account access checked separately for GitHub, Dropbox and optional Overleaf.
- Skill installation and running-session discovery checked separately.
- Git/common directory, environments, caches and fresh runs outside every known sync root.
- Only approved task inputs obtained; trusted hashes verified; licensing gaps recorded.
- Exact required environment configured, with platform limits stated.
- Cheap test checked; substantive pilot proposed or run with its own authority and evidence.
- Manuscript ownership, review/merge rules, output policy and handoff location agreed.
- No credentials, private records or restricted data added to shared Git content.

## Later: request publication explicitly

```text
Review the intended files and local checks. If clean and within our project rules, commit only
those reviewed changes to my working branch, push that branch and open a pull request to the
agreed base. Include run/snapshot references, actual checks and open scientific questions.
Do not merge, change sharing, upload data/results or synchronize Overleaf.
```

That is an optional later request, not part of onboarding. Account configuration may change:
consult the current official [Claude Code skills documentation](https://code.claude.com/docs/en/skills),
[GitHub CLI authentication](https://cli.github.com/manual/gh_auth_login) and
[Overleaf Git setup](https://docs.overleaf.com/integrations-and-add-ons/git-integration-and-github-synchronization/git-integration)
when those stages are actually performed.
