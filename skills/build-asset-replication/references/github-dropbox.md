# GitHub code, Dropbox snapshots, local computation

## Boundaries and authority

Use this architecture when requested; do not impose a new storage provider on an
existing working collaboration. Resolve repository owner/name/privacy and exact
Dropbox destinations from user choices or ask when ambiguous. Follow connected
tool/skill requirements for confirmation even when the high-level plan is approved.

GitHub contains reviewed code, portable wrappers, preserved source snapshots,
contracts, frozen document source when permitted, environment specifications, tests
and onboarding instructions. It does not contain credentials, authenticated Git
mirrors, restricted observations, local ledgers or private feedback. Review provider
locators and license information before deciding which metadata can be tracked.

Dropbox stores versioned source/prepared inputs, references, retained run bundles
and release evidence. A useful layout is `source-snapshots/`,
`prepared-snapshots/`, `references/`, `runs/`, `releases/`; adapt it to the project.
These are immutable-by-convention snapshots backed by hashes, not a claim that
Dropbox technically prevents edits. A changed byte requires a new snapshot ID.

Compute in a local checkout/vault outside Dropbox sync folders. Materialize a
selected snapshot once; production must not read mutable Dropbox, historical
working trees, the live document editor or external websites.

## Acquisition and snapshots

Review a task-minimal file manifest before copying large distributed trees.
Record provider path/file ID/revision/modified date/size and provider hash where
available, plus local SHA-256. Download temporary links directly into ignored
staging files without logging or retaining the URLs. Verify bytes before atomic
promotion. Preserve differing versions in quarantine; never overwrite a competing
local input and silently bless the newer timestamp.

Use the provider's content-hash algorithm correctly; it may differ from ordinary
SHA-256. Compare duplicate folders by hashes and use the script-referenced lineage
only when supported. Revision restoration or creation of remote copies is a write
requiring appropriate authority, not a read-only workaround.

A snapshot manifest should include relative paths, sizes, SHA-256, provenance,
access/license class, preparation level and file role. Clearly tag reference-only
artifacts and runtime dependencies. Pin the manifest hash in Git, and record an
archive hash when distributing an archive. Setup must reject path traversal,
escaping symlinks, duplicate targets, changed bytes and conflicting local files.
Treat extracted archives as untrusted until paths and hashes are checked.

For upload, the exact local source and remote destination must be unambiguous and
authorized, especially for restricted data inheriting shared-folder access. Do not
claim completion until the tool reports it; retain stable uploaded file metadata.
Never create public links or alter sharing just to make onboarding convenient.

## Selective code publication

Inspect dirty state and preserve unrelated changes. If the original repository has
unsafe history, create a clean code-only export with a reviewed allowlist and file
hashes rather than committing or pushing the working directory wholesale. Check
that frozen source files and required templates/styles were not accidentally omitted.
Preserve historical bytes, including line endings, when hashes are provenance.

Scan prospective files and Git history for real credentials, signed/tokenized URLs,
private keys, restricted observations and unintended artifacts. Tests for secret
detection should use generated synthetic values without weakening real-secret
detection. Avoid printing any suspected secret in scanner output.

Run local checks first, then publish a coherent reviewed change when authorized.
Respect repository contribution/branch policies. Keep hosted CI lightweight and
synthetic; run licensed-data and multi-day model jobs on the agreed workstation.
Do not weaken required checks, register runners, change billing or sharing, or
invite collaborators without authorization. Report actual publication/run outcomes.

## Coauthor instructions and acceptance

Provide commands for cloning, obtaining the authorized snapshot, verifying hashes,
installing environments, materializing the local vault, reproducing one asset,
running the selected profile, resuming, reviewing differences and publishing a
release. Offer direct CLI equivalents for convenience wrappers such as Make when
useful, but do not accept software licenses or change system tools by inference.

Keep four things visibly distinct: code commit, data snapshot, scientific run,
and certified release. A release receipt binds them to the frozen document and
environment. A successfully uploaded archive or a private repository is not
evidence that results replicate, nor evidence of redistribution permission.

Verify a clean clone and relocated offline rebuild before claiming portability.
Record an assembly/prepared-subset milestone when that is all that passes. Preserve
the complete blocker register and earlier evidence; do not publish an unsupported
“complete replication” release to finish the workflow cosmetically.
