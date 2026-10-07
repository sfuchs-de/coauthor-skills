# QA and Provenance

## Numerical Checks

- Reconcile every displayed number against the generated CSV, Parquet, or model output.
- Confirm denominators, weights, units, signs, and scenario identifiers.
- Confirm that labels such as observed, calibrated, model-implied, diagnostic, and unsupported are accurate.
- Check that formatting changes did not alter the sample or values.

## Visual Checks

Inspect both the standalone asset and its rendered destination:

- title and caption hierarchy;
- font consistency and minimum readable size;
- panel alignment and equal dimensions;
- clipping and overlap;
- excessive blank margins;
- legend and colorbar placement;
- land/sea contrast;
- visible route and closure layers;
- common axes and color limits;
- grayscale and reduced-size legibility.

Render a contact sheet when changing more than three pages. For maps, inspect representative pixels or layers if land and sea colors could have been overwritten.

## Asset Manifest

For promoted assets, record at least:

| Field | Meaning |
|---|---|
| `asset_id` | Stable identifier |
| `source_script` | Generating program |
| `source_inputs` | Principal data/configuration |
| `generated_source` | Canonical generated file |
| `destination` | Paper/slide asset path |
| `document_figure` | Figure or slide reference |
| `model_scenario` | Model and scenario identifier |
| `units` | Displayed unit and sign convention |
| `support_status` | Headline, robustness, diagnostic, or unsupported |
| `sha256` | Content hash |

Promotion must fail on missing sources, stale hashes, or unsupported headline assets. A second promotion run should be idempotent.

## Delivery Checks

- Compile with the repository's standard command.
- Scan logs for missing assets, undefined references, font substitution, and material overfull boxes.
- Run `qpdf --check` and `pdfinfo` for PDF deliverables.
- Run `git diff --check`.
- Report the exact generating script, final asset path, target document, and QA result.
