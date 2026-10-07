# Economics Writing Use Cases and Checklist

## Contents

- Drafting and rewriting
- Introductions, literature reviews, abstracts, conclusions, results, and model sections
- Author-side reviewing and auditing
- Pre-submission checklist

Use placeholders or explicit missing-input notes when evidence is absent. Do not fabricate the
specificity requested by a checklist item.

# USE CASE INSTRUCTIONS

## When asked to DRAFT a section or full paper:
1. Determine the paper type (applied empirical, theory, mixed, structural, descriptive) and adapt accordingly
2. Follow the formulas above for the relevant section
3. Use concrete placeholder language where you need the author's specific results
4. Mark areas needing the author's input with [AUTHOR: description of what's needed]
5. Apply all style rules from the start
6. Write in the triangular/newspaper style -- most important first

## When asked to REWRITE existing text:
1. Identify specific violations of the rules above
2. Fix passive voice, vague language, throat-clearing, buried leads
3. Tighten prose -- cut unnecessary words and sentences
4. Ensure concrete results are stated with magnitudes
5. Preserve the author's meaning and contribution
6. Briefly note what you changed and why

## When asked to write an INTRODUCTION:
Apply the Introduction Formula above (Hook → Question → Results → Literature Review & Value Added → Roadmap): results at 25-30% of the intro, the literature review as the last substantive section before the roadmap, and a 3-5 page cap. See WRITING THE INTRODUCTION.

## When asked to write a LITERATURE REVIEW:
1. Place it as the last part of the introduction (before roadmap), NOT as a separate section
2. Tell a STORY, not an annotated bibliography
3. Focus on 5-10 closest papers
4. Build toward a "however" or "although" that establishes your paper's niche
5. Be generous with credit, never insulting

## When asked to write an ABSTRACT:
Apply the 4-part formula above (What / How / Findings / Implications): 100-150 words, concrete findings with magnitudes, no citations, no jargon, no passive voice. See WRITING THE ABSTRACT.

## When asked to write a CONCLUSION:
Apply the 3-part formula above (Summary / Implications / Future Research): one page, phrase findings differently from the abstract and introduction, and do not speculate beyond the data or model. Project confidence -- avoid a generic caveats dump, though a brief, specific limitations note is fine (especially for experimental/policy work). See WRITING THE CONCLUSION.

## When asked to write RESULTS:
1. Main result first -- no warmup exercises
2. Most parsimonious to least parsimonious specifications
3. Explain economic magnitude, not just statistical significance
4. Include robustness checks, mechanisms, and limitations subsections
5. Use visuals before tables for preliminary results
6. For null results: frame as informative, report confidence intervals, discuss power

## When asked to write a THEORY or MODEL section:
1. The introduction must state the main insight/mechanism in plain English within the first two paragraphs
2. Motivate with a puzzle, stylized fact, or policy question -- not with "the literature lacks a model of..."
3. Model section: state assumptions clearly, explain their economic content, and note which are essential vs. simplifying
4. Present propositions with economic intuition BEFORE the formal proof. Readers should understand the result before seeing the math
5. Use the simplest model that generates the key insight, and start from a concrete example rather than the general case (Varian)
6. Discuss comparative statics verbally: "When X increases, Y falls because..."
7. Generate testable predictions -- even if you do not test them, state what data would be needed
8. Proofs belong in the appendix unless they illuminate the economic mechanism
9. For mixed theory-empirical papers: map each regression to a specific proposition

## When asked to write a DATA SECTION:
Apply the Data Section guidance above: name the dataset, time period, and unit of observation in the first sentence; describe sample construction and variable definitions; include a summary statistics table; address limitations and sample selection in the text (not footnotes); give enough institutional background for the identification strategy. See WRITING THE DATA SECTION.

## When asked about PRESENTATIONS: use `design-econ-seminar`

## When asked to write a SURVEY or REVIEW PAPER (JEL, JEP, Handbook chapter): see [specialized-tasks.md](specialized-tasks.md)

## When asked to convert a WORKING PAPER to a JOURNAL VERSION: see [specialized-tasks.md](specialized-tasks.md)

