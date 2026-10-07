# Urban Writing Extension

This is an opt-in extension to the general 45-paper writing library. Eight pinned
urban papers add 513 extracted pages, producing a combined 53-paper inventory
with 22,108 attested writing forms and 2,254 additions relative to edition05.
The preceding editions remain unchanged. This is a selected corpus, not an
exhaustive account of urban economics or every author's work.

Use the [urban guide](URBAN_EXPOSITION.md) for housing, neighborhoods, commuting,
transport, and policy incidence. The [source study](SOURCE_STUDY.md) records
55 selected passage pages, 32 observations, and exact PDF versions. Consult
[24 usage distinctions](USAGE_SUPPLEMENT.md) and [six worked repairs](WORKED_EXAMPLES.md)
when the relevant economic object or transition is unclear.

The [policy](VOCABULARY_POLICY.md) preserves the distinction between attested
words and scientifically justified concepts. No exceptions are newly approved.

```sh
python3 scripts/edition.py lookup neighborhood
python3 scripts/edition.py check /absolute/path/section.tex --strict
python3 scripts/edition.py verify
python3 scripts/audit_examples.py
```

For the installed skill, select this inventory with `--urban`; its default stays
at 45 papers. Local acquisition, extraction, and rendering require the public
source PDFs and Poppler. Offline vocabulary, study, example, and package checks
need Python 3.10+ with SQLite FTS5. Full source text and rendered source pages
are intentionally excluded from portable ZIPs. Main-page ranges are approximate
page-level classifications, not exact English prose spans.

Source reading is selective. The examples are original fictional exercises and
same-context editorial work, not independent validation or new research results.
This extension does not authorize changes to manuscripts, methods, or results.
