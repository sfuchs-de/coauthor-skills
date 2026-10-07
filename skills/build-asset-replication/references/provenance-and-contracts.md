# Provenance and contracts

## Document boundary

Freeze a revision, not a mutable link. Retain a source/version hash and a rendered
reference where permitted. Record scope choices such as appendix, supplementary
materials, backup slides, animations and speaker notes. Keep later revision exhibits
separate from results used in the frozen target.

For TeX, traverse the active input/include/graphics tree; account for macros,
conditionals, graphics paths and extensions rather than assuming a regex resolves
everything. Exclude commented or dormant alternatives only after confirming scope.
For slides, distinguish embedded pictures, editable charts, linked workbooks,
objects drawn by hand and externally linked media. Include result statements in
titles, labels and notes when in scope. PDF extraction alone cannot establish an
embedded chart's data or a figure's producer.

Compare the source census with the rendered pages/slides. Give each occurrence an
anchor and each result a stable ID. Repeated occurrences may share one computed
object but require separate unit, rounding, sign and wording checks. Maintain
explicit placeholders for unresolved panels or semantic claims; never equate a
numeric-token count with an exhaustive result catalogue.

## Distributed source search

Inventory only systems and projects in scope. Record logical local paths, stable
file/repository/project IDs, revisions, hashes, ownership/access and modification
metadata. Keep live authorized URLs transient and omit credentials and message
bodies from a publication manifest. Relevant correspondence may resolve provenance;
it is not itself executable evidence.

For each asset/result, search in this order where feasible:

1. Exact path/name and identical bytes under other names.
2. Code that writes, exports, copies or renames it, with source-line anchors.
3. Immediate inputs and the scripts producing those inputs.
4. Git history, provider revisions and retained result receipts.
5. Equivalent historical implementations, clearly distinguished from exact recovery.

Pin dirty or untracked code by content hashes. A Git commit does not describe
untracked files. Newest code may implement a different model or shock. Document
lineage distinctions rather than silently replacing the historical computation.

Keep provenance confidence separate from reproduction status:

| Provenance status | Minimum evidence |
| --- | --- |
| `verified_exact` | Producer identified and an available output is byte-identical; this alone does not prove a rerun |
| `verified_renamed` | An explicit export/copy/rename chain explains the document filename |
| `producer_identified` | Executable code names the output, but identity/agreement is not established |
| `artifact_only` | Matching output exists; generating chain remains unresolved |
| `manual_source` | Authored/static origin and transformation documented |
| `unresolved` | No defensible chain |

Newly rerun outputs may be scientifically equivalent without byte equality, owing
to PDF timestamps or serialization. Record their validated numerical comparison
separately; do not misuse `verified_exact` to mean “looks similar.”

## Manifest families

CSV, JSON, YAML or existing project formats are acceptable. Use stable keys and
cross-references; do not invent values to satisfy a schema.

| Manifest | Essential fields |
| --- | --- |
| Target | Document revision/hash, rendered reference, included scope, excluded material, verification date |
| Assets/occurrences | Asset ID, occurrence anchor/page/panel, relative path, caption, type, size/hash, producer, lineage, provenance status, static/generated role |
| Results | Result ID, all occurrences, type, units/denominator, source output and selector, transform, expected unrounded/printed value, comparison rule, evidence status, receipt |
| Tasks | Task ID, code paths/hashes, file inputs, dependencies, outputs, command, profile/parameters, environment, checks and resume contract |
| Inputs | Input ID, relative vault path, raw/prepared/derived boundary, provider/version, size/hashes, schema/keys/row and coverage rules, license/access |
| Acquisition ledger | Stable provider path/ID/revision, modified date, size, provider content hash, local SHA-256, acquired time and outcome; no temporary URL |
| Runs | Run ID, task/profile/sequence, actual commands, code/input/environment/parameter hashes, runtime versions, completion, diagnostics, output hashes |
| Corrections | Original and recomputed values, affected occurrences, explanation, supporting run, author approval; never automatic manuscript edits |

For tables, selectors should name model/row/column and distinguish standard errors,
sample sizes and diagnostics. For figures, retain every plotted series, panel,
group, transformation, uncertainty band and selection rule. For maps, record
quantity units separately from geometry/crosswalk lineage and coverage. External
statistics and authored illustrations need citations/origins, not fictional
computational producers.

## Minimal checker schema

`assets/contracts.example.json` demonstrates these fields for the bundled checker.
It is intentionally an incomplete synthetic example, so coverage checks block it.

- `schema_version`: `1`; `target`: nonempty `kind` and frozen `version`.
- `inputs`: retained starting files with `id`, relative `path`, nullable `sha256`,
  `data_class`, `source_level`; newly generated intermediates belong to task outputs,
  not this starting-input list.
- `tasks`: `id`, `input_ids`, `dependencies`, `code_paths`, `output_paths`, nullable `command`.
- `assets`: `id`, `path`, `kind` (`generated`, `static`, `authored`), `anchors`, nullable
  `producer_task`, `provenance_status`; manual records also provide `origin`.
- `results`: `id`, `kind`, `anchors`, `asset_ids`, nullable `producer_task`,
  `comparison` (`method`, `rule`, `unit`) and `status`. A `verified` record also
  names a relative `receipt`; that path is not proof that the receipt is valid.

Declared input/output paths must be relative and must not escape the package.
External provider locators belong in metadata, not executable local paths.
Paths and IDs must remain unambiguous when multiple model profiles coexist.
