# Connected Writing Examples

Original fictional exercises, not BCN results or text copied from the corpus. The first drafts and repairs are preserved. These are revised examples, not evidence of reliable first-pass generation or independent validation.

## L01

An increase in the price of a service changes both what residents pay and what
local producers receive. These effects depend on different links: initial purchases
determine price exposure, while work and ownership determine income exposure.
We first value these changes without imposing a particular form on preferences
or technology. The aim is a local welfare expression, not yet a way to identify
the responses from observed spending.

Consider a competitive firm with smooth production $Q=F(L_0,x)$. Workplace labor
$L_0$ is fixed over the period, but the firm chooses purchased inputs $x$ after
observing the service price $p$. Their price $r$ remains fixed. Payments available
to the fixed workers and owners are the value of this restricted problem:
\[
G(p)=\max_x\{pF(L_0,x)-rx\}.
\]
At an interior optimum, $pF_x=r$: an additional input purchase raises revenue
by exactly its cost. Differentiating around the initial optimum therefore gives
\[
\mathrm dG=Q_0\,\mathrm dp+(p_0F_x-r)\,\mathrm dx=Q_0\,\mathrm dp.
\]
The input choice can change. It contributes no separate first-order term because
the initial choice is optimal. A price increase raises the payments remaining for
workers and owners by its value on initial output, rather than by the full change
in sales. Fixed labor and the given input price are important here. Workplace
labor is fixed, but the wage has not been held constant: the expression
concerns the total payments available to workers and owners.

Resident $n$ receives a fixed share $h_n$ of these payments and fixed outside
earnings $\bar v_n$, so income is $v_n=\bar v_n+h_nG(p)$. The resident chooses
service consumption $c$ and a numeraire good $m$ under $m+pc=v_n$, with general
smooth preferences. Initial optimization again removes a separate first-order
contribution from changing choices. In numeraire units, the local welfare change is
\[
\mathrm dEV_n=\mathrm dv_n-c_{n0}\,\mathrm dp
             =(h_nQ_0-c_{n0})\,\mathrm dp.
\]
Initial output values the income effect, and initial consumption values the
additional purchase cost. A resident gains from a small price increase when the
first exposure exceeds the second; living near the producer is not sufficient.

The budget line makes this comparison visible. Holding the initial production
plan fixed, a higher service price changes the slope of the line while leaving its
point at $c=h_nQ_0$ unchanged. At initial consumption $c_{n0}$, the change in
available $m$ is exactly $(h_nQ_0-c_{n0})\,\mathrm dp$. The line moves outward
there when income exposure is larger, and inward when purchase exposure is larger.
For a finite change, input adjustment shifts the budget and consumers substitute;
with smooth value functions, these additional gains are locally second-order. The local
formula does not itself recover causal income or price changes. To use it with
spending data, the empirical analysis must supply those responses under further
demand and identifying restrictions.


## L02

Tourist purchases do not determine where residents spend or where their income
changes. In the hypothetical city, 300 areas have large increases in tourist spending.
Of these, 110 have low increases in resident spending and 100 have high increases.
The contrast rules out a simple descriptive equivalence between the two local
spending measures. It does not establish that visitors reduce resident purchases
or that tourist demand causes either pattern.

The data distinguish these purchases through different links. The country where
a tourist card was issued and its purchase destination measure demand at that destination. Resident
records with an observed home address instead connect purchases to residential
origins, including purchases elsewhere. Workplace and ownership links provide
another route: a destination can pay workers who live in other areas, and those
workers can spend their income away from that destination. These links help
explain why local tourist purchases need not track local resident purchases.
Unobserved changes in amenities and common seasonal movements can also produce
the contrast. Recovering the effect of tourist demand therefore requires more
than adding the links to a map.

We estimate responses of resident spending using bilateral origin-destination
observations. The specification includes direct tourist exposure and exposure
through baseline work and purchase links, together with pair and month effects
and predictable direct and network controls. The baseline exposure is a constructed
regressor, not the equilibrium response that we seek to estimate. Variation comes
from changes in spending across tourist origin countries interacted with initial
destination composition. This variation helps distinguish changes in tourist
demand from resident purchases, but does not become exogenous merely because its
shares are measured before the shock. The identifying restriction excludes omitted
effects correlated with these constructed shocks after the controls. Correlated
seasonal changes or destination amenities would violate that restriction if the
controls did not remove their relevant variation.

