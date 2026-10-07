# Theory08 Vocabulary Policy

Select this edition before drafting, rather than switching inventories after a
failed check. Its 59-paper inventory includes all earlier urban and transport
papers and six additions documented in [the source cards](SOURCE_STUDY.md).

- Prefer ordinary main-text words with relevant usage. Page attestation is
  evidence that a form occurred, not permission to import a technical concept.
- Check exact normalized forms, including possessives, plurals, and compounds.
  Attested components do not authorize their joined compound. A suggested spaced
  form still needs a grammatical and economic review.
- Inspect rare words, extraction fragments, uppercase-only forms, and evidence
  confined to references or appendices. Correct PDF extraction does not establish
  that an apparent token is ordinary prose.
- Keep an essential scientific term when alternatives would change the claim.
  Record its need, alternatives, and approval separately; do not weaken a theorem
  merely to satisfy the checker. The inherited exception register is still empty.
- Single uppercase letters following recognized statement names, for example
  `Assumption H` or `Study B`, are reported as nonprose labels, not approved words.
  Arbitrary symbols and prose words are not exempt. TeX comments, math, and
  citation commands retain their earlier exclusions and manual-review limits.
- Audit changed prose modules. The checker does not traverse an arbitrary TeX
  input graph, judge flow, or certify mathematical correctness.

Run `scripts/edition.py check FILE --strict`. A zero exit means the checked
prose has no unapproved lexical forms under this edition, not that every sentence
is good or that the result follows. Earlier inventories remain reproducible.
