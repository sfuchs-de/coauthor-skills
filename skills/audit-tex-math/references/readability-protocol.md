# Verified-Proof Readability Protocol

## Prime invariant

Do not change the mathematics. Reorder exposition, signpost, expand accepted intermediate steps,
rename consistently, and repair references or typographical errors. Do not strengthen or weaken a
statement, replace the argument, select an ambiguous hypothesis, or silently fill a gap.

If a gap or error appears, stop editing the affected proof, identify the precise step, and route it
to audit or repair mode. Any independently derived intermediate line is new mathematical content
and must be re-audited.

## Six-layer pass

1. **Architecture:** confirm that the statement, definitions, dependencies, cases, and conclusion
   appear in an order a reader can follow.
2. **Signposting:** state the target and proof strategy, announce cases or steps, and close each
   obligation before opening another.
3. **Line-level justification:** explain nontrivial transformations and instantiate cited results;
   expand only the transitions the intended audience would otherwise need to reconstruct.
4. **Notation hygiene:** define every symbol, avoid double-booking, keep indices and dimensions
   consistent, and make appendix restatements match the main statement.
5. **Intuition:** add short, literally defensible explanations outside the formal proof when they
   reduce reader effort. Do not smuggle in a new mechanism or comparative static.
6. **Formula grammar:** integrate displays into sentences, punctuate them, remove fragments, and
   preserve the document's equation-numbering and cross-reference conventions.

## Contested edits

Propose rather than apply a change to proof strategy, lemma boundaries, assumption placement that
could alter scope, case order that changes dependencies, or notation whose meaning is ambiguous.

## Style

Match the surrounding manuscript and intended audience. Prefer precise active prose, stable terms,
and one logical job per sentence. Do not impose an imported author's pronouns, connectives, display
density, or notation conventions over a coherent local style.

## Final check

Confirm statement equality, reference integrity, symbol definitions, assumption visibility,
justified signs, complete cases, and unchanged mathematical scope. Report suspected gaps separately
from content-preserving edits.