## When asked to write a GRANT PROPOSAL (NSF, NBER, ERC, institutional): see [specialized-tasks.md](specialized-tasks.md)

## When asked to write for a NON-ACADEMIC AUDIENCE (policy brief, op-ed, blog post): see [specialized-tasks.md](specialized-tasks.md)

## When asked to REVIEW or AUDIT the author's own draft before submission:
1. Use the review checklist framework (see [review-checklist.md](review-checklist.md))
2. Provide three perspectives: Methodologist (identification, robustness), Field Expert (contribution, economic significance), Writing Critic (style, clarity)
3. Score the paper on each component (title, abstract, introduction, methodology, results, writing, tables/figures, conclusion) out of 100
4. Flag any AI-generated writing patterns (see Anti-AI section above)
5. Prioritize feedback: list the 3 most impactful changes first, then minor issues
6. For each issue, state what is wrong, why it matters, and how to fix it with a concrete example

Independent reviewer-side reports, editor notes, and revision-round judgments belong to the
`referee-report` skill, not this author-side audit.

## When asked to write a REFEREE RESPONSE: see [specialized-tasks.md](specialized-tasks.md)

---

# REVISION CHECKLIST

Before submitting, verify:
- [ ] Central contribution is stated concretely in paragraphs 1-3 of introduction
- [ ] Main results appear in the introduction with magnitudes
- [ ] No needless passive voice in prose (search for "to be" + past participle -- "was estimated", "is shown", "are reported" -- and "by"-agent phrases, NOT every "is"/"are", which also mark present tense; passive acceptable in table captions and methods)
- [ ] No throat-clearing before the main point
- [ ] Literature review tells a story, not a list
- [ ] Every table has a self-contained caption with clustering/SE specification
- [ ] Every number in tables is discussed in text
- [ ] Standard errors reported for every important number
- [ ] Identification strategy is clearly explained in economic terms
- [ ] Conclusion is under one page and projects confidence -- no generic caveats dump (a brief, specific limitations note is fine, especially for experimental/policy work)
- [ ] Abstract is under 150 words and concrete
- [ ] Paper is under 40 pages (check target journal guidelines)
- [ ] All Greek letters and notation are defined with names
- [ ] No "illustrative" empirical work
- [ ] No abbreviations of author names
- [ ] Pre-trends shown visually for DiD designs; RD plot shown for RDD designs
- [ ] Heterogeneity results are pre-specified and multiple-testing-aware
- [ ] Mechanisms section tests channels rather than speculates
- [ ] Data availability and replication information are clearly stated
- [ ] Appendix items are all referenced from the main text
- [ ] Title is under 15 words and contains the treatment and outcome (or key mechanism for theory)
- [ ] For theory papers: main propositions have clear economic intuition before formal proofs
- [ ] Descriptive statistics table included with variable definitions in notes
- [ ] All equations introduced verbally before display; all variables defined after display

---

*For identification-strategy-specific writing guidance (RCT, DiD, IV, RDD, Synthetic Control, Bunching, Shift-Share, ML), see [identification-strategies.md](identification-strategies.md).*

*For LaTeX formatting guidance (tables, figures, bibliography, journal submission), see [latex-tips.md](latex-tips.md).*

*For structured author-side paper review with simulated reviewers and scoring, see [review-checklist.md](review-checklist.md).*

*For specialized tasks (survey/review papers, working-paper-to-journal conversion, grant proposals,
policy briefs/op-eds, and referee responses), see [specialized-tasks.md](specialized-tasks.md). Use
`design-econ-seminar` for presentations.*

*This skill synthesizes advice from 50+ sources. Top sources: Cochrane (Chicago/Hoover), McCloskey (Chicago/UIC), Shapiro (Harvard), Head (UBC), Bellemare (Minnesota), Goldin & Katz (Harvard), Glaeser (Harvard), Kremer (Harvard/Chicago), Nikolov (Binghamton/Harvard), Schwabish (JEP), Evans (CGDev), Dudenhefer (Duke). Full source list: github.com/hanlulong/econ-writing-skill*
