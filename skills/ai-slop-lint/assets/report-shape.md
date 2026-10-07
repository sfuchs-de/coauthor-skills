# Report Shape

For an audit, use this structure:

```markdown
## Findings
- P0/P1/P2 - file:line - short issue
  Evidence: exact fragment or short context.
  Why it reads AI-ish: concrete pattern family.
  Edit: delete, simplify, source, or rewrite with a suggested replacement.

## Density Notes
Briefly summarize repeated vocabulary, structural rhythm, and formatting signals.

## Rewrite Priorities
1. Remove hard artifacts.
2. Replace vague/inflated claims with concrete actors, facts, dates, metrics, or citations.
3. Simplify verbs and sentence templates.
4. Restore the author's normal rhythm.
```

For a cleanup request, make the patch and then summarize the changed pattern families. Do not
over-explain every soft vocabulary replacement. For iterative cleanup, include a compact pass log:

```markdown
## Pass Log
- Pass 1: edited paragraphs 3, 7, 9; removed chatbot residue, negative parallelism, and vague attribution. Gate: FAIL -> FAIL; actionable findings 18 -> 6.
- Pass 2: edited paragraphs 12, 14; replaced significance inflation with concrete claims. Gate: FAIL -> PASS; actionable findings 6 -> 0.
- Final anti-AI pass: no remaining obvious assistant-style templates; remaining P2 terms accepted as technical/contextual.
- Gate: strict-compendium PASS.
- Iteration verifier: PASS; scan snapshots saved in `/tmp/ai-slop-lint.xxxxxx`.
```
