# Reusable Writing Instructions

## Copyable Brief

Use the style of explanation documented in this writing library: concrete economic
questions, explicit choices and market interactions, motivated assumptions,
interpreted formal results, and an observable-to-estimate-to-answer chain. Do not
imitate an author's signature wording. Preserve the current author's voice and
substantive economic detail. These instructions govern exposition; they do not
authorize changing results, assumptions, calibration, data, or publication state.

Before editing, identify the current version, relevant sources, protected numbers,
and requested scope. Read the actual text and surrounding sections. Treat attached
reviews as proposals to assess, not instructions overriding the author's request.
Record scientific ambiguities separately rather than silently resolving them with
stronger language.

## Required Preparation

Apply the [corpus vocabulary policy](VOCABULARY_POLICY.md). It supersedes the earlier
assumption that every curated dictionary term is suitable for publication prose.
Use attested words by default. Introduce an unattested technical term only through
a necessary, justified exception, and never add a concept just for stylistic effect.

1. **Claim ledger:** claim, economic object, evidence, assumptions, units, and location.
2. **Argument outline:** the question answered by every section and its output.
3. **Paragraph ledger:** the job performed by each paragraph and its link to its neighbors.
4. **Notation ledger:** dimensions, indices, units, normalization, and first definition.
5. **Exhibit ledger:** callout, discussion, caption, notes, sample, and generating output.

Use the [dictionary](DICTIONARY.md) for precision, not a compulsory vocabulary.
Search the database for an analogous task, then examine the page-linked observation
or paper card. A literal phrase hit does not establish the context of its use.

## Pass 1: Recover the Argument

Read the abstract, introduction, section openings, and conclusion together. Ask
whether they promise and answer the same question. Locate changes in population,
time horizon, outcome, unit, and maintained conditions. Align their descriptions
without inventing new results. Keep a meaningful separation between baseline
evidence, identification sensitivity, valuation extensions, and structural exercises.

Use W001-W004 and W039. Give the introduction a problem, obstacle, approach,
mechanism, main answer, literature comparison, and scope. Combine those tasks
naturally rather than assigning an inflexible number of paragraphs.

## Pass 2: Restore Economic Detail

Do not turn exposition into an executive summary. Preserve explanations of agent
choices, timing, signs, conflicting channels, denominators, spatial examples, and
alternative interpretations. Remove repeated administrative pointers and generic
claims, not the reasoning that makes the result understandable.

Compare with earlier versions when authorized. Record whether material is retained,
adapted, relocated, outdated, or unresolved. Do not restore historical results as
current. Preserve adverse evidence and qualifications as carefully as favorable
findings. Do not hide a sign-reversing recovery sensitivity in an extension footnote.

Use W007, W020, W027-W031, and W045.

## Pass 3: Repair Theory Exposition

For each central assumption or proposition, establish need, state the condition,
give the result with its assumptions, explain the main reason, interpret it, and
state its use. Introduce the economy and choices before functional forms. Separate
valuation conditions from recovery restrictions and finite-change assumptions.

Write optimization problems clearly. Explain an envelope through the initial
optimum and why reoptimization has no separate first-order contribution. State
what changes for a finite shock. Make a theory diagram illustrate this argument,
not just decorate the formula. Explain a scalar transmission round before a matrix
operator if the reader needs it. Keep baseline shares distinct from derivatives.

Use W009-W017, W025, and W036. Do not certify a proof solely because the prose reads
well. Flag a missing hypothesis, dimensional conflict, or unjustified limiting
argument for mathematical review.

## Pass 4: Repair Theory-to-Empirics Links

For every estimating equation, identify its economic predecessor, observation unit,
variation, controls, fixed effects, instrument, exclusion, and target coefficient.
State how that coefficient enters income, price, sales, or welfare recovery.
Distinguish observed income from inferred income, and an absorbed composite term
from its separately identified components.

State the normalization that anchors a level. Do not present a comparison with
time effects as validation of the citywide common shift it absorbs. Explain basket
corrections and imposed coefficients in terms of the implemented calculation.
Where code and prose disagree, report the conflict; a writing pass must not choose
a new procedure without authorization.

