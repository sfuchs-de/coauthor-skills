# ChatGPT/LLM Writing Style Fragments Compendium

Compiled May 20, 2026. This is a practical editing and detection reference for identifying prose that reads like default LLM output, then removing the patterns without flattening the writer's own voice.

## Contents

- Core principle and operational definition
- Source map, source-specific coverage audit, evidence classes
- Reliability tiers and vocabulary taxonomy
- Phrase families, sentence templates, grammar-level patterns
- Content, structural/rhythm, and formatting patterns
- Context-specific profiles
- Detection rubric, scoring, and scanner architecture
- Rewrite playbook
- Starter machine-readable checklist and regex patterns
- Caveats and minimal operating procedure

## Core principle

Treat every item here as a style signal, not authorship proof. A single flagged word means almost nothing. A dense cluster across vocabulary, sentence shape, formatting, and paragraph rhythm is the useful signal.

Use this compendium to:

- Clean up drafts that sound like default assistant prose.
- Build a phrase/pattern linter for editorial review.
- Explain why a passage feels machine-written.
- Prioritize concrete rewrites over cosmetic word swaps.

The best product framing is an AI-style lint pass, not an AI detector. Hard artifacts get deleted or repaired. Structural patterns get rewritten. Vocabulary tells get scored by density. Claims and citations get verified. Voice gets restored from a human sample when one exists.

Do not use it as the sole basis for academic misconduct, hiring, publication, or authorship accusations. Several sources explicitly warn that detectors and style rules produce false positives, especially for non-native English writers, highly polished institutional prose, and formulaic technical genres.

## Operational definition

For this compendium, a detectable fragment means any recurring unit of style that can be operationalized for review:

- A word or inflection family: `delve`, `delves`, `delving`.
- A phrase: `it is worth noting`, `stands as a testament`.
- A clause template: `not just X, but Y`.
- A transition formula: `Furthermore`, `That being said`.
- A punctuation or formatting habit: em-dash density, bold-first bullets, title-case headings.
- A discourse move: vague attribution, generic conclusion, formulaic challenges/future outlook.
- A document-level signal: uniform sentence length, low lexical diversity, repeated paragraph shape.

This broader definition matters because the best sources do not all operate at the same level. Some are word lists, some are syntactic feature studies, and some are editorial playbooks.

## Source map