Even under the identifying restriction, a response of resident spending is not an
income response. Its origin component combines changes in income with changes
in destination prices and attractiveness. A stated demand restriction permits
initial expenditure shares to correct for the destination component. When the
restriction is imposed through adjusted regressors, their estimated origin
coefficients describe the restricted income response; they are not unrestricted
fixed effects for every origin and month that separately measure income. This distinction also
limits the comparison with observed income. Month effects absorb common monthly
changes, so the comparison can examine spatial differences without independently
recovering the common aggregate income change. The remaining empirical task is
to assess the restriction on income recovery, not to treat a good spatial fit as
validation of the aggregate welfare mean.


## L03

Valuing a shock and recovering its effects from data are different tasks. Initial
expenditure shares value price changes once those changes and income responses
are known. Aggregate welfare results in Arkolakis, Costinot and Rodriguez-Clare
(2012) instead rely on restrictions defining the class of trade models they
consider. Their result is useful for comparing what information is sufficient
within that class, rather than as a general proof of household valuation under
unrestricted preferences. The hypothetical tourist application starts from local
valuation and then asks how to recover its income and price terms.

That recovery question brings demand restrictions into the argument. Redding and
Weinstein (2020) study price index recovery under CES preferences, including how
demand residuals and normalization affect the recovered index. A destination
effect in a spending equation is therefore not automatically a measured price
change. Its interpretation depends on the demand system and the chosen
normalization. This connection helps organize the correction from spending to
income, but it does not establish that the tourist demand variation is exogenous.
The latter requires a separate condition on other influences on resident spending.

Spatial interactions raise a further question: which responses occur away from
the directly affected destination? Allen, Arkolakis and Takahashi (2020) provide
a gravity representation, while Allen, Arkolakis and Li (2024) characterize
equilibrium properties under stated conditions on interactions. Adao, Arkolakis
and Esposito, in their September 2025 manuscript, use a spatial response
representation to distinguish differential and aggregate effects of trade shocks.
These connections concern different parts of the same problem: representing
links, characterizing the resulting system, and relating a response to an empirical
specification. The tourist application uses work and purchase links to recover a
local welfare response under its maintained restrictions. It does not inherit
causal validity from an equilibrium theorem or solve a general dynamic economy.
Keeping these tasks separate makes the literature comparison useful for deciding
what the observed purchases can tell us.


## L04

\subsection{Income and purchase costs}
The hypothetical road shock raises the benchmark population-weighted income
measure by 3.2 log points and the cost of initial purchases by 1.6. Their difference
gives a local welfare gain of 1.6 log points. This accounting comparison values
both terms for the same population and shock. It does not by itself show whether
the income response is recovered correctly from spending or whether every
resident gains. Comparing income restrictions is therefore part of interpreting
the result, rather than a separate exercise with no bearing on the benchmark mean.

\subsection{Sensitivity of income recovery}
An alternative allocation gives income gains of 2.4 log points with the same
initial purchase cost change, leaving welfare at 0.8. Changing the allocation changes
how receipts are assigned in the calculation; it does not establish a change in
their actual recipients. A separate unrestricted recovery is more consequential:
income falls by 0.5 log points and welfare by 2.1, again with costs rising by 1.6.
Similar spatial rankings across these exercises preserve part of the relative
comparison, but not the positive mean. They are not confidence bounds, and the
supplied evidence does not rank the credibility of the restrictions. The
comparison with observed income cannot settle the disagreement over the common income
change because month effects absorb that component. It provides a comparison
of spatial responses, not an independent estimate of aggregate income.

\subsection{Structural and policy comparisons}
The structural exercise asks how the same shock changes welfare when prices
and choices adjust jointly in the model. Solving the model with fixed workplaces
gives a finite gain of 2.6 percent, compared with 2.5 percent when workers choose
workplaces. Both use the same baseline and shock, and total hours remain fixed.
The mobile alternative changes workplace choice rather than adding an hours
response. These finite percentages are different objects from the empirical
local calculation in log points, which was not a calibration target. Similar model
means neither establish similar gains for each residence nor resolve the
disagreement over income recovery in the spending estimates.

The policy exercise yields gains of 0.30 percent under a uniform tax and 0.34
percent under differentiated taxes. The additional gain is 0.04 percentage points;
it is not 0.04 percent of the gain under the uniform policy. This modest additional gain concerns
the specified feasible policies and model. It does not imply that differences in
local rates are caused by sparse data. A policy with constant rates within districts
has not yet been computed, and checks of local necessary conditions do not establish
a unique global optimum. The policy results should therefore answer the model's
tax question without becoming a recommendation based on observed data alone.

Together these comparisons locate the stronger and weaker conclusions. Much of
the spatial ordering remains similar across changes in recovery, but the mean welfare gain is
conditional on the income restriction. Structural comparisons show what changes
under additional assumptions about adjustment and policy, but cannot replace
evidence for that empirical restriction. The economic answer is thus a spatial
incidence pattern with a conditional aggregate gain, not a single welfare number
validated by several close model predictions.

