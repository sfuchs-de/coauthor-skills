# Mathematical Exposition and Derivation Protocol

## Contents

- Formal-object classification and motivation
- Definitions, dimensions, derivation routes, and equality audits
- Assumptions, interpretation, intuition, and downstream use
- Theorem presentation, equation placement, appendices, and correctness routing

## Purpose

A technical result should never appear as an isolated display. The reader needs to know:

1. why the result is needed;
2. what prior result it uses;
3. what every new object means;
4. how the result is obtained;
5. what the result says mathematically;
6. what it says economically or scientifically;
7. what the paper can do after obtaining it;
8. which assumptions limit the interpretation.

Use the sequence:

`motivate -> inherit -> define -> derive -> state -> parse -> interpret -> use -> qualify`.

Not every routine equation requires a long discussion, but every central result requires the full chain.

## 1. Classify the formal object

Before reviewing exposition, classify the object:

- primitive definition;
- accounting identity;
- behavioral equation;
- equilibrium condition;
- estimator or estimating equation;
- first-order condition;
- fixed point;
- reduced form;
- local approximation;
- theorem, proposition, lemma, or corollary;
- special case;
- decomposition;
- comparative static;
- welfare formula;
- algorithm or computational procedure.

The prose must not blur these categories. An accounting identity is not an estimated behavioral relation. A projection is not automatically a structural derivative. A special case is not the general model.

## 2. Motivation before notation

Before introducing a new formal object, state the unresolved task.

Weak:

> Let \(M=D_y^{-1}SD_vC\).

Stronger:

> The direct shock identifies where demand first arrives, but it does not capture the income that is subsequently earned and spent elsewhere. To represent one such income-and-spending round, define \(M=D_y^{-1}SD_vC\).

The motivation should be specific enough that the reader can predict the role of the object.

## 3. Inheritance from prior results

Name the starting point. Prefer exact references:

