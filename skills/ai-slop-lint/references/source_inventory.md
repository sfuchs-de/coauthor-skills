# Source Inventory

Use this file as a compact source map. Use `compendium.md` for the full taxonomy, examples, regexes, caveats, and rewrite playbook.

## Primary field guides and tools

- Wikipedia: Signs of AI writing: broad community field guide for hard artifacts, language, formatting, vague attribution, markup leakage, citation leaks, and anti-misuse cautions.
- hardikpandya/stop-slop: removal-oriented phrase and structure rules.
- conorbronsdon/avoid-ai-writing: detect/rewrite workflow, severity tiers, context profiles, and replacement tables.
- blader/humanizer: Wikipedia-derived 29-pattern skill and voice-calibration workflow.
- brandonwise/humanizer: CLI/skill shape with 29 pattern detectors, 500+ terms, density scoring, and statistical text analysis.
- matsuikentaro1/humanizer_academic: academic/medical adaptation; preserve field terminology while cleaning formulaic academic prose.
- JohnCrickett/ai-writing-detector: weighted detector modules and highlighted pattern output.
- jpeggdev/humanize-writing: multi-pass cleanup discipline.
- stephenturner/skill-deslop and tropes.fyi: trope-level taxonomy for scientific and general prose.
- nanxstats/llm-cliches: compact adjective/noun/verb lists for soft vocabulary rules.
- aismells, Bloomberry, HumanizeThisAI, DashAway, GPTZero, Pangram, TechHarvey, WildandFree: secondary phrase-list and scanner-style cross-checks.

## GitHub repo crosswalk

| Repo | Use in this skill | Scanner/rulebook impact |
|---|---|---|
| `hardikpandya/stop-slop` | Directness, throat-clearing, false drama, actorless prose, vague declaratives | Source for false-suspense phrases, not-because/because, X-is-not-the-problem, Wh/So/Look openers, narrator-distance review, and vague-declarative edits. |
| `jpeggdev/humanize-writing` | Multi-pass cleanup and pattern stacking | Source for pass ordering, overlapping-pattern collapse, rhythm/style review, and final human-texture checks. |
| `conorbronsdon/avoid-ai-writing` | Severity tiers, context profiles, vague endorsement, social/crypto boilerplate | Source for `worth X-ing`, real/actual/genuine inflation, generic future-narrative closers, hashtag stuffing, bare noun-phrase bullets, and Tier-3 phrase density. |
| `blader/humanizer` | Wikipedia-derived 29-pattern workflow and voice calibration | Source for optional voice-sample calibration and final "what still reads AI?" review before declaring cleanup complete. |
| `brandonwise/humanizer` | CLI-oriented scoring, short-sample confidence, code masking, hidden Unicode | Source for reliability scoring, component scoring, Markdown code masking, hidden Unicode rules, before/after pass logs, and nonblocking statistical metrics. |
| `matsuikentaro1/humanizer_academic` | Academic preservation and field-register repair | Source for cited-transition carve-outs, data/citation support checks, academic context defaults for TeX, and caution against medical-specific overblocking. |
| `JohnCrickett/ai-writing-detector` | Modular detector architecture | Source for false-range exceptions, named-entity plus vague-attribution review, passive frequency review, and paragraph coherence prompts. |
| `stephenturner/skill-deslop` | Trope-level taxonomy | Source for listicle-in-prose, fractal summaries, dead metaphor repetition, historical analogy stacking, and strict no-handholding rewrite advice. |
| `nanxstats/llm-cliches` | Compact adjective/noun/verb vocabulary list | Source for Tier 2/Tier 3 vocabulary reconciliation, with ordinary words kept nonblocking. |
| `sam-paech/antislop-sampler` | Generation-time phrase suppression | Source for corroborating phrase/regex bans only; raw 2,000+ word and 50,000+ adjustment lists are intentionally not imported wholesale. |

## Research anchors

- Kobak et al.: PubMed excess-vocabulary evidence and biomedical terms.
- Juzek and Ward: focal scientific-abstract words.
- Matsui: medical-writing term comparison in PubMed.
- Kousha and Thelwall: multi-database academic-paper and full-text evidence.
- Reinhart et al.: grammar and rhetoric features such as participial clauses, nominalizations, noun-heavy density, coordination, and downtoners.
- Zamaraeva et al.: parser-level syntactic distribution differences.
- Tercon and Dobrovoljc: survey support for formal/impersonal style, lower lexical diversity, repetition, and smaller vocabulary.
- Yakura et al.; Anderson, Galpin, and Juzek: spoken-language/podcast shifts in LLM-associated vocabulary.
- Liang et al.; Stanford HAI; Turnitin guidance: false-positive, bias, and governance cautions.
- Sadasivan et al.; Cheng et al.: paraphrasing can evade detectors without fixing factuality or authorship problems.

## Implementation stance

- Use hard artifacts as near-automatic repair targets.
- Use structural patterns as rewrite targets.
- Use vocabulary lists as density evidence.
- Use stylometric metrics as review prompts, not verdicts.
- Apply stricter thresholds for consequential review and looser thresholds for self-editing.
- Keep `rulebook.json` as the scanner-facing layer derived from `compendium.md`; it is a distilled index, not the full example bank. Update the rulebook first when adding deterministic blockers.
- Use `--gate strict-compendium` as the stop condition for iterative cleanup: the scanner exits 1 while obvious compendium-backed hard artifacts, phrase families, structural patterns, or density findings remain.
- Use `--mode compendium` for ChatGPT-focused semantic review. It produces a paragraph review packet and family checklist; load `compendium.md` alongside it for high-recall examples. Exact scanner hits are only hints, not the boundary of what can be flagged.
- Use `scripts/ai_slop_pass_report.py` to verify iterative cleanup evidence from JSON scan snapshots. If the first strict scan fails, cleanup requires an edit plus at least one rescan and final pass verification.
- Cross-repo tuning changes added May 21, 2026: reliability scoring for short samples, explicit blocking vs nonblocking findings, stricter raw Markdown rules for bold-first bullets/hashtag blocks, hidden Unicode detection, reasoning-chain and acknowledgment-loop artifacts, notability name-dropping, real/actual/genuine intensifier inflation, generic future-narrative closers, safer copula matching so ordinary noun uses of "features" do not block cleanup, Markdown code-block masking, false-range exceptions, named-entity/passive/coherence review prompts, Tier-3 phrase-density rules, stacked-pattern paragraph reporting, distinct `actionable` vs `strict-compendium` gate semantics, pass-ledger verification for scan-edit-rescan loops, and ChatGPT-focused compendium semantic review mode.
