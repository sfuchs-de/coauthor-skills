# ChatGPT Compendium Review

Use this reference when the user asks for compendium mode, ChatGPT-style review, or a review that flags text similar to the compendium without relying on exact phrase matches.

This file is the ChatGPT-focused review lens. It is not the full compendium. For high-recall review, load `references/compendium.md` as the example bank and source map, then use the families below to decide what to flag.

## Review Standard

This is a semantic style review. The scanner is only a triage aid. Flag a passage when it performs the same function, sentence shape, cadence, or specificity failure as a compendium pattern, even if none of the exact phrases appear.

Do not write "this was AI-written." Write "this resembles the ChatGPT-style compendium family X because..."

When the scanner returns no exact hits, still compare the paragraph against the full compendium's phrase families, sentence templates, grammar-level patterns, content patterns, structural/rhythm patterns, formatting patterns, and context-specific profiles. Exact matches are evidence; they are not the boundary of the review.

## ChatGPT-Focused Families

1. **Assistant residue**: helpful signoffs, prompt acknowledgments, disclaimers, capability language, or chatty scaffolding.
2. **Generic setup**: broad world/era/context framing before a concrete point.
3. **Throat-clearing**: announcing the point instead of making it.
4. **Inflated significance**: routine facts framed as pivotal, transformative, landscape-shaping, testament-like, or profound.
5. **Promotional register**: neutral description turns into press-release, tourism, LinkedIn, or product-marketing voice.
6. **Vague authority**: unnamed experts, observers, studies, industry reports, consensus, or critics.
7. **Formulaic reversal**: not-X-but-Y, X-isn't-the-problem/Y-is, no-X-no-Y-just-Z, or tidy "actually" reframes.
8. **Superficial analysis tails**: trailing clauses that gesture at meaning with highlighting, reflecting, showcasing, underscoring, demonstrating, or contributing logic.
9. **Rule-of-three padding**: triads where the third item is rhythm filler rather than information.
10. **False ranges**: "from X to Y" used as a fancy list rather than a real scale.
11. **Generic conclusions**: recap phrases, bright-future endings, only-time-will-tell uncertainty, or neat wrapups.
12. **Default Markdown cadence**: bold-first bullets, symmetrical lists, repeated section forms, and table/list overuse.
13. **AI vocabulary clusters**: multiple polished abstraction words replacing actors, facts, numbers, or mechanisms.
14. **Over-smooth rhythm**: neutral, evenly balanced prose that could fit any topic after noun swapping.
15. **Academic slop**: cited-looking but vague claims, excessive "important/notably/furthermore" transitions without data, or significance claims around otherwise precise methods prose.

## How To Flag

For each flagged passage, produce:

```markdown
- Severity: P0/P1/P2
- Family: <one compendium family>
- Evidence: "<short fragment>"
- Why similar: <function/shape/cadence/specificity reason, not just word overlap>
- Edit: <delete, simplify, name source, add concrete fact, or rewrite>
```

Use severity this way:

- **P0**: hard assistant/citation/markup artifacts.
- **P1**: structural or rhetorical ChatGPT-style shape that should be rewritten.
- **P2**: softer resemblance, vocabulary density, cadence, or review prompt.

## False-Positive Discipline

- Keep technical terms when they are precise.
- Preserve academic transitions when backed by citations, data, or a concrete finding.
- Do not flag a single common word by itself.
- Do not penalize non-native, formal, or institutional prose merely for being polished.
- If the similarity is only "this is boring," do not flag it. The finding needs a compendium family and an edit path.