- “Starting from goods-market clearing in (2.4)...”
- “Substituting the income envelope (2.3) into the bilateral identity (2.9)...”
- “Premultiplying the destination response by the shopping-share matrix \(S'\)...”
- “Applying the implicit function theorem to \(F(x,\theta)=0\)...”
- “Using the spectral-radius condition in Proposition 2.2...”

Avoid vague phrases such as “using the framework above” when a numbered equation or proposition is available.

## 4. Define mathematical objects completely

For each new symbol, check:

- scalar, vector, matrix, function, operator, set, or measure;
- dimensions;
- domain and codomain when non-obvious;
- row or column orientation;
- indices and their meaning;
- units or normalization;
- whether it is observed, constructed, estimated, calibrated, or theoretical;
- whether it is baseline, counterfactual, exact, fitted, or approximated;
- sign, support, or regularity restrictions;
- whether it depends on time, state, parameter, or shock even if notation suppresses that dependence.

Do not define six objects in a single trailing “where” clause after a dense equation. Group definitions in the order the equation uses them.

### Dimension audit

For every matrix expression, verify conformity. Record dimensions for central operators at least once. Examples:

- \(S\in\mathbb R^{N\times N}\);
- \(C\in\mathbb R^{N\times N}\);
- \(g\in\mathbb R^N\);
- \(D_T\in\mathbb R^{N\times N}\);
- \(M=D_y^{-1}SD_vC\in\mathbb R^{N\times N}\);
- \((I-M)^{-1}D_Tg\in\mathbb R^N\).

Check whether rows refer to origins or destinations and whether a transpose is required.

## 5. Name the derivation route

Every important result should identify how it is obtained. Use one or more of these labels.

### Direct substitution

State the chain explicitly:

1. start from equation A;
2. substitute equation B for object X;
3. use identity or assumption C;
4. collect terms;
5. obtain equation D.

Do not say merely “combining the previous equations.”

### Differentiation or log-linearization

State:

- the equation differentiated;
- variables held fixed;
- evaluation point;
- whether the differential is exact or first order;
- what normalization permits log changes;
- whether higher-order terms are omitted.

### Envelope theorem

State:

- the optimization problem;
- the choice variables already optimized;
- which parameters change;
- what baseline shares or derivatives weight the change;
- whether the result is exact to first order;
- whether fixed endowments enter through an envelope or directly.

### First-order or KKT conditions

State:

- objective and constraints;
- interior or boundary status;
- regularity or constraint qualification;
- complementary slackness where relevant;
- whether the condition is necessary, sufficient, or both.

### Market clearing and fixed points

State:

- the clearing identity;
- how endogenous responses feed back;
- the one-round operator;
- the shock-entry term;
- the condition for inversion or convergence;
- whether the Neumann series is nonnegative or signed.

### Implicit function theorem

State:

- equilibrium system \(F(x,\theta)=0\);
- regularity and nonsingularity condition;
- derivative formula;
- which states have been eliminated;
- local nature of the result.

### Projection or regression mapping

State:

- exact response being projected;
- exposure or regressor basis;
- residualization and weights;
- rank condition;
- condition for exact recovery;
- interpretation when the span condition fails.

### Duality or conjugacy

State:

- primal and dual problems;
- conjugate exponents or functions;
- equality condition;
- mapping between primal choices and dual derivatives;
- economic interpretation of the dual object.

### Spectral or resolvent argument

State:

- operator and state space;
- spectral-radius or norm condition;
- why the inverse exists;
- what each power represents;
- whether eigenmode intuition is exact or illustrative;
- whether nonnormality matters.

### Approximation

State:

- small parameter or expansion variable;
- order of approximation;
- remainder term;
- norm or metric;
- uniformity and stability conditions;
- empirical or computational implication.

If the route is different, name it precisely.

## 6. Equality-by-equality audit

For every nontrivial chain of equalities, annotate the justification:

| Step | Equality | Justification | Assumption used | Potential issue |
|---|---|---|---|---|

Common hidden steps:

- changing from levels to logs without positivity;
- replacing an average share with a marginal response;
- using homogeneity or Euler’s theorem without stating degree;
- replacing a matrix with a scalar loading;
- commuting matrices that need not commute;
- treating a projection coefficient as a derivative;
- dropping an origin price-index term;
- inserting a transpose to fix dimensions without explaining orientation;
- changing a direct-plus-tail basis to a direct-plus-full basis without matching scaling;
- using a local approximation for a large counterfactual;
- taking a special eigenmode result as a generic operator result.

## 7. State assumptions where they do work

Do not collect all assumptions in a remote list if the reader cannot tell which result uses which restriction.

For each result, distinguish:

- assumptions needed for existence;
- assumptions needed for uniqueness;
- assumptions needed for an algebraic simplification;
- assumptions needed for empirical implementation;
- assumptions needed only for structural interpretation;
- assumptions needed for a sign result;
- assumptions needed for aggregation;
- assumptions needed for a special case.

A result may be general while its empirical mapping is restrictive. Keep those layers separate.

## 8. Explain the displayed result

Immediately after a central display, parse it.

A useful order is:

1. left-hand side: what outcome is being characterized;
2. direct or primitive term;
3. endogenous propagation or transformation;
4. incidence or loading term;
5. conditions for sign, convergence, or identification.

Do not repeat the symbols in prose without adding meaning.

Weak:

> The first term is the direct term and the second term is the indirect term.

Stronger:

> The diagonal term injects the tourist shock at the destinations where spending occurs. The resolvent then repeats the income-and-spending cycle, so the \(h\)-th power records the \(h\)-th subsequent round.

## 9. Economic or scientific intuition

For an economically important result, answer:

- Who gains or loses?
- Through which margin?
- Where does the shock enter?
- What is held fixed?
- What leaks out or feeds back?
- Which baseline shares act as sufficient statistics?
- What forces determine the sign or magnitude?
- What familiar benchmark does the result nest?
- What new margin changes the benchmark intuition?

Avoid intuition that merely anthropomorphizes the equation. Explain the mechanism.

## 10. Mathematical significance

Discuss mathematical properties only when they matter, but do so explicitly when central:

- existence and uniqueness;
- invertibility;
- stability;
- positivity or sign indefiniteness;
- monotonicity;
- convexity or concavity;
- rank;
- continuity or differentiability;
- eigenstructure;
- approximation error;
- boundary conditions;
- invariance;
- identification and collinearity.

Do not call a result “closed form” if it still requires solving an unspecified equilibrium object. Do not call a condition “mild” without explaining its content.

## 11. Explain what the result enables

Every central result should have a use sentence:

- “This formula supplies the welfare weights used in Section 4.”
- “The multiplier turns the full shock vector into the origin and destination exposures used in the regression.”
- “The rank condition clarifies when the four coefficients recover common structural loadings rather than a best linear projection.”
- “The nonlinear derivative provides the policy gradient used by the optimizer.”

A theorem that is never used is either an orphan or an appendix result.

## 12. Distinguish levels of interpretation

Use stable labels and do not move between them silently:

1. **identity**;
2. **fitted response**;
3. **projection coefficient**;
4. **reduced-form causal response**;
5. **structural derivative**;
6. **calibrated model response**;
7. **counterfactual outcome**;
8. **welfare object**.

If a mapping requires a span, pass-through, ownership, or functional-form condition, state that before adopting the stronger label.

## 13. Theorem and proposition protocol

Before the statement:

- identify the unresolved question;
- explain why a formal result is useful;
- preview the result in words without giving away every detail.

In the statement:

- include the assumptions actually needed;
- define objects before use;
- distinguish general result from special case;
- avoid packing interpretation into the theorem statement unless it is mathematically part of the claim.

After the statement:

- explain the mechanism;
- parse the terms;
- state the key condition;
- give a special case or sanity check when useful;
- say where the proof is;
- state how the paper uses the result.

For an appendix proof:

- reproduce the exact main-text statement or reference it unambiguously;
- use matching notation;
- number steps when the proof has a substitution chain;
- state where each prior result enters;
- close by identifying the main-text equation or proposition obtained.

## 14. Equation placement and numbering

Display an equation when it is central, reused, or easier to parse in display. Keep routine algebra inline or in an appendix.

Number an equation when the manuscript refers back to it or when it is a named step in the argument. Avoid numbering every display and then never citing it.

Do not leave a display grammatically detached. The sentence before it should lead into the display, and the sentence after it should complete the grammar or interpretation.

## 15. Footnote and appendix allocation for math

Keep in the main text:

- the problem the result solves;
- essential definitions;
- the central equation;
- key assumptions;
- economic interpretation;
- why the result matters for the next step.

Move to a footnote:

- short alternative normalization;
- local edge case;
- one-line algebraic identity;
- citation or nomenclature point;
- brief technical qualification that does not alter the headline claim.

Move to an appendix:

- multi-step proof;
- complete Jacobian;
- regularity conditions;
- projection geometry;
- error bounds;
- alternate closures;
- lengthy special cases;
- numerical implementation and validation.

Do not move the only explanation of a result’s meaning to the appendix.

## 16. Mathematical correctness checklist

Use this as an exposition-screening checklist. For every central result, either cite an existing
verification or explicitly flag the item and route correctness work to `audit-tex-math`; do not
silently repair mathematics during a writing pass.

- [ ] all symbols defined;
- [ ] dimensions conform;
- [ ] index orientation consistent;
- [ ] positivity permits logs or ratios;
- [ ] differentiability and local uniqueness stated where required;
- [ ] inverses have conditions;
- [ ] spectral or norm conditions are sufficient for the stated expansion;
- [ ] signs follow from the stated assumptions;
- [ ] special cases are derived from the general result rather than asserted;
- [ ] approximation order and remainder are correct;
- [ ] projection and identification language match rank and span conditions;
- [ ] empirical scaling matches the theoretical basis;
- [ ] main text and appendix use the same normalization;
- [ ] the conclusion does not strengthen the theorem;
- [ ] any computational implementation matches the displayed mathematics.

## 17. Preferred rewrite pattern

For a poorly introduced equation, use this template:

> **Unresolved task.** [State what the previous result does not yet determine.]
> **Starting point.** [Name the equation or proposition used.]
> **New objects.** [Define the minimal notation, dimensions, and meaning.]
> **Operation.** [State the substitution, differentiation, aggregation, or theorem.]
> **Result.** [Display equation.]
> **Interpretation.** [Parse the central terms and mechanism.]
> **Use and scope.** [State what follows and the conditions needed.]

Compress this template for routine results; do not omit its logic for central ones.
