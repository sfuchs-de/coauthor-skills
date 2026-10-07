# Writing Spatial Economics

## Purpose and Evidence

This is a working guide for theory, empirical, and quantitative economics, not an
attempt to imitate an individual's voice. It draws on 23 distinct papers involving
Dave Donaldson, Treb Allen, Costas Arkolakis, and Stephen J. Redding. Coauthors are
credited in the [catalogue](catalogue.md). The review examines selected substantive
passages across each paper, plus rendered page samples. It does not certify proofs,
estimates, or every sentence in every supplement.

**Observed** means a practice recorded at a page-linked source. **Recommended**
means a house instruction developed from that evidence and the needs of an author.
A practice appearing in a successful paper is not automatically a good choice for
every paper. The [rule register](data/rules.json), [paper cards](reviews/), and
[dictionary](DICTIONARY.md) provide the audit trail.

## The Main Principle

Give the reader an economic question, the object needed to answer it, the reason
that object is difficult to observe, and the argument that makes it recoverable.
Keep that sequence visible as the paper moves from theory to data to results.

This is a recommendation about reasoning, not a requirement that every paper use
the same section order. A data-first paper may establish a pattern before modeling
it. A theory-first paper may derive an object before measuring it. Neither should
ask the reader to infer how its successive sections answer the opening question.

Before drafting, complete this chain:

1. **Question:** What change, population, horizon, and outcome are at issue?
2. **Mechanism:** Which choices and market interactions could produce the effect?
3. **Valuation:** How does the outcome relate to the quantity the reader cares about?
4. **Recovery:** Which unobserved objects must be inferred, under which restrictions?
5. **Identification:** What variation separates the effect from other influences?
6. **Implementation:** How do observed records become the required objects?
7. **Evidence:** What is estimated, what is tested, and what is only illustrated?
8. **Application:** Which extra assumptions permit the counterfactual or policy exercise?

Every arrow needs an argument. A regression is not itself a welfare formula; an
accounting identity is not a behavioral response; a fitted residual is not an
independently measured amenity. An exactly matched baseline is not an independent
validation exercise. Use the dictionary's distinctions before polishing vocabulary.

## Sentence to Sentence

### Use the Corpus Vocabulary

Apply the [adopted vocabulary policy](VOCABULARY_POLICY.md): default to words used
in the sampled articles, checked against their complete included extracts. New
technical wording requires necessity and an explicit exception. Words in this
guide's editorial instructions or original examples are not automatically licensed
for publication. Preserve exact scientific meaning instead of forcing an inaccurate
substitution.

### Carry the Object Forward

Start a sentence with something the preceding sentence established, then add the
new information. This is useful for dense theory because the reader need not solve
notation and argument order simultaneously.

Original example:

> Residents buy services away from where they live. Their expenditure shares
> therefore measure access to several destinations, not just local purchases.
> Those shares determine how a destination price change enters each resident's
> initial-basket cost.

The sequence is residents -> purchases -> expenditure shares -> valuation. Each
sentence changes the argument by one intelligible step. Do not enforce this
mechanically when a contrast or a new question is the more natural connection.

### Put the Economic Actor in the Sentence

Prefer “firms buy the flexible input after observing the output price” to “the
flexible-input optimization stage is undertaken subsequent to price realization.”
Use active voice for choices, measurement, and assumptions. Passive voice remains
useful when the object matters more than the actor: “Standard errors are clustered
by municipality” is direct and informative.

Be precise about agency. Prices do not optimize; firms do. A matrix propagates a
constructed exposure algebraically; an equilibrium system describes endogenous
adjustment. Neither “the network responds” nor “the model identifies” is sufficient
when the underlying operation matters.

### Keep Conditions Beside the Claim They Govern

Write “With fixed workplaces and a given input price, the producer envelope…”
rather than making an unrestricted claim and attaching several exceptions two
paragraphs later. Give long conditions a named assumption and refer to that
assumption in the formal result.

Separate three kinds of qualification:

- A condition needed for the claim belongs in the claim or its immediate context.
- A limitation changing the headline interpretation belongs in the main discussion.
- A proof location, computational detail, or narrow secondary case can be a footnote.

Do not turn every sentence into a disclaimer. Establish a restriction clearly,
then use it consistently until it changes.

### Use Verbs That Match Evidence

