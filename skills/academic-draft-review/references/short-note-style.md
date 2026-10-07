# Short-Note TeX Style

## Contents

- Purpose and preamble
- Theorem, equation, list, and algorithm formatting
- Notation, appendix placement, and build standard

## Purpose

Use this style for short academic notes aimed at applied economists or related technical
readers. The note should read as a coherent argument, not as a derivation dump. Main text
should emphasize problem, object, regression/procedure, test/result, and intuition. Proofs,
notation tables, fragile qualifications, and implementation edge cases belong in appendices.

## Preamble

Prefer a simple `article` layout with:

```tex
\documentclass[11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[margin=1in]{geometry}
\usepackage{microtype}
\usepackage{setspace}
\setstretch{1.15}
\usepackage{amsmath,amssymb,amsthm,amsfonts,mathtools}
\usepackage{bm}
\usepackage{booktabs}
\usepackage{array}
\usepackage{graphicx}
\usepackage[font=small,labelfont=bf]{caption}
\usepackage{xcolor}
\usepackage{url}
\usepackage{titlesec}
\usepackage{hyperref}
\usepackage{cleveref}
```

Use black internal links and blue URLs unless a project style file overrides this:

```tex
\hypersetup{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=blue}
```

Use compact section styling:

```tex
\titleformat{\section}{\large\bfseries}{\thesection.}{0.5em}{}
\titleformat{\subsection}{\normalsize\bfseries}{\thesubsection.}{0.5em}{}
\titleformat{\subsubsection}{\normalsize\itshape}{\thesubsubsection.}{0.5em}{}
\titlespacing*{\section}{0pt}{1.2em plus 0.3em minus 0.1em}{0.8em}
\titlespacing*{\subsection}{0pt}{1em plus 0.2em minus 0.1em}{0.5em}
\titlespacing*{\subsubsection}{0pt}{0.8em plus 0.2em minus 0.1em}{0.4em}
```

Do not add heavy layout packages unless the local document already depends on them.

## Theorem And Equation Style

Number equations by section when the note has multiple sections:

```tex
\numberwithin{equation}{section}
```

Use theorem environments sparingly and precisely. Before a major formula or proposition,
add one or two prose sentences explaining what the object does empirically or conceptually.
After the formula, summarize the applied implication before moving to proof details.

## Lists

Avoid active `itemize` and `enumerate` environments in the note. Rewrite short lists as
prose paragraphs. Convert comparison bullets into compact prose or, only when genuinely
helpful, a small table. Preserve commented-out historical drafts unless the user asks for
cleanup.

For procedural material, do not use an enumerated list. Use an algorithm box.

## Algorithm Box

Short notes should include a main-text algorithm box when a procedure is central to the
empirical or computational implementation. Define a lightweight box in the preamble:

```tex
\newcounter{algorithm}
\newsavebox{\algorithmbox}
\renewcommand{\thealgorithm}{\arabic{algorithm}}
\newenvironment{algorithmblock}[1]{%
  \refstepcounter{algorithm}%
  \par\medskip\noindent
  \begingroup
  \setlength{\fboxsep}{0.75em}%
  \setlength{\fboxrule}{0.45pt}%
  \begin{lrbox}{\algorithmbox}%
  \begin{minipage}{\dimexpr\linewidth-2\fboxsep-2\fboxrule\relax}
  \textbf{Algorithm~\thealgorithm. #1}\par\smallskip
  \small
}{%
  \end{minipage}%
  \end{lrbox}%
  \fbox{\usebox{\algorithmbox}}%
  \endgroup
  \par\medskip
}
```

The main-text algorithm should be compact: initialize, update key object, refit or iterate,
and stop. Move software details, tolerances, edge cases, and diagnostics to an appendix
algorithm or prose subsection.

## Notation

Notation tables belong in the appendix, not the main text. In the main text, introduce
symbols locally and add a sentence such as:

```tex
Appendix~\ref{app:notation} collects the notation used in the theory and estimation
sections; the main text introduces only the objects needed for each result.
```

The appendix notation table should include domains, normalizations, and distinctions between
raw and centered objects when those distinctions matter.

## Appendix Placement

Use appendices for:

- notation tables
- proof details
- derivation edge cases
- implementation details
- numerical stability details
- generated-regressor or inference qualifications

The main text should retain the minimal formal statement needed for correctness and
readability.

## Build Standard

Compile with `latexmk -pdf -interaction=nonstopmode -halt-on-error`. A completed formatting
pass should leave no undefined references, no unresolved rerun warnings, and no serious
overfull/underfull boxes. Report any remaining warning that cannot be resolved without
changing substance.
