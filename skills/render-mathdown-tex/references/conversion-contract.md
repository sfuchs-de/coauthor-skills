# Markdown-to-TeX conversion contract

## Source selection and authority

Treat owner Markdown as authoritative unless the user names another source. Read linked notation,
result registries, dependency graphs, proof audits, and bibliographies when they constrain the selected
claims. Do not promote generated syntheses, indexes, projections, or status tables to mathematical
owners.

For multiple notes, construct a dependency order and a one-owner map before writing TeX. If the same
result appears in several notes, preserve the complete owner derivation once and convert the other
appearances into cross-references or specialization mappings.

## Structural mapping

| Markdown source | TeX rendering |
|---|---|
| YAML frontmatter | Omit from prose; transfer title, author, date, status, and provenance where relevant |
| `#`, `##`, `###` headings | `\section`, `\subsection`, `\subsubsection`; use run-in `\paragraph` only for short orientation labels |
| Inline `$...$` | Preserve mathematical content inside `\(...\)` or `$...$` consistently |
| `$$...$$`, `\[...\]` | `equation`, `align`, or an unnumbered display according to reference needs |
| Equation/result anchors | Stable `\label{...}` plus a source-provenance comment |
| Emphasis | `\emph{...}`; use bold only for labels and genuinely structural emphasis |
| Markdown links | `\href{URL}{text}` for external links; `\cref{...}` for converted internal owners |
| Wikilinks | Resolve to the converted owner label; never print unresolved `[[...]]` syntax |
| Tables | `booktabs` table; preserve notes, units, and definitions |
| Lists | Prose by default; assumption enumeration, comparisons, or algorithms when structure requires it |
| Blockquotes | Ordinary prose, `quote`, or a `remark` according to semantic role—not appearance alone |
| Fenced code | `verbatim`/`lstlisting` only if the code is part of the deliverable; otherwise summarize the algorithm and link the source |
| Footnotes | `\footnote{...}` while preserving placement and scope |
| Citations | Preserve citation keys and use the project's citation command; never invent bibliography entries |

Escape TeX-special characters in prose (`%`, `&`, `_`, `#`, `$`) without modifying math. Normalize
Unicode minus signs, nonbreaking spaces, apostrophes, and dashes only when their TeX meaning is clear.

## Mathematical preservation

For each registered result, preserve:

- stable ID and owner;
- statement and status;
- domains, quantifiers, and maintained assumptions;
- exact, local, asymptotic, approximate, sufficient, or necessary scope;
- all nontrivial algebraic transitions;
- theorem-condition mappings;
- existence, uniqueness, positivity, support, boundary, invertibility, and convergence conditions;
- approximation remainder, order, and uniformity domain;
- distinction between analytic proof, deterministic check, simulation, and empirical evidence;
- failure cases and unresolved obligations.

Place `% mathdown-result:RESULT-ID` immediately before the owner theorem, proposition, definition,
or derived identity. If a source contains separate claim and derivation anchors, record them as:

```tex
% mathdown-claim:RESULT-ID
% mathdown-derivation:RESULT-ID
% mathdown-result:RESULT-ID
```

An imported specialization keeps its own label but identifies the generic owner in prose and proves
only the mapping and added assumptions.

## Streamlining rules

Safe reductions include duplicate motivation, repeated object definitions, repeated proposition
summaries after a complete proof, and hand-maintained status tables whose authority lives elsewhere.

Unsafe reductions include omitted substitutions, hidden reverse implications, dropped assumptions,
collapsed remainder bounds, erased model-state conflicts, or replacing proof with numerical evidence.

When two source passages are similar but not identical, compare assumptions and scope before merging.
If equivalence is not proved, retain both as separate cases.

## Citation and provenance rules

Keep source commit, source path, and source hash in a short provenance appendix or TeX comments when
available. Preserve primary-source theorem locations and assumption mappings. A generated TeX note
must not imply that a secondary synthesis is the original mathematical source.

## Verification ledger

Before delivery, compare the source inventory with the TeX output:

- selected files and hashes;
- headings represented or intentionally merged;
- result IDs and owner labels;
- equation and theorem counts as a diagnostic, not a quota;
- citations and external links;
- omitted material with a reason;
- mathematical changes, if repair mode was authorized.

The comparison is evidence against accidental loss; it does not replace reading the rendered note.