“Proves” requires a derivation under stated conditions. “Identifies” requires an
identification argument. “Estimates” describes a statistical procedure, not proof
that its assumptions hold. “Predicts” describes a model implication. “Is consistent
with” does not establish uniqueness of a mechanism. “Cannot reject” does not mean
“confirms.” “Is unchanged across these specifications” is more informative than
“is robust” without a named scope.

Avoid causal verbs for purely descriptive maps. Say what is plotted and what the
contrast motivates. Save “raises,” “reduces,” and “causes” for a causal claim whose
identification is established, or explicitly qualify them as model predictions.

### Manage Length by Structure, Not a Numerical Limit

There is no defensible universal sentence-length target in this corpus. A short
sentence can be vague; a longer sentence can state a necessary condition cleanly.
Split a sentence when it has competing main claims, several nested qualifications,
or a change of object that deserves its own sentence. Keep a condition and its
consequence together when separating them would obscure the logic.

Remove an introductory phrase only after checking its function. “To recover
income…” signals a purpose. “As noted above…” often adds nothing. “In contrast…”
is useful only if the contrasted object is clear. Words such as “tractable,”
“framework,” and “heterogeneous” are not banned; say what becomes tractable, what
the framework contains, and which dimension is heterogeneous.

## Paragraph to Paragraph

### Give Each Paragraph an Economic Job

An effective paragraph generally does four things, though not always in four
sentences: makes a claim, supplies its reason or evidence, interprets it, and
establishes the next unresolved question. A paragraph devoted to a formal
definition or a data limitation may legitimately do fewer things.

Use a paragraph ledger before editing. Label each paragraph as motivation,
definition, mechanism, derivation, identification, construction, evidence,
interpretation, limitation, or transition. If a paragraph has no job, integrate
its useful content elsewhere. If it has several unrelated jobs, split it.

Do not delete substantive interpretation merely because it is longer than a
summary. Detail earns its place when it explains a sign, a spatial contrast, a
weight, a denominator, a competing channel, or an identifying threat.

### Open with the Claim, Not the Exhibit Number

Instead of:

> Table 2 reports results. Column 1 includes fixed effects. Column 2 adds controls.

Prefer, where supported:

> The income response remains positive when the controls absorb predictable
> seasonal variation. Table 2 compares the baseline with these specifications.
> The estimate changes little, but its interval widens because less identifying
> variation remains.

This is an invented example, not a description of an actual result. If the sign
changes, report that change with equal prominence. A table tour cannot substitute
for the economic argument.

### Write a Handoff, Not Just a Signpost

A signpost says where the paper goes. A handoff says why it must go there.

Weak:

> We next turn to estimation.

Better:

> The envelope values welfare once income and destination prices are known.
> Prices are not observed in the transaction records, so we next use bilateral
> spending responses to recover the price-related component.

The second version leaves the reader with a specific problem and a promised
operation. It must still be scientifically correct for the actual recovery method.

For adjacent paragraphs, write the missing “because,” “therefore,” or “however”
in a private margin note. If no relationship exists, the order may be wrong.
Usually the final prose should express the relation directly rather than repeating
those connectors in every paragraph.

### Avoid Orphaned Qualifications and References

A sentence about an appendix equation should not interrupt the economic argument
unless that equation supplies the next necessary step. Integrate the content,
move the navigation to a footnote, or remove the pointer if it is redundant.

An important assumption must not survive only in a footnote. Conversely, a
technical cross-reference should not receive a standalone main-text paragraph.
Footnotes should explain the relevance of their destination, not just list labels.

## Subsection to Section

### State the Output of Each Subsection

The opening should tell the reader what the subsection establishes or measures.
Its ending should identify the object handed to the next subsection. Prefer
semantic continuity over repeated roadmaps.

For a recursive method, make the sequence explicit once:

> We first construct the baseline shares. We then estimate the response parameters.
> Together these objects recover income and sales changes. Finally, price shares
> translate recovered sales into destination-price changes.

Later openings can carry the actual object: “The recovered sales responses provide
the variation used to estimate price shares.” They need not repeat the entire plan.

### Choose an Order That Matches the Argument

Possible research architecture:

