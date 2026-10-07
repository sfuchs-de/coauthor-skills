# Referee Comment Contract

Use this contract to turn a valid concern into a proportionate report comment.

## Concern Record

Record these fields internally:

- `anchor`: section, table, figure, equation, or appendix supporting the paper-specific claim.
- `claim_at_stake`: the paper claim affected by the concern.
- `threat`: the omitted assumption, confound, measurement problem, or logical gap.
- `consequence`: what no longer follows, changes magnitude, or needs narrower wording.
- `severity`: `fatal`, `materially-addressable`, `interpretive-limit`, `optional-extension`, or
  `presentation`.
- `primary_request`: the single smallest analysis or clarification needed.
- `resolution_threshold`: the result, evidence, or qualification that would close the concern.
- `burden`: `text-only`, `small-check`, `new-analysis`, `new-data`, or `new-model`.
- `verification_status`: `verified`, `uncertain`, or `not-found`.

Only verified concerns may become major comments. Uncertain concerns must be verified, qualified,
or omitted.

## Extension Filter

For every omitted feature, ask:

1. Does the omission overturn identification, equilibrium closure, or the headline claim?
2. Does it leave the direction intact but plausibly change the magnitude enough to matter?
3. Does it only limit interpretation, external validity, or the domain of the result?
4. Is it simply an intellectually interesting extension?

Cases 1 and 2 may justify required analysis. Case 3 normally requires a scope qualification or one
small sensitivity check. Case 4 is future research and should not be a publication condition.

## Request Discipline

- One major comment has one primary required action.
- Combine several symptoms only when they arise from one economic problem and can be resolved by
  the same primary action. Otherwise prioritize the decisive one rather than creating a laundry
  list.
- State that action once. Do not duplicate it with both an `I ask` sentence and a second
  `primary request` sentence.
- Examples are substitutes unless explicitly identified as sequential diagnostics.
- A `new-data` or `new-model` request requires a fatal or materially addressable concern and an
  explanation of why a text qualification cannot resolve it.
- A report should not demand that authors replace their central question with the reviewer's
  preferred paper.
- Minor comments may correct facts, notation, exposition, or request genuinely small checks. They
  may not conceal an additional major concern.

For mechanism or welfare claims, consider an alternative mechanism only when it can change the
sign, magnitude, or interpretation of the headline result. Map an omitted margin to the particular
estimate or counterfactual it affects; do not demand a richer model merely because the margin exists.

## Natural Report Form

The final comment should read as referee prose, not a labeled template. A typical sequence is:

> Section X uses Y to support claim Z. The difficulty is A, which also changes B. This matters
> because C no longer has the stated interpretation. I would ask the authors to do D. If D shows E,
> or if the claim is narrowed to F, I would regard the concern as resolved.

Vary this form. Keep the logical components, not the wording.
