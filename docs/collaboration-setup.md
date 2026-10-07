# Collaboration setup

## GitHub

For everyday coauthor use, start with the
[GitHub and Dropbox handbook](../skills/coauthor-github-workflow/references/coauthor-handbook.md).
It includes a visual GitHub Desktop route, command-line equivalents and explicit team agreements.

Install Git and the GitHub CLI if you want command-line repository access. Authenticate using
`gh auth login` or your operating system's credential manager. Check the authenticated account
and repository permissions without printing tokens or credential-bearing remote URLs.

Use `gh-local-first` to keep intermediate work and tests local. A normal implementation request
does not authorize commits, pushes, PRs, merges or deployment. Ask for publication explicitly when
ready. Avoid making a remote CI run the first way to discover a predictable local error.

## Overleaf

Each collaborator needs project access and their own Overleaf Git token. Confirm that Git
integration is available for the project; it can depend on the Overleaf subscription.

1. In Overleaf, open the project's Git integration and obtain its clone URL.
2. Generate a Git authentication token in your account settings.
3. Store it in macOS Keychain, Windows Git Credential Manager, or a secure Linux credential helper.
4. Clone with a credential-free URL. Use username `git` and enter the token only at the secure
   authentication prompt. Never paste it into a chat or put it in a remote URL.
5. Identify the source root, bibliography and existing build command in project instructions.

```sh
git clone https://git@git.overleaf.com/PROJECT_ID paper-overleaf
```

Do not use Git's plaintext credential store for an account-wide token. Configure credentials
locally, not in this repository. The installed skill includes an authentication reference and a
preflight helper. A successful fetch proves Git access, not successful compilation.

Overleaf guides: [Git integration](https://docs.overleaf.com/integrations-and-add-ons/git-integration-and-github-synchronization/git-integration),
[token authentication](https://www.overleaf.com/learn/how-to/Git_integration_authentication_tokens).
Check current provider documentation when configuring an account.

## Local manuscript setup

A practical arrangement is one editing folder and a separate authenticated Overleaf clone, but
working directly in the clone is also supported. Declare which files are authoritative; do not
keep two independently edited copies without an explicit reconciliation workflow.

Use your project's LaTeX toolchain, normally `latexmk` plus the required engine and bibliography
tools. Compilation and rendered inspection are not mathematical verification. Do not upload
generated PDFs or broad directory copies unless the project and requested workflow require them.

## Shared project memory

Use project-local instructions and a handoff log, not copied credentials or whole chat transcripts:

```text
paper/
  AGENTS.md
  CLAUDE.md
  .agents/
    memory/MEMORY.md
    memory/project-status.md
    HANDOFF_LOG.md
```

`CLAUDE.md` may import `AGENTS.md`. Both agents read the same index and status file. Use
`agent-handoff` to catch up at the start and record a concise handoff at the end. Only one agent
should write in a folder at a time. Past transcripts are evidence, never fresh authorization.

The optional catch-up helper reads only the current user's local transcript stores. It does not
share transcripts with another person, and it should not be run against another user's account.
Keep unpublished reasoning graphs, review notes and case materials private or Git-ignored.

## Limits

For repository-plus-data setup, use `organize-econ-research-project` for the task layout and
`build-asset-replication` for traceable GitHub-code/Dropbox-snapshot packages. Data access and
redistribution permissions are separate from access to this public toolkit.

Optional tools depend on the chosen workflow: Node.js for dependency-graph validation, a TeX
installation for LaTeX builds, SymPy for symbolic checks, and Pandoc plus Chrome/Chromium for
reMarkable PDF rendering. The corpus's offline checks require SQLite with FTS5. Install these
only when needed; installing the skill package does not install or authorize external services.

Skills do not transfer connector permissions, SSH identities, API keys or account sessions between
agents or collaborators. A configured connector is not proof of authentication or reachability.
Referee reports and confidential editor notes must remain outside a shared coauthor repository.
