---
name: render-mathdown-tex
description: "Convert one or more Markdown or Mathdown research notes into a cohesive, compilation-ready TeX theory note in a clean economics short-note style. Use when Codex is asked to export Markdown mathematics to LaTeX, combine Mathdown owner notes into one TeX document, reproduce the supplied summary-plus-technical-appendix presentation, preserve detailed derivations while streamlining overlap, or generate a polished TeX/PDF research note from Markdown sources."
---

# Render Mathdown to TeX

Create a semantically faithful TeX document, not a blind Pandoc transcription. Preserve the
mathematics, result scope, provenance, and derivational detail while giving the material one
coherent exposition and the presentation grammar in `references/style-contract.md`.

## Choose the mode

Use **faithful** mode by default. Translate and reorganize for readability, but do not change a
claim, assumption, result status, approximation order, or dependency.

Use **curated** mode when the user asks to combine or streamline notes. Remove duplicated
narrative and duplicate theorem statements, but retain one complete owner derivation and replace
other copies with precise cross-references. Never shorten algebra merely because it is repeated.

Use **repair** mode only when the user authorizes mathematical review or correction. Then use
`audit-tex-math` in audit mode before editing a substantive claim, repair mode for an authorized
mathematical correction, and readability mode only after the proof closes. Record every narrowing,
added assumption, or unresolved gap.

## Workflow

### 1. Freeze and inventory the sources

Identify the requested Markdown files, their order or dependency graph, and any notation,
bibliography, provenance, registry, or status files that govern them. Exclude indexes, generated
projections, audit digests, and compatibility views unless the user wants them in the document.

Read `references/conversion-contract.md`. Run the inventory helper:

```bash
python3 "<skill-directory>/scripts/inventory_markdown.py" \
  note-a.md note-b.md --output /tmp/mathdown-tex-inventory.json
```

Inspect the resulting headings, explicit result markers, equations, links, citations, and hashes.
For Mathdown projects, also read the authoritative result registry and dependency graph; frontmatter
alone does not define theorem scope.

### 2. Set the authority and document map

State which source owns each claim. In faithful and curated modes, Markdown remains authoritative
for the mathematics and TeX is a presentation artifact. If sources disagree, stop synthesis of the
affected claim, expose the discrepancy, and retain the narrower statement unless the user authorizes
repair.

Build a short content map before drafting:

1. Summary of main results: goal, objects, logic, intuition ladder, headline results, limitations.
2. Main exposition: primitives, assumptions, derivations in dependency order, formal statements,
   interpretation, and implementation when relevant.
3. Technical appendix: notation, proof algebra, theorem-condition mappings, boundary cases,
   computational details, and source/provenance anchors.

When the conversion participates in a shared suite graph, read
`../econ-writing-suite/references/reasoning-graph-integration.md` and own its `conversion` layer.
Map each source owner result to its TeX owner node, record specializations and deliberate
deduplication, and flag any lost assumption, status qualifier, derivation step, or provenance anchor.
Do not mark a converted result mathematically verified merely because its text was preserved.

For a short technical memo, the main body may be the summary and the detailed derivations may begin
after the technical-appendix divider, as in the supplied example. For a full paper-length note, keep
core derivations in the main text and move only proof details and long ledgers to appendices.

### 3. Start from the neutral template

Read `references/style-contract.md` and use `assets/theory-note-template.tex` as the presentation
base. Replace every `@@TOKEN@@`; do not copy subject-specific prose, notation, macros, or equations
from the example that motivated the template.

Keep only packages and macros used by the output. Add recurring notation after scanning all source
math, not one macro per symbol. Preserve existing equation and theorem labels when the Markdown
defines them. Add stable TeX labels otherwise.

### 4. Translate semantically

For every result:

- restate the domain, quantifiers, maintained assumptions, and local/global or exact/approximate scope;
- define intermediate objects before use;
- show every nontrivial substitution, differentiation, normalization, inversion, reverse implication,
  and approximation remainder present in the source;
- map external theorem conditions to local assumptions;
- separate analytic proof, numerical verification, and empirical interpretation;
- retain sanity checks, boundary cases, failure conditions, and open obligations;
- copy explicit result provenance into a TeX comment of the form
  `% mathdown-result:RESULT-ID` immediately before the owner statement.

Use the rhythm “lead-in sentence → display → interpretation.” Use a small scalar or low-dimensional
case before the full operator or system only when it genuinely clarifies the general derivation.
Do not manufacture examples or proofs that the source does not support.

### 5. Streamline without loss

In curated mode, merge repeated definitions into one object dictionary, choose one owner statement
per result, and replace repeated summaries with `\cref` pointers. Preserve imported specializations:
state the generic result once, then prove the mapping and additional local conditions. Keep distinct
model states, approximations, and conflicting closures visibly separate.

Do not remove algebraic transitions, theorem-condition mappings, failure cases, status qualifications,
or source anchors. A shorter document is acceptable only when the removed material was genuinely
duplicative.

### 6. Compile and verify

Compile with the project command when one exists; otherwise run:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error note.tex
python3 "<skill-directory>/scripts/check_tex_output.py" note.tex \
  --inventory /tmp/mathdown-tex-inventory.json --log note.log --strict-log
```

The checker requires explicitly marked source results. If the selected inputs are themselves a
complete owner registry rather than prose containing cross-references, add
`--require-all-result-tokens`. Otherwise verify unmarked owner coverage against the registry by hand;
do not mistake every mentioned dependency ID for a locally owned result.

Resolve fatal errors, undefined references or citations, duplicate labels, unresolved template
tokens, missing result markers, and material overfull boxes. Use `academic-draft-review` in
short-note-layout mode for the final house-style check. If the user requests a PDF or layout
matching matters, render and inspect the PDF using the `pdf` workflow; source compilation alone is
not visual verification.

## Acceptance contract

The deliverable is complete only when:

- every selected source result is represented once as an owner statement or explicitly mapped
  specialization;
- no derivation, assumption, status qualifier, or approximation domain was silently lost;
- every source/result link has a stable TeX label or provenance comment;
- all `@@TOKEN@@` placeholders are replaced;
- TeX compiles without fatal errors or unresolved references/citations;
- the generated PDF has no material layout defect; and
- the final report identifies the source files, output root, mode, any mathematical changes, and
  verification result. In a shared graph workflow, also require resolved conversion mappings or
  explicitly stale anchors and report the conversion-layer status.

Do not overwrite an authoritative TeX manuscript unless the user explicitly requests replacement.
Prefer a new, clearly named TeX root for a refactored rendering.