| Stage | Reader's question | Section output |
|---|---|---|
| Motivation | Why does the usual local comparison miss something? | A precise research question |
| Theory | What choices connect the shock to welfare? | Valuation and recovery relationships |
| Data and facts | Can the required links be measured? | Samples, accounts, and motivating patterns |
| Identification | What separates the shock from other changes? | Estimating equations and assumptions |
| Baseline results | What do the estimates imply? | Income, costs, welfare, and credible scope |
| Sensitivity | Which conclusions depend on maintained choices? | A map of stable and changing conclusions |
| Extensions | What additional margins or structure change the answer? | Clearly conditional comparisons |
| Conclusion | What has been learned? | The answer, its boundaries, and unresolved questions |

This is a recommendation, not a mandatory table of contents. Facts may come before
theory when they motivate its mechanism. Identification may follow the data when
the design depends on provider coverage. Keep the dependency order intact.

## Abstract and Introduction

### Abstract

Use a question or object, the method and setting, the main answer, and the most
important condition governing that answer. Define unusual terms. Include numbers
only if their units and comparison are intelligible without the paper. Do not use
the abstract as a compressed literature review or a catalogue of every appendix.

Original skeleton:

> We study how [shock] affects [outcome/population]. We combine [data] with [specific
> theoretical or empirical operation] to account for [missing channel]. For
> [comparison and horizon], [principal finding with units]. [Important heterogeneity
> or sensitivity]. These results show [bounded economic implication].

Do not fill the skeleton with inflated novelty claims. “We develop a method to
recover…” is useful only after saying which object is otherwise unavailable.

### Introduction Paragraphs

An introduction needs a reader-facing argument, not a rigid paragraph quota:

1. Establish the economic problem with a concrete example, fact, or puzzle.
2. Explain the obstacle in the existing comparison or measurement.
3. State what the paper does and why the method addresses that obstacle.
4. Introduce the mechanism and the data that make the approach possible.
5. Give the principal findings in an economically meaningful hierarchy.
6. Compare with the closest literature by object, assumption, or identification.
7. State the scope and supply a short roadmap if it helps.

Paragraphs can combine these jobs. Do not preserve a generic opening simply because
it sounds academic. Do not remove concrete mechanism discussion to force a shorter
introduction. Readers should understand the core contribution before encountering
an inventory of papers.

### Literature Discussion

Group references by the claim they support or the contrast they establish. A
useful comparison identifies a shared idea and the precise difference: a new
observable, an additional adjustment margin, weaker assumptions, a different shock,
or a separate validation exercise. Avoid claiming superiority over a caricature.

Check that a citation supports the exact use. A paper about commuting cannot
automatically justify a shopping-demand restriction. A specific-factor analogy
does not establish all of the timing and input-price assumptions of a new model.
References to a general theorem still require its hypotheses in the current setting.

## Theory: Generality Without Losing the Reader

### Introduce the Economy Before Functional Forms

Name agents, locations, choices, endowments, prices, income, and the shock. Define
index domains and distinguish origins from destinations. Explain timing before
writing an optimized value function. State which decisions are fixed and which
adjust after the shock.

Then introduce restrictions when they become necessary. Separate:

- Conditions for first-order valuation.
- Conditions for identifying behavioral responses.
- Conditions for a finite-change bound.
- Conditions for a particular quantitative calibration or equilibrium solve.

A general utility function in the opening does not make every later recovery
formula general. A CES implementation should be called CES when it enters.

### The Formal-Statement Protocol

For every assumption or proposition:

1. **Need:** Explain what the reader is trying to establish.
2. **Condition:** State the restriction and its economic content.
3. **Result:** Name relevant assumptions and specify the object, units, and domain.
4. **Reason:** Give the main argument or a proof sketch when it illuminates the result.
5. **Interpretation:** Explain signs, margins, aggregation, and the held-fixed objects.
6. **Use:** State what becomes measurable or computable next.

Not every theorem needs a long discussion. The required amount depends on its role
in the paper. Never strand a formal statement between unrelated paragraphs, or
follow it only with “see Appendix A.” Appendix proofs supplement the argument;
they do not supply its main-text purpose.

### Explain Optimization and Envelopes

Write the choice problem before invoking the envelope when the problem is central.
Explain why a behavioral adjustment has no separate first-order term: its marginal
contribution at the initial optimum is zero under the stated regularity conditions.
This does not mean quantities never change or that finite changes are linear.

An original producer illustration:

