# Economics Derivation Patterns

Use this reference for substantial derivations in self-contained research notes. The target style is an economics appendix: transparent algebra plus interpretation of the economic margin.

## Standard Derivation Block

Use this structure in appendices and for important main-text derivations:

```tex
\subsection{Deriving the [object]}\label{app:derive-object}

\paragraph{Economic object.}
We derive [object], which measures [economic meaning]. The relevant margin is a change in [policy/price/shock] holding fixed [objects] and allowing [objects] to adjust.

\paragraph{Primitives and notation.}
Let [definitions]. The relevant equilibrium conditions are
\begin{align}
  [condition 1], \label{eq:derive-condition-1}\\
  [condition 2]. \label{eq:derive-condition-2}
\end{align}

\paragraph{Step 1: Differentiate the primitive condition.}
Starting from \eqref{eq:derive-condition-1},
\begin{align}
  [left-hand side]
  &= [first expansion] \notag\\
  &= [substitution] \notag\\
  &= [simplified expression], \label{eq:derive-step-1}
\end{align}
where the first equality uses [identity/theorem], and the second substitutes [definition].

\paragraph{Step 2: Substitute the equilibrium response.}
Using \eqref{eq:derive-condition-2} in \eqref{eq:derive-step-1},
\begin{align}
  [object]
  &= [intermediate expression] \notag\\
  &= [final expression]. \label{eq:derive-final}
\end{align}

\paragraph{Economic interpretation.}
Equation \eqref{eq:derive-final} decomposes the effect into [term 1], [term 2], and [term 3]. The first term captures [economic force]. The second term captures [behavioral or general-equilibrium adjustment]. The sign is [positive/negative/ambiguous] because [economic reason].

\paragraph{Checks.}
If [special case], then \eqref{eq:derive-final} reduces to [known benchmark]. If [parameter] goes to [limit], the [term] vanishes, matching the intuition that [economic intuition].
```

## Common Derivation Types

### FOC or Euler Equation

Start from the objective and constraint. Write the Lagrangian if there is a constraint. Take derivatives with respect to the choice variable. Substitute prices, wedges, or multipliers only after the raw FOC is visible. Interpret marginal benefit, marginal cost, and wedge terms.

### Envelope or Welfare Derivative

State which variables are optimized and which are policy shifters. Show why choice-response terms drop out or do not drop out. Identify mechanical, behavioral, fiscal, and distributional components separately.

### Elasticity or Pass-Through System

Define the log differential. Write the primitive demand/supply/equilibrium response in differentials. Stack the system only after the scalar or block equations are clear. Check signs and row/column sums when the object is a share or probability system.

### Hat-Algebra or Counterfactual Mapping

Define hats before using them. State the baseline normalization. Derive each block in logs or hats before stacking. Explain which objects are solved endogenously and which are treated as shocks.

### Empirical Microfoundation

Start from the structural relationship. Take the first-order approximation explicitly. Show what is absorbed by fixed effects. Define the residualized regressor or exposure term only after showing why common components drop out.

### Decomposition

Define the total effect. Add and subtract terms explicitly. Label each component by economic force, not only by algebraic origin. Include a benchmark where one component is zero.

## Style Rules

- Prefer `align` for multi-line derivations and reserve `equation` for single final objects.
- Put `\notag` on intermediate lines unless they are referenced later.
- Label final equations and important intermediate equations.
- Use prose between displays to explain the economic step being taken.
- Avoid long unbroken equation chains. Break after a substitution, a normalization, or an economic interpretation point.
- Do not hide sign restrictions in prose; state them as assumptions or directly after the relevant equation.
- Do not use theorem environments for conjectural or numerically suggested claims.
- Use "maintained approximation" for linearizations and first-order systems whose neglected terms matter conceptually.
