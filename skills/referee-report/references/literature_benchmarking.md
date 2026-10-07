# Literature Benchmarking

Use this workflow only when the user requests a literature review or external contribution check.

## Search Order

1. Extract the manuscript's closest cited predecessors and its stated novelty claims.
2. Search the configured Paperpile library for title, author, topic, and citation matches.
3. Search primary sources: published articles, working-paper pages, journal pages, and author pages.
4. Use secondary sources only for discovery, not to support technical comparisons.

## Evidence Separation

Maintain two ledgers:

- `manuscript_positioning`: what the paper says about prior work.
- `external_verification`: what verified external sources establish.

Do not treat a title match or bibliographic similarity as evidence that two models, designs, or
results are the same. Verify the relevant section of each source.

## Comparison Grid

Compare the focal paper with the three to eight closest papers across the dimensions relevant to
the claim: question, model, identifying variation, data or measurement, mechanism, quantification,
and external validity. Use `same`, `incremental`, `distinct`, or `unclear`, with a short reason and
source link or local citation key.

Translate the grid into a report comment only when positioning affects the journal-level
contribution. Do not turn a comprehensive bibliography into an author-facing citation list.
In the synthesis, state each incremental margin positively. Avoid a repeated inventory of
`the contribution is not X but Y` contrasts, which makes distinct comparisons sound templated.