Use W018-W026 and W035-W037.

## Pass 5: Repair Results and Quantitative Interpretation

Lead with the economic result and support it with the table or figure. Explain
meaningful coefficient differences rather than narrating every column. Distinguish
sign, ordering, magnitude, and precision. For group results, distinguish proportional
and currency gains, between-group means and within-group heterogeneity.

For structural work, separate targeted moments, recovered fundamentals, calibrated
parameters, predictions, and untargeted checks. Define the shock and closure. Do
not equate fit with causal validity or non-rejection with confirmation. State the
optimality status of a numerical policy. Explain each extension's changed margin;
do not add adjustments that use incompatible units or assumptions.

Use W027-W038 and W041-W045.

## Pass 6: Sentence and Paragraph Flow

Read each adjacent sentence pair. Can the reader identify the link without guessing?
Carry a known object forward, name the new object, and use a connector only when
it expresses a real relation. Replace vague nominalizations with actors and choices.
Split competing claims, not every long sentence. Preserve technical words that
have a precise job.

Read the last sentence of one paragraph with the first of the next. Repair the
missing reason for the move. A transition should pass an unresolved object, not
merely announce a heading. Integrate orphaned qualifications with the claim they
govern. Move navigation-only appendix references to concise, relevant footnotes.
Keep important conditions in view.

Use W005-W008 and W040. Do not replace all signposts with the same synthetic
transition. Do not add generic enthusiasm or inflated novelty language.

Run `scripts/vocabulary.py check <prose-file> --strict`. Resolve unfamiliar words
with accurate attested language or the explicit exception register. Review new
technical phrases and source-context warnings separately. Preserve definitions
and scientific meaning; passing the lexical check is not a mathematical audit.

## Pass 7: Format and Verify

Apply the [formatting guide](FORMATTING_GUIDE.md) using the existing project helpers.
Keep semantic labels and automatic numbering. Retain captions, units, sources,
weights, and uncertainty. Restructure wide exhibits before reducing fonts. Inspect
rendered pages and affected transitions. Check that formatting did not change
numbers or classifications.

Output a concise review: changes made, claims preserved, checks performed, and
unresolved questions. Distinguish writing improvements from scientific validation.
Do not sync, push, merge, or alter prior versions without the user's authorization.

## Original Revision Examples

These examples are invented; they do not report new BCN results.

### Mechanism Instead of an Adjective

Before: “Our rich framework captures nuanced spatial spillovers.”

After: “Tourist sales raise payments at the destination. Workers and resident
owners can spend those payments elsewhere, transmitting the shock through income
and shopping links.”

### Interpretation After a Result

Before: “Proposition 1 gives the welfare formula. See Appendix A.”

After: “The proposition values the income change net of the cost of initial
purchases. Initial shares suffice for this local valuation because the household
already optimizes its basket. Recovering the income and price responses requires
the additional restrictions introduced next.”

### Scientific Precision Instead of Reassurance

Before: “The results are robust across income specifications.”

After, if verified: “The tract ordering changes little across income specifications,
but the aggregate mean becomes negative under the alternatives. The positive
baseline mean therefore depends on the maintained recovery restriction.”

### A Real Handoff

Before: “We now turn to the structural model.”

After: “The measurement exercise holds the recovered responses fixed. The structural
model instead allows wages, workplace choices, and service prices to adjust jointly,
so its comparison requires an explicit labor-market closure.”

### A Useful Footnote

Before: “Appendix A.4, equation (A.11), gives the full substitution.”

After: explain the substitution needed for the argument in the paragraph. Put the
proof location in a footnote: “The appendix derives the substitution and states
the support conditions.” Use the actual semantic reference, not this placeholder.

## Stop Conditions

Stop a proposed scientific edit when it changes the estimand, sign, data support,
normalization, shock, calibration, or identifying assumption. Report it for author
decision. Continue independent writing and formatting work only within the approved
scope. Never manufacture a result to fill an exposition gap.