Primary field guides and reusable checklists:

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing): broad field guide from WikiProject AI Cleanup; strongest source for content, language, formatting, citation, and markup artifacts.
- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop): compact removal-oriented phrase and structure rules.
- [jpeggdev/humanize-writing](https://github.com/jpeggdev/humanize-writing): eight-pass editing workflow and detailed checklist.
- [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing): tiered severity rules, context profiles, and rewrite/detect modes.
- [blader/humanizer](https://github.com/blader/humanizer): Wikipedia-derived humanizing skill with 29 before/after pattern types and voice calibration.
- [brandonwise/humanizer](https://github.com/brandonwise/humanizer): CLI/skill with 29 pattern detectors, 500+ vocabulary terms, density scoring, and statistical text analysis.
- [matsuikentaro1/humanizer_academic](https://github.com/matsuikentaro1/humanizer_academic): academic/medical-writing humanizer adapted from Wikipedia-style AI-writing patterns.
- [JohnCrickett/ai-writing-detector](https://github.com/JohnCrickett/ai-writing-detector): open-source pattern detector with 11 weighted modules and highlight output.
- [stephenturner/skill-deslop](https://github.com/stephenturner/skill-deslop) and [tropes.fyi](https://tropes.fyi/): trope taxonomy for sentence, paragraph, tone, formatting, and composition patterns.
- [nanxstats/llm-cliches](https://github.com/nanxstats/llm-cliches): concise adjective/noun/verb cliche lists.
- [aismells](https://aismells.com/) and its [common phrase list](https://aismells.com/common-chatgpt-phrases): density-first AI writing smell taxonomy.
- [sam-paech/antislop-sampler](https://github.com/sam-paech/antislop-sampler) and [Antislop paper](https://arxiv.org/abs/2510.15061): generation-time suppression of over-represented strings.

Research and empirical grounding:

- [Kobak et al., 2025](https://arxiv.org/abs/2406.07016): PubMed excess-vocabulary analysis; estimates at least 13.5% of 2024 biomedical abstracts were LLM-processed.
- [Juzek and Ward, 2024/2025](https://arxiv.org/abs/2412.11385): method for identifying 21 focal words in scientific abstracts; discusses possible RLHF contribution.
- [Matsui, 2025, Perspectives on Medical Education](https://pmejournal.org/articles/10.5334/pme.1929): 135 potentially AI-influenced medical-writing terms compared with controls in 2000-2024 PubMed records.
- [Kousha and Thelwall, 2025/2026](https://arxiv.org/abs/2509.09596): multi-database and full-text academic-paper analysis of 12 LLM-associated terms from 2015-2024 and PMC full texts through July 2025.
- [Reinhart et al., 2025](https://arxiv.org/abs/2410.16107): grammatical and rhetorical feature study using Biber-style variables across human and LLM-written corpora.
- [Zamaraeva et al., 2025](https://arxiv.org/abs/2506.01407): formal syntactic comparison of NYT-style human and LLM-generated text using HPSG grammar-type distributions.
- [Tercon and Dobrovoljc, 2025](https://arxiv.org/abs/2510.05136): survey of linguistic characteristics of AI-generated text, including formal/impersonal style, lower lexical diversity, and repetition.
- [Geng and Trotta, 2025](https://arxiv.org/abs/2502.09606): shows human/LLM coevolution, including drops in some known tell words after public attention.
- [Yakura et al., 2025](https://arxiv.org/abs/2409.01754): 740,249 hours of videos/podcasts; finds post-ChatGPT increases in words preferentially generated by ChatGPT.
- [Anderson, Galpin, and Juzek, 2025](https://arxiv.org/abs/2508.00238): 22.1M words of unscripted science/tech podcasts; finds increases in LLM-associated words but not baseline synonyms.
- [Liang et al., 2024/2026](https://arxiv.org/abs/2403.07183): estimates 6.5%-16.9% of AI conference peer-review text was substantially LLM-modified.
- [Liang et al., 2023 / Patterns](https://www.sciencedirect.com/science/article/pii/S2666389923001307): GPT detectors misclassify non-native English writing, raising fairness and robustness concerns.
- [Stanford HAI summary of Liang et al.](https://hai.stanford.edu/news/ai-detectors-biased-against-non-native-english-writers): reports that seven detectors classified 61.22% of TOEFL essays by non-native English students as AI-generated.
- [Cheng et al., 2025](https://arxiv.org/abs/2506.07001): adversarial paraphrasing reduces detector true-positive rates across detector classes.
- [Sadasivan et al., 2023/2024](https://arxiv.org/abs/2303.11156): recursive paraphrasing can substantially reduce detection rates while preserving much of the text quality.
- [Jabarian and Imas / BFI, 2025](https://bfi.uchicago.edu/insights/artificial-writing-and-automated-detection/): detector benchmarking; commercial detectors outperform open-source ones, but thresholds and policy context matter.
- [Turnitin AI Writing Report guidance](https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report): official guidance warning that AI reports may misidentify human, AI-generated, and AI-paraphrased text and should not be the sole basis for adverse actions.

Additional phrase-list sources used as secondary cross-checks:

- [Bloomberry AI Writing Patterns Database](https://www.bloomberry.ai/research/ai-writing-patterns) and [AI Dialects](https://www.bloomberry.ai/research/ai-dialects).
- [HumanizeThisAI Cliche Detector](https://humanizethisai.com/tools/cliche-detector): deterministic phrase scanner over 200+ AI-typical phrases.
- [DashAway](https://dashaway.io/): practical scanner for em dashes, cliches, jargon, and common AI tells.
- [GPTZero AI Vocabulary](https://gptzero.me/ai-vocabulary) and [GPTZero top-10 explainer](https://gptzero.me/news/most-common-ai-vocabulary/): vendor-maintained moving vocabulary list and public examples of overused AI words and phrases.
- [Pangram Labs guide](https://www.pangram.com/blog/comprehensive-guide-to-spotting-ai-writing-patterns): categorized vocabulary, phrase, structure, grammar, tone, specificity, and repetition guide.
- [TechHarvey: Avoiding common ChatGPT writing styles and structures](https://techharvey.com/avoiding-common-chatgpt-writing-styles-and-structures/): practical structural editing guide.
- [WildandFree Tools: Most common ChatGPT words](https://wildandfreetools.com/blog/most-common-chatgpt-ai-words/): word-frequency editing workflow and replacement suggestions.
- [The Verge on Humanizer](https://www.theverge.com/news/865627/wikipedia-ai-slop-guide-anthropic-claude-skill): secondary coverage connecting Wikipedia's guide, Humanizer, vague attributions, promotional language, and chatbot residue.
- [Plus AI: Most overused ChatGPT words](https://plusai.com/blog/the-most-overused-chatgpt-words).
- [Walter Writes: Most common ChatGPT words to avoid](https://walterwrites.ai/most-common-chatgpt-words-to-avoid/).
- [Humaneer: AI words to avoid](https://humaneer.me/blog/ai-words-to-avoid).
- [FreeAcademicTools: AI signature words](https://freeacademictools.com/ai-signature-words).
- [Scientific American on spoken-language shifts](https://www.scientificamerican.com/article/chatgpt-is-changing-the-words-we-use-in-conversation/): accessible summary of Yakura et al.'s evidence that ChatGPT-associated words are appearing more in speech.
- [Washington Post / syndicated analysis of shared ChatGPT messages](https://brb.yahoo.net/news/articles/clues-chatgpt-wrote-something-analyzed-214947550.html): forensic journalism on 328,744 public ChatGPT messages, including em dashes, emojis, `not just X, but Y`, and vocabulary drift.

## Source-specific coverage audit

This section records the source-by-source checks that were folded into the rest of the compendium.

- The local deep-research report adds an evidence hierarchy: corpus studies, linguistic-stylometric papers, community/editorial guides, and GitHub tools all matter, but they should not be weighted equally. Corpus studies are strongest for domain-specific vocabulary; stylometric papers are strongest for feature families; community guides are strongest for human-noticed editing patterns; GitHub tools are strongest for implementation design.
- Wikipedia contributes the broad taxonomy: significance inflation, canned notability, vague attribution, superficial analysis, promotional language, AI vocabulary density, copula avoidance, negative parallelism, rule-of-three, lexical variety, title case, boldface, inline-header lists, em dashes, unusual tables, curly quotes, broken markup, citation leaks, and hard chatbot artifacts.
- `hardikpandya/stop-slop` contributes removal-first rules: cut throat-clearing, emphasis crutches, business jargon, adverbs, meta-commentary, performative emphasis, vague declaratives, binary contrasts, negative listing, dramatic fragments, rhetorical setups, formulaic constructions, false agency, passive voice, Wh-word openers, `So` paragraph openers, `Look,` sentence openers, lazy extremes, pull-quote endings, and narrator-from-a-distance voice.
- `blader/humanizer` contributes a Wikipedia-derived 29-pattern rewrite taxonomy, voice calibration from user samples, and a final "what still sounds AI-generated?" audit pass. Its incremental deltas include tailing negations, hyphenated word-pair overuse, persuasive authority tropes, signposting announcements, and fragmented headers.
- The Verge's coverage of Humanizer is useful as secondary validation: it highlights the same practical cleanup targets, especially vague attributions, promotional phrasing, chatbot residue, and Wikipedia-driven update loops.
- `conorbronsdon/avoid-ai-writing` contributes the most operational editing workflow: rewrite mode, detect-only mode, four-part audit output, a second-pass audit, 42 pattern categories, severity tiers, rewrite-vs-patch thresholds, context profiles, and a three-tier vocabulary table with Tier 3 phrase clustering.
- `brandonwise/humanizer` contributes a composite implementation shape: 70% pattern score, 30% uniformity score; density scoring; category breadth; burstiness, type-token ratio, sentence-length coefficient of variation, trigram repetition, readability consistency, repo scan, baseline-aware regression checks, and code-aware analysis.
- `matsuikentaro1/humanizer_academic` contributes a domain-specific medical/academic cleanup angle: use stricter academic hot-word and formulaic-section rules, but preserve technical terminology and field-conventional methods language.
- `JohnCrickett/ai-writing-detector` contributes an implementation model: 11 modules for AI vocabulary, undue emphasis, superficial analysis, promotional language, outline conclusions, negative parallelism, rule of three, vague attribution, overgeneralization, elegant variation, and false ranges, each with its own score cap and highlighted matches.
- `nanxstats/llm-cliches` contributes a compact exact wordlist. Its full adjective/noun/verb inventory is included below so a linter can import it without reverse-engineering categories.
- `jpeggdev/humanize-writing` contributes the pass order and review discipline: kill structure tells first, then significance/promo language, vocabulary, grammar-level patterns, rhythm, hedging/filler/vague attribution, connective tissue, and finally human texture. It also adds pattern stacking, count-before-flagging, and preserve-technical-meaning rules.
- `stephenturner/skill-deslop` contributes the scientific-writing register rules and the broader trope catalog: magic adverbs, `delve` cousins, `serves as` dodge, false ranges, superficial participle analyses, invented concept labels, grandiose stakes inflation, pedagogical hand-holding, false vulnerability, anaphora abuse, listicle-in-disguise, Unicode decoration, dead metaphors, one-point dilution, and content duplication.
- Kobak et al. grounds the PubMed signal: 15.1M English PubMed abstracts from 2010-2024, an abrupt 2023-2024 rise in excess style words, and a lower-bound estimate of at least 13.5% LLM-processed 2024 biomedical abstracts.
- Juzek and Ward grounds a focused scientific-abstract lexicon: 21 focal words that spiked in scientific abstracts and were overused by ChatGPT-3.5 in abstract-writing tasks.
- Matsui's medical-writing study adds a controlled PubMed comparison: 135 potentially AI-influenced terms, 84 common medical academic control phrases, 27.5M PubMed records from 2000-2024, and 103 potentially AI-influenced terms showing meaningful 2024 increases.
- Kousha and Thelwall add cross-database and full-text support: the largest 2022-2024 increases were `delve`, `underscore`, and `intricate`; full-text PMC papers increasingly show repeated and co-occurring LLM-associated terms.
- Reinhart et al. add grammar/rhetoric features that are not captured by wordlists: present participial clauses, nominalizations, noun-heavy informational density, phrasal coordination, clausal coordination, downtoners, and `that` clauses as subjects.
- Zamaraeva et al. add a reminder that parser-level syntactic distributions can separate LLM and human writing even when phrase lists are incomplete; this is more useful for research tooling than for hand editing.
- Tercon and Dobrovoljc add survey-level support for formal/impersonal style, lower lexical diversity, smaller vocabulary size, and repetition as recurring cross-study signals.
- Liang et al.'s Patterns paper anchors the fairness caveat: AI-detector outputs can be biased against non-native English writers, so style linting should never be treated as standalone evidence of authorship.
- Stanford HAI's summary gives a policy-friendly version of that caveat: seven detectors were near-perfect on U.S.-born eighth-grade essays but classified 61.22% of TOEFL essays by non-native English students as AI-generated.
- Sadasivan et al. and Cheng et al. anchor the paraphrase caveat: removing or paraphrasing visible tells can bypass detectors without making the text more factual, sourced, or genuinely authored.
- Turnitin's guidance reinforces the governance rule: detector output is a review aid, not a sole basis for adverse action.
- `aismells` reinforces the same pattern taxonomy and adds operational heuristics: density over single hits, repeated sentence templates, uniform paragraph shape, generic caution/enthusiasm, bold-first bullets, emoji bullets, and scanner output as a map rather than a verdict.
- Bloomberry adds a dataset-style frame: vocabulary cliches, cadence structures, hook formulas, transition/filler phrases, and replacement pairs. The public page reports 4,628 phrase entries, 129 cadence structures, 17 hook patterns, 625 transition/filler phrases, 77 structural patterns, 287 replacement pairs, and 7,400+ total entries as of April 2026.
- HumanizeThisAI contributes a deterministic scanner model: exact phrase matching, category counts, highlights in context, and rough phrase-count risk bands of low at 3 or fewer, medium at 4-8, and high at 9+.
- DashAway contributes a pragmatic UI taxonomy: em dashes, cliches, jargon, AI tells, and grade-level feedback as separate review channels.
- GPTZero contributes a live-vocabulary framing: terms can be compared against human baselines and can change as models change. Its May 2026 AI Vocabulary page says its top-50 words and phrases are ranked from 3.3M texts by comparing AI documents with human documents, with top-list terms used 10x to 200x+ more often in AI documents. Its public examples include `play a significant role in shaping`, `showcasing`, `remarked`, `aligns`, `aims to explore`, `today's fast-paced world`, `notable works include`, `surpassing`, `tragically`, and `impacting`.
- Pangram contributes broad surface indicators that should be treated as low-confidence unless clustered: monotonous complex clauses, em-dash asides, rare contractions, very tidy grammar, American spelling/Oxford-comma drift, neat long conclusions, generic positivity, lack of proper nouns, prompt restatement, and abrupt style shifts.
- TechHarvey contributes broad structural tells: formulaic introductions/conclusions, predictable topic-three-support-conclusion paragraphs, neutral overexplaining, overused cliches, lack of lived examples, and overuse of bullets.
- WildandFree contributes a simple frequency-counter workflow: flag AI-characteristic vocabulary if it repeats, especially 3+ times in roughly 500 words.
- Scientific American summarizes Yakura et al.'s spoken-language evidence: ChatGPT-associated words such as `delve`, `realm`, and `meticulous` rose in YouTube talks and podcasts after ChatGPT's release, supporting the caveat that humans can absorb AI-sounding habits too.
- The Washington Post shared-message analysis adds forensic, model-period evidence: public ChatGPT messages showed heavy em-dash use, emoji patterns, `not just X, but Y`, and drift from older `delve` discourse toward newer words such as `core` and `modern`.

## Evidence classes

Use source type to decide how much weight to give a rule.

- Corpus studies: best for domain-specific vocabulary and time-series shifts. They justify density features, not per-document accusations.
- Linguistic-stylometric papers: best for structural features such as nominalization, coordination, sentence-length variation, lexical diversity, and repetition.
- Community/editorial guides: best for patterns human readers notice and can rewrite quickly.
- GitHub tools: best for implementation ideas, severity tiers, scoring, auto-fix boundaries, and output formats.
- Commercial detector documentation: best for caution, governance, and high-level feature families, not for extracting complete public rule lists.
- Forensic journalism: useful for model-period and UI-context clues, but should be treated as descriptive and time-sensitive.

Deployment assumptions to set before automation:

- Target language. This compendium is English-first unless otherwise noted.
- Genre/profile. Technical docs, academic abstracts, LinkedIn posts, investor emails, and encyclopedia articles need different thresholds.
- Acceptable false-positive rate. High-recall cleanup rules are fine for one's own drafts; consequential review needs conservative thresholds and human process evidence.

## Reliability tiers

### Tier 0: Hard artifacts

These are not merely style. They usually mean text was copied from a chat tool, template, or AI-assisted workflow without cleanup.

- Model disclaimers: `as an AI language model`, `as of my last update`, `I do not have access to real-time data`, `based on available information`.
- Chat UI residue: `Regenerate response`, `I hope this helps`, `let me know if you would like me to expand`.
- Citation leaks: `turn0search0`, `turn0image0`, `contentReference`, `oaicite`, `oai_citation`, `attached_file`, `grok_card`, generated citation placeholder IDs.
- AI-generated URL parameters: `utm_source=chatgpt.com`, `utm_source=claude.ai`, `utm_source=perplexity.ai`, `referrer=grok.com`.
- Template placeholders shipped in final prose: `[Your Name]`, `[INSERT SOURCE]`, `[Describe X]`, `2025-XX-XX`, `<!-- add citation -->`.
- Markdown or wikitext leaks in non-Markdown contexts: stray `###`, triple backticks, bold markers, thematic breaks before every heading.

Action: strip the artifact, then check whether the surrounding claim has a real source. If not, remove or verify it.

### Tier 1: Strong style signals

These are common across multiple independent lists and research discussions. Flag on first appearance, but judge by context.

High-signal words and phrases:

- `delve`, `delve into`, `delving`
- `tapestry`, especially metaphorical `rich tapestry`
- metaphorical `landscape`, `realm`, `paradigm`
- `testament to`, `serves as a testament`
- `pivotal`, `crucial`, `paramount`, `vital`
- `robust`, `comprehensive`, `nuanced`, `multifaceted`, `intricate`
- `leverage`, `utilize`, `harness`, `facilitate`, `foster`, `underscore`, `showcase`, `navigate`
- `groundbreaking`, `transformative`, `revolutionary`, `game-changing`, `cutting-edge`
- `synergy`, `ecosystem` when used as vague business metaphor
- `at its core`, `when it comes to`, `in today's world`, `in today's fast-paced landscape`
- `it is important to note`, `it is worth noting`, `needless to say`
- `let's unpack`, `let's dive in`, `let's break this down`
- `here's the thing`, `here's the kicker`, `here's what most people miss`

Action: replace the abstract word with a concrete noun, actor, fact, metric, source, or plain verb. Often the best edit is deletion.

### Tier 2: Cluster signals

These are normal words in isolation but AI-like when stacked.

- Formal transitions: `furthermore`, `moreover`, `additionally`, `consequently`, `subsequently`, `nonetheless`, `similarly`, `thus`.
- Emphasis adverbs: `notably`, `importantly`, `interestingly`, `significantly`, `essentially`, `ultimately`, `fundamentally`, `inherently`.
- Inflated adjectives: `valuable`, `compelling`, `innovative`, `seamless`, `dynamic`, `scalable`, `impactful`, `sophisticated`, `remarkable`, `exceptional`.
- Abstract nouns: `underpinnings`, `interplay`, `complexities`, `implications`, `perspectives`, `trajectory`, `spectrum`, `framework`, `methodology`.
- Bureaucratic verbs: `optimize`, `enhance`, `streamline`, `empower`, `elevate`, `bolster`, `cultivate`, `illuminate`, `elucidate`, `redefine`, `orchestrate`.
- Corporate/social phrases: `move the needle`, `double down`, `thought leadership`, `best practices`, `stakeholders`, `actionable insights`.

Action: flag when two or more appear in the same paragraph, or when five or more appear in a short piece.

### Tier 3: Context-sensitive signals

These can be legitimate in technical, academic, or institutional writing.

- `robust`, `comprehensive`, `framework`, `ecosystem`, `scalable`, `leverage`, `facilitate`.
- Passive voice in scientific methods.
- Numbered lists in documentation.
- Bold labels in API docs.
- Straight or curly quotes depending on publication style.
- Em dashes when a writer naturally uses them sparingly.

Action: preserve when the term has domain meaning. Rewrite only if it is doing vague promotional work.

## Vocabulary taxonomy

### Abstract grandeur nouns

These words make weak claims sound larger than they are.

- `tapestry`, `landscape`, `realm`, `paradigm`, `spectrum`, `nexus`, `panorama`, `odyssey`, `journey`, `trajectory`, `cornerstone`, `beacon`, `testament`, `symphony`, `kaleidoscope`.

Rewrite moves:

- Replace `landscape` with the actual market, field, law, dataset, or institutional setting.
- Replace `tapestry`/`symphony`/`kaleidoscope` with the concrete parts being combined.
- Replace `testament to` with the specific evidence.
- Replace `journey` with the actual action: `start`, `migration`, `launch`, `transition`, `training period`, `review process`.

### Inflated adjectives

Common clusters:

- Importance: `pivotal`, `crucial`, `paramount`, `vital`, `integral`, `key`, `significant`.
- Scale: `comprehensive`, `holistic`, `systemic`, `overarching`, `multifaceted`.
- Complexity: `nuanced`, `intricate`, `complex`, `sophisticated`.
- Novelty: `groundbreaking`, `transformative`, `innovative`, `revolutionary`, `cutting-edge`, `unprecedented`, `paradigm-shifting`.
- Praise: `commendable`, `meticulous`, `invaluable`, `remarkable`, `compelling`, `exceptional`, `stunning`, `vibrant`, `thriving`, `renowned`.

Rewrite moves:

- Ask: important to whom, compared with what, by what measure?
- Replace praise with evidence: numbers, dates, citations, specific consequences.
- Replace novelty claims with a concrete before/after.

### Abstract verbs

High-frequency replacements:

- `delve` -> examine, look at, test, analyze, read, inspect, audit.
- `utilize` -> use.
- `leverage` -> use, draw on, apply.
- `harness` -> use, capture, convert, apply.
- `facilitate` -> help, enable, make possible.
- `foster` -> build, encourage, support.
- `underscore` -> show, support, point to.
- `showcase` -> show, present, demonstrate.
- `navigate` -> handle, manage, work through.
- `embark` -> start.
- `streamline` -> simplify, shorten, remove steps.
- `elevate` -> improve, raise, strengthen.
- `empower` -> let, allow, give authority to.
- `bolster` -> support, strengthen.
- `cultivate` -> build, grow, develop.
- `illuminate`/`elucidate` -> explain, show, clarify.
- `commence` -> start.
- `ascertain` -> find out, determine.

Rewrite moves:

- Prefer the verb a person would say aloud.
- Name the actor: not `the data underscores`, but `the regression shows` or `we infer`.
- If the verb is metaphorical, ask whether it hides the actual mechanism.

### Academic excess words

Research sources repeatedly discuss spikes in scientific/academic language after ChatGPT:

- `delve`, `intricate`, `underscore`, `meticulous`, `commendable`, `boast`, `comprehend`, `swift`, `garner`, `surpass`, `strategically`, `innovative`, `versatile`, `pivotal`, `showcasing`, `realm`, `grappling`.
- Common biomedical excess terms to score only in clusters: `across`, `additionally`, `comprehensive`, `crucial`, `enhancing`, `exhibited`, `insights`, `notably`, `particularly`, `within`.

Notes:

- These words are not individually wrong. The signal is abnormal frequency or abrupt corpus-level change.
- Geng and Trotta show known tell words can decline after public attention, while other AI-favored terms keep rising. A linter should therefore support regular updates.

Juzek and Ward's 21 focal words for scientific abstracts:

- `delves`, `delved`, `delving`, `showcasing`, `delve`, `boasts`, `underscores`, `comprehending`, `intricacies`, `surpassing`, `intricate`, `underscoring`, `garnered`, `showcases`, `emphasizing`, `underscore`, `realm`, `surpasses`, `groundbreaking`, `advancements`, `aligns`.

Kobak et al. identify hundreds of excess 2024 PubMed style words. A practical linter should sample from the full family rather than rely only on `delve`:

- `accentuates`, `acknowledges`, `addresses`, `adept`, `advancement`, `aligns`, `amidst`, `bolster`, `broader`, `burgeoning`, `capabilities`, `commendable`, `compelling`, `comprehending`, `consequently`, `culminating`, `delineates`, `delve`, `delved`, `delves`, `delving`, `discern`, `distinctive`, `elevate`, `elucidate`, `embracing`, `emphasizing`, `groundbreaking`, `harness`, `illuminates`, `imperative`, `innovative`, `interconnectedness`, `interplay`, `intricacies`, `intricate`, `intricately`, `invaluable`, `leverages`, `meticulous`, `meticulously`, `multifaceted`, `notable`, `noteworthy`, `nuanced`, `optimizing`, `orchestrating`, `pioneering`, `pivotal`, `poised`, `pronounced`, `realm`, `renowned`, `revolutionize`, `seamless`, `showcased`, `showcases`, `showcasing`, `signifying`, `streamline`, `surmount`, `surpass`, `surpassed`, `surpasses`, `surpassing`, `swift`, `transformative`, `ultimately`, `unprecedented`, `utilizing`.

Matsui's PubMed study strengthens the medical-writing profile. The strongest 2024 increases overlap with the usual word families:

- `delve`, `underscore`, `meticulous`, `boast`, `primarily`, `commendable`, `intricate`, `surpass`, `garner`, `pivotal`, `realm`, `showcase`, `innovative`, `versatile`, `utilize`, `foster`, `comprehensive`.

Kousha and Thelwall's cross-database academic-paper analysis focuses on 12 terms, with the biggest 2022-2024 increases around:

- `delve`, `underscore`, `intricate`, `meticulous`, `realm`, `pivotal`, `showcase`, `garner`, `boast`, `comprehensive`, `commendable`, `meticulously`.

Yakura et al. and Scientific American's summary extend the signal beyond writing into speech. Their spoken-corpus examples overlap heavily with the academic lists:

- `delve`, `realm`, `meticulous`, `comprehend`, `boast`, `swift`, `inquiry`.

Implication for editing: do not assume a writer used AI just because they use these words. People now pick up AI-associated vocabulary from the surrounding language environment. Use the words as a revision signal, not an accusation.

### Exact small repo wordlists

`nanxstats/llm-cliches` is small enough to carry as an exact import list.

Adjectives:

- `avant-garde`, `captivating`, `crucial`, `bustling`, `distinguished`, `esteemed`, `exquisite`, `formidable`, `game-changing`, `groundbreaking`, `holistic`, `iconic`, `indomitable`, `irrefutable`, `meticulous`, `multifaceted`, `omniscient`, `paradigm-shifting`, `paramount`, `pioneering`, `pivotal`, `predominant`, `profound`, `prominent`, `quintessential`, `revolutionary`, `seamless`, `tangible`, `trailblazing`, `ubiquitous`, `unassailable`, `unblemished`, `unequaled`, `unmatched`, `unparalleled`, `unrivaled`, `unsurpassed`, `unwavering`, `unyielding`, `visionary`.

Nouns:

- `apogee`, `epitome`, `facet`, `gusto`, `journey`, `landscape`, `nexus`, `odyssey`, `panorama`, `paradigm`, `pinnacle`, `spectrum`, `symphony`, `tapestry`, `testament`, `trajectory`.

Verbs:

- `brace`, `delve`, `discover`, `dive`, `elevate`, `embark`, `embrace`, `emerge`, `ensure`, `envision`, `foster`, `galvanize`, `harness`, `orchestrate`, `redefine`, `reinforce`, `streamline`, `transcend`, `unleash`, `unlock`, `usher`.

### Creative/narrative slop

The Antislop sampler includes many fiction-oriented cliches from a large generated-story dataset. Do not apply these rules to literary prose without care.

Common clusters:

- Over-ornate image nouns: `symphony`, `kaleidoscope`, `tapestry`, `labyrinthine`.
- Whisper/quiet intensity: `barely above a whisper`, `quietly`, `silent witness`.
- Stock story beats: `little did he know`, `life would never be the same`, `for what seemed like an eternity`, `the choice is yours`, `only just beginning`.
- Sensory cliches: `palpable`, `ethereal`, `glinting`, `twinkled`, `shivers down`, `air filled with anticipation`.

Rewrite moves:

- Replace stock atmosphere with a concrete observation.
- Avoid repeating one metaphor across multiple paragraphs.
- Cut melodrama unless the genre calls for it.

## Phrase families

### Assistant preambles

Patterns:

- `Here is an overview of...`
- `Here is a...`
- `In this article, we will explore...`
- `This guide will walk you through...`
- `Let me walk you through...`
- `In this section, we'll...`
- `As we'll see...`
- `I want to explore...`
- `Let's dive into...`
- `Let's take a closer look...`
- `Without further ado...`

Fix: start with the claim, question, result, or object. The reader does not need the table of contents in sentence form.

### Generic scene setters

Patterns:

- `In today's fast-paced world`
- `In today's digital landscape`
- `In an era where`
- `In the realm of`
- `In a world where`
- `Imagine a world where`
- `As we navigate`
- `When it comes to`

Fix: replace with the actual time, setting, institution, audience, or constraint.

### Business and strategy filler

Patterns:

- `navigate challenges`
- `unpack the analysis`
- `lean into`
- `game-changer`
- `double down`
- `deep dive`
- `take a step back`
- `moving forward`
- `circle back`
- `on the same page`
- `best practices`
- `actionable insights`
- `stakeholders`
- `move the needle`
- `paradigm shift`
- `speaks volumes`
- `thought leader`
- `thought leadership`
- `food for thought`
- `playbook`
- `signal vs noise`
- `hold space`
- `making an impact`
- `impacting`

Fix: replace with the actual action: handle, explain, accept, increase, analyze, reconsider, next, revisit, agree, use, decide, measure, ship, fund, hire, cut.

### Hedging preambles

Patterns:

- `It is important to note that`
- `It is worth noting that`
- `It goes without saying`
- `It bears mentioning`
- `Generally speaking`
- `While this may vary`
- `To be sure`
- `To be clear`
- `That being said`
- `At the same time`
- `On the other hand`
- `In other words`
- `In the grand scheme of things`
- `In a nutshell`
- `In order to`
- `Due to the fact that`
- `At this point in time`
- `In the event that`
- `has the ability to`
- `While specific details are limited`
- `While specific details are scarce`
- `This is not without its challenges`
- `It remains to be seen`
- `Could potentially`
- `May eventually`
- `Might ultimately`

Fix: cut the hedge, or keep one uncertainty word if the uncertainty is real. Avoid stacked hedges.

### Confidence calibration

Patterns:

- `Importantly`
- `Interestingly`
- `Surprisingly`
- `Notably`
- `Significantly`
- `Undoubtedly`
- `Without a doubt`
- `The key takeaway is`
- `The most important thing is`

Fix: let the fact carry the weight. If the fact is genuinely surprising, make the contrast explicit.

### False suspense

Patterns:

- `Here's the thing`
- `Here's the kicker`
- `Here's where it gets interesting`
- `Here's what most people miss`
- `Here's what I find interesting`
- `Here's the problem though`
- `Here's the starting point`
- `Here's the deal`
- `The truth is simple`
- `The reality is`
- `The uncomfortable truth is`
- `It turns out`
- `The real question is`
- `The real X is`
- `At its core`
- `The heart of the matter`

Fix: state the point directly. These phrases usually announce insight instead of providing it.

### Hook formulas

Patterns:

- `Have you ever wondered...`
- `Let's be honest...`
- `Most people believe X. They're wrong.`
- `Stop doing X. Start doing Y.`
- `I used to think X. I was wrong.`
- `The window for X is closing.`
- `What if the way we think about X is wrong?`
- `The more you try to X, the less Y you get.`
- `Whether you're a founder, a marketer, or a...`
- `Right now, X is changing faster than...`
- `X is changing the way we Y.`
- `X is more than just Y.`

Fix: replace the prefabricated hook with the actual tension, evidence, or scene. Hooks are fine; interchangeable hook skeletons are the problem.

### Emphasis crutches and meta-commentary

Patterns:

- `Full stop.`
- `Period.`
- `Let that sink in.`
- `This matters because`
- `Make no mistake`
- `Here's why that matters`
- `Here's what you need to know`
- `Now let's look at`
- `Hint:`
- `Plot twist:`
- `Spoiler:`
- `You already know this, but`
- `But that's another post`
- `X is a feature, not a bug`
- `Dressed up as`
- `The rest of this essay explains...`
- `Here's what I mean:`

Fix: delete the phrase and keep the sentence only if it still says something. These fragments are usually labels attached to an under-argued point.

### Pedagogical hand-holding

Patterns:

- `Let's break this down step by step`
- `Let's unpack what this really means`
- `Let's explore this idea further`
- `Think of it as...`
- `Think of it like...`
- `Think about it:`
- `It's like a...`
- `And that's okay`

Fix: use this voice only when the audience genuinely needs instruction. For expert prose, make the distinction directly and skip the classroom posture.

### False vulnerability and polished candor

Patterns:

- `And yes, ...`
- `Since we're being honest...`
- `I'm going to be honest`
- `To be honest`
- `I promise`
- `They exist, I promise`
- `This is not a rant; it's a diagnosis`
- `Can we talk about...`
- `I'll say it again`

Fix: replace performed sincerity with the concrete admission, limitation, or evidence. If there is no risk or specificity, delete it.

### Chatbot sycophancy

Patterns:

- `Great question`
- `Excellent point`
- `You're absolutely right`
- `I'd be happy to help`
- `Certainly`
- `Absolutely`
- `Of course`
- `I hope this helps`
- `Would you like...`
- `Feel free to reach out`
- `Let me know if you need anything else`

Fix: delete. In prose, answer without praising the prompt.

### Generic conclusions

Patterns:

- `In conclusion`
- `In summary`
- `To summarize`
- `Overall`
- `The bottom line is`
- `Only time will tell`
- `The future looks bright`
- `Exciting times lie ahead`
- `As we move forward`
- `One thing is certain`
- `Start your journey today`
- `a major step in the right direction`

Fix: end with the concrete implication, next step, or unresolved problem.

## Sentence templates

### Negative parallelism

Templates:

- `It is not X, it is Y.`
- `It is not just X, it is Y.`
- `X is not about Y; it is about Z.`
- `Not because X, but because Y.`
- `The question is not X. The question is Y.`
- `X, no guessing.`
- `X, no wasted motion.`

Why it reads as AI: it manufactures a reframe whether or not the argument needs one.

Fix: state Y directly, or turn tailing negations into real clauses: `The options come from the selected item, so the user does not have to guess.` Keep one antithesis only when it carries real argumentative force.

### Countdown punch

Templates:

- `No X. No Y. Just Z.`
- `Not X. Not Y. A Z.`
- `Not always. Not perfectly. But enough.`

Why it reads as AI: it builds drama around a routine claim.

Fix: write the claim in one sentence.

### Self-posed question

Templates:

- `The result? X.`
- `The takeaway? Y.`
- `The problem? Z.`
- `The best part? It already works.`

Fix: use a normal declarative sentence unless the question creates genuine tension.

### Immediate rhetorical Q&A

Templates:

- `So why does this matter? Because...`
- `What does this mean for teams? It means...`
- `But what happens next?`

Fix: replace with a bridge sentence or direct claim.

### False range

Templates:

- `From X to Y` where X and Y are not endpoints on a meaningful scale.
- `Whether you're X or Y` when it means everyone.
- `Across X, Y, and Z` when the list pads breadth without analysis.

Fix: name the actual scope or pick the relevant audience.

### Tricolon/rule of three

Templates:

- Three adjectives in a row.
- Three parallel nouns or clauses in every paragraph.
- Every section offering three lessons, three steps, or three takeaways.

Fix: use the number of items the content actually needs. Two often beats three; one strong item often beats both.

## Grammar-level patterns

### Copula avoidance

AI often replaces `is`, `are`, and `has` with inflated verbs:

- `serves as`, `stands as`, `represents`, `marks`, `features`, `boasts`, `offers`, `presents`.

Fix: use `is` or `has` unless the alternate verb adds information.

### Superficial participle tails

Patterns:

- `highlighting the importance of`
- `underscoring the need for`
- `emphasizing the significance of`
- `reflecting broader trends`
- `symbolizing the community's`
- `showcasing how`
- `contributing to`
- `fostering a sense of`

Fix: delete, or turn into a sourced sentence with a real claim.

### Present participial clause density

Pattern: frequent comma-attached `-ing` clauses, especially at sentence ends: `..., highlighting...`, `..., ensuring...`, `..., reflecting...`, `..., contributing...`. This is broader than a short blacklist: linguistic studies identify present participial clauses as a feature family worth tracking.

Fix: if the clause adds no evidence, delete it. If it matters, make it a main clause with an actor, method, or source.

### Nominalization and noun-heavy density

Patterns:

- Dense suffix clusters: `-tion`, `-ment`, `-ity`, `-ness`, `-ance`, `-ence`.
- Phrases such as `the implementation of`, `the optimization of`, `the integration of`, `the development of`, `the utilization of`.
- Abstract noun stacks with few actors or verbs.

Fix: turn some nouns back into verbs and name the actor. `the implementation of model monitoring` often becomes `the team monitored the model`.

### Formal coordination and downtoners

Patterns:

- Repeated phrasal coordination: `X and Y`, `X, Y, and Z`, `both X and Y`, `not only X but also Y`.
- Repeated clausal coordination with `and`, `while`, `whereas`, `although`, or `that`.
- Downtoners and careful-softening adverbs: `somewhat`, `relatively`, `fairly`, `rather`, `quite`, `largely`.
- `That` clauses as subjects: `That X occurred suggests Y`.

Fix: do not remove these automatically. Use them as structural density signals. If a paragraph feels overloaded, split clauses, make the main claim explicit, and reduce unnecessary balance language.

### False agency

Patterns:

- `the data tells us`
- `the market rewards`
- `the decision emerged`
- `the conversation moved toward`
- `the culture shifted`

Fix: name the human, institution, method, buyer, editor, or decision-maker.

### Synonym cycling

Pattern: `developers`, `engineers`, `builders`, `practitioners` all used for the same group in one paragraph.

Fix: choose the clearest term and repeat it.

### Hollow intensifiers

Patterns:

- `real`, `actual`, `true`, `genuine`, `truly`, `really`, `deeply`, `fundamentally`, `remarkably`, `arguably`, `quietly`, `quite frankly`, `to be honest`.

Fix: remove unless the sentence names the contrast. `Actual revenue from paying customers, not grant funding` works; `actual traction` does not.

### Adverb and softener clusters

Patterns:

- Common softeners: `just`, `simply`, `actually`, `basically`, `generally`, `quite`.
- Empty sincerity: `honestly`, `genuinely`, `truly`, `literally`.
- Importance labels: `interestingly`, `importantly`, `crucially`, `notably`, `significantly`.
- Magic subtlety: `quietly`, `remarkably`, `arguably`, `deeply`, `inherently`, `inevitably`.

Fix: delete first, then restore only if the adverb changes the factual meaning. A dense adverb cluster is a strong style signal even when every individual word is defensible.

### Passive or subjectless fragments

Patterns:

- `Mistakes were made`
- `The decision was reached`
- `No configuration needed`
- `Results are preserved automatically`

Fix: when clarity improves, name the actor: `The system preserves results automatically`.

### Sentence-start crutches

Patterns:

- Sentences repeatedly starting with `What`, `When`, `Where`, `Which`, `Who`, `Why`, or `How`, especially `What makes this hard is...`.
- Paragraphs starting with `So,`.
- Sentences starting with `Look,`.
- Repeated sentence openings such as `They assume... They assume... They assume...`.

Fix: lead with the subject, actor, constraint, or result. Keep genuine questions, but remove question-shaped transitions that exist only to cue the next sentence.

### Lazy extremes

Patterns:

- `every`, `always`, `never`, `everyone`, `everybody`, `nobody`, `no one`, `all`, `none`.

Fix: replace sweeping claims with the actual population, condition, date range, or dataset. These words become especially suspect when paired with confident generalizations or broad social claims.

### Mechanical polish and house-style drift

Low-confidence signals:

- No contractions anywhere in an informal piece.
- Perfectly consistent American spelling in a document that otherwise appears non-US.
- Mechanical Oxford-comma consistency where the writer's sample does not use it.
- Every sentence is complete, balanced, and equally polished.
- Common compound modifiers stacked with perfect hyphenation: `third-party`, `cross-functional`, `client-facing`, `data-driven`, `decision-making`, `well-known`, `high-quality`, `real-time`, `long-term`, `end-to-end`.

Fix: do not blindly introduce errors or remove correct hyphens. Use these only as voice-matching checks. If the target writer has a sample, match their contractions, spelling, punctuation, and compound-word habits.

## Content patterns

### Significance inflation

Common fragments:

- `marking a pivotal moment`
- `a key turning point`
- `sets the stage for`
- `reflects broader trends`
- `underscores its importance`
- `underscores the significance of`
- `plays a significant role in shaping`
- `plays a crucial role in determining`
- `an enduring legacy`
- `an indelible mark`
- `deeply rooted`
- `vital role`
- `shaping the landscape`
- `transformative power`

Fix: state what happened and what changed. Let the reader judge importance.

### Vague declaratives

Common fragments:

- `The reasons are structural`
- `The implications are significant`
- `This is the deepest problem`
- `The stakes are high`
- `The consequences are real`
- `This is genuinely hard`
- `This is what leadership actually looks like`
- `This is what X actually looks like`
- `This actually matters`

Fix: name the specific reason, implication, stake, consequence, or behavior. If the sentence only announces seriousness, cut it.

### Grandiose stakes inflation

Common fragments:

- `will define the next era`
- `will fundamentally reshape`
- `the fate of`
- `something entirely new`
- `history is clear`
- `history is unambiguous`
- `the real story is`
- `none of them is the real story`

Fix: reduce the claim to a falsifiable consequence. If it cannot be tied to a mechanism, scope, or time frame, it is probably dramatic framing.

### Promotional or tourism-brochure prose

Common fragments:

- `nestled in`
- `vibrant hub`
- `rich cultural heritage`
- `breathtaking`
- `renowned`
- `stunning`
- `must-visit`
- `commitment to excellence`
- `thriving ecosystem`

Fix: use plain description, numbers, geography, dates, named institutions, or sourced claims.

### Vague attribution

Common fragments:

- `experts argue`
- `industry reports suggest`
- `observers have cited`
- `many studies show`
- `several publications report`
- `critics say`
- `research suggests`

Fix: name the expert, paper, source, date, and claim. If no source is available, remove the attribution.

### Narrator-from-a-distance voice

Common fragments:

- `Nobody designed this`
- `This happens because`
- `This is why`
- `People tend to`
- `It has long been recognized that`
- `It is widely understood that`

Fix: put the writer, reader, study, institution, or actor into the sentence. In scientific writing, use `we` for the authors' own work and cite named authors for others' claims.

### Specificity avoidance

Patterns:

- Few or no proper nouns in a topic that should require names, places, products, laws, dates, or sources.
- Generic examples that could fit any domain.
- Placeholder-like people, companies, or anecdotes that are not sourced or clearly personal.
- Prompt restatement: the introduction echoes the assignment wording before saying anything substantive.
- Abrupt style shifts between paragraphs, especially when one paragraph is plain and another becomes polished, generic, or promotional.

Fix: add real names, dates, examples, citations, and mechanisms, or cut the generic material. If an anecdote is illustrative rather than real, label it as hypothetical.

### Canned notability and media coverage

Pattern: listing prestigious outlets, awards, followers, or generic `independent coverage` as proof of importance.

Fix: cite one source in context and explain what it verifies.

Common fragments:

- `notable works include`
- `notable figures include`
- `has been cited`
- `independent coverage`
- `active social media presence`
- `leading expert`

### Challenges/future prospects template

Pattern:

- `Despite its promise, X faces challenges...`
- `Despite these challenges, X continues to thrive...`
- `Future Outlook`
- `Challenges and Legacy`

Fix: name the concrete challenge, the actor responding, and the evidence of outcome. Delete generic optimism.

### One-point dilution

Pattern: one thesis restated repeatedly with different metaphors, examples, or headings.

Fix: reduce to one thesis sentence and keep only sections that add new evidence or implications.

### Historical analogy stacking

Pattern: rapid-fire comparisons to Apple, Amazon, AWS, Uber, Facebook, Spotify, the web, mobile, cloud, or similar examples to create borrowed authority.

Fix: keep one analogy only if it supports the argument at the mechanism level.

### Invented concept labels

Pattern: coined labels that sound analytical but are not established or defined, often using abstract nouns such as `paradox`, `trap`, `divide`, `gap`, `inversion`, `vacuum`.

Fix: define the mechanism or remove the label.

## Structural and rhythm patterns

### Paragraph machine

Pattern: every paragraph has the same shape: topic sentence, two support sentences, transition or takeaway. Paragraphs are interchangeable and similar length.

Fix: vary paragraph length and function. Some paragraphs should introduce evidence, some should analyze, some should qualify, and some can end bluntly.

### Dramatic fragmentation and pull-quote bait

Patterns:

- `X. That's it. That's the point.`
- `X. And Y. And Z.`
- `This unlocks something. X.`
- Short standalone sentence fragments used as paragraph endings.
- Paragraphs that repeatedly end with a quotable one-liner.

Fix: complete the sentence or merge the fragment into surrounding prose. Use blunt short sentences sparingly; a whole piece of punchlines reads manufactured.

### Anaphora abuse

Pattern: repeated sentence openings in close succession, such as `They assume... They assume... They assume...` or `The first... The second... The third...`.

Fix: combine related claims, vary sentence openings, or turn a disguised list into a real list if the list is useful.

### Listicle in disguise

Pattern: numbered or labeled points dressed as prose: `The first reason... The second reason... The third reason...` across paragraph after paragraph.

Fix: either write an honest list or write a continuous argument. Do not hide a list inside padded paragraphs.

### Fragmented headers

Pattern: a heading is followed by a one-line paragraph that only restates the heading before the real content starts.

Example shape:

```text
## Performance

Speed matters.

When users hit a slow page, they leave.
```

Fix: delete the warm-up sentence. Let the heading do its work or make the first sentence substantive.

### Excessive structure

Patterns:

- More than three headings in under 300 words.
- `Overview`, `Key Points`, `Introduction`, `Conclusion`, `Summary` as generic scaffolding.
- Too many bullets in short prose.
- Bullets all the same grammatical shape and length.

Fix: merge sections, write prose, or use headings that say something specific.

### Balanced conclusion

Pattern: `The good news... The challenge... The opportunity...` followed by an inspirational closer.

Fix: choose the actual conclusion and stop.

### Fractal summaries

Pattern: the piece previews, summarizes, and re-summarizes at the paragraph, section, and document level.

Fix: remove recaps unless the structure is genuinely complex.

### Low burstiness

Pattern: every sentence lands in the same length band, often 15-25 words; no short sentences, no longer syntactic movement, no aside, no rough edge.

Fix: vary sentence length intentionally. Add specificity rather than thesaurus variation.

### Statistical uniformity metrics

Use these as review aids for longer prose, not short snippets:

- Burstiness: human prose often varies sentence length sharply; AI-like drafts often sit in a low-variation band.
- Type-token ratio: a rough warning band for general English prose over 200 words is below about `0.40`; narrow technical topics and second-language writing can be lower for legitimate reasons.
- Sentence-length coefficient of variation: very low variation suggests metronomic prose.
- Trigram repetition: repeated three-word phrases above roughly `0.10` can indicate boilerplate loops.
- Readability consistency: AI often sits in a steady middle grade band; human drafts vary by section and purpose.

Fix: do not thesaurus the text. Broaden the underlying material: add concrete cases, actors, dates, measurements, or mechanisms so the vocabulary and rhythm vary for real reasons.

### Dead metaphor

Pattern: one metaphor repeated across a full piece until it becomes the argument: every section returns to `ecosystem`, `walls`, `doors`, `machinery`, `engine`, `fabric`, `tapestry`, or another framing device.

Fix: use the metaphor once if it clarifies the point, then switch back to literal mechanism and evidence.

### Content duplication

Pattern: repeated paragraphs, repeated section claims, or near-identical sentences separated by headings. This is strongest in long-form generated drafts where the model loses track of previous material.

Fix: keep the best version and delete the rest. If multiple sections make the same point, merge them and add new evidence or stop.

## Formatting patterns

### Em dash density

Do not flag one dash by itself. Flag:

- Multiple em dashes in one paragraph.
- Dashes used repeatedly for dramatic asides or negation reframes.
- Dashes appearing in headings, bullets, and ordinary explanatory prose.

Fix: use periods, commas, parentheses, or rewrite.

### Bold-first bullets

Pattern:

- Every bullet starts with `**Label:**` and then a sentence.
- Label repeats the first words of the sentence.

Fix: remove bold labels or convert to prose. Keep labels in technical reference material when useful.

### Title case headings

Pattern: AI-like over-capitalized subheads such as `Strategic Negotiations And Global Partnerships`.

Fix: use sentence case for subheads unless the style guide requires title case.

### Emoji decoration

Pattern:

- Emoji in headers.
- Emoji-prefixed bullets.
- Repeated checkmarks or sparkles in professional prose.

Fix: delete unless the genre is social and the emoji carries meaning.

### Tables where prose would work

Wikipedia notes unusual table use as a sign in article drafts. AI often turns ordinary explanation into tables because it looks organized.

Fix: keep tables only for genuinely tabular comparisons.

### Unicode decoration and typography drift

Patterns:

- Unicode arrows used as visual glue: `→`, `⇒`, `⟶`.
- Smart or curly quotes appearing in plain-text drafts that otherwise use straight quotes.
- Decorative symbols used as section dividers.
- Mixed typography where one paragraph uses straight quotes and the next uses curly quotes.

Fix: normalize to the target publication style. Do not flag curly quotes in edited publications that require them; flag inconsistent typography or ornamental Unicode in otherwise plain drafts.

## Context-specific profiles

### Academic prose

Tighten:

- `delve`, `intricate`, `underscore`, `meticulous`, `commendable`, `pivotal`, `comprehensive`, `robust`, `significant`.
- Vague claims like `studies show`.
- Superficial participle tails.
- Abstract importance claims without citations.
- Distant narrator frames like `It has long been recognized that`.
- Generic literature gestures like `researchers have shown` without named authors.
- Overly casual blog voice in methods, results, or theory sections.

Preserve:

- Passive voice in methods when it is a field convention.
- Technical terms with precise definitions.
- Formal transitions when required by journal style, but avoid density.
- `we` for the authors' own contribution when the discipline permits it.
- Domain terms that look like jargon but have exact meaning, such as proper scoring rules, named estimators, clinical endpoints, or statistical objects.

### Wikipedia or encyclopedia drafts

Tighten:

- Notability inflation.
- Promotional language.
- Broken citations, invented sources, citation markup leaks.
- Title-case subheads, bold overuse, inline-header lists.
- Generic `legacy`, `impact`, `future prospects`, and `challenges` sections.

Preserve:

- Neutral prose, but make it sourced and specific.

### Technical blogs and docs

Tighten:

- `let's unpack`, `deep dive`, `game changer`, `seamless`, `robust` when vague.
- Bold-first bullets in blog prose.
- Excessive structure and repetitive headings.
- False agency: `the data tells us`, `the architecture wants`.

Preserve:

- Lists, parameter tables, API headings, `robust`, `framework`, `ecosystem`, or `leverage` when they have exact technical meaning.

### Investor or executive writing

Tighten hard:

- `thriving ecosystem`, `strategic partnership`, `unlock value`, `transformative opportunity`, `poised to become`, `long-term sustainability`, `real traction`, `community-driven`, `scalable`, `actionable`.
- Future-narrative closers without falsifiable claims.
- Hedge-stacked predictions.

Fix:

- Replace broad claims with revenue, customer, adoption, margin, retention, or product evidence.

### LinkedIn/social posts

Tighten:

- Punchy fragments stacked for drama.
- `No X. No Y. Just Z.`
- `Here's what most people miss`.
- Hashtag stuffing.
- Emoji-prefixed bullets.
- `Curious what others think`.

Preserve:

- Some short fragments, one hook, and light formatting if it matches the writer.

### Creative writing

Tighten:

- Stock atmospherics, repeated metaphors, melodramatic countdowns, overused fantasy names, and generic sensory cliches.

Preserve:

- Figurative language that is fresh, context-specific, and not repeated mechanically.

## Detection rubric

Use this as an editorial score, not a verdict.

Pattern stacking rule: when several weak signals hit the same phrase or sentence, count them as one stronger finding, not three separate findings. Example: a coined term in boldface, scare quotes, and an em-dash aside is one stacked pattern.

Quantitative rule: count before claiming density. Count em dashes, scare-quoted terms, repeated sentence openings, heading patterns, three-item lists, and Tier 1 vocabulary hits instead of relying on a vague impression.

### P0: fix immediately

- Chatbot disclaimers or UI residue.
- Citation/markup leaks.
- Visible placeholders.
- Unsourced vague attributions.
- Generic claims of importance or notability.
- Formulaic prompt restatement or sycophantic opener in published prose.

### P1: fix before publishing

- Tier 1 vocabulary clusters.
- `not X but Y` repeated.
- `let's` transition openers.
- `here's the thing/kicker` transitions.
- Generic scene setters.
- Copula avoidance clusters.
- Superficial participle tails.
- Em dash overuse.
- Bold-first bullets in prose.
- Generic conclusions.
- Vague declaratives that announce importance without evidence.
- Pull-quote endings repeated across paragraphs.
- Pedagogical hand-holding in expert prose.

### P2: polish when time allows

- Rule-of-three overuse.
- Uniform paragraph length.
- Formal transitions used too often.
- Hollow intensifiers.
- Magic adverbs and softener clusters.
- Low sentence-length variation.
- Over-clean, neutral voice where the genre calls for judgment.

### Suggested density thresholds

- 1 hard artifact: inspect and fix.
- 3+ Tier 1 vocabulary hits in a short piece: rewrite paragraph-level prose.
- 5+ Tier 2 hits across 500 words: style pass.
- 3+ repeats of the same AI-characteristic word in roughly 500 words: run a word-frequency edit.
- 4-8 exact phrase-list hits: medium-risk style cluster; review by paragraph.
- 9+ exact phrase-list hits: high-density cliche cluster; rebuild affected sections.
- 2+ negative-parallelism templates: rewrite structure.
- 3+ rhetorical self-questions: rewrite structure.
- 30%+ of paragraphs with the same opening/closing shape: rewrite from outline.
- 3+ repeated sentence openers in one paragraph or section: check for anaphora abuse.
- 2+ paragraphs ending in short punchy fragments: check for pull-quote bait.
- 2+ uses of the same metaphor family across a short piece: check for dead metaphor.
- 5+ pattern categories triggered: do not patch word by word; rebuild from the core claim.

### Simple weighted score

Use this as a style-quality triage score, not an accusation score.

- Hard artifact: `+10` each. Examples: `as an AI language model`, `I hope this helps`, `contentReference`, `oaicite`, `turn0search0`.
- Medium structural pattern: `+3` each. Examples: `serves as`, `not only...but also`, vague attribution, rule-of-three, `Despite challenges...`.
- Soft vocabulary: `+1` per unique Tier 1 word, plus `+1` if repeated.
- Tier 2 paragraph cluster: `+2` if three or more Tier 2 words appear in the same paragraph.
- Transition repetition: `+2` if the same transition appears three or more times.
- Formatting/cadence: `+2` each for excessive bold-first bullets, every paragraph being the same length, repeated title-case headings, or em-dash density above house style.

Suggested interpretation:

- `0-3`: ignore or make only obvious fixes.
- `4-8`: light edit.
- `9-15`: targeted rewrite.
- `16+`: full human edit plus source/fact check.

Alternative composite for larger tooling:

- Pattern score: about 70% of the total, based on weighted rule hits per 100 words, category breadth, and repeated patterns.
- Uniformity score: about 30% of the total, based on burstiness, type-token ratio, trigram repetition, sentence-length variation, and paragraph uniformity.
- Confidence: downgrade scores for short samples, quoted examples, code-heavy docs, and genres with naturally formulaic structure.

### Scanner categories to expose

If implementing this as a linter, separate the output by issue type so the editor can choose the right pass:

- Hard artifacts: chatbot residue, citation leaks, placeholders, broken markup.
- Vocabulary cliches: single words and multi-word terms.
- Hedging and filler: caution preambles, transition padding, restatement bridges.
- Hook formulas: canned openers, reveal setups, motivational frames.
- Cadence structures: negation reframes, self-posed questions, tricolons, aphoristic closers.
- Formatting tells: em dashes, bold-first bullets, emoji bullets, decorative Unicode.
- Jargon/cliche: corporate filler, vague strategy language, marketing adjectives.
- Rhythm: uniform paragraph length, repeated sentence openings, low sentence-length variation.
- Specificity: vague attribution, absent actors, unsupported importance claims.

### Example weighted-module architecture

JohnCrickett's detector is a useful implementation reference because it scores categories separately, caps their contribution, and highlights matches in context. A linter can adapt the same structure without presenting the result as authorship proof:

- AI vocabulary: cap around 40 points; count distinct markers and total occurrences.
- Undue emphasis: cap around 30; catch `stands as`, `serves as`, `plays a pivotal role`, `reflects broader`, `indelible mark`, and notability padding.
- Superficial analysis: cap around 30; catch vague significance claims, `It is worth noting`, `various sources indicate`, and loose participle endings.
- Promotional language: cap around 25; catch tourism, product, brand, and superlative language.
- Outline conclusions: cap around 30; weight rigid `Despite challenges...` patterns strongly.
- Negative parallelism: cap around 25; catch `not only...but`, `not just...it's`, `not...but`, `not...rather`, and `no...no...just`.
- Rule of three: cap around 30; catch repetitive adjective/verb triples rather than all legitimate lists.
- Vague attributions: cap around 30; catch `experts argue`, `studies show`, `industry reports`, `is believed`, and `has been shown`.
- Overgeneralization: cap around 25; catch `academic consensus`, `widespread agreement`, `most experts`, `widely accepted`, and `universally acknowledged`.
- Elegant variation: cap around 25; catch needless synonym cycling for the same entity.
- False ranges: cap around 30; catch meaningless `from X to Y` scopes.

### Rewrite and detect modes

A practical tool should support two modes:

- Rewrite mode: identify AI-style issues, rewrite the text, summarize what changed, then run a second-pass audit on the rewrite.
- Detect mode: flag issues only, grouped by severity, and label each as a clear problem or a judgment call.

Recommended output shape for rewrite mode:

1. Issues found, with quoted fragments.
2. Rewritten version.
3. What changed.
4. Second-pass audit, including any remaining tells and final fixes.

Recommended output shape for detect mode:

1. Issues found, grouped by P0/P1/P2.
2. Assessment of which flags should definitely be fixed and which may be intentional or acceptable in context.

### Context profiles

Adjust strictness by genre:

- `linkedin`: tolerate one hook, short fragments, and light visual formatting; tighten hashtag stuffing and generic thought-leadership phrasing.
- `blog`: default profile; all rules apply.
- `technical-blog`: relax technical uses of `robust`, `comprehensive`, `ecosystem`, `leverage`, and parameter-style lists; still flag `delve`, `tapestry`, `game-changer`, and vague significance claims.
- `investor-email`: extra strict on promotional language, future-narrative closers, unsupported traction claims, and hedge-stacked predictions.
- `docs`: tolerate lists, tables, and headings when they serve reference use; tighten chatbot residue and vague claims.
- `casual`: focus on hard artifacts and obvious chat residue; skip most style-polish rules.

### Self-reference escape hatch

When a document is about AI writing patterns, do not flag examples inside quotes, code blocks, tables of examples, or explicitly introduced bad-writing samples. Only flag patterns that appear in the author's own prose.

### Batch and CI workflow

For repo or documentation scans, borrow the safer parts of CLI-style tools:

- Ignore fenced code blocks and inline code unless the user explicitly wants examples reviewed.
- Save a baseline JSON/report and fail only on regressions instead of failing legacy material.
- Report recurring pattern hotspots across files so teams can fix style guides or prompts upstream.
- Use a minimum word threshold for statistical metrics; short snippets should get phrase-only review.
- Keep generated/vendor/archive folders out of default scans.

## Rewrite playbook

Recommended pass order:

1. Kill structure tells: repeated section shapes, mechanical headings, identical paragraph arcs, disguised lists, fractal summaries.
2. Strip significance inflation and promotional language.
3. Replace AI vocabulary and imported cliche wordlists.
4. Fix grammar-level patterns: copula avoidance, false agency, passive actor-hiding, superficial participle tails, negative parallelism.
5. Fix rhythm: vary sentence length, remove staccato drama, break metronomic paragraphs.
6. Cut hedging, filler, vague attributions, lazy extremes, and adverb clusters.
7. Fix connective tissue: remove transition crutches and make real logical links.
8. Add human texture only where it fits: a specific judgment, concrete detail, constraint, uncertainty, or authorial stake.

Operating moves:

1. Delete preambles. Start with the point.
2. Replace abstract nouns with concrete objects, people, institutions, dates, numbers, or mechanisms.
3. Replace inflated verbs with plain verbs.
4. Name the actor.
5. Name the source.
6. Remove one hedge from every hedge stack.
7. Keep one rhetorical flourish only if it earns its place.
8. Collapse three-item filler lists into one or two real items.
9. Vary paragraph shape.
10. Preserve domain terms when they are precise.
11. Match the writer's sample if one exists.
12. Run a second pass for remaining structure tells, not just vocabulary.

Preserve:

- Technical accuracy, proper nouns, citations, equations, variables, named concepts, and domain terms with exact meaning.
- The writer's core argument and any deliberate style choices supported by a sample.
- Formatting that is required by the target venue.

Read-aloud test:

- Does it sound like a press release?
- Would a person in this field actually say this?
- Could the paragraph fit almost any topic if the nouns were swapped?
- Is it trying too hard to sound smart, balanced, or inspirational?

## Starter machine-readable checklist

This is a seed list for a linter. Use case-insensitive matching and word boundaries where possible. Prefer density scoring over binary flags.

### Hard artifacts

```text
as an ai language model
as of my last update
as of my last knowledge update
regenerate response
i do not have access to
i don't have access to
based on available information
turn0search
turn0image
contentreference
oaicite
oai_citation
attached_file
grok_card
utm_source=chatgpt.com
utm_source=claude.ai
utm_source=perplexity.ai
```

### Vocabulary

```text
delve
tapestry
landscape
realm
paradigm
testament
leverage
utilize
harness
facilitate
foster
underscore
showcase
navigate
embark
robust
comprehensive
nuanced
multifaceted
intricate
pivotal
crucial
paramount
certainly
indeed
ultimately
fundamentally
groundbreaking
transformative
revolutionary
cutting-edge
synergy
ecosystem
streamline
elevate
empower
bolster
cultivate
illuminate
elucidate
ensure
aligns
aims
remarked
surpassing
tragically
primarily
commendable
meticulous
invaluable
vibrant
thriving
seamless
swift
inquiry
avant-garde
captivating
bustling
distinguished
esteemed
exquisite
formidable
iconic
indomitable
irrefutable
omniscient
pioneering
predominant
prominent
quintessential
tangible
trailblazing
ubiquitous
unassailable
unblemished
unequaled
unmatched
unparalleled
unrivaled
unsurpassed
unwavering
unyielding
visionary
apogee
epitome
facet
gusto
nexus
pinnacle
brace
discover
dive
embrace
emerge
ensure
envision
galvanize
orchestrate
redefine
reinforce
transcend
unleash
unlock
usher
quietly
remarkably
arguably
```

### Phrase fragments

```text
it is important to note
it's important to note
it is worth noting
it's worth noting
needless to say
furthermore
moreover
additionally
in today's
today's fast-paced world
in the realm of
in a world where
when it comes to
at its core
at the end of the day
navigate challenges
lean into
game-changer
double down
deep dive
take a step back
moving forward
circle back
on the same page
best practices
actionable insights
move the needle
paradigm shift
speaks volumes
thought leader
thought leadership
food for thought
playbook
signal vs noise
hold space
making an impact
impacting
plays a significant role in shaping
plays a crucial role in determining
stands as a testament
underscores the significance of
shaping the landscape
transformative power
notable works include
notable figures include
the reality is
here's the thing
here's the kicker
here's where it gets interesting
here's what i find interesting
here's the problem though
here's the starting point
here's the deal
the uncomfortable truth is
it turns out
the real question is
the truth is simple
the heart of the matter
have you ever wondered
let's be honest
most people believe
they're wrong
stop doing
start doing
i used to think
i was wrong
the window for
what if the way we think about
right now
x is changing the way
x is more than just
let's unpack
let's dive in
let's break this down
let's break this down step by step
let me walk you through
in this section, we'll
as we'll see
i want to explore
think of it as
think of it like
think about it
imagine a world where
full stop
let that sink in
make no mistake
here's why that matters
plot twist
spoiler
you already know this, but
that's another post
is a feature, not a bug
dressed up as
the rest of this essay explains
and yes
since we're being honest
this is not a rant
it's a diagnosis
the reasons are structural
the implications are significant
the stakes are high
the consequences are real
history is clear
history is unambiguous
it goes without saying
it bears mentioning
that being said
to be clear
in other words
on the other hand
at the same time
in the grand scheme of things
in a nutshell
aims to explore
aims to enhance
in order to
due to the fact that
at this point in time
in the event that
has the ability to
while specific details are limited
while specific details are scarce
would you like
here is a
in conclusion
in summary
overall
to summarize
only time will tell
the future looks bright
exciting times lie ahead
a major step in the right direction
```

### Regex-style structural patterns

```regex
\bnot\s+(just\s+)?[^.!?;]{1,80}\bbut\s+(also\s+)?[^.!?;]{1,80}
\bit'?s\s+not\s+[^.!?;]{1,80}\bit'?s\s+[^.!?;]{1,80}
\bno\s+[^.!?]{1,50}\.\s+no\s+[^.!?]{1,50}\.\s+just\s+[^.!?]{1,80}
\bthe\s+\w+\?\s+[A-Z][^.!?]{1,80}[.!?]
\bfrom\s+[^.!?]{1,80}\s+to\s+[^.!?]{1,80}
\bserves\s+as\b|\bstands\s+as\b|\bboasts\b|\bfeatures\b
\bcould\s+potentially\b|\bmay\s+eventually\b|\bmight\s+ultimately\b
,\s+no\s+(guessing|wasted\s+motion|extra\s+steps)\b
,\s+\b(highlighting|showcasing|reflecting|ensuring|contributing|underscoring|emphasizing)\b[^.!?]{0,120}[.!?]
\b(the\s+)?(implementation|optimization|integration|development|utilization|enhancement)\s+of\b
^(What|When|Where|Which|Who|Why|How)\b
^So,\s+
^Look,\s+
\b(The first|The second|The third|The fourth)\b
\b(every|always|never|everyone|everybody|nobody|no one)\b
\b(consensus|widespread agreement|most experts|most scholars|widely accepted|universally acknowledged)\b
\b[\w-]+ing\s+(the\s+)?(importance|significance|need|role|impact)\s+of\b
\b(it|this|that)\s+(is|was)\s+not\s+[^.!?]{1,60}[.!?]\s+(it|this|that)\s+(is|was)\s+[^.!?]{1,80}
\b(is|are|was|were|remains?|becomes?|became)\s+[^.!?\n:]{2,90}:\s+[^.!?\n]{8,160}
\borganizing object\b
→|⇒|⟶
```

### Conservative scoring regexes

These are starter rules for a deterministic linter. Use them to collect evidence and drive edits, not to declare authorship.

```regex
# Hard delete / repair
\b(as an ai language model|as a large language model)\b
\b(i hope this helps|let me know if|would you like me to|great question|certainly!?|of course!?)\b
\b(as of my last knowledge update|up to my last training update|based on available information)\b
(contentReference\[oaicite|oai_citation|turn0(search|image|news|file)\d+|attached_file|grok_card)
\[[^\]]*(describe|insert|add|replace)[^\]]*\]

# Medium rewrite
\b(stands|serves)\s+as\s+(a|an|the)?\b
\bboasts?\s+(a|an|the|over|\d)
\bplays?\s+a\s+(crucial|pivotal|significant|vital)\s+role\b
\b(marking|represents?|underscores?|showcases?|highlights?)\s+.*\b(significance|importance|legacy|impact)\b
\bnot\s+(just|only|merely)\b.+?\bbut(\s+also)?\b
\bdespite\b.+?\b(continues?\s+to\s+thrive|future\s+looks\s+bright|offers?\s+opportunities)\b
\b(experts|observers|industry reports|critics|researchers)\s+(believe|argue|suggest|note|say)\b
\b(in conclusion|in summary|overall|as we move forward|only time will tell)\b

# Soft vocabulary, count density rather than auto-remove
\b(delve|tapestry|realm|pivotal|intricate|meticulous|robust|underscore|showcase|seamless|leverage|foster|enhance|bolster|navigate|empower|facilitate|myriad|plethora|transformative)\b

# Biomedical/academic cluster terms, count density only
\b(across|additionally|comprehensive|crucial|enhancing|exhibited|insights|notably|particularly|within)\b
```

## Caveats and anti-misuse notes

- Words change. Once a tell becomes famous, writers and models adapt. Keep the list updateable.
- Tells vary by model and date. A word like `delve` can be highly diagnostic during one model era and less useful after public attention or model updates.
- Human writers can sound like AI because AI learned from human genres: press releases, LinkedIn posts, school essays, corporate docs, and tourist prose.
- Non-native English writers can be falsely flagged because detectors reward certain native-like variation patterns.
- Neurodivergent, highly formal, or deadline-pressed writers can also trigger uniformity signals.
- A polished rewrite can become more AI-like if it removes every idiosyncrasy. The goal is not messiness. The goal is authored specificity.
- Removing surface tells may make detection harder without fixing underlying problems. Paraphrase attacks can reduce detector scores while leaving hallucinated citations, overgeneralized claims, or unsupported significance intact. Always check factuality, citations, claims, and authorial accountability.
- Set the acceptable false-positive tolerance before automation. A personal style-cleanup linter can be aggressive; any workflow with consequences for another person must be conservative, appealable, and backed by human review.

## Minimal operating procedure

For any draft:

0. Confirm target language, genre/profile, and false-positive tolerance.
1. Run hard-artifact scan.
2. Count Tier 1 vocabulary.
3. Run a word-frequency pass for repeated AI-characteristic terms.
4. Search phrase fragments.
5. Search structural regexes.
6. Apply the simple weighted score if triage is useful.
7. Group hits by category instead of showing one flat warning list.
8. Look at paragraph rhythm by eye.
9. For longer prose, check burstiness, type-token ratio, trigram repetition, and sentence-length variation.
10. Check sources and specificity.
11. Decide: patch or rebuild.
12. Rewrite.
13. Re-scan.
14. Read aloud.
15. If a writer sample exists, calibrate sentence length, diction, paragraph starts, punctuation habits, recurring phrases, and transition style to that sample.

If the draft still sounds like it could have been produced by a neutral assistant for any topic, add specifics from the writer, project, evidence, audience, and stakes.

## May 2026 repo-by-repo refinements

This compendium now distinguishes source-backed lint families from raw phrase dumps:

- `stop-slop` and `skill-deslop` support stronger structural rules for false reversals (`the answer isn't X; it is Y`), narrator-distance phrases (`people tend to`, `this happens because`), listicle-in-prose, fractal summaries, repeated metaphors, and historical analogy stacking.
- `humanize-writing` and `blader/humanizer` support the workflow layer: structure first, then inflation, vocabulary, grammar-level templates, rhythm, hedging, voice calibration, and a final anti-AI pass.
- `avoid-ai-writing` supports context-sensitive Tier-3 phrase density: `worth checking out`, `the integration of`, `the intersection of`, `community-driven`, and related boilerplate should be flagged when repeated or clustered, not when used once with a concrete claim.
- `brandonwise/humanizer` supports implementation discipline: short-sample reliability, component scoring, code-block masking, hidden Unicode detection, before/after score deltas, and regression-aware cleanup.
- `humanizer_academic` supports academic carve-outs: cited transitions and attribution phrases are ordinary scholarly prose when tied to citations, data, or a concrete finding.
- `JohnCrickett/ai-writing-detector` supports nonblocking review prompts for named-entity density plus vague attribution, passive-voice frequency, paragraph coherence, and false-range exceptions.
- `nanxstats/llm-cliches` is used as a vocabulary cross-check only; ordinary verbs such as `discover`, `ensure`, and `emerge` should not become hard blockers.
- `antislop-sampler` is useful for generation-time phrase suppression, but its very large word and probability-adjustment lists are too broad for a style linter. Import only cross-confirmed items.
- `colon-gloss` academic scaffolding is a soft but recurring tell: sentences like `The index is a ratio: the numerator is...` or `The second factor is pass-through: it asks...` often read like assistant exposition when repeated. Split the sentence or state the mechanism directly.
- `organizing object` is a weak meta-label in theory and empirical writing unless the paper has formally defined an object with that name. Prefer the actual equation, cutoff, statistic, or comparison.

Strict cleanup should therefore use three layers:

1. Hard and structural blockers: delete or rewrite.
2. Density blockers: rewrite when repeated or clustered.
3. Review prompts: passive voice, coherence, named-entity density, title case, single soft vocabulary, and academic transitions with citations.
