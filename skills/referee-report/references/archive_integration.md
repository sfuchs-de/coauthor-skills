# Private Archive Integration

Use archive integration only when the user supplies an existing case path or case ID, or explicitly
asks to create or archive a case.

## Existing Round

Save durable artifacts in the round's standard locations:

- `notes/00-review-log.md`: artifact inventory, commands, unresolved verification items.
- `notes/10-paper-review.md`: synopsis, evidence ledger, and substantive review.
- `notes/20-literature-review.md`: external benchmarking, only when requested.
- `notes/30-theory-investigation.md`: technical audit, only when relevant.
- `notes/40-decision-log.md`: private decision reasoning and recommendation history.
- `deliverables/referee-report.md`: author-facing report.
- `deliverables/editor-note.md`: confidential note, only when requested.

## Boundaries

- Do not copy manuscripts, extracted text, screenshots, literature PDFs, or build artifacts into
  Git.
- Use the archive's local vault locators and checksums rather than absolute paths.
- Do not create a new case merely because a manuscript was opened.
- Do not archive, tag, or submit a round without an explicit request.
- Keep recommendation and outcome data out of the central index.
