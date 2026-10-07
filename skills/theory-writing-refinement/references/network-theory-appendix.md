# Appendix Organization Reference

Use this reference when reorganizing a long mathematical appendix after the main text has
been made prose-led.

## Preferred Order

### 1. Finite-Network Identities and Fixed Points

Start with notation and finite-dimensional mechanics:

- notation table;
- weighted finite-dimensional adjoints if transpose/measure conventions matter later;
- resolvent and access identities;
- choice shares, adding-up, and mass preservation;
- clearing and power closure;
- traffic factorization;
- congestion closed forms and elasticities;
- fixed-point maps, well-posedness bounds, and existence/uniqueness qualifications.

Keep existence and uniqueness separate.  If a map includes an inner nonlinear solve, state
that solve as an assumption unless you prove it.

### 2. Continuum Limit, Adjoints, and Spectral Formulas

Then move from discrete sums to PDE objects:

- weighted sums to integral operators;
- killing plus graph Laplacian to killed diffusion;
- local-kernel Taylor expansion;
- reversible drift formula;
- finite-volume weighted Laplacian;
- continuum rescaling;
- theorem-level convergence template;
- nonreversible adjoint system;
- continuum mass preservation;
- self-adjointness and Dirichlet form;
- spectral resolvent;
- nonreversible spectral caveat;
- linearized eigenmode responses and implicit-function comparative statics;
- rectangle/torus modes, large-parameter expansions, zero-mode limits, and Green kernels.

Put nonreversible spectral material after the self-adjoint spectral derivation so it reads
as a caveat/generalization rather than a prerequisite.

### 3. Transport, Welfare, Infrastructure, and Dynamics

Close with interpretive and comparative-static material:

- path-flow to OD inclusive costs;
- log-sum-exp and entropic transport KKT conditions;
- endogenous-destination KKT system;
- Pigouvian/access-externality wedges;
- Wasserstein linearization and mode costs;
- eigenvalue shifts;
- resolvent sensitivity to infrastructure;
- adjoint infrastructure gradients;
- continuous-time closure and local stability.

Keep global optimal-transport or Wasserstein claims conditional unless potential structure
and convexity are explicitly assumed.

## Main-Text Linking Pattern

After a main equation that hides derivation, add one short sentence:

```tex
Appendix~\ref{app:...} derives this identity and records the required assumptions.
```

For fragile claims, use:

```tex
Appendix~\ref{app:...} gives a sufficient-condition version of this statement; it is not a
global uniqueness theorem.
```

Avoid duplicating derivations in the main text.
