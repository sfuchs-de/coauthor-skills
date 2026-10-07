---
name: stop-slop
description: Perform a quick, unscored cleanup of formulaic or generic prose when the user explicitly asks to stop slop, deslop, or make a short passage sound more natural. Preserve technical language and authorial voice. Use `ai-slop-lint` instead for scored audits, evidence reports, long drafts, or iterative validation.
metadata:
  author: Hardik Pandya (https://hvpandya.com)
---

# Stop Slop

Use this skill for a fast editorial pass, not authorship detection or a scored audit.

## Boundary

- Use `ai-slop-lint` for file-level scans, rule evidence, academic or referee profiles, and repeated
  scan-rewrite loops.
- Use `econ-write` when revising the substance or structure of an economics manuscript.
- Use `referee-report` when drafting or evaluating a referee report.

## Quick Pass

1. Remove throat-clearing, prompt acknowledgments, generic praise, and empty emphasis.
2. Replace abstract claims with the actor, action, evidence, mechanism, or consequence.
3. Prefer active voice when the actor matters. Keep standard passive constructions when the actor
   is immaterial or the genre expects them.
4. Break formulaic contrasts, tidy triads, repeated transitions, and generic conclusions.
5. Vary sentence rhythm without manufacturing fragments or changing technical meaning.
6. Review dense dash-asides and adverbs individually; keep those that match the author's voice or
   carry real meaning.
7. Preserve citations, equations, notation, qualifications, and field-specific terms.

Read the reference examples only when a pattern is unclear:

- `references/phrases.md`
- `references/structures.md`
- `references/examples.md`

## Output

Return the cleaned passage. Briefly identify material changes only when the user asks. Do not assign
a score, claim AI authorship, or create a lint report.

## Final Check

- The revision says the same thing.
- No evidence, qualification, citation, or technical distinction was lost.
- The prose is direct without becoming abrupt or artificially casual.
- Remaining passive voice, dashes, adverbs, and first-person language are deliberate.

## License

MIT. Original skill concept and source attribution are preserved in repository metadata and license.
