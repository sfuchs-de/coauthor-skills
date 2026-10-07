# A coauthor's guide to GitHub and Dropbox

This is a practical default for a research team. Follow the project's own `README` and
`AGENTS.md` first. Examples use `main`, `origin` and a short-lived working branch; substitute the
actual project names. Do not run commands with unresolved example filenames.

## 1. What goes where

| Place | Purpose | Usually contains |
|---|---|---|
| GitHub repository | Shared, reviewable history | Code, manuscript sources, environment files, tests, task instructions and small approved outputs |
| Local clone | Your editing and computing workspace | A copy of the repository plus ignored local configuration and temporary outputs |
| Private Dropbox project folder | Authorized data and retained artifacts | Versioned input snapshots, references and selected run/results bundles |
| Overleaf, when used | The agreed manuscript editor | Only the manuscript sources explicitly assigned to it |

Keep a Git clone outside cloud-sync folders. Each person and machine uses its own clone; do not
share one `.git` directory through Dropbox. Run computations on a local or agreed compute machine
against a pinned input snapshot, not against files that another person is actively syncing.

Agree which location owns each manuscript file. If Overleaf is authoritative, use `overleaf-sync`
to reconcile before publishing. Do not create two independently edited copies without a plan.
Never put credentials, private referee reports or restricted observations in GitHub. A private
repository still needs content and license review.

## 2. Save, commit, push, merge: four different things

| Action | What it does | What it does not do |
|---|---|---|
| Save | Writes edits to your local files | Create a Git checkpoint or share changes |
| Commit | Records the selected changes in local Git history | Upload them; protect untracked or ignored files |
| Push | Uploads committed changes to a GitHub branch | Merge them into the agreed version or deploy an app |
| Merge | Integrates a reviewed branch into another branch | Prove the science, sync Dropbox or deploy unless configured |

Save frequently. Commit when you have a meaningful, reviewable checkpoint. Push when you want a
remote backup or review and the project's policy permits it. An unfinished branch can be pushed
and marked as a draft PR if the team allows it; label what is incomplete. Do not treat Git as the
only backup: uncommitted work, licensed data and local configuration need separate protection.

For an AI assistant, permissions are narrower: “edit this” does not mean “commit and push.” Say
explicitly which actions you want. A standing project agreement may set a routine, but the assistant
must not infer publication, invitations or data sharing from the existence of this handbook.

## 3. First-time setup

1. Get the repository link and, for a private repository, accept the owner's invitation. Public
   read access does not give permission to push; contributors without write access can use a fork
   and PR. Do not request write access merely to download these skills.
2. Sign in with your own GitHub account. Install GitHub Desktop for a visual workflow, or Git and
   your preferred editor for command-line work. Keep authentication in the operating system's
   credential manager; never put a token in a clone URL or project file.
3. Clone into a local folder outside Dropbox/iCloud/OneDrive. Read the README, project instructions,
   latest handoff and data-access instructions before editing.
4. Install the declared environment and obtain only the authorized data snapshot. Check its
   manifest/hashes and run the project's small example or smoke test.
5. Confirm the default branch, reviewer, expected checks and authoritative manuscript location.
   Missing access or instructions are questions to resolve, not reasons to invent a substitute.

For the toolkit itself, follow its root README and selective installer. Installing skills does
not grant access to any coauthor's research repository, Overleaf project or Dropbox folder.

## 4. Daily routine with GitHub Desktop

At the start, choose the correct repository and inspect **Changes** and **Current branch**. If
you have unfinished edits, preserve them before changing branches or integrating updates. Click
**Fetch origin** to learn about remote changes; fetching alone does not change your working files.
When the appropriate branch is clean, use **Pull origin** to bring it up to date. Stop if Desktop
reports conflicts or divergence rather than discarding edits to make the warning disappear.

For a new task, create a short branch such as `alex/revise-introduction` from the updated default
branch. Make and save your edits. In **Changes**, review each diff and select only intended files.
Write a specific summary—“Clarify iceberg-cost assumption”—and commit to the working branch.
Run the required local checks before **Push origin** or **Publish branch**. Create a pull request
with a short explanation, tests, data snapshot and anything needing a research decision.

After review and merge, fetch and pull the default branch while clean. Keep the old local branch
until its work is safely merged; delete it only when no unique work remains. Button names and
permissions can vary: consult the current official Desktop instructions linked below.

## 5. The same routine at the command line

### Start a new task from a clean, up-to-date main branch

```sh
git status --short --branch
git fetch origin
# Continue only after preserving local work and confirming main is the agreed default.
git switch main
git pull --ff-only origin main
git switch -c alex/revise-introduction
```

`--ff-only` refuses an update when local and remote histories have diverged. That is a useful
stop signal, not an error to fix with a hard reset. Inspect and agree a reconciliation instead.
To resume an existing working branch, switch to that branch only when safe; do not create a new
one or pull `main` into it blindly. After fetching, compare its upstream and current base first.

### Review and save a local checkpoint

```sh
git status --short --branch
git diff -- paper/introduction.tex
git add -- paper/introduction.tex
git diff --cached
git diff --cached --check
git commit -m "Clarify the introduction's contribution"
```

The staged diff is the exact content being committed. Inspect it for accidental data, unrelated
edits and secrets. Avoid `git add .` as a routine in mixed code/data folders. Review untracked
files explicitly: ordinary `git diff` does not include them. New ignore rules do not remove files
that are already tracked. Use the project's approved output policy, not a blanket ban on every PDF.

### Share for review

Run the documented tests/build and check the rendered result when relevant. Fetch once more and
resolve meaningful base movement before sharing. When ready and authorized:

