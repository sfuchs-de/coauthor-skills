# Theory Audit Bridge For Referee Reports

The purpose of this pass is to identify theory findings that change a paper claim. It is not to
reproduce a proof notebook in the report.

## Compact Audit

Check:

- primitives, domains, normalizations, and timing;
- individual decisions and the objects agents take as given;
- aggregation and market-clearing conditions;
- simultaneous equilibrium blocks and any fixed-point or existence requirement;
- route, path, chain, or network consistency where relevant;
- comparative statics and the assumptions that sign them;
- mapping from model objects to data, moments, and counterfactual shocks;
- limiting cases used as benchmarks;
- whether finite counterfactuals use an exact identity, path integration, or approximation.

Use `audit-tex-math` referee bridge mode for pivotal derivations with source access. Use
`map-theory-dependencies` referee bridge mode for hidden dependencies, joint equilibrium blocks,
or circular closure.

For calibrated or estimated structural work, also run `quantitative_model_audit.md`. A model can
be mathematically closed and still give an unpersuasive counterfactual because a calibrated
primitive absorbs several mechanisms, is not invariant to the policy, or is disciplined by data
from a different market.

## Translation Gate

For each finding, record the source anchor, affected claim, verification status, and smallest
repair. Keep it in the technical note unless it changes contribution, validity, interpretation, or
quantification. Translate no more than one or two decisive theory findings into major comments.

An omitted extension is not a theory error. Apply the extension filter before requesting a richer
model.
