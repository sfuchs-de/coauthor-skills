# Authentication

## Existing clone

Use the clone's configured credential flow. Test it with a fetch. Do not display `remote.origin.url`, because older clones may contain embedded credentials. When the remote identity is needed, sanitize it before reporting.

## New clone

Use a credential-free URL:

```text
https://git.overleaf.com/<project-id>
```

Overleaf uses username `git` and a Git authentication token as the password. Prefer the operating system's credential manager or an interactive prompt outside the transcript. Do not place the token in:

- the clone URL;
- shell history or command arguments;
- Git configuration committed with the project;
- notes, logs, task prompts, or chat summaries.

If credentials are unavailable, stop after reporting the exact credential-free clone command and ask the user to configure authentication. Do not ask them to paste a token into a document or repository.

## Failure handling

- Authentication error: preserve the worktree and request credential setup.
- Push rejected: fetch and reclassify divergence; never force-push.
- Project migrated to another Overleaf account: create or use a distinct clone and record which project is current. Do not repoint or delete the former clone until the migration is verified.
