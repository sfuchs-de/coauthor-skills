#!/usr/bin/env python3
"""AI-style prose lint for Markdown, text, and TeX drafts.

This is a deterministic first pass. It maps likely "AI slop" patterns to
file/line findings so an editor can inspect and rewrite them. It is not an AI
authorship detector.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable


FLAGS = re.IGNORECASE | re.UNICODE
DEFAULT_RULEBOOK_PATH = Path(__file__).resolve().parents[1] / "references" / "rulebook.json"
DEFAULT_COMPENDIUM_PATH = Path(__file__).resolve().parents[1] / "references" / "compendium.md"
FILE_LEVEL_RULE_IDS = {
    "low-type-token-ratio",
    "low-sentence-burstiness",
    "trigram-repetition",
    "em-dash-density",
    "bold-first-bullets",
    "title-case-heading-density",
    "passive-voice-frequency",
    "named-entity-vague-attribution",
    "low-entity-confident-generalization",
}
SOFT_NONBLOCKING_CATEGORIES = {
    "soft vocabulary",
    "statistical uniformity",
}
STRICT_NONBLOCKING_RULE_IDS = FILE_LEVEL_RULE_IDS | {
    "paragraph-coherence-review",
}
ACADEMIC_TRANSITION_TERMS = {
    "additionally",
    "consequently",
    "furthermore",
    "indeed",
    "interestingly",
    "moreover",
    "notably",
    "primarily",
    "subsequently",
    "ultimately",
}
ACADEMIC_CONTEXTS = {"academic", "referee"}
COMMON_ENTITY_WORDS = {
    "a",
    "an",
    "and",
    "as",
    "but",
    "figure",
    "for",
    "in",
    "it",
    "section",
    "table",
    "the",
    "this",
    "we",
}
CHATGPT_COMPENDIUM_FAMILIES = [
    {
        "family": "chatbot residue and assistant scaffolding",
        "flag_when_similar": "The prose sounds like a ChatGPT answer, apology, prompt acknowledgment, capability disclaimer, or helpful signoff even if the exact phrase differs.",
        "review_question": "Could this sentence be copied from an assistant reply rather than authored prose?",
    },
    {
        "family": "generic scene-setting and throat-clearing",
        "flag_when_similar": "The sentence delays the point with broad context, setup, or reader steering before giving a specific actor, claim, or evidence.",
        "review_question": "Can the setup be deleted without losing substance?",
    },
    {
        "family": "throat-clearing and insight announcement",
        "flag_when_similar": "The prose announces that something is interesting, important, worth noting, or the real issue before making the actual point.",
        "review_question": "Does the sentence announce insight instead of delivering it?",
    },
    {
        "family": "inflated significance and promotional framing",
        "flag_when_similar": "Routine facts are framed as pivotal, transformative, remarkable, testament-like, landscape-shaping, or press-release-worthy.",
        "review_question": "Does the prose assert importance instead of proving it with facts?",
    },
    {
        "family": "promotional register",
        "flag_when_similar": "Neutral description turns into press-release, tourism, LinkedIn, or product-marketing voice.",
        "review_question": "Could the passage be made neutral by removing praise adjectives and adding evidence?",
    },
    {
        "family": "vague authority and unsupported consensus",
        "flag_when_similar": "Authority is attributed to unnamed experts, observers, studies, reports, consensus, or a field at large without a concrete source.",
        "review_question": "Could the sentence name the source, study, person, date, or evidence?",
    },
    {
        "family": "formulaic contrast and tidy reframing",
        "flag_when_similar": "The sentence uses a not-X-but-Y, X-is-not-the-problem/Y-is, no-X-no-Y-just-Z, or similarly tidy reversal shape.",
        "review_question": "Would a direct positive claim be clearer?",
    },
    {
        "family": "rule-of-three padding",
        "flag_when_similar": "Ideas are forced into triads where the third item adds rhythm more than information.",
        "review_question": "Is the list three items because there are three real points, or because the cadence wants three?",
    },
    {
        "family": "false ranges",
        "flag_when_similar": "A from-X-to-Y construction acts as a fancy list rather than a real scale, interval, geography, date range, or quantity range.",
        "review_question": "Do the endpoints belong on a real scale?",
    },
    {
        "family": "superficial analysis tails",
        "flag_when_similar": "A trailing clause adds highlighting, showcasing, reflecting, underscoring, or implying-broader-meaning analysis without mechanism.",
        "review_question": "Does the tail add evidence or only a gesture at significance?",
    },
    {
        "family": "balanced template conclusions",
        "flag_when_similar": "The passage ends with generic future optimism, only-time-will-tell uncertainty, or a neat recap that could close any article.",
        "review_question": "Could the ending be replaced with a concrete final fact or implication?",
    },
    {
        "family": "mechanical formatting and list cadence",
        "flag_when_similar": "Bullets, bold labels, equal-length items, or repeated section shapes make the text feel like generated Markdown.",
        "review_question": "Does the layout reveal a default assistant template?",
    },
    {
        "family": "AI-favored vocabulary clusters",
        "flag_when_similar": "Several abstract, polished, or overused ChatGPT words cluster in the same paragraph even if no single word is decisive.",
        "review_question": "Are vague style words replacing nouns, actors, numbers, and mechanisms?",
    },
    {
        "family": "over-smooth rhythm and generic voice",
        "flag_when_similar": "Paragraphs have a neutral, evenly balanced, always-explanatory voice that lacks author-specific judgment, friction, or specificity.",
        "review_question": "Could this paragraph have been generated for almost any topic by swapping nouns?",
    },
    {
        "family": "academic ChatGPT slop",
        "flag_when_similar": "Academic prose uses cited-looking but vague claims, unsupported importance framing, or stacked formal transitions without data or a concrete finding.",
        "review_question": "Is the academic phrasing tied to citations/data, or is it generic scholarly-sounding filler?",
    },
]


@dataclasses.dataclass(frozen=True)
class Rule:
    rule_id: str
    category: str
    priority: str
    weight: int
    pattern: str
    why: str
    edit: str
    sources: tuple[str, ...] = ()
    blocking: bool = False
    scan_raw: bool = False
    contexts: tuple[str, ...] = ()
    exceptions: tuple[str, ...] = ()


@dataclasses.dataclass
class Finding:
    path: str
    line: int
    priority: str
    category: str
    rule_id: str
    weight: int
    match: str
    context: str
    why: str
    edit: str
    blocking: bool = False
    start: int = 0
    end: int = 0
    sources: tuple[str, ...] = ()


@dataclasses.dataclass
class ParagraphBlock:
    path: str
    index: int
    start_line: int
    end_line: int
    text: str


@dataclasses.dataclass
class ParagraphFindingGroup:
    path: str
    index: int
    start_line: int
    end_line: int
    score: int
    priorities: dict[str, int]
    categories: dict[str, int]
    excerpt: str
    edit_directions: list[str]
    stacked_patterns: list[str]
    findings: list[Finding]


SKIP_TEX_ENVS = {
    "align",
    "align*",
    "algorithm",
    "algorithmic",
    "bmatrix",
    "cases",
    "displaymath",
    "equation",
    "equation*",
    "gather",
    "gather*",
    "lstlisting",
    "matrix",
    "minted",
    "pmatrix",
    "smallmatrix",
    "tabular",
    "tabularx",
    "thebibliography",
    "tikzpicture",
    "verbatim",
}


HARD_RULES = [
    Rule(
        "ai-self-disclosure",
        "hard artifact",
        "P0",
        10,
        r"\b(as an ai language model|as a large language model|as an artificial intelligence|i am an ai)\b",
        "AI self-disclosure belongs to a chat transcript, not polished prose.",
        "Delete it or replace with the author's real limitation.",
        ("Wikipedia", "humanizer"),
    ),
    Rule(
        "knowledge-cutoff",
        "hard artifact",
        "P0",
        10,
        r"\b(as of my last (knowledge |training )?update|up to my last (knowledge |training )?update|i do not have access to real-time data|based on available information)\b",
        "Knowledge-cutoff language is copied from assistant behavior.",
        "Verify the claim and replace with sourced uncertainty, or delete.",
        ("Wikipedia", "avoid-ai-writing"),
    ),
    Rule(
        "chatbot-residue",
        "hard artifact",
        "P0",
        10,
        r"\b(certainly!?|of course!?|great question!?|i hope this helps|let me know if|would you like me to|happy to help|here'?s a draft)\b",
        "Conversational assistant residue is not draft prose.",
        "Delete unless the text is quoted dialogue.",
        ("Wikipedia", "stop-slop", "aismells"),
    ),
    Rule(
        "citation-leak",
        "hard artifact",
        "P0",
        10,
        r"\b(contentReference|oaicite|oai_citation|turn0(?:search|image|news|file)\d+|attached_file|grok_card)\b",
        "Generated citation or tool markup leaked into the draft.",
        "Remove the artifact and verify the citation manually.",
        ("Wikipedia", "humanizer"),
    ),
    Rule(
        "template-placeholder",
        "hard artifact",
        "P0",
        8,
        r"\[(?:your name|insert [^\]]+|describe [^\]]+|add [^\]]+|replace [^\]]+|citation needed|source needed)\]|20\d{2}-XX-XX|<!--\s*(?:add|insert|todo)",
        "Template placeholder appears to have shipped into the draft.",
        "Fill it with real content or delete the placeholder.",
        ("Wikipedia", "avoid-ai-writing"),
    ),
    Rule(
        "markdown-leak",
        "hard artifact",
        "P0",
        7,
        r"```|^\s*#{2,6}\s+\S",
        "Markdown formatting may have leaked into a non-Markdown draft.",
        "Normalize formatting for the target document format.",
        ("Wikipedia", "DashAway"),
    ),
]


MEDIUM_RULES = [
    Rule(
        "significance-inflation",
        "significance inflation",
        "P1",
        3,
        r"\b(stands as a testament to|serves as a testament to|marks? a pivotal moment|plays? a (?:crucial|pivotal|significant|vital) role|underscores? (?:the )?(?:importance|significance)|shap(?:e|es|ing) the landscape)\b",
        "Inflated significance language often substitutes for the concrete claim.",
        "Replace with what happened, who did it, and why it matters.",
        ("Wikipedia", "JohnCrickett", "avoid-ai-writing"),
    ),
    Rule(
        "promotional-puffery",
        "promotional puffery",
        "P1",
        3,
        r"\b(boasts?|nestled in the heart of|rich cultural heritage|breathtaking|groundbreaking|cutting-edge|game-changing|revolutionary|world-class|renowned|vibrant)\b",
        "Promotional phrasing weakens neutral or analytical prose.",
        "Use a neutral description or add evidence.",
        ("Wikipedia", "humanizer", "Pangram"),
    ),
    Rule(
        "vague-attribution",
        "vague attribution",
        "P1",
        3,
        r"\b(?:experts|observers|critics|analysts|industry reports|researchers|studies|many|some)\s+(?:believe|argue|suggest|note|say|contend|claim|indicate|show)\b",
        "Authority is invoked without naming a source.",
        "Name the source/study or cut the attribution.",
        ("Wikipedia", "JohnCrickett", "The Verge"),
    ),
    Rule(
        "negative-parallelism",
        "formulaic sentence template",
        "P1",
        3,
        r"\bnot\s+(?:just|only|merely)\b.{0,120}?\bbut(?:\s+also)?\b",
        "The not-X-but-Y template is a common LLM rhetorical crutch.",
        "State the positive claim directly.",
        ("Wikipedia", "stop-slop", "Washington Post"),
    ),
    Rule(
        "generic-conclusion",
        "generic conclusion",
        "P1",
        3,
        r"\b(in conclusion|in summary|to summarize|overall,|as we move forward|only time will tell|the future (?:looks|remains) bright)\b",
        "Formulaic wrap-up phrases often add no content.",
        "Delete the transition or end on a concrete final point.",
        ("Wikipedia", "avoid-ai-writing", "TechHarvey"),
    ),
    Rule(
        "challenge-future-template",
        "formulaic challenge/future template",
        "P1",
        3,
        r"\bdespite (?:these )?challenges\b.{0,160}?\b(?:continues? to thrive|future (?:looks|remains) bright|offers? opportunities)\b",
        "Generic adversity-plus-optimism templates hide the actual analysis.",
        "Name the specific challenge, response, and evidence.",
        ("Wikipedia", "JohnCrickett"),
    ),
    Rule(
        "participial-tail",
        "superficial participial analysis",
        "P1",
        3,
        r",\s+\b(?:highlighting|showcasing|reflecting|underscoring|emphasizing|demonstrating|illustrating|contributing to|ensuring)\b.{0,140}$",
        "Tacked-on -ing clauses often gesture at analysis without proving it.",
        "Cut the clause or convert it into a sourced, specific claim.",
        ("Wikipedia", "deslop", "Reinhart"),
    ),
    Rule(
        "copula-avoidance",
        "copula avoidance",
        "P1",
        2,
        r"\b(?:serves|served|stands|stood)\s+as\s+(?:a|an|the)?\b",
        "Fancy linking verbs often replace simpler 'is' or 'was'.",
        "Use 'is/was' unless the verb adds meaning.",
        ("Wikipedia", "deslop"),
    ),
    Rule(
        "generic-scene-setter",
        "generic scene setter",
        "P1",
        3,
        r"\b(in today'?s (?:fast-paced|rapidly evolving|digital|modern) (?:world|landscape|environment|era)|in a world where|when it comes to|at its core|it is (?:important|worth) noting)\b",
        "Generic scene-setting delays the specific claim.",
        "Start with the actor, event, evidence, or question.",
        ("stop-slop", "Bloomberry", "GPTZero"),
    ),
    Rule(
        "false-range",
        "false range",
        "P1",
        2,
        r"\bfrom\s+[^,.;:!?]{3,60}\s+to\s+[^,.;:!?]{3,80}",
        "From-X-to-Y phrasing can imply a scale where none exists.",
        "List the real categories or specify the actual range.",
        ("JohnCrickett", "deslop"),
    ),
    Rule(
        "nominalization-density",
        "nominalization",
        "P2",
        1,
        r"\b(?:the\s+)?(?:implementation|optimization|integration|development|utilization|enhancement|facilitation|exploration|evaluation)\s+of\b",
        "Noun-heavy wording can make prose abstract and impersonal.",
        "Prefer the active verb when no technical distinction is lost.",
        ("Reinhart", "Tercon-Dobrovoljc"),
    ),
]


REFEREE_RULES = [
    Rule(
        "referee-generic-praise",
        "referee generic praise",
        "P2",
        2,
        r"\bi (?:very much )?(?:enjoyed|liked) reading (?:this|the)\s+(?:(?:interesting|ambitious|excellent|fascinating|impressive)\s+)?(?:paper|manuscript)\b",
        "Formulaic praise delays the report's substantive judgment.",
        "Name the specific contribution, evidence, or revision that earned the positive assessment.",
        ("referee-report corpus",),
        False,
        False,
        ("referee",),
    ),
    Rule(
        "referee-tentative-request",
        "referee tentative request",
        "P2",
        1,
        r"\b(?:it would be (?:interesting|helpful|useful|informative|valuable) to|i would (?:probably )?(?:suggest|like) (?:to see|the authors to))\b",
        "Tentative request language can hide whether a change is required or optional.",
        "Use a direct request for required work or label the point as optional future work.",
        ("referee-report corpus",),
        False,
        False,
        ("referee",),
    ),
    Rule(
        "referee-recommendation-leak",
        "possible recommendation leakage",
        "P1",
        3,
        r"\b(?:i recommend (?:reject(?:ion)?|accept(?:ance)?|major revision|minor revision)|the paper is below the bar|does not clear the bar)\b",
        "A publication recommendation may have leaked into an author-facing report.",
        "Keep the precise recommendation in the confidential editor note, or confirm that this file is the editor note.",
        ("referee-report protocol",),
        False,
        False,
        ("referee",),
    ),
]


TIER1_TERMS = {
    "delve": r"delv(?:e|es|ed|ing)",
    "tapestry": r"tapestr(?:y|ies)",
    "realm": r"realms?",
    "landscape": r"landscapes?",
    "testament": r"testaments?",
    "pivotal": r"pivotal",
    "intricate": r"intricate",
    "meticulous": r"meticulous(?:ly)?",
    "robust": r"robust",
    "underscore": r"underscor(?:e|es|ed|ing)",
    "showcase": r"showcas(?:e|es|ed|ing)",
    "seamless": r"seamless(?:ly)?",
    "leverage": r"leverag(?:e|es|ed|ing)",
    "harness": r"harness(?:es|ed|ing)?",
    "foster": r"foster(?:s|ed|ing)?",
    "elevate": r"elevat(?:e|es|ed|ing)",
    "unlock": r"unlock(?:s|ed|ing)?",
    "unleash": r"unleash(?:es|ed|ing)?",
    "navigate": r"navigat(?:e|es|ed|ing)",
    "nuanced": r"nuanced",
    "multifaceted": r"multi[- ]?faceted",
    "comprehensive": r"comprehensive(?:ly)?",
    "paradigm": r"paradigms?",
}


TIER2_TERMS = {
    "additionally",
    "align",
    "bolster",
    "burgeoning",
    "compelling",
    "consequently",
    "cultivate",
    "crucial",
    "dynamic",
    "ecosystem",
    "elucidate",
    "empower",
    "enhance",
    "facilitate",
    "framework",
    "furthermore",
    "impactful",
    "importantly",
    "innovative",
    "insights",
    "interestingly",
    "moreover",
    "myriad",
    "notably",
    "plethora",
    "remarkable",
    "significant",
    "streamline",
    "subsequently",
    "sophisticated",
    "transformative",
    "ultimately",
    "valuable",
}


ACADEMIC_CLUSTER = {
    "across",
    "additionally",
    "comprehensive",
    "crucial",
    "delve",
    "enhancing",
    "exhibited",
    "insights",
    "meticulous",
    "notably",
    "particularly",
    "underscore",
    "within",
}


TIER3_PHRASES = {
    "emerging sector",
    "emerging space",
    "emerging category",
    "the integration of",
    "the intersection of",
    "community-driven",
    "long-term sustainability",
    "user engagement",
    "designed for long-term",
    "worth reading",
    "worth checking out",
    "worth exploring",
    "worth a look",
    "worth paying attention to",
}


def make_soft_rules() -> list[Rule]:
    rules: list[Rule] = []
    for term, pattern in TIER1_TERMS.items():
        rules.append(
            Rule(
                f"tier1-{term}",
                "soft vocabulary",
                "P2",
                1,
                rf"\b{pattern}\b",
                "High-signal AI-style vocabulary; meaningful mainly in context or clusters.",
                "Keep if precise. Otherwise replace with a concrete actor, action, fact, or simpler word.",
                ("Wikipedia", "llm-cliches", "GPTZero", "Pangram"),
            )
        )
    return rules


ALL_RULES = HARD_RULES + MEDIUM_RULES + REFEREE_RULES + make_soft_rules()
COMPILED_RULES = [(rule, re.compile(rule.pattern, FLAGS)) for rule in ALL_RULES]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:80] or "rule"


def literal_pattern(value: str) -> str:
    escaped = re.escape(value.strip())
    escaped = escaped.replace(r"\ ", r"\s+").replace(r"\-", r"[- ]")
    if value[:1].isalnum():
        escaped = r"\b" + escaped
    if value[-1:].isalnum():
        escaped = escaped + r"\b"
    return escaped


def compile_rules(rules: list[Rule]) -> list[tuple[Rule, re.Pattern[str]]]:
    compiled: list[tuple[Rule, re.Pattern[str]]] = []
    for rule in rules:
        try:
            compiled.append((rule, re.compile(rule.pattern, FLAGS)))
        except re.error as exc:
            print(f"warning: skipping invalid rule {rule.rule_id}: {exc}", file=sys.stderr)
    return compiled


def load_rulebook(path: Path) -> tuple[list[Rule], dict[str, str], set[str], set[str], set[str], dict[str, str]]:
    if not path.exists():
        print(f"warning: rulebook not found, using built-in rules only: {path}", file=sys.stderr)
        return [], {}, set(), set(), set(), {"path": str(path), "loaded": "false"}

    data = json.loads(path.read_text(encoding="utf-8"))
    rules: list[Rule] = []
    metadata = {
        "path": str(path),
        "loaded": "true",
        "version": str(data.get("version", "unknown")),
        "derived_from": str(data.get("derived_from", "")),
    }

    for phrase in data.get("hard_artifact_phrases", []):
        rules.append(
            Rule(
                f"rulebook-hard-{slugify(phrase)}",
                "hard artifact",
                "P0",
                10,
                literal_pattern(str(phrase)),
                "Compendium hard artifact: copied assistant/template residue is not polished prose.",
                "Delete or repair the artifact, then verify nearby claims and citations.",
                ("compendium rulebook",),
                True,
                False,
                (),
                (),
            )
        )

    for group in data.get("phrase_rules", []):
        for phrase in group.get("phrases", []):
            rules.append(
                Rule(
                    f"{group.get('rule_id', 'rulebook-phrase')}-{slugify(str(phrase))}",
                    str(group.get("category", "phrase fragment")),
                    str(group.get("priority", "P2")),
                    int(group.get("weight", 1)),
                    literal_pattern(str(phrase)),
                    str(group.get("why", "Compendium phrase fragment matched.")),
                    str(group.get("edit", "Inspect the passage and rewrite concretely if needed.")),
                    tuple(str(source) for source in group.get("sources", ["compendium rulebook"])),
                    bool(group.get("blocking", False)),
                    bool(group.get("scan_raw", False)),
                    tuple(str(context) for context in group.get("contexts", [])),
                    tuple(str(exception) for exception in group.get("exceptions", [])),
                )
            )

    for item in data.get("regex_rules", []):
        rules.append(
            Rule(
                str(item.get("rule_id", "rulebook-regex")),
                str(item.get("category", "structural pattern")),
                str(item.get("priority", "P2")),
                int(item.get("weight", 1)),
                str(item["pattern"]),
                str(item.get("why", "Compendium structural pattern matched.")),
                str(item.get("edit", "Inspect the passage and rewrite concretely if needed.")),
                tuple(str(source) for source in item.get("sources", ["compendium rulebook"])),
                bool(item.get("blocking", False)),
                bool(item.get("scan_raw", False)),
                tuple(str(context) for context in item.get("contexts", [])),
                tuple(str(exception) for exception in item.get("exceptions", [])),
            )
        )

    tiers = data.get("vocabulary_tiers", {})
    tier1_terms = {str(term): literal_pattern(str(term)) for term in tiers.get("tier1", [])}
    tier2_terms = {str(term).lower() for term in tiers.get("tier2", [])}
    academic_cluster = {str(term).lower() for term in tiers.get("academic_cluster", [])}
    tier3_phrases = {str(term).lower() for term in tiers.get("tier3_phrases", [])}
    return rules, tier1_terms, tier2_terms, academic_cluster, tier3_phrases, metadata


def expand_paths(paths: Iterable[str]) -> list[Path]:
    out: list[Path] = []
    exts = {".tex", ".ltx", ".md", ".markdown", ".txt", ".rst"}
    for raw in paths:
        path = Path(raw).expanduser()
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file() and child.suffix.lower() in exts and not any(part.startswith(".") for part in child.parts):
                    out.append(child)
        elif path.is_file():
            out.append(path)
        else:
            print(f"warning: skipping missing path: {raw}", file=sys.stderr)
    return out


def strip_unescaped_percent(line: str) -> str:
    escaped = False
    for idx, char in enumerate(line):
        if char == "\\" and not escaped:
            escaped = True
            continue
        if char == "%" and not escaped:
            return line[:idx]
        escaped = False
    return line


def strip_inline_math(text: str) -> str:
    text = re.sub(r"\\\(.+?\\\)", " ", text)
    text = re.sub(r"\\\[.+?\\\]", " ", text)
    text = re.sub(r"\$\$.+?\$\$", " ", text)
    text = re.sub(r"(?<!\\)\$[^$\n]+(?<!\\)\$", " ", text)
    return text


def strip_tex_markup(text: str) -> str:
    text = strip_unescaped_percent(text)
    text = strip_inline_math(text)
    text = re.sub(r"\\(?:cite|citep|citet|autocite|parencite|textcite|ref|eqref|label|url|href)\*?(?:\[[^\]]*\])*\{[^{}]*\}", " ", text)
    text = re.sub(r"\\(?:begin|end)\{[^{}]*\}", " ", text)
    for _ in range(3):
        text = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?", " ", text)
    text = text.replace("``", '"').replace("''", '"')
    text = re.sub(r"[{}~^]", " ", text)
    return normalize_space(text)


def strip_markdown_markup(text: str) -> str:
    text = re.sub(r"`[^`]+`", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[*_]{1,3}([^*_]+)[*_]{1,3}", r"\1", text)
    return normalize_space(text)


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def iter_clean_lines(path: Path) -> tuple[list[tuple[int, str, str]], list[str]]:
    raw_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    scan_raw_lines: list[str] = []
    clean: list[tuple[int, str, str]] = []
    suffix = path.suffix.lower()
    in_fence = False
    in_display_math = False
    tex_env_stack: list[str] = []

    for line_no, raw in enumerate(raw_lines, start=1):
        line = raw.rstrip("\n")
        stripped = line.strip()

        if suffix in {".md", ".markdown", ".txt", ".rst"}:
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fence = not in_fence
                scan_raw_lines.append("")
                clean.append((line_no, "", ""))
                continue
            if in_fence:
                scan_raw_lines.append("")
                clean.append((line_no, "", ""))
                continue
            scan_raw_lines.append(line)
            clean.append((line_no, strip_markdown_markup(line), line))
            continue

        if suffix in {".tex", ".ltx"}:
            begin_match = re.search(r"\\begin\{([^{}]+)\}", line)
            end_match = re.search(r"\\end\{([^{}]+)\}", line)
            if begin_match and begin_match.group(1) in SKIP_TEX_ENVS:
                tex_env_stack.append(begin_match.group(1))
                scan_raw_lines.append("")
                clean.append((line_no, "", ""))
                continue
            if tex_env_stack:
                if end_match and end_match.group(1) == tex_env_stack[-1]:
                    tex_env_stack.pop()
                scan_raw_lines.append("")
                clean.append((line_no, "", ""))
                continue
            if stripped.startswith(r"\[") or stripped.startswith("$$"):
                in_display_math = True
                scan_raw_lines.append("")
                clean.append((line_no, "", ""))
                continue
            if in_display_math:
                if stripped.endswith(r"\]") or stripped.endswith("$$"):
                    in_display_math = False
                scan_raw_lines.append("")
                clean.append((line_no, "", ""))
                continue
            scan_raw_lines.append(line)
            clean.append((line_no, strip_tex_markup(line), line))
            continue

        scan_raw_lines.append(line)
        clean.append((line_no, normalize_space(line), line))

    return clean, scan_raw_lines


def has_academic_support(raw: str, clean_text: str) -> bool:
    text = f"{raw} {clean_text}"
    if re.search(r"\\(?:cite|citep|citet|autocite|parencite|textcite)\*?(?:\[[^\]]*\])*\{[^{}]+\}", text):
        return True
    if re.search(r"\[[0-9,;\s-]+\]|\([A-Z][A-Za-z-]+(?:\s+et\s+al\.)?,?\s+20\d{2}[a-z]?\)", text):
        return True
    if re.search(r"\b\d+(?:\.\d+)?\s*(?:%|percent|pp|p\.p\.|basis points?|b\.p\.|kg|mg|ml|km|miles?|years?|months?)\b", text, FLAGS):
        return True
    if re.search(r"\b(?:Table|Figure|Appendix|Section)\s+[A-Z0-9.]+", text):
        return True
    return False


def has_rule_exception(rule: Rule, target_text: str) -> bool:
    return any(re.search(exception, target_text, FLAGS) for exception in rule.exceptions)


def is_false_range_exception(match_text: str) -> bool:
    lower = match_text.lower()
    if re.search(r"[$€£¥]?\d|(?:19|20)\d{2}|\b\d+(?:\.\d+)?\s*(?:%|percent|years?|months?|days?|kg|mg|km|miles?|meters?|hours?)\b", lower):
        return True
    if re.search(r"\b(?:january|february|march|april|may|june|july|august|september|october|november|december|spring|summer|fall|autumn|winter)\b", lower):
        return True
    if re.search(r"\b(?:age|ages|aged|grade|grades|level|levels|low|medium|high|beginner|intermediate|advanced|north|south|east|west)\b", lower):
        return True

    parts = re.split(r"\bto\b", match_text, maxsplit=1, flags=re.IGNORECASE)
    if len(parts) == 2:
        left = re.sub(r"^\s*from\s+", "", parts[0], flags=re.IGNORECASE).strip(" ,;:.")
        right = parts[1].strip(" ,;:.")
        proper_nounish = re.compile(r"^(?:[A-Z][A-Za-z.'-]+(?:\s+[A-Z][A-Za-z.'-]+){0,3})$")
        if proper_nounish.match(left) and proper_nounish.match(right):
            return True
    return False


def short_context(text: str, max_len: int = 180) -> str:
    text = normalize_space(text)
    if len(text) <= max_len:
        return text
    return text[: max_len - 3].rstrip() + "..."


def priority_sort_key(priority: str) -> int:
    return {"P0": 0, "P1": 1, "P2": 2, "P3": 3}.get(priority, 9)


def add_finding(
    findings: list[Finding],
    path: Path,
    line: int,
    priority: str,
    category: str,
    rule_id: str,
    weight: int,
    match: str,
    context: str,
    why: str,
    edit: str,
    blocking: bool = False,
    start: int = 0,
    end: int = 0,
    sources: tuple[str, ...] = (),
) -> None:
    findings.append(
        Finding(
            path=str(path),
            line=line,
            priority=priority,
            category=category,
            rule_id=rule_id,
            weight=weight,
            match=short_context(match, 90),
            context=short_context(context),
            why=why,
            edit=edit,
            blocking=blocking,
            start=start,
            end=end,
            sources=sources,
        )
    )


def scan_regex_rules(
    path: Path,
    clean_lines: list[tuple[int, str, str]],
    compiled_rules: list[tuple[Rule, re.Pattern[str]]],
    context: str,
) -> list[Finding]:
    findings: list[Finding] = []
    for line_no, clean_text, raw in clean_lines:
        if not clean_text and not raw:
            continue
        for rule, compiled in compiled_rules:
            if rule.contexts and context not in rule.contexts:
                continue
            if rule.rule_id == "markdown-leak" and path.suffix.lower() in {".md", ".markdown"}:
                continue
            target_text = raw if rule.scan_raw else clean_text
            if not target_text:
                continue
            if has_rule_exception(rule, target_text):
                continue
            if context in ACADEMIC_CONTEXTS and rule.category == "vague attribution" and has_academic_support(raw, clean_text):
                continue
            for match in compiled.finditer(target_text):
                if rule.category == "false range" and is_false_range_exception(match.group(0)):
                    continue
                priority = rule.priority
                blocking = rule.blocking
                if context in ACADEMIC_CONTEXTS and rule.category in {
                    "false range",
                    "formulaic sentence template",
                }:
                    priority = "P2"
                    blocking = False
                if context == "referee" and rule.category == "generic conclusion":
                    priority = "P2"
                    blocking = False
                add_finding(
                    findings,
                    path,
                    line_no,
                    priority,
                    rule.category,
                    rule.rule_id,
                    rule.weight,
                    match.group(0),
                    raw if raw.strip() else clean_text,
                    rule.why,
                    rule.edit,
                    blocking,
                    match.start(),
                    match.end(),
                    rule.sources,
                )
    return findings


def build_paragraphs(path: Path, clean_lines: list[tuple[int, str, str]]) -> list[ParagraphBlock]:
    paragraphs: list[ParagraphBlock] = []
    current: list[str] = []
    current_lines: list[int] = []
    start_line = 1
    for line_no, clean_text, _raw in clean_lines:
        if not clean_text:
            if current:
                paragraphs.append(
                    ParagraphBlock(
                        path=str(path),
                        index=len(paragraphs) + 1,
                        start_line=start_line,
                        end_line=current_lines[-1],
                        text=normalize_space(" ".join(current)),
                    )
                )
                current = []
                current_lines = []
            continue
        if not current:
            start_line = line_no
        current.append(clean_text)
        current_lines.append(line_no)
    if current:
        paragraphs.append(
            ParagraphBlock(
                path=str(path),
                index=len(paragraphs) + 1,
                start_line=start_line,
                end_line=current_lines[-1],
                text=normalize_space(" ".join(current)),
            )
        )
    return paragraphs


def scan_density(
    path: Path,
    paragraphs: list[ParagraphBlock],
    context: str,
    tier1_terms: dict[str, str],
    tier2_terms: set[str],
    academic_cluster: set[str],
    tier3_phrases: set[str],
) -> list[Finding]:
    findings: list[Finding] = []
    tier1_compiled = {term: re.compile(pattern, FLAGS) for term, pattern in tier1_terms.items()}
    tier2_re = re.compile(r"\b(" + "|".join(sorted(map(re.escape, tier2_terms), key=len, reverse=True)) + r")\b", FLAGS) if tier2_terms else None
    acad_re = re.compile(r"\b(" + "|".join(sorted(map(re.escape, academic_cluster), key=len, reverse=True)) + r")\b", FLAGS) if academic_cluster else None
    tier3_phrase_re = re.compile("|".join(sorted(map(re.escape, tier3_phrases), key=len, reverse=True)), FLAGS) if tier3_phrases else None

    for paragraph_block in paragraphs:
        words = word_tokens(paragraph_block.text)
        if len(words) < 35:
            continue
        tier1_hits = []
        for term, compiled in tier1_compiled.items():
            if compiled.search(paragraph_block.text):
                tier1_hits.append(term)
        tier2_hits = [m.group(1).lower() for m in tier2_re.finditer(paragraph_block.text)] if tier2_re else []
        acad_hits = [m.group(1).lower() for m in acad_re.finditer(paragraph_block.text)] if acad_re else []
        tier3_phrase_hits = [m.group(0).lower() for m in tier3_phrase_re.finditer(paragraph_block.text)] if tier3_phrase_re else []

        if context in ACADEMIC_CONTEXTS:
            tier2_hits = [hit for hit in tier2_hits if hit not in ACADEMIC_TRANSITION_TERMS]

        if len(tier1_hits) >= 3:
            add_finding(
                findings,
                path,
                paragraph_block.start_line,
                "P1",
                "vocabulary density",
                "tier1-density",
                3,
                ", ".join(sorted(tier1_hits)[:12]),
                paragraph_block.text,
                "Multiple high-signal style words occur in one paragraph.",
                "Replace vague terms with concrete facts; keep technically precise terms.",
                True,
                sources=("brandonwise/humanizer", "nanxstats/llm-cliches", "GPTZero"),
            )
        if len(tier2_hits) >= 5 or len(set(tier2_hits)) >= 4:
            add_finding(
                findings,
                path,
                paragraph_block.start_line,
                "P2",
                "vocabulary density",
                "tier2-density",
                2,
                ", ".join(sorted(set(tier2_hits))[:12]),
                paragraph_block.text,
                "Clustered formal transitions and abstract modifiers create a default-assistant register.",
                "Cut filler transitions and replace abstract modifiers with specifics.",
                True,
                sources=("brandonwise/humanizer", "nanxstats/llm-cliches", "avoid-ai-writing"),
            )
        if tier3_phrase_hits:
            phrase_counts = Counter(tier3_phrase_hits)
            repeated_phrases = [phrase for phrase, count in phrase_counts.items() if count >= 2]
            if repeated_phrases or len(phrase_counts) >= 3:
                add_finding(
                    findings,
                    path,
                    paragraph_block.start_line,
                    "P2",
                    "tier3 phrase density",
                    "tier3-phrase-density",
                    2,
                    ", ".join(sorted(repeated_phrases or phrase_counts.keys())[:12]),
                    paragraph_block.text,
                    "Repeated low-specificity phrases create boilerplate even when each phrase is mild alone.",
                    "Replace repeated boilerplate with the mechanism, actor, metric, or reason it matters.",
                    True,
                    sources=("conorbronsdon/avoid-ai-writing", "brandonwise/humanizer"),
                )
        if context in ACADEMIC_CONTEXTS and acad_hits and has_academic_support("", paragraph_block.text):
            acad_hits = [hit for hit in acad_hits if hit not in ACADEMIC_TRANSITION_TERMS]
        if context in ACADEMIC_CONTEXTS and len(acad_hits) >= 4:
            add_finding(
                findings,
                path,
                paragraph_block.start_line,
                "P2",
                "academic vocabulary density",
                "academic-cluster-density",
                2,
                ", ".join(sorted(set(acad_hits))[:12]),
                paragraph_block.text,
                "Academic terms associated with LLM-processed biomedical/scientific prose cluster in one paragraph.",
                "Keep field terms only when they are necessary; otherwise simplify.",
                True,
                sources=("humanizer_academic", "Kobak", "Juzek-Ward"),
            )
    return findings


def scan_paragraph_review(path: Path, paragraphs: list[ParagraphBlock]) -> list[Finding]:
    findings: list[Finding] = []
    for paragraph_block in paragraphs:
        sentences = sentence_tokens(paragraph_block.text)
        if len(sentences) < 4:
            continue
        similarity = average_adjacent_similarity(paragraph_block.text)
        if similarity is not None and similarity > 0.48:
            add_finding(
                findings,
                path,
                paragraph_block.start_line,
                "P2",
                "paragraph coherence review",
                "paragraph-coherence-review",
                1,
                str(round(similarity, 3)),
                paragraph_block.text,
                "Adjacent sentences have unusually similar vocabulary, which can indicate over-smoothed paragraph progression.",
                "Review for repeated framing; keep the paragraph if the repetition is necessary for technical precision.",
                False,
                sources=("JohnCrickett/ai-writing-detector",),
            )
    return findings


def word_tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'-]*", text.lower())


def sentence_tokens(text: str) -> list[str]:
    candidates = re.split(r"(?<=[.!?])\s+", normalize_space(text))
    return [s for s in candidates if len(word_tokens(s)) >= 3]


def coefficient_of_variation(values: list[int]) -> float | None:
    if len(values) < 2:
        return None
    mean = statistics.mean(values)
    if mean == 0:
        return None
    return statistics.pstdev(values) / mean


def passive_voice_count(sentences: list[str]) -> int:
    passive_re = re.compile(r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+\s+){0,3}\w+(?:ed|en)\b", FLAGS)
    return sum(1 for sentence in sentences if passive_re.search(sentence))


def named_entities(text: str) -> list[str]:
    candidates = re.findall(r"\b(?:[A-Z][A-Za-z.'-]+(?:\s+[A-Z][A-Za-z.'-]+){0,3})\b", text)
    entities = []
    for candidate in candidates:
        words = word_tokens(candidate)
        if not words:
            continue
        if all(word in COMMON_ENTITY_WORDS for word in words):
            continue
        if len(words) == 1 and words[0] in COMMON_ENTITY_WORDS:
            continue
        entities.append(candidate)
    return entities


def has_vague_attribution(text: str) -> bool:
    return bool(
        re.search(
            r"\b(?:experts|observers|critics|analysts|industry reports|researchers|studies|sources|many|some)\s+"
            r"(?:believe|argue|suggest|note|say|contend|claim|indicate|show|report)\b",
            text,
            FLAGS,
        )
    )


def has_confident_generalization(text: str) -> bool:
    return bool(re.search(r"\b(?:clearly|obviously|universally|always|never|everyone knows|well established)\b", text, FLAGS))


def average_adjacent_similarity(paragraph: str) -> float | None:
    sentences = sentence_tokens(paragraph)
    if len(sentences) < 3:
        return None
    similarities: list[float] = []
    for left, right in zip(sentences, sentences[1:]):
        left_words = {word for word in word_tokens(left) if len(word) > 3}
        right_words = {word for word in word_tokens(right) if len(word) > 3}
        if not left_words or not right_words:
            continue
        similarities.append(len(left_words & right_words) / len(left_words | right_words))
    return statistics.mean(similarities) if similarities else None


def collect_metrics(
    path: Path,
    clean_lines: list[tuple[int, str, str]],
    raw_lines: list[str],
    context: str,
) -> tuple[dict[str, float | int | None], list[Finding]]:
    text = " ".join(clean_text for _line_no, clean_text, _raw in clean_lines if clean_text)
    words = word_tokens(text)
    sentences = sentence_tokens(text)
    sentence_lengths = [len(word_tokens(sentence)) for sentence in sentences]
    unique_words = set(words)
    ttr = len(unique_words) / len(words) if words else None
    sent_cov = coefficient_of_variation(sentence_lengths)

    trigrams = list(zip(words, words[1:], words[2:]))
    trigram_counts = Counter(trigrams)
    repeated_trigrams = sum(count - 1 for count in trigram_counts.values() if count > 1)
    trigram_repeat_ratio = repeated_trigrams / len(trigrams) if trigrams else None
    passive_count = passive_voice_count(sentences)
    passive_ratio = passive_count / len(sentences) if sentences else 0
    entities = named_entities(text)
    unique_entities = set(entities)
    entity_density = len(unique_entities) / len(words) if words else 0

    raw_text = "\n".join(raw_lines)
    em_dash_count = len(re.findall(r"[\u2014\u2013]", raw_text))
    em_dash_per_1000 = (em_dash_count / len(words) * 1000) if words else 0
    bold_first_bullets = len(re.findall(r"(?m)^\s*[-*]\s+\*\*[^*\n:]{1,80}:?\*\*\s*[:\-]?", raw_text))
    title_case_headings = len(re.findall(r"(?m)^\s*(?:#{1,6}\s+|\\(?:sub)*section\*?\{)(?:[A-Z][A-Za-z0-9()/-]*\s+){2,}[A-Z][A-Za-z0-9()/-]*", raw_text))

    metrics: dict[str, float | int | None] = {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "type_token_ratio": round(ttr, 3) if ttr is not None else None,
        "sentence_length_cov": round(sent_cov, 3) if sent_cov is not None else None,
        "trigram_repeat_ratio": round(trigram_repeat_ratio, 3) if trigram_repeat_ratio is not None else None,
        "passive_voice_ratio": round(passive_ratio, 3),
        "named_entity_density": round(entity_density, 3),
        "named_entity_count": len(unique_entities),
        "em_dash_count": em_dash_count,
        "em_dash_per_1000_words": round(em_dash_per_1000, 2),
        "bold_first_bullets": bold_first_bullets,
        "title_case_headings": title_case_headings,
    }

    findings: list[Finding] = []
    first_line = 1
    if len(words) >= 200 and ttr is not None and ttr < 0.40:
        add_finding(
            findings,
            path,
            first_line,
            "P2",
            "statistical uniformity",
            "low-type-token-ratio",
            2,
            str(round(ttr, 3)),
            f"type-token ratio={round(ttr, 3)} over {len(words)} words",
            "Low lexical diversity can indicate mechanical or repetitive prose.",
            "Check whether repeated abstract nouns or transitions can be replaced with specifics.",
            False,
        )
    if len(sentences) >= 10 and sent_cov is not None and sent_cov < 0.45:
        add_finding(
            findings,
            path,
            first_line,
            "P2",
            "statistical uniformity",
            "low-sentence-burstiness",
            2,
            str(round(sent_cov, 3)),
            f"sentence length CoV={round(sent_cov, 3)} across {len(sentences)} sentences",
            "Uniform sentence length can make a draft read machine-polished.",
            "Vary rhythm only where the source material supports it.",
            False,
        )
    if len(words) >= 200 and trigram_repeat_ratio is not None and trigram_repeat_ratio > 0.10:
        add_finding(
            findings,
            path,
            first_line,
            "P2",
            "repetition",
            "trigram-repetition",
            2,
            str(round(trigram_repeat_ratio, 3)),
            f"trigram repeat ratio={round(trigram_repeat_ratio, 3)}",
            "Repeated three-word sequences can indicate boilerplate or templated prose.",
            "Find repeated frames and rewrite or delete duplicative passages.",
            True,
            sources=("brandonwise/humanizer",),
        )
    if len(sentences) >= 8 and passive_ratio > 0.15:
        add_finding(
            findings,
            path,
            first_line,
            "P2",
            "passive voice frequency",
            "passive-voice-frequency",
            1,
            str(round(passive_ratio, 3)),
            f"{passive_count} of {len(sentences)} sentences match a passive-voice heuristic",
            "High passive frequency can make prose actorless and default-formal.",
            "Review for missing actors; keep passive constructions that are standard for the genre.",
            False,
            sources=("JohnCrickett/ai-writing-detector", "stop-slop"),
        )
    if len(words) >= 120 and entity_density > 0.08 and has_vague_attribution(text):
        add_finding(
            findings,
            path,
            first_line,
            "P2",
            "named-entity attribution risk",
            "named-entity-vague-attribution",
            2,
            str(round(entity_density, 3)),
            f"{len(unique_entities)} named-entity candidates plus vague attribution language",
            "Packed names combined with unnamed authorities can signal hallucinated or synthetic sourcing.",
            "Verify named claims and replace vague authority with exact sources.",
            False,
            sources=("JohnCrickett/ai-writing-detector",),
        )
    elif len(words) >= 120 and entity_density < 0.01 and has_confident_generalization(text):
        add_finding(
            findings,
            path,
            first_line,
            "P2",
            "low-specificity generalization",
            "low-entity-confident-generalization",
            1,
            str(round(entity_density, 3)),
            "confident generalization with very low named-entity density",
            "Broad claims without named actors, sources, places, or studies can read generic.",
            "Add the concrete actor, case, source, date, or scope if the claim remains.",
            False,
            sources=("JohnCrickett/ai-writing-detector",),
        )
    dash_threshold = 6 if context == "referee" else 8
    if em_dash_count >= 4 and em_dash_per_1000 > dash_threshold:
        add_finding(
            findings,
            path,
            first_line,
            "P2",
            "formatting",
            "em-dash-density",
            2,
            str(em_dash_count),
            f"{em_dash_count} dash characters, {round(em_dash_per_1000, 2)} per 1000 words",
            "Dense dash-aside punctuation is a common current LLM surface tell.",
            "Normalize to house style; keep only dashes that match the author's voice.",
            True,
        )
    if bold_first_bullets >= 3:
        add_finding(
            findings,
            path,
            first_line,
            "P2",
            "formatting",
            "bold-first-bullets",
            2,
            str(bold_first_bullets),
            f"{bold_first_bullets} bold-first bullets",
            "Repeated bold-label bullets are a default assistant formatting habit.",
            "Use prose, normal bullets, or section headings according to the target format.",
            True,
        )
    if title_case_headings >= 4:
        add_finding(
            findings,
            path,
            first_line,
            "P2",
            "formatting",
            "title-case-heading-density",
            1,
            str(title_case_headings),
            f"{title_case_headings} title-case headings",
            "Dense title-case headings can signal assistant-generated outline structure.",
            "Normalize heading style to the venue or author's house style.",
            False,
        )
    return metrics, findings


def scan_referee_structure(path: Path, paragraphs: list[ParagraphBlock]) -> list[Finding]:
    findings: list[Finding] = []
    request_pattern = re.compile(
        r"\b(?:the primary request is|my primary request is|i (?:ask|request) (?:that|the authors)|"
        r"i would ask (?:that|the authors))\b",
        FLAGS,
    )
    requests: list[tuple[int, str]] = []
    for paragraph in paragraphs:
        for sentence in sentence_tokens(paragraph.text):
            if request_pattern.search(sentence):
                normalized = re.sub(r"\([^)]*(?:section|table|figure|appendix|p\.)[^)]*\)", "", sentence, flags=FLAGS)
                normalized = normalize_space(re.sub(r"[^a-z0-9 ]+", " ", normalized.lower()))
                requests.append((paragraph.start_line, normalized))

    if len(requests) >= 5:
        add_finding(
            findings,
            path,
            requests[0][0],
            "P2",
            "referee request density",
            "referee-request-density",
            2,
            str(len(requests)),
            f"{len(requests)} request sentences in one report",
            "A high number of asks can obscure which revisions are decisive.",
            "Keep one primary request per major comment and demote optional extensions.",
            True,
            sources=("referee-report corpus",),
        )

    for index, (left_line, left) in enumerate(requests):
        left_words = set(left.split())
        if len(left_words) < 8:
            continue
        for right_line, right in requests[index + 1 :]:
            right_words = set(right.split())
            union = left_words | right_words
            if not union:
                continue
            similarity = len(left_words & right_words) / len(union)
            if similarity >= 0.72:
                add_finding(
                    findings,
                    path,
                    right_line,
                    "P2",
                    "possible repeated remedy",
                    "referee-repeated-remedy",
                    2,
                    short_context(right, 90),
                    f"Request resembles an earlier request near line {left_line}",
                    "The same remedy may appear in both a major and smaller comment.",
                    "Keep the remedy once and use the other location for a distinct point.",
                    False,
                    sources=("referee-report protocol",),
                )
                break
    return findings


def scan_file(
    path: Path,
    context: str,
    compiled_rules: list[tuple[Rule, re.Pattern[str]]],
    tier1_terms: dict[str, str],
    tier2_terms: set[str],
    academic_cluster: set[str],
    tier3_phrases: set[str],
) -> tuple[list[Finding], dict[str, float | int | None], list[ParagraphBlock]]:
    clean_lines, raw_lines = iter_clean_lines(path)
    paragraphs = build_paragraphs(path, clean_lines)
    findings = []
    findings.extend(scan_regex_rules(path, clean_lines, compiled_rules, context))
    findings.extend(scan_density(path, paragraphs, context, tier1_terms, tier2_terms, academic_cluster, tier3_phrases))
    findings.extend(scan_paragraph_review(path, paragraphs))
    if context == "referee":
        findings.extend(scan_referee_structure(path, paragraphs))
    metrics, metric_findings = collect_metrics(path, clean_lines, raw_lines, context)
    findings.extend(metric_findings)
    return findings, metrics, paragraphs


def findings_overlap(left: Finding, right: Finding) -> bool:
    if not left.start or not left.end or not right.start or not right.end:
        return False
    return left.path == right.path and left.line == right.line and left.start < right.end and right.start < left.end


def score_findings(findings: list[Finding]) -> int:
    """Score findings while capping overlapping matches as one stacked tell."""
    score = 0
    span_findings = sorted(
        [finding for finding in findings if finding.start and finding.end],
        key=lambda finding: (finding.path, finding.line, finding.start, finding.end, -finding.weight),
    )
    no_span_findings = [finding for finding in findings if not finding.start or not finding.end]
    score += sum(finding.weight for finding in no_span_findings)

    idx = 0
    while idx < len(span_findings):
        cluster = [span_findings[idx]]
        idx += 1
        while idx < len(span_findings) and any(findings_overlap(span_findings[idx], existing) for existing in cluster):
            cluster.append(span_findings[idx])
            idx += 1
        if len(cluster) == 1:
            score += cluster[0].weight
            continue
        categories = {finding.category for finding in cluster}
        score += max(finding.weight for finding in cluster) + min(2, max(0, len(categories) - 1))
    return score


def score_components(findings: list[Finding]) -> dict[str, int]:
    components = {
        "hard_artifacts": 0,
        "rewrite_patterns": 0,
        "density": 0,
        "formatting": 0,
        "statistical_review": 0,
    }
    for finding in findings:
        category = finding.category.lower()
        if finding.priority == "P0" or "artifact" in category:
            components["hard_artifacts"] += finding.weight
        elif "density" in category or "vocabulary" in category or "repetition" in category:
            components["density"] += finding.weight
        elif "formatting" in category or "bullet" in category or "unicode" in category:
            components["formatting"] += finding.weight
        elif "statistical" in category or "passive voice" in category or "coherence" in category:
            components["statistical_review"] += finding.weight
        else:
            components["rewrite_patterns"] += finding.weight
    return components


def is_actionable_finding(finding: Finding, gate: str) -> bool:
    if gate == "none":
        return False
    if gate == "actionable":
        if finding.priority in {"P0", "P1"}:
            return True
        if finding.priority == "P2":
            return finding.blocking
        return False
    if finding.priority in {"P0", "P1"}:
        return True
    if finding.priority == "P2":
        if finding.blocking:
            return True
        if gate == "strict-compendium":
            if finding.category in SOFT_NONBLOCKING_CATEGORIES or finding.rule_id in STRICT_NONBLOCKING_RULE_IDS:
                return False
            return finding.rule_id.startswith(("compendium-", "repo-"))
    return False


def actionable_findings(findings: list[Finding], gate: str) -> list[Finding]:
    return [finding for finding in findings if is_actionable_finding(finding, gate)]


def gate_summary(findings: list[Finding], gate: str) -> dict[str, int | str | bool]:
    actionable = actionable_findings(findings, gate)
    return {
        "mode": gate,
        "passed": len(actionable) == 0,
        "actionable_count": len(actionable),
        "actionable_score": score_findings(actionable),
        "p0": sum(1 for finding in actionable if finding.priority == "P0"),
        "p1": sum(1 for finding in actionable if finding.priority == "P1"),
        "p2": sum(1 for finding in actionable if finding.priority == "P2"),
    }


def reliability_summary(
    findings: list[Finding],
    metrics_by_path: dict[str, dict[str, float | int | None]],
) -> dict[str, object]:
    total_words = sum(int(metrics.get("word_count") or 0) for metrics in metrics_by_path.values())
    total_sentences = sum(int(metrics.get("sentence_count") or 0) for metrics in metrics_by_path.values())
    pattern_families = {finding.category for finding in findings}
    confidence = 100
    reasons: list[str] = []

    if total_words < 80:
        confidence -= 40
        reasons.append("sample is very short (<80 words)")
    elif total_words < 150:
        confidence -= 20
        reasons.append("sample is shorter than the recommended 150+ words")

    if total_sentences < 4:
        confidence -= 25
        reasons.append("fewer than 4 sentences limits rhythm analysis")
    elif total_sentences < 7:
        confidence -= 10
        reasons.append("low sentence count weakens statistical signals")

    if len(pattern_families) <= 1 and findings:
        confidence -= 15
        reasons.append("only one pattern family was detected")

    if not findings:
        confidence -= 10
        reasons.append("no configured pattern matches; absence of matches is not proof of human authorship")

    confidence = max(0, min(100, confidence))
    level = "high" if confidence >= 75 else "medium" if confidence >= 45 else "low"
    return {
        "level": level,
        "score": confidence,
        "word_count": total_words,
        "sentence_count": total_sentences,
        "pattern_family_count": len(pattern_families),
        "reasons": reasons,
    }


def dedupe_findings(findings: list[Finding]) -> list[Finding]:
    deduped: list[Finding] = []
    seen: set[tuple[str, int, str, str, str]] = set()
    for finding in findings:
        key = (
            finding.path,
            finding.line,
            finding.priority,
            finding.category,
            finding.match.lower(),
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(finding)
    return deduped


def score_label(score: int) -> str:
    if score <= 3:
        return "ignore unless a hard artifact is present"
    if score <= 8:
        return "light edit"
    if score <= 15:
        return "targeted rewrite"
    return "full human edit plus source/fact check"


def escape_md(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def stacked_pattern_summaries(findings: list[Finding]) -> list[str]:
    span_findings = sorted(
        [finding for finding in findings if finding.start and finding.end],
        key=lambda finding: (finding.line, finding.start, finding.end, finding.category),
    )
    summaries: list[str] = []
    idx = 0
    while idx < len(span_findings):
        cluster = [span_findings[idx]]
        idx += 1
        while idx < len(span_findings) and any(findings_overlap(span_findings[idx], existing) for existing in cluster):
            cluster.append(span_findings[idx])
            idx += 1
        if len(cluster) <= 1:
            continue
        categories = ", ".join(sorted({finding.category for finding in cluster}))
        match = max(cluster, key=lambda finding: len(finding.match)).match
        summaries.append(f"line {cluster[0].line}: `{match}` combines {categories}")
    return summaries


def group_findings_by_paragraph(
    all_findings: list[Finding],
    paragraphs_by_path: dict[str, list[ParagraphBlock]],
    min_score: int,
) -> list[ParagraphFindingGroup]:
    findings_by_path = defaultdict_findings(all_findings)
    groups: list[ParagraphFindingGroup] = []
    for path, paragraphs in paragraphs_by_path.items():
        file_findings = findings_by_path.get(path, [])
        for paragraph in paragraphs:
            paragraph_findings = [
                finding
                for finding in file_findings
                if paragraph.start_line <= finding.line <= paragraph.end_line
                and finding.rule_id not in FILE_LEVEL_RULE_IDS
            ]
            score = score_findings(paragraph_findings)
            if score < min_score:
                continue
            priorities = Counter(f.priority for f in paragraph_findings)
            categories = Counter(f.category for f in paragraph_findings)
            edit_directions = []
            seen_edits = set()
            for finding in sorted(paragraph_findings, key=lambda f: (priority_sort_key(f.priority), -f.weight, f.rule_id)):
                if finding.edit not in seen_edits:
                    seen_edits.add(finding.edit)
                    edit_directions.append(finding.edit)
            groups.append(
                ParagraphFindingGroup(
                    path=path,
                    index=paragraph.index,
                    start_line=paragraph.start_line,
                    end_line=paragraph.end_line,
                    score=score,
                    priorities=dict(priorities),
                    categories=dict(categories),
                    excerpt=short_context(paragraph.text, 900),
                    edit_directions=edit_directions[:6],
                    stacked_patterns=stacked_pattern_summaries(paragraph_findings)[:6],
                    findings=sorted(paragraph_findings, key=lambda f: (priority_sort_key(f.priority), -f.weight, f.line, f.rule_id)),
                )
            )
    groups.sort(
        key=lambda group: (
            -(group.priorities.get("P0", 0)),
            -(group.priorities.get("P1", 0)),
            -group.score,
            group.path,
            group.start_line,
        )
    )
    return groups


def paragraph_review_hints(findings: list[Finding]) -> list[str]:
    categories = []
    seen = set()
    for finding in sorted(findings, key=lambda f: (priority_sort_key(f.priority), -f.weight, f.category)):
        if finding.category in seen:
            continue
        seen.add(finding.category)
        categories.append(f"{finding.priority} {finding.category}")
    return categories[:8]


def compendium_paragraph_cards(
    all_findings: list[Finding],
    paragraphs_by_path: dict[str, list[ParagraphBlock]],
    top: int,
    min_words: int = 20,
) -> list[dict[str, object]]:
    findings_by_path = defaultdict_findings(all_findings)
    cards: list[dict[str, object]] = []
    for path, paragraphs in paragraphs_by_path.items():
        file_findings = findings_by_path.get(path, [])
        for paragraph in paragraphs:
            words = word_tokens(paragraph.text)
            if len(words) < min_words:
                continue
            paragraph_findings = [
                finding
                for finding in file_findings
                if paragraph.start_line <= finding.line <= paragraph.end_line
                and finding.rule_id not in FILE_LEVEL_RULE_IDS
            ]
            priorities = Counter(f.priority for f in paragraph_findings)
            categories = Counter(f.category for f in paragraph_findings)
            score = score_findings(paragraph_findings)
            cards.append(
                {
                    "path": path,
                    "paragraph": paragraph.index,
                    "start_line": paragraph.start_line,
                    "end_line": paragraph.end_line,
                    "word_count": len(words),
                    "score": score,
                    "priorities": dict(priorities),
                    "categories": dict(categories),
                    "deterministic_hints": paragraph_review_hints(paragraph_findings),
                    "stacked_patterns": stacked_pattern_summaries(paragraph_findings)[:6],
                    "excerpt": short_context(paragraph.text, 1000),
                }
            )
    cards.sort(
        key=lambda card: (
            -int(card["priorities"].get("P0", 0)),
            -int(card["priorities"].get("P1", 0)),
            -int(card["score"]),
            str(card["path"]),
            int(card["start_line"]),
        )
    )
    return cards[:top]


def compendium_reference_stats(path: Path = DEFAULT_COMPENDIUM_PATH) -> dict[str, int | str]:
    stats: dict[str, int | str] = {
        "path": str(path),
        "loaded": "false",
        "lines": 0,
        "section_headings": 0,
        "inline_code_examples": 0,
        "backtick_bullet_examples": 0,
    }
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        stats["error"] = str(exc)
        return stats
    stats["loaded"] = "true"
    stats["lines"] = len(text.splitlines())
    stats["section_headings"] = len(re.findall(r"(?m)^#{2,3}\s+", text))
    stats["inline_code_examples"] = len(re.findall(r"`[^`\n]{2,160}`", text))
    stats["backtick_bullet_examples"] = len(re.findall(r"(?m)^-\s+`", text))
    return stats


def defaultdict_findings(findings: list[Finding]) -> dict[str, list[Finding]]:
    grouped: dict[str, list[Finding]] = {}
    for finding in findings:
        grouped.setdefault(finding.path, []).append(finding)
    return grouped


def render_markdown(
    all_findings: list[Finding],
    metrics_by_path: dict[str, dict[str, float | int | None]],
    top: int,
    rulebook_metadata: dict[str, str] | None = None,
    gate: str = "none",
) -> str:
    sorted_findings = sorted(
        all_findings,
        key=lambda f: (priority_sort_key(f.priority), -f.weight, f.path, f.line, f.rule_id),
    )
    score = score_findings(all_findings)
    components = score_components(all_findings)
    counts = Counter(f.priority for f in all_findings)
    cats = Counter(f.category for f in all_findings)
    gate_info = gate_summary(all_findings, gate)
    reliability = reliability_summary(all_findings, metrics_by_path)

    lines: list[str] = []
    lines.append("# AI Slop Lint Report")
    lines.append("")
    lines.append("This is a style-lint report, not proof of AI authorship.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Weighted score: `{score}` ({score_label(score)})")
    component_text = ", ".join(f"{key}={value}" for key, value in components.items() if value)
    if component_text:
        lines.append(f"- Score components: {component_text}")
    lines.append(f"- Findings: `{len(all_findings)}` total; P0 `{counts.get('P0', 0)}`, P1 `{counts.get('P1', 0)}`, P2 `{counts.get('P2', 0)}`")
    if gate != "none":
        status = "PASS" if gate_info["passed"] else "FAIL"
        lines.append(f"- Gate `{gate}`: `{status}` with `{gate_info['actionable_count']}` actionable findings, score `{gate_info['actionable_score']}`")
    lines.append(f"- Reliability: `{reliability['level']}` (`{reliability['score']}`/100)")
    if rulebook_metadata:
        rulebook_status = "loaded" if rulebook_metadata.get("loaded") == "true" else "not loaded"
        lines.append(f"- Rulebook: `{rulebook_status}` `{rulebook_metadata.get('path', '')}` version `{rulebook_metadata.get('version', 'n/a')}`")
    if cats:
        top_cats = ", ".join(f"{cat}={count}" for cat, count in cats.most_common(8))
        lines.append(f"- Main categories: {top_cats}")
    lines.append("")
    lines.append("## Metrics")
    lines.append("")
    for path, metrics in metrics_by_path.items():
        metric_text = ", ".join(f"{key}={value}" for key, value in metrics.items())
        lines.append(f"- `{path}`: {metric_text}")
    lines.append("")
    lines.append(f"## Top Findings ({min(top, len(sorted_findings))} of {len(sorted_findings)})")
    lines.append("")
    if not sorted_findings:
        lines.append("No configured AI-style lint findings were detected.")
    else:
        lines.append("| Pri | Location | Category | Match | Why | Edit |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for finding in sorted_findings[:top]:
            loc = f"{finding.path}:{finding.line}"
            lines.append(
                "| "
                + " | ".join(
                    [
                        escape_md(finding.priority),
                        escape_md(loc),
                        escape_md(finding.category),
                        "`" + escape_md(finding.match) + "`",
                        escape_md(finding.why),
                        escape_md(finding.edit),
                    ]
                )
                + " |"
            )
    lines.append("")
    lines.append("## Rewrite Priorities")
    lines.append("")
    lines.append("1. Delete hard artifacts and verify nearby claims or citations.")
    lines.append("2. Replace vague significance, promotional language, and unnamed authority with concrete facts or named sources.")
    lines.append("3. Simplify formulaic sentence templates and tacked-on analysis clauses.")
    lines.append("4. Treat vocabulary hits as density evidence; keep precise technical terms.")
    return "\n".join(lines)


def render_paragraph_markdown(
    all_findings: list[Finding],
    metrics_by_path: dict[str, dict[str, float | int | None]],
    paragraphs_by_path: dict[str, list[ParagraphBlock]],
    top: int,
    min_score: int,
    rulebook_metadata: dict[str, str] | None = None,
    gate: str = "none",
) -> str:
    groups = group_findings_by_paragraph(all_findings, paragraphs_by_path, min_score)
    score = score_findings(all_findings)
    components = score_components(all_findings)
    counts = Counter(f.priority for f in all_findings)
    gate_info = gate_summary(all_findings, gate)
    reliability = reliability_summary(all_findings, metrics_by_path)
    lines: list[str] = []
    lines.append("# AI Slop Paragraph Report")
    lines.append("")
    lines.append("This is a style-lint report, not proof of AI authorship. Use it to rewrite paragraph by paragraph, then rerun the scanner.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Weighted file score: `{score}` ({score_label(score)})")
    component_text = ", ".join(f"{key}={value}" for key, value in components.items() if value)
    if component_text:
        lines.append(f"- Score components: {component_text}")
    lines.append(f"- Findings: `{len(all_findings)}` total; P0 `{counts.get('P0', 0)}`, P1 `{counts.get('P1', 0)}`, P2 `{counts.get('P2', 0)}`")
    lines.append(f"- Flagged paragraphs at score >= {min_score}: `{len(groups)}`")
    if gate != "none":
        status = "PASS" if gate_info["passed"] else "FAIL"
        lines.append(f"- Gate `{gate}`: `{status}` with `{gate_info['actionable_count']}` actionable findings, score `{gate_info['actionable_score']}`")
    lines.append(f"- Reliability: `{reliability['level']}` (`{reliability['score']}`/100)")
    if rulebook_metadata:
        rulebook_status = "loaded" if rulebook_metadata.get("loaded") == "true" else "not loaded"
        lines.append(f"- Rulebook: `{rulebook_status}` `{rulebook_metadata.get('path', '')}` version `{rulebook_metadata.get('version', 'n/a')}`")
    lines.append("")
    lines.append("## Metrics")
    lines.append("")
    for path, metrics in metrics_by_path.items():
        metric_text = ", ".join(f"{key}={value}" for key, value in metrics.items())
        lines.append(f"- `{path}`: {metric_text}")
    lines.append("")
    lines.append(f"## Paragraph Queue ({min(top, len(groups))} of {len(groups)})")
    lines.append("")
    if not groups:
        lines.append("No paragraphs met the configured paragraph score threshold.")
        return "\n".join(lines)

    for group in groups[:top]:
        location = f"{group.path}:{group.start_line}"
        if group.end_line != group.start_line:
            location = f"{group.path}:{group.start_line}-{group.end_line}"
        lines.append(f"### Paragraph {group.index}: `{location}`")
        priority_bits = ", ".join(f"{priority}={count}" for priority, count in sorted(group.priorities.items()))
        category_bits = ", ".join(f"{category}={count}" for category, count in Counter(group.categories).most_common(6))
        lines.append("")
        lines.append(f"- Score: `{group.score}`; priorities: {priority_bits or 'none'}")
        lines.append(f"- Pattern families: {category_bits or 'none'}")
        lines.append("")
        lines.append("Original excerpt:")
        lines.append("")
        lines.append("> " + escape_md(group.excerpt))
        lines.append("")
        lines.append("Matched fragments:")
        for finding in group.findings[:12]:
            lines.append(f"- {finding.priority} `{escape_md(finding.match)}` ({escape_md(finding.category)}): {escape_md(finding.why)}")
        if group.stacked_patterns:
            lines.append("")
            lines.append("Stacked pattern clusters:")
            for summary in group.stacked_patterns:
                lines.append(f"- {escape_md(summary)}")
        lines.append("")
        lines.append("Edit directions:")
        for direction in group.edit_directions:
            lines.append(f"- {escape_md(direction)}")
        lines.append("")
        lines.append("Proposed rewrite slot:")
        lines.append("")
        lines.append("> Replace this paragraph only if the edit preserves the author's claim, evidence, citations, and technical meaning.")
        lines.append("")
    lines.append("## Iteration Stop Rule")
    lines.append("")
    lines.append("Rerun after each patch. Continue while the gate fails. Stop only when the gate passes, or when all remaining matches are explicitly documented false positives such as precise technical terms, quotations, or required house style.")
    return "\n".join(lines)


def render_compendium_markdown(
    all_findings: list[Finding],
    metrics_by_path: dict[str, dict[str, float | int | None]],
    paragraphs_by_path: dict[str, list[ParagraphBlock]],
    top: int,
    rulebook_metadata: dict[str, str] | None = None,
    gate: str = "none",
) -> str:
    cards = compendium_paragraph_cards(all_findings, paragraphs_by_path, top)
    gate_info = gate_summary(all_findings, gate)
    reliability = reliability_summary(all_findings, metrics_by_path)
    compendium_stats = compendium_reference_stats()
    lines: list[str] = []
    lines.append("# ChatGPT Compendium Review Packet")
    lines.append("")
    lines.append("This packet is for semantic review against the compendium. Deterministic matches are hints, not the standard of review. Flag passages that perform the same ChatGPT-style move even when the wording is different.")
    lines.append("")
    lines.append("## Review Standard")
    lines.append("")
    lines.append("- Do not treat this as proof of AI authorship.")
    lines.append("- Do not limit review to exact strings or regex hits.")
    lines.append("- Compare each paragraph to the full compendium by function, sentence shape, cadence, and specificity.")
    lines.append("- The rulebook and deterministic hits are a distilled index; the full compendium is the source of examples and pattern families.")
    lines.append("- A strong finding should name the family, quote a short fragment, explain the similarity, and suggest a concrete edit.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Candidate paragraphs: `{len(cards)}`")
    lines.append(f"- Reliability: `{reliability['level']}` (`{reliability['score']}`/100)")
    if gate != "none":
        status = "PASS" if gate_info["passed"] else "FAIL"
        lines.append(f"- Deterministic gate `{gate}`: `{status}` with `{gate_info['actionable_count']}` actionable findings")
    if rulebook_metadata:
        rulebook_status = "loaded" if rulebook_metadata.get("loaded") == "true" else "not loaded"
        lines.append(f"- Rulebook: `{rulebook_status}` `{rulebook_metadata.get('path', '')}` version `{rulebook_metadata.get('version', 'n/a')}`")
    compendium_status = "loaded" if compendium_stats.get("loaded") == "true" else "not loaded"
    lines.append(
        "- Full compendium: "
        f"`{compendium_status}` `{compendium_stats.get('path', '')}`; "
        f"lines `{compendium_stats.get('lines', 0)}`, "
        f"section headings `{compendium_stats.get('section_headings', 0)}`, "
        f"inline examples `{compendium_stats.get('inline_code_examples', 0)}`"
    )
    lines.append("- Packet scope: paragraph queue plus review prompts. It intentionally does not print every compendium example.")
    lines.append("")
    lines.append("## ChatGPT-Focused Families")
    lines.append("")
    for item in CHATGPT_COMPENDIUM_FAMILIES:
        lines.append(f"- **{escape_md(item['family'])}**: {escape_md(item['flag_when_similar'])}")
    lines.append("")
    lines.append("## Paragraph Review Queue")
    lines.append("")
    if not cards:
        lines.append("No paragraphs met the minimum length for compendium review.")
    for card in cards:
        location = f"{card['path']}:{card['start_line']}"
        if card["end_line"] != card["start_line"]:
            location = f"{card['path']}:{card['start_line']}-{card['end_line']}"
        lines.append(f"### Paragraph {card['paragraph']}: `{location}`")
        lines.append("")
        hints = card["deterministic_hints"]
        lines.append(f"- Deterministic hint score: `{card['score']}`")
        lines.append(f"- Hints from scanner: {', '.join(hints) if hints else 'none; review semantically against the full compendium'}")
        if card["stacked_patterns"]:
            lines.append(f"- Stacked exact-pattern hints: {'; '.join(str(item) for item in card['stacked_patterns'])}")
        lines.append("")
        lines.append("Text:")
        lines.append("")
        lines.append("> " + escape_md(str(card["excerpt"])))
        lines.append("")
        lines.append("Semantic review prompts:")
        for item in CHATGPT_COMPENDIUM_FAMILIES:
            lines.append(f"- {escape_md(item['review_question'])}")
        lines.append("")
        lines.append("Reviewer output slot:")
        lines.append("")
        lines.append("- Finding: `<family or none>`")
        lines.append("- Evidence: `<short fragment>`")
        lines.append("- Why similar to compendium: `<function/shape/cadence, not just word match>`")
        lines.append("- Edit: `<delete, simplify, source, or rewrite concretely>`")
        lines.append("")
    return "\n".join(lines)


def render_json(
    all_findings: list[Finding],
    metrics_by_path: dict[str, dict[str, float | int | None]],
    paragraphs_by_path: dict[str, list[ParagraphBlock]] | None = None,
    min_score: int = 1,
    rulebook_metadata: dict[str, str] | None = None,
    gate: str = "none",
    include_compendium_review: bool = False,
    top: int = 80,
) -> str:
    gate_info = gate_summary(all_findings, gate)
    reliability = reliability_summary(all_findings, metrics_by_path)
    payload = {
        "warning": "style lint, not proof of AI authorship",
        "score": score_findings(all_findings),
        "score_label": score_label(score_findings(all_findings)),
        "score_components": score_components(all_findings),
        "gate": gate_info,
        "reliability": reliability,
        "rulebook": rulebook_metadata or {},
        "metrics": metrics_by_path,
        "findings": [dataclasses.asdict(f) for f in all_findings],
        "actionable_findings": [dataclasses.asdict(f) for f in actionable_findings(all_findings, gate)],
    }
    if paragraphs_by_path is not None:
        payload["paragraphs"] = [
            dataclasses.asdict(group)
            for group in group_findings_by_paragraph(all_findings, paragraphs_by_path, min_score)
        ]
    if include_compendium_review and paragraphs_by_path is not None:
        payload["compendium_review"] = {
            "warning": "semantic review packet; deterministic matches are hints, not the limit of review",
            "full_compendium": compendium_reference_stats(),
            "families": CHATGPT_COMPENDIUM_FAMILIES,
            "paragraphs": compendium_paragraph_cards(all_findings, paragraphs_by_path, top),
        }
    return json.dumps(payload, indent=2, sort_keys=True)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit prose files for LLM-style writing patterns.")
    parser.add_argument("paths", nargs="+", help="Files or folders to scan.")
    parser.add_argument(
        "--context",
        choices=["general", "academic", "referee", "wiki", "technical", "executive", "social", "creative"],
        default="general",
        help="Genre profile for density thresholds. Use academic for papers and referee for referee reports.",
    )
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format.")
    parser.add_argument(
        "--mode",
        choices=["findings", "paragraphs", "compendium"],
        default="findings",
        help="Use paragraphs mode for rewrite targets; compendium mode creates a ChatGPT-focused semantic review packet.",
    )
    parser.add_argument(
        "--min-paragraph-score",
        type=int,
        default=1,
        help="Minimum paragraph score to include in paragraphs mode.",
    )
    parser.add_argument(
        "--rulebook",
        default=str(DEFAULT_RULEBOOK_PATH),
        help="Machine-readable compendium rulebook JSON. Defaults to references/rulebook.json.",
    )
    parser.add_argument(
        "--no-rulebook",
        action="store_true",
        help="Use only the scanner's built-in fallback rules.",
    )
    parser.add_argument(
        "--gate",
        choices=["none", "actionable", "strict-compendium"],
        default="none",
        help=(
            "Pass/fail mode for iterative cleanup. 'actionable' fails on P0/P1 plus explicit blocking P2 "
            "density/formatting findings. 'strict-compendium' also fails on most P2 compendium phrase/regex "
            "matches, while leaving single soft vocabulary, file metrics, and statistical-review prompts nonblocking."
        ),
    )
    parser.add_argument("--top", type=int, default=80, help="Maximum findings to print in markdown output.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    paths = expand_paths(args.paths)
    if not paths:
        print("No readable files found.", file=sys.stderr)
        return 2

    rules = list(ALL_RULES)
    tier1_terms = dict(TIER1_TERMS)
    tier2_terms = set(TIER2_TERMS)
    academic_cluster = set(ACADEMIC_CLUSTER)
    tier3_phrases = set(TIER3_PHRASES)
    rulebook_metadata = {"loaded": "false", "path": "", "version": "n/a", "derived_from": ""}
    if not args.no_rulebook:
        rulebook_rules, rulebook_tier1, rulebook_tier2, rulebook_academic, rulebook_tier3_phrases, rulebook_metadata = load_rulebook(Path(args.rulebook).expanduser())
        rules.extend(rulebook_rules)
        tier1_terms.update(rulebook_tier1)
        tier2_terms.update(rulebook_tier2)
        academic_cluster.update(rulebook_academic)
        tier3_phrases.update(rulebook_tier3_phrases)
    compiled_rules = compile_rules(rules)

    all_findings: list[Finding] = []
    metrics_by_path: dict[str, dict[str, float | int | None]] = {}
    paragraphs_by_path: dict[str, list[ParagraphBlock]] = {}
    for path in paths:
        findings, metrics, paragraphs = scan_file(path, args.context, compiled_rules, tier1_terms, tier2_terms, academic_cluster, tier3_phrases)
        all_findings.extend(findings)
        metrics_by_path[str(path)] = metrics
        paragraphs_by_path[str(path)] = paragraphs

    all_findings = dedupe_findings(all_findings)
    all_findings = sorted(all_findings, key=lambda f: (priority_sort_key(f.priority), -f.weight, f.path, f.line, f.rule_id))
    if args.format == "json":
        if args.mode == "paragraphs":
            print(render_json(all_findings, metrics_by_path, paragraphs_by_path, args.min_paragraph_score, rulebook_metadata, args.gate))
        elif args.mode == "compendium":
            print(render_json(all_findings, metrics_by_path, paragraphs_by_path, args.min_paragraph_score, rulebook_metadata, args.gate, True, args.top))
        else:
            print(render_json(all_findings, metrics_by_path, rulebook_metadata=rulebook_metadata, gate=args.gate))
    elif args.mode == "paragraphs":
        print(render_paragraph_markdown(all_findings, metrics_by_path, paragraphs_by_path, args.top, args.min_paragraph_score, rulebook_metadata, args.gate))
    elif args.mode == "compendium":
        print(render_compendium_markdown(all_findings, metrics_by_path, paragraphs_by_path, args.top, rulebook_metadata, args.gate))
    else:
        print(render_markdown(all_findings, metrics_by_path, args.top, rulebook_metadata, args.gate))
    if args.gate != "none" and actionable_findings(all_findings, args.gate):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
