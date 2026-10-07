---
name: ai-slop-lint
description: Audit, score, and clean Markdown, plain-text, TeX, academic, and referee-report prose for ChatGPT-style residue, formulaic structure, inflated vocabulary, vague attribution, and suspicious density patterns. Use for evidence-backed style reports and iterative validated cleanup. Use `stop-slop` instead for an explicit quick, unscored cleanup.
---

# AI Slop Lint

Use `report` for scored findings and `rewrite` for an explicitly authorized scan/edit/rescan loop.
For a quick unscored cleanup, route to the bundled `stop-slop` instead of imposing the scoring gate.
In a shared graph workflow, read
`../econ-writing-suite/references/reasoning-graph-integration.md` and own the `prose` layer only.
Preserve scientific claims, mathematics and the other specialists' judgments.

## Core Rule

Treat this as a style lint pass, not an AI-authorship detector. Report "this reads like default LLM prose because..." rather than "this was written by AI." A single word is weak evidence. Clusters across artifacts, sentence templates, vocabulary density, formatting, and rhythm are actionable.

## Quick Workflow

1. Identify the target files or pasted text. For `.tex`, assume `academic`. For author-facing
   referee reports, use `referee`; scan confidential editor notes separately because recommendation
   language is expected there.
2. Run the bundled scanner for an initial map:

```bash
python3 "<skill-directory>/scripts/ai_slop_lint.py" <file-or-folder> --context academic --format markdown --top 120
```

For referee reports:

```bash
python3 "<skill-directory>/scripts/ai_slop_lint.py" <referee-report.md> --context referee --format markdown --top 80
```

3. For long drafts, switch to paragraph queue mode:

```bash
python3 "<skill-directory>/scripts/ai_slop_lint.py" <file-or-folder> --context academic --mode paragraphs --format markdown --top 40 --min-paragraph-score 2 --gate strict-compendium
```

4. Use the scanner output to inspect the highest-priority passages in the source file. Do not blindly accept every hit.
5. If the user asks for compendium mode or ChatGPT-focused review, use the ChatGPT Compendium Review workflow below. Load the full `references/compendium.md`; do not rely only on the distilled rulebook or exact matches.
6. If the user provided a human writing sample, quickly calibrate sentence length, paragraph starts, punctuation habits, transition style, and recurring plain-language choices before rewriting.
7. If the user asked for a report, lead with file/line findings ordered by severity. If they asked for cleanup, patch only the flagged prose and preserve math, citations, labels, commands, and field terms.
8. Before declaring strict cleanup complete, do one final anti-AI pass: ask what still makes the edited text read like default assistant prose, then rerun the scanner and either fix the residual tell or document why it is a false positive.
9. When a finding is ambiguous, search `references/compendium.md` for the pattern family before deciding.

The `referee` context adds diagnostics for formulaic praise, tentative requests, possible
recommendation leakage, repeated remedies, request density, and heavy dash use. These are editorial
signals, not automatic evidence that a report is poor or machine-written. Preserve manuscript
anchors, technical terms, and natural first-person judgment.

## Reference Files

- `references/compendium.md`: full ChatGPT/LLM writing-style fragments compendium assembled from Wikipedia, public GitHub tools, phrase-list sites, and research papers. This is the high-recall reference file for source-specific rules, examples, domain profiles, caveats, and rewrite guidance.
- `references/chatgpt_compendium_review.md`: semantic ChatGPT-focused review rubric. Load this as the review lens, but not as a replacement for the full compendium.
- `references/rulebook.json`: machine-readable subset of the compendium. The scanner loads this by default for exact phrases, regex templates, source-backed categories, and vocabulary tiers; it is not the full example bank.
- `references/source_inventory.md`: compact map of the repos and external sources that informed the skill.
- `scripts/ai_slop_lint.py`: deterministic first-pass scanner for Markdown, text, and TeX/LaTeX.
- `scripts/ai_slop_pass_report.py`: compares JSON scan snapshots from multiple cleanup passes and verifies that the agent actually scanned, edited, rescanned, improved, and reached the final gate.

## Compendium-Backed Scanning

The scanner uses `references/rulebook.json` by default, then merges those compendium-derived rules with built-in fallback safety rules. Prefer editing `rulebook.json` when adding or refining phrase families, structural regexes, vocabulary tiers, source notes, priorities, weights, or rewrite guidance.

Use `--no-rulebook` only for debugging the built-in fallback rules:

```bash
python3 "<skill-directory>/scripts/ai_slop_lint.py" <file-or-folder> --no-rulebook
```

Use `--gate strict-compendium` for cleanup jobs. The scanner exits nonzero while obvious compendium-backed slop remains, so the agent has a concrete stop condition.

Gate semantics:

- `--gate actionable`: fails on P0/P1 findings and explicit blocking P2 density/formatting findings.
- `--gate strict-compendium`: also fails on compendium-backed P2 phrase and structure findings, while leaving single soft vocabulary hits, file-level metrics, passive/coherence review prompts, and short-sample warnings nonblocking.

## ChatGPT Compendium Review Mode