> The firm chooses a flexible input after observing the service price, while its
> workplace labor is fixed. At the initial optimum, the extra revenue from a small
> input expansion equals its extra cost. A small service-price increase therefore
> changes the optimized return through its value on initial output; the input
> adjustment adds no separate first-order contribution.

An original consumer illustration:

> A price increase changes the cost of the initial basket. The consumer can revise
> purchases, but optimization makes the value of that revision second-order locally
> under smoothness. First-order valuation therefore uses initial purchases rather
> than a newly chosen basket.

For an income-exposure diagram, connect the motion to the formula: identify the
pivot, hold the initial production plan fixed, and evaluate the budget's movement
at initial consumption. Then explain which input or shopping adjustments make a
finite change depart from a pure rotation. Do not infer second-order magnitudes
from a purely first-order diagram.

### Matrices Need Economic Interpretation

Before defining a matrix, say what one entry measures, its units, and its index
direction. State whether rows or columns sum to one and why. A baseline allocation
matrix, a marginal derivative matrix, and an equilibrium feedback operator are
different objects even when their dimensions match.

Show one scalar transmission round before a matrix expansion when the audience
needs intuition. Explain what is held fixed in each round. Distinguish an inverse's
existence from convergence of a geometric expansion; check the spectral condition
for the expansion actually used. Interpret the resulting term rather than merely
calling it a “multiplier.”

### Simple Examples and General Results

An illustration should remove distracting dimensions, not silently establish the
full theorem. State what it retains and what it omits. A general-preference,
general-production example is useful when the central point is optimization. A
parametric example is useful when a curvature or substitution parameter is central.
Return to the general economy with an explicit explanation of what survives.

## Data and Stylized Facts

### Describe Data by the Question They Answer

For each source, record provider, unit, geography, dates, population coverage,
observed variables, exclusions, and the role in the analysis. Distinguish raw
records, imputed links, scaled aggregates, calibrated accounts, and estimated
responses. Put the authoritative construction detail in a data appendix, but keep
coverage differences that affect interpretation in the main text.

Explain why two spending measures are not interchangeable. A transaction's
merchant location measures demand at a destination; an observed home address
assigns a resident purchase to its origin. These records can differ in provider
coverage and sample selection. Neither automatically measures all consumption.

### Give Every Fact Substantive Interpretation

Use the sequence **pattern -> magnitude -> possible mechanisms -> design implication**.
For a map, specify the variable and denominator, discuss real spatial contrasts,
then explain why they matter. Do not spend the paragraph reciting colors. For
seasonality, distinguish changes in totals from changes in shares or profiles.
For networks, discuss which residents or firms are reached through which links.

Alternative explanations should sharpen the empirical question. A geographic
contrast can reflect demand, substitution, earnings links, or common seasonal
shocks. Do not resolve these by assertion before the identification section.

Use counts and concentration statistics only from verified support. State whether
groups are defined using baseline values, ranks, or changes. A tercile comparison
is not a correlation coefficient; it does not establish a causal mismatch.

## Identification and Empirical Recovery

### Keep Three Arguments Separate

1. **Economic representation:** why the outcome decomposes into the named terms.
2. **Statistical identification:** which variation and orthogonality restrictions recover them.
3. **Normalization or level recovery:** what anchors otherwise undetermined components.

Fixed effects can absorb an unobserved term without identifying its economic
components separately. An origin effect containing income and a price-index term
does not become pure income merely because it is called an origin effect. Explain
the correction, restriction, or normalization that permits the interpretation.

For a basket correction, state the destination terms being netted, the baseline
weights, the timing, and whether the coefficient is imposed or estimated. If
relaxing a restriction reverses the headline sign, that is an identification
sensitivity in the main results, not a minor appendix robustness note.

### Introduce the Regression as an Estimand

State the observation unit and variation first. Then show the equation, define the
regressors and fixed effects, explain endogeneity or interference, introduce the
instrument or control construction, and state the exclusion restriction. Finish
by describing which coefficient or combination feeds the recovery formula.

Controls remove named variation; they do not prove exogeneity. Network exposure
can remain in nominally untreated places. Explain what the control or instrument
does under its actual construction, not an informal description of an earlier version.

### Discuss Inference at the Relevant Level

Name clustering, weights, and generated-regressor uncertainty. Say which uncertainty
is included and which is conditional on calibration or maintained allocation.
Separate a coefficient confidence interval from a welfare sensitivity range and
from a partially identified bound. Label observed-income comparisons by the
variation they retain; a comparison with time fixed effects need not validate an
aggregate common shift.

