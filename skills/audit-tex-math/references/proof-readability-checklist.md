# Detailed Proof-Readability Checklist

## Contents

- Architecture and signposting
- Line-level justification and notation
- Intuition and formula grammar
- Phrase repairs, mechanical lint, and contested edits

Use this checklist for a long or publication-facing proof after reading
`readability-protocol.md`. Adapt the level of detail to the audience and the manuscript's coherent
local style.

## Architecture

- For a central result, consider a three-layer presentation: statement and proof sketch in the main
  text, a short intuition paragraph outside the proof, and the formal proof in the appendix.
- State explicitly where a deferred proof lives. Restate a deferred proposition or theorem exactly
  before its appendix proof when the surrounding source does not already make it self-contained.
- Precede a supporting lemma with a plain-language sentence saying what it establishes and which
  later result needs it.
- Close a composite proof by naming the lemmas or steps that jointly discharge the target.
- Factor an exact repeated derivation into a reusable lemma only with approval when the new lemma
  structure could affect how the argument is understood or verified.
- Follow logical order. When an auxiliary result must appear before its motivation is evident, say
  what later obligation it resolves.
- Make formal statements readable in isolation: include load-bearing objects, domains, quantifiers,
  and assumptions rather than relying on a distant standing convention.
- Use theorem, proposition, lemma, and corollary labels consistently with their role in the paper.

## Signposting

- Open with the method and plan: direct proof, contrapositive, contradiction, induction, construction,
  case split, or reduction to a prior result.
- Give a long proof named or numbered steps. State the goal of each step before its algebra and close
  it before moving on.
- Verify that every announced number of cases or steps matches the proof and every later pointer.
- Enumerate cases up front and make their exhaustiveness and mutual exclusivity visible.
- Mark where temporary assumptions, cases, and induction hypotheses begin and end. Remind the reader
  of them when a case spans substantial text.
- Distinguish a genuine maintained assumption from an assumption made for contradiction or a
  degenerate branch.
- Before a long computation, state the precise inequality, identity, bound, or convergence claim it
  is intended to establish.
- Keep brief methodological asides only when they answer a likely reader question or explain why a
  natural shortcut fails.

## Line-level justification

- Make the status of each assertion recoverable: source assumption, definition, previous proof step,
  prior result, theorem application, or standard background fact.
- Give every load-bearing inequality a reason at the line where it occurs. A trailing explanation
  must cover every relation in the displayed chain.
- Justify every sign, monotonicity, limit, interchange, or dominance claim with a named condition,
  result, or one-clause argument.
- Instantiate an imported theorem's variables and map its conditions to local assumptions. Use a
  precise theorem pointer rather than a bare citation.
- Chain only relations that compose in the written order. Do not use nontransitive patterns such as
  `a <= b >= c`, and do not chain nonequality.
- Align relation symbols in displayed derivations and avoid repeating an unchanged side when the
  local TeX style has a clearer convention.
- Narrate nontrivial algebra with the actual operation: substitute, factor, rearrange, differentiate,
  normalize, take a limit, or apply an envelope condition.
- Expand a compressed substitution, telescoping sum, optimization step, or cancellation when the
  intended reader would otherwise need to reconstruct it.
- Display and label a derived cutoff, threshold, operator, or closed form if later reasoning relies
  on it.

## Notation

- State a definition symbolically and in words when the verbal gloss reduces ambiguity.
- Define each symbol before use. Collect proof-local abbreviations near the start rather than
  introducing them inside dense algebra.
- Avoid notation dumps. Introduce one object at a time with its role.
- On reuse after a long gap, recall an object's type or economic meaning, especially when decorated
  and undecorated variants coexist.
- Pair numeric references with descriptive names when that materially reduces back-searching.
- Keep names stable, use parallel names for parallel objects, and never reuse one symbol for two
  roles in the same scope.
- Describe a constructed object in words as well as by its encoding when the encoding obscures the
  construction.
- Use unambiguous subset, floor, norm, and operator notation consistent with the manuscript.
- Check argument order, epsilon variants, indices, subsequence notation, and statement/appendix
  bounds mechanically.
- Abbreviate a repeated long parameter list only after defining the abbreviation clearly.

## Intuition

- Add a short intuition sentence after a key derivation when it explains the mechanism rather than
  merely translating symbols.
- Give a main theorem an intuition paragraph outside the proof when useful.
- Translate a dense formal statement into words without weakening its quantifiers or scope.
- Supply the small figure, table, region sketch, or worked example that readers would otherwise need
  to construct for themselves.
- Keep intuition visibly separate from formal proof and make every informal gloss literally
  defensible.

## Formula grammar

- Integrate formulas into complete, punctuated sentences. Treat a displayed formula as part of the
  sentence around it.
- Avoid beginning a sentence with a bare symbol when a noun phrase is clearer.
- Put a connective such as “then” between adjacent formulas when punctuation alone would make the
  grammar ambiguous.
- Use relation symbols between mathematical expressions, not between prose fragments.
- Write logical symbols as words in ordinary prose unless the surrounding text is fully symbolic.
- Expand blackboard abbreviations when the venue expects formal prose; keep standard local
  abbreviations when they are genuinely clearer.
- Avoid programming notation in mathematical prose and preserve consistent operator and variable
  typography.
- Give every pronoun an unmistakable antecedent.
- Prefer a positive formulation when it is equally precise and easier to parse.
- Untangle `respectively` constructions when they force the reader to zip multiple lists.
- Run two diagnostics: read relation symbols aloud as verbs, and replace displays mentally with a
  placeholder to see whether the surrounding prose still carries the argument.

## Phrase repairs

| Weak phrase | Repair |
|---|---|
| “Clearly,” “obviously,” or “it is easy to see” | Delete it or give the one-line reason. |
| “It is straightforward to show” | Show the computation or cite the exact accepted result. |
| “Naturally follows” | Name the result and the condition that makes it apply. |
| “The other case is similar” | State the substitution, symmetry, or sign reversal. |
| “This leads to a contradiction” | Display or name the two incompatible statements. |
| “A dominates B” | Give the inequality or a verified pointer. |
| A bare citation as a proof | State the imported fact and instantiate it locally. |

## Mechanical lint

1. Confirm every typed cross-reference points to an object of that type and every reference resolves.
2. Remove doubled proof boilerplate, use a consistent terminator, and place `\qedhere` correctly when
   a proof ends in a display.
3. Match announced step and case counts to the body.
4. Compare every appendix restatement with the main statement, including bounds, indices,
   quantifiers, and assumptions.
5. Re-read around every math-adjacent typo, fragment, unmatched parenthesis, or agreement error.
6. Promote any footnote required for verification into the proof body and place footnote anchors so
   they cannot be mistaken for exponents.
7. Confirm every symbol is defined, no symbol is double-booked, and comma-separated conditions are
   syntactically unambiguous.

## Contested edits

Propose rather than apply:

- replacing contradiction with a direct proof;
- merging or splitting lemmas;
- adding, removing, bundling, or rewording assumptions; or
- reordering a relation chain when validating the new order requires a correctness judgment.

Report any such proposal separately from content-preserving edits.