```sh
git push -u origin alex/revise-introduction
```

Open a PR to the agreed base. State the problem, the change, checks run, remaining uncertainties
and the pinned data/run references. A coauthor reviews the diff and scientific substance. Merge
only under the team's agreed permission and review rules. After merge, update clean local `main`.

### If main changed while your branch was in progress

With your own work safely checkpointed and the tree clean, an agreed conservative approach is
`git fetch origin` followed by `git merge origin/main` on the working branch. Inspect conflicts,
run checks again, then publish the updated branch when authorized. A merge preserves shared
history. Do not rebase a shared branch or force-push as the default update procedure.

For a fork, distinguish `origin` (your fork) from `upstream` (the shared repository); follow the
official fork instructions below instead of assuming `origin/main` is the team's latest branch.

## 6. Conflicts and mistakes

- **Overlapping edits:** a conflict marker is not a scientific decision. Read both changes and
  understand the common base. Ask the relevant coauthor about incompatible model, sample,
  estimate or interpretation changes. Stage a deliberate resolution, test and review it.
- **Cannot pull or push:** inspect branch/upstream and local status. A rejected non-fast-forward
  push often means someone else updated the branch. Fetch and reconcile; do not force-push.
- **Wrong file staged:** `git restore --staged -- path/to/file` removes it from the next commit
  without discarding the working edits. This is different from `git restore path/to/file`, which
  can discard edits. Do not use the latter casually.
- **Bad change already shared:** propose a new correcting/revert commit after reviewing its
  dependencies. Do not erase shared history. A merge revert requires special care.
- **Secret accidentally committed:** stop publishing, revoke/rotate the secret through the
  provider, and contact the owner for a controlled cleanup. Deleting the current file does not
  remove it from Git history or make the secret safe again.
- **Large/restricted data accidentally tracked:** stop and review permissions/history before
  publication. Ask the owner how to migrate it; do not blindly rewrite the collaboration history.

If you are stuck, preserve the folder and tell the team the branch, status and last safe commit.
Send sanitized errors—not credentials or whole environment dumps. An assistant should explain
the proposed recovery and its data-loss risk before any destructive action.

## 7. Dropbox data and result conventions

Use the approved project area, with access set deliberately. A useful layout is
`source-snapshots/`, `prepared-snapshots/`, `references/`, `runs/` and `releases/`. Do not restructure
an existing shared folder just because these names are suggested.

Treat raw/source snapshots as immutable. If inputs change, create a new snapshot ID and manifest;
never replace bytes under an old ID. Record relative paths, sizes, hashes, source revisions and
access/license restrictions. Pin the reviewed manifest hash in Git where its metadata is safe.
Acquire and validate the selected snapshot before computation, keeping a local vault outside sync.
Dropbox's provider content hash is not ordinary SHA-256; label the algorithm accurately.

Create a new run folder for each scientific run and retain code commit, data snapshot, environment,
parameters and checks together. Upload selected retained results only with the agreed permission.
Do not overwrite another coauthor's run or claim reproducibility from a folder's existence.
For full asset-to-result tracing, use `build-asset-replication` and its contract checker.

## 8. What to agree as a team

Record the following in the project's existing instructions, not in this toolkit:

- Repository owner/visibility, default branch, reviewers and who can merge.
- File ownership when work overlaps, and how scientific disagreements are decided.
- Authoritative manuscript location and how Overleaf changes are reconciled.
- Allowed committed outputs, excluded private/licensed data and Dropbox access.
- Environment, minimum local checks, compute host, data snapshot and run naming.
- Whether local checkpoint commits/draft PRs are routine, and explicit AI publication permissions.
- Backup responsibility, end-of-session handoff and how interrupted work is resumed.

One person/agent writes in a checkout at a time. Separate clones or worktrees can support parallel
work, but the authors still need to reconcile overlapping files and conclusions.

## 9. Useful requests to your AI assistant

> Catch up on this repository. Inspect local changes and remote updates, then explain what needs
> reconciling. Do not edit, commit, push or change data.

> Update the clean working branch from its agreed upstream, preserving my work. Stop on divergence
> or a scientific conflict. Then revise Section 2 and run the existing checks. Do not commit or push.

> Save the reviewed files in a local checkpoint commit. Do not push; leave unrelated edits alone.

> Publish this reviewed change on its working branch and open a PR. Do not merge, change sharing
> or upload data. Include the checks actually run and remaining uncertainties.

> Prepare a GitHub-code/Dropbox-data coauthor package. First inventory sources and permissions;
> propose the exact repository, data snapshot and destinations before external writes.

## 10. End-of-session checklist

Save your files; inspect staged, unstaged and untracked work; run the applicable checks. Create a
checkpoint or remote review only under the agreed authority. Record what changed, what is still
open and where to resume. Include code commit, data snapshot and run IDs when relevant. State
plainly whether the work is only saved, committed, pushed, merged or deployed.

## Official references

- [GitHub Desktop cloning](https://docs.github.com/en/desktop/adding-and-cloning-repositories/cloning-and-forking-repositories-from-github-desktop)
- [Updating a pull request branch](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/keeping-your-pull-request-in-sync-with-the-base-branch)
- [Fork synchronization](https://docs.github.com/en/pull-requests/how-tos/work-with-forks/syncing-a-fork)
- [Git pull and fast-forward-only updates](https://git-scm.com/docs/git-pull)
- [Git restore: index versus working-tree changes](https://git-scm.com/docs/git-restore)

Provider features and policies change; verify current official guidance during live setup. This
handbook is a collaboration default, not permission to change a team's accounts or repository rules.
