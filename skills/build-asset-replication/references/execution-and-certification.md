# Execution and certification

## Closed task boundaries

Preserve frozen upstream scripts; put portability repairs in documented wrappers
or reviewed patches. Execute only the retained target-producing blocks. Document
which transformations are presentation-only and which change the computation.

Use individual input contracts, not directory-exists checks. Validate hashes and
format-appropriate schemas, keys, rows, join/geometry coverage and aggregates.
Describe hash-only validation honestly for unsupported formats. Missing inputs,
unexpected duplicates, nonfinite values or silently dropped observations block the
affected task unless an explicit economic/statistical rule accounts for them.

Keep task outputs inside run-specific directories. Fail before changing a staged
release if any required producer, validation or receipt is missing. Promote a fully
validated build atomically where feasible; otherwise use rollback-safe publication.
Never use frozen reference outputs as production fallbacks. Documented static inputs
are legitimate exceptions, not a route for relabeling orphaned generated figures.

Cache keys must cover scientifically relevant code, orchestration, inputs,
environment and parameters. Documentation-only changes need not force expensive
reruns; preserve the original versioned receipt rather than relabeling stale
results as produced by current code. Choose explicit profiles/run IDs, not the
latest modification time. Keep earlier outputs and failed runs inspectable.

## Historical and computational agreement

Maintain two independent conclusions: **is the returned solution valid?** and
**does it reproduce the frozen result?** A numerically sound disagreement belongs
in the correction/lineage ledger, not under reproduction success.

Before a large grid, validate representative cases and execution assumptions.
For structural models or stateful sequences:

- Preserve primitive shocks, equilibrium closure, scenario order and inherited
  warm starts. Log their identities and relevant state hashes.
- Inspect actual returned-state residuals and accounting identities, not only an
  iteration message or a residual evaluated at a discarded trial state.
- Include no-shock behavior, support constraints, positivity/normalization and
  economically meaningful aggregate reconciliation where applicable.
- Record convergence criteria and inner/outer fixed-point outcomes. Reaching an
  iteration cap is not success. Raising a cap is not proof of convergence.
- Do not resume paused jobs or change solver mathematics without task authority.
  Agree on resources for multi-day runs; avoid arbitrary wall-clock cutoffs once
  authorized. Do not restart a costly sequence from scratch by default.
- Prove resumed and uninterrupted representative runs agree before using recovered
  checkpoints for production. Aggregate-only checkpoints cannot identify detailed
  flows that were discarded.

For cross-language or refactored implementations, compare intermediate objects,
support, indexing, missing values, serialization and downstream outputs. Formatting
precision can change later estimation; do not “improve” historical export precision
without testing whether it changes the reproduction target.

## Numerical and visual validation

Compare tables by named row/column/model, not unordered bags of numbers. Check
sample counts and diagnostics as well as headline coefficients. Reject extra,
missing or duplicated cells unless an explicitly separate extension is intended.
Include model/control labels, captions and repeated claims in semantic review.

Choose tolerances from reported precision and justified numerical error; do not
widen them after observing a mismatch. Integer counts generally require equality.
Distinguish absolute, relative, rounding and inequality rules. Use unrounded
producer outputs whenever available; rounded table values can be inadequate inputs
to a derived claim.

For figures, retain and compare underlying plotted data. Image similarity,
readability and PDF compilation are separate visual/format checks. Review panels,
units, axis transforms, baselines, uncertainty, clipping and selection rules.
Native model-network edges and physically routed traffic are distinct objects;
do not convert geometry assumptions into economic quantities or invent units.

## Rebuild evidence

Test the smallest sufficient verification tier, then expand toward the requested
scope. Meaningful negative tests should reject wrong input versions, stale hashes,
altered cells, invalid numerics, duplicate IDs, incomplete outputs and prohibited
reference fallbacks. The bundled checker only covers metadata invariants.

An offline claim needs enforced network denial and blocked legacy data/code
locations, not an assurance that scripts probably avoid them. Use the platform's
appropriate sandbox/container or equivalent isolation. Include required fonts,
route geometry, package libraries and external executables in the dependency audit.
Do not silently relax isolation when it fails. Some platforms reject nested
sandboxes; combine denials in one policy and test that access is actually denied.

Test a clean clone, pin and materialize its data snapshot, relocate it and rebuild.
Record separately whether environments were freshly installed or already present.
Language/package/compiler/TeX and licensed-runtime dependencies are part of the
closure; installing them or accepting licenses can require user action.

Prepared mode begins from retained analysis-ready files. Full-source mode rebuilds
those files from documented provider snapshots and compares declared intermediate
checkpoints. Full-source certification requires both modes' agreement, exhaustive
result coverage, successful final document construction and independent collaborator
reproduction of representative paths. Open discrepancies block complete certification.

## Deliverable checklist

- Frozen-target catalogue with every occurrence and an explicit uncovered register.
- Source-to-transform-to-result DAG and task commands; distinguish executable
  dependencies from proposed or unrecovered edges.
- Current run receipts and a result-by-result comparison report.
- Separate correction ledger and scientific/operational blocker register.
- Document build from production outputs, without reference substitution.
- Release receipt binding code, target revision, snapshot, environment locks,
  scenario configuration and validated runs, with an honest scope/status.

Do not implement a checker that always says “certified” from manually filled status
fields. Conversely, if a provisional gate is deliberately blocked because the
scientific checks are not yet implemented, label it as a blocking interface rather
than a finished certification engine.
