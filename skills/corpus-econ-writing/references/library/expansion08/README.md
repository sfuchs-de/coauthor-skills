# Theory08 Writing Resource

This edition adds six pinned papers to the spatial, trade, urban, and transport
corpus: **59 papers, 3,217 extracted pages, and 23,211 attested writing forms**.
The six additions contain 287 pages and add 1,103 forms relative to urban06.
The previous 23-, 31-, 45-, and 53-paper inventories remain unchanged.

Use the [theory guide](THEORY_EXPOSITION.md) for assumption placement, derivation
depth, interpretation, policy derivatives, and literature organization. Consult
the [source cards](SOURCE_STUDY.md) and [usage distinctions](USAGE_SUPPLEMENT.md)
only where relevant. The [evaluation](evaluation/REVIEW.md) separates editorial
judgment from mathematical checks and vocabulary status.

```sh
python3 scripts/edition.py lookup basket
python3 scripts/edition.py check /absolute/path/theory_section.tex --strict
python3 scripts/edition.py verify
```

The [policy](VOCABULARY_POLICY.md) still requires exact attestation and context
review. No stemming, automatic compound approval, or approved vocabulary
exceptions have been added. Statement labels are classified separately from
prose only in explicitly recognized contexts; the checker reports every such
classification. Mathematics and unfamiliar macros require human review.

The local acquisition and full-text extracts are not distributed. Portable ZIPs
contain original guidance, page provenance, vocabulary records, tests, and
fictional examples. Public download access does not imply redistribution rights.
This resource update does not adopt or rewrite any research manuscript.