## Results and Robustness

### Interpret Before Touring Columns

Report the economic answer, its magnitude and units, the evidence supporting it,
and the mechanism consistent with it. Use column numbers to locate the evidence,
not to determine the paragraph's structure. Explain meaningful changes in the
sample or support before comparing estimates.

For distributions, discuss the mean, relevant dispersion, non-monotonicity, and
the economic links behind the pattern. A low-income group can gain more
proportionally but less in currency. Distinguish group means from within-group
household heterogeneity. Do not infer unobserved ownership or employment channels
from a map without supporting allocation or data.

### Organize Robustness by the Threat

Use headings or paragraphs for sample selection, recovery restrictions, weights,
price mapping, propagation horizon, inference, and equilibrium closure. Explain
what each check changes and what conclusion survives. Keep unfavorable findings
as visible as favorable ones.

A strong summary separates:

- Sign and aggregate level.
- Spatial or distributional ordering.
- Magnitude and uncertainty.
- Channel attribution.
- Comparability of units and samples.

Do not call all of these stable because one remains stable. “The ordering survives,
but the mean becomes negative” is a substantive result, not an embarrassment to
write around.

## Quantitative Models and Policy

### Explain What Is Matched

List baseline accounts, calibrated parameters, estimated parameters, free residuals,
and untargeted moments. State the labor and ownership closure, numeraire, shock,
and welfare weights. Distinguish matching an initial account from predicting a
response. Compare local and nonlinear responses using matched inputs before
attributing disagreement to model curvature.

A scatter is not a causal test. Report its transformation, residualization, support,
weights, fit line or smoother, and comparison benchmark. Explain whether those
moments were used in calibration. A high correlation may coexist with biased
levels or slopes. A non-rejection can coexist with low power or alternative models.

### Explain What the Policy Exercise Assumes

Define the tax base, gross payments, producer receipts, revenue, rebates, and who
receives them. State whether the exercise holds observed responses fixed or
re-solves equilibrium. Separate estimated elasticities from calibrated ones.
Report a local optimum as local unless global optimality is established.

For a small differentiated-policy gain, distinguish an economically small premium
from solver disagreement, sparse support, or untested restrictions. A district-level
policy changes the feasible set. It cannot be presumed to improve the true optimum
of a more flexible problem, though it may be more stable or easier to implement.

### Keep Extensions Non-Additive Unless Proven Otherwise

Shopping-cost residuals, workplace mobility, curvature, housing, and tax counterfactuals
can alter different objects and denominators. Explain whether each is a valuation
extension, a recovery change, or a new equilibrium exercise. Do not add their
reported changes as though they were independent adjustments to one common outcome.

## Conclusion and Appendices

The conclusion should answer the opening question in the same units and scope,
state the mechanism supported by the evidence, and name the principal limitation.
Use unresolved questions to explain what data or identification would improve the
answer. Do not add a new result, convert a conditional exercise into an unconditional
policy recommendation, or repeat every contribution claim from the introduction.

Organize appendices around the current argument. A short paper appendix should
support central derivations, measurement, and diagnostics. An online appendix can
hold detailed proofs, finite-change programs, additional margins, and numerical
verification. Historical or incompatible exercises belong in a recoverable archive,
not in the active evidence chain. Preserve adverse findings and disclose missing
current checks where they affect credibility.

## Practical Review Protocol

1. Freeze the draft and results; record what a writing pass may change.
2. Build the claim ledger: claim, evidence, assumption, units, and destination.
3. Read headings alone. Check that their order follows the dependency chain.
4. Read first and last sentences of every paragraph. Repair missing handoffs.
5. Read each paragraph in full. Restore economic detail that a summary omitted.
6. Check every assumption/result pair using the formal-statement protocol.
7. Trace each empirical coefficient to the object used in valuation.
8. Trace each headline to its sample, weights, uncertainty, and sensitivity.
9. Move navigation-only material to useful footnotes; keep essential scope in view.
10. Read prose around every exhibit before reviewing its typography.
11. Render the revised document and inspect affected pages, not just the TeX log.
12. Record unresolved scientific questions separately from completed writing edits.

The aim is an argument a reader can follow without repeatedly searching backward
for a definition or forward for an essential qualification. It is not simply a
shorter paper.