Use this when the user asks to review text against the compendium, wants ChatGPT-focused flags, or explicitly says not to rely on exact matches. This is a review mode, not a cleanup loop unless the user separately asks for rewrites.

1. Load `references/compendium.md` and `references/chatgpt_compendium_review.md`. Treat `compendium.md` as the comprehensive source of examples and `chatgpt_compendium_review.md` as the ChatGPT-focused review frame.
2. Run the scanner in compendium packet mode:

```bash
python3 "<skill-directory>/scripts/ai_slop_lint.py" <file-or-folder> --context academic --mode compendium --format markdown --top 80
```

3. Read the target prose. Use the packet as a queue and hint layer only; it does not print every compendium example.
4. Compare each paragraph to the full compendium by function, sentence shape, cadence, and specificity. Flag paraphrased ChatGPT patterns even when no exact word or regex matched.
5. When a paragraph is suspicious but has no deterministic hit, search the full compendium by family or rhetorical move before deciding, for example:

```bash
rg -n "false range|generic conclusion|vague attribution|rule of three|significance inflation|assistant preamble|over-smooth" "<skill-directory>/references/compendium.md"
```

6. For every finding, include:
   - Severity: P0/P1/P2.
   - Family: one ChatGPT compendium family.
   - Evidence: a short fragment.
   - Why similar: the rhetorical function or shape, not just word overlap.
   - Edit: delete, simplify, source, add a concrete fact, or rewrite.
7. If no compendium-similar pattern is present, say so. Do not manufacture flags for merely polished, formal, non-native, or institutional prose.

Use JSON when building a larger report or when another script will consume the candidate queue:

```bash
python3 "<skill-directory>/scripts/ai_slop_lint.py" <file-or-folder> --context academic --mode compendium --format json --top 120
```

## Iterative Long-Draft Workflow

Use this loop when the draft is long, the user asks for paragraph-by-paragraph cleanup, or the first scan shows many hits:

1. Run `--mode paragraphs --gate strict-compendium` and rank paragraphs by P0 count, P1 count, then score.
2. Work in slices of roughly 4-8 flagged paragraphs or 800-1,500 words so edits stay local and reviewable.
3. For each flagged paragraph, inspect the original source lines and produce:
   - Pattern summary: the concrete P0/P1/P2 families.
   - Proposed edit: a replacement paragraph or a line-level deletion/simplification.
   - Preservation note: claim, citation, math reference, or technical term that must remain intact.
4. Patch the slice if the user requested cleanup. If the user requested review only, present the proposed edits without patching.
5. Rerun the scanner on the edited file after each slice:

```bash
python3 "<skill-directory>/scripts/ai_slop_lint.py" <file-or-folder> --context academic --mode paragraphs --format markdown --top 40 --min-paragraph-score 2 --gate strict-compendium
```

6. Iterate until:
   - the paragraph-mode gate passes;
   - a final full-file scan with `--gate strict-compendium` exits 0;
   - any remaining nonblocking P2 hits are explicitly justified as technical, house-style, quoted, or genre-conventional.
7. Keep a compact pass log with the paragraphs edited, major pattern families removed, gate status before/after, and any accepted residual false positives.
8. Save JSON scan snapshots for each pass and verify them with `scripts/ai_slop_pass_report.py` before finishing.

If the scanner still flags precise technical language after two careful passes, document the residual false positives rather than weakening the prose.

## Mandatory Cleanup Loop

When the user asks to clean, deslop, humanize, or iterate until AI slop is gone, do not stop after one rewrite pass. Use this exact control loop:

```text
trace_dir = a temp directory for this cleanup
write scan JSON after every scan into trace_dir/pass-00.json, pass-01.json, ...
pass = 1
while scanner exits nonzero with --gate strict-compendium:
  1. Read the highest-ranked paragraph queue items.
  2. Patch a bounded slice of flagged prose only.
  3. Preserve math, citations, labels, claims, and technical terms.
  4. Rerun paragraph-mode scanner with --gate strict-compendium and save the JSON.
  5. Run the pass reporter to check whether actionable findings decreased.
  6. Increment pass and continue.
run final full-file scanner with --gate strict-compendium and save final.json
run ai_slop_pass_report.py over the pass JSON files plus final.json
finish only if the final gate passes and the pass report verifies the loop, or list exact residual false positives and why they should remain
```

Use `--gate actionable` instead of `--gate strict-compendium` only when the user asks for a lighter editorial pass. In strict mode, phrase and structural matches from `rulebook.json` are blockers; isolated soft vocabulary and statistical metrics are review prompts unless they form density findings.

### Required Iteration Evidence

For cleanup requests, produce scan evidence. A final answer should not merely say "I iterated"; it should include the pass report summary or the key numbers from it.

Recommended command pattern:

```bash
trace_dir=$(mktemp -d /tmp/ai-slop-lint.XXXXXX)
python3 "<skill-directory>/scripts/ai_slop_lint.py" <file-or-folder> --context academic --mode paragraphs --format json --top 40 --min-paragraph-score 2 --gate strict-compendium > "$trace_dir/pass-00.json"
# patch one bounded slice of flagged prose, then rescan:
python3 "<skill-directory>/scripts/ai_slop_lint.py" <file-or-folder> --context academic --mode paragraphs --format json --top 40 --min-paragraph-score 2 --gate strict-compendium > "$trace_dir/pass-01.json"
# repeat patch/rescan until paragraph gate passes, then run a full-file final scan:
python3 "<skill-directory>/scripts/ai_slop_lint.py" <file-or-folder> --context academic --format json --top 120 --gate strict-compendium > "$trace_dir/final.json"
python3 "<skill-directory>/scripts/ai_slop_pass_report.py" "$trace_dir"/pass-*.json "$trace_dir/final.json" --require-rescan-after-failure --require-improvement --require-final-pass
```

If the initial scan already passes, one fast pass is acceptable only if the report states that no rewrite loop was needed. For that case:

```bash
python3 "<skill-directory>/scripts/ai_slop_pass_report.py" "$trace_dir/pass-00.json" --min-scans 1 --allow-clean-initial --require-final-pass
```

If the initial scan fails, there must be at least one edit and one rescan before the cleanup can be considered complete.

## Cross-Repo Tuning Lessons

The rulebook and scanner are tuned from the public repos in `references/source_inventory.md`:

- Use density and breadth, not raw hit count. `brandonwise/humanizer` and `JohnCrickett/ai-writing-detector` both cap/weight categories so one repeated word does not dominate the review.
- Treat short samples cautiously. Reports include a reliability score; do not overstate findings on fewer than 150 words or fewer than 4 sentences.
- Make P2 findings nonblocking unless they are density findings or explicitly marked `blocking` in `rulebook.json`. This prevents single technical words such as `robust` from blocking the final gate.
- Use `strict-compendium` when the user wants a cleanup guarantee. It intentionally treats source-backed P2 phrase and structure matches more aggressively than `actionable`.
- Collapse overlapping line-level matches as stacked patterns in paragraph mode. Do not count one phrase as three independent problems when the fixes are the same.
- Keep hard artifacts, chatbot residue, reasoning-chain artifacts, acknowledgment loops, hidden Unicode, and citation/tool leaks as blocking findings.
- Keep structural templates blocking: negative parallelism, false ranges, notability name-dropping, generic future-narrative closers, real/actual adjective inflation, bold-first bullets, hashtag stuffing, and bare noun-phrase bullet runs.
- In academic/TeX contexts, preserve legitimate scientific phrasing when it carries data, a citation, or conventional methods language. Cited academic transitions such as `Prior studies have shown`, `Notably`, `Furthermore`, and `Moreover` are review prompts only when they cluster without support.
- Treat passive voice, named-entity density, paragraph coherence, and title-case headings as nonblocking review prompts unless they combine with stronger source-backed patterns.
- Do not import raw antislop mega-lists wholesale. Use them only to corroborate phrases already supported by the compendium or multiple repos.

## What To Flag

Prioritize in this order:

1. P0 hard artifacts: `as an AI language model`, knowledge-cutoff disclaimers, chatbot residue, citation leaks like `turn0search0` or `contentReference`, and final-draft placeholders.
2. P1 rewrite patterns: vague attribution, significance inflation, promotional puffery, negative parallelism, generic conclusions, superficial participial tails, copula avoidance, false ranges, and formulaic challenge/future sections.
3. P2 density patterns: repeated AI-favored vocabulary, formal transition clusters, low burstiness, low lexical diversity, trigram repetition, bold-first bullets, title-case heading drift, and em-dash density.

## TeX Handling

When auditing `.tex` or `.ltx` files:

- Ignore math environments, code/listing environments, labels, refs, citations, and raw bibliography entries unless the user explicitly asks to lint them.
- Do not rewrite equations, theorem statements, proofs, references, labels, macros, or citation commands unless the issue is prose around them.
- Prefer targeted sentence edits over paragraph-wide rewrites.
- Preserve domain terms when they are technically precise: e.g. `robust standard errors`, `comprehensive margin`, `framework`, or `identification strategy` may be correct.
- Treat academic hot words as density evidence, not automatic deletion.

## Report Shape

Read [assets/report-shape.md](assets/report-shape.md) before producing an audit report or iterative
pass log. It retains the findings template, evidence fields, priorities and worked pass-log example.
For cleanup, summarize changed pattern families without over-explaining soft vocabulary replacements.

## Rewrite Policy

- Delete meta-chat: `Certainly`, `I hope this helps`, `Would you like me to`.
- Replace inflation with facts: `pivotal moment` becomes what happened, when, and why it matters.
- Replace vague authority with named authority or cut it.
- Prefer simple verbs: `utilize` -> `use`, `serves as` -> `is`, `boasts` -> `has`.
- Break mechanical symmetry only where it improves the author's actual draft.
- Keep precise technical words. The goal is not synonym swapping.
- Use the reliability score to calibrate tone: low reliability means "review prompt," not strong finding.

## Misuse Guardrails

Always include the caveat when the result could be consequential: these findings are style signals, not proof of AI authorship. False positives are common for non-native English writers, institutional prose, academic abstracts, and polished technical genres.
