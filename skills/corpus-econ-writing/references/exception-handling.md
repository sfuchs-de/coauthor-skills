# Necessary Vocabulary Exceptions

The frozen library has no approved exceptions. Keep project-specific approvals
outside the installed skill so other projects do not inherit them.

Copy `references/library/data/vocabulary_policy.json` into the project's editing
records and add individual terms. An approved entry has this schema:

```json
{
  "term": "exact-word-or-compound",
  "necessity": "Why this argument, source, or official name requires the term.",
  "why_no_attested_alternative": "How an attested substitute changes or obscures meaning.",
  "approved_by": "Author and the approval record",
  "status": "approved"
}
```

This is a schema example, not an approval. A proposed term stays `pending` until
the author approves it; pending entries do not pass strict checking. Keep the
reason and approval alongside the writing review. Names, acronyms, inflections,
and compound families are not blanket exemptions.

Pass that project register explicitly with `--policy`. Do not reset source
hashes or add the term to the corpus database. If precise established terminology
is missing, explain the exception rather than weakening the scientific statement.
Introducing a genuinely new assumption or method still needs separate authority.
