# Vocabulary Policy: Edition 05

The default inventory is the frozen 45-paper edition. The original 23-paper and
31-paper inventories remain unchanged and available explicitly. Source versions
and permitted extraction exclusions are declared in [sources.json](data/sources.json).
Do not add papers, forms, or approved exceptions silently.

Prefer plain main-text usage. Check revised prose rather than just an input driver.
Read rare, appendix-only, name-like, and extraction-flagged evidence in context.
Main-text classifications are page approximations, not sentence-level annotation.
Existing normalized compound handling does not authorize inventing compounds from
attested component words. Inflections are not freely licensed.

Lexical evidence does not establish an economic meaning, identify a parameter,
justify an assumption, or establish that a concept belongs in a particular paper.
Consult the original dictionary and the two versioned usage supplements for
selected distinctions, not as an exhaustive semantic whitelist.

Retain necessary technical meaning. If an unattested term is essential, explain
its necessity and why an attested alternative changes the meaning; obtain narrow
approval through the existing exception policy. No new exceptions are approved
by this edition. Examples, source prose, and automated tests are not approval.

Use `scripts/edition.py check FILE --strict --policy POLICY` to check a declared
policy. The checker’s math and macro exclusions must not be used to conceal prose.
A successful lexical check is only one part of a writing review.
