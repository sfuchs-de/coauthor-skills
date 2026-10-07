# BQ Design System

## Identity

This profile distills the revised McGill BQ deck, not all choices in Baqaee's presentations
and not the older Fuchs NBER format. The source is authoritative for visual precedent, not
for copying factual content. See the contact sheet and measured profile beside this file.

| Element | Default |
| --- | --- |
| Canvas | Beamer 16:9; approximately 453.54 x 255.12 PDF points; white |
| Base font | 10pt class; T1 Helvetica with `helvet` scaled .9; sans math inherited from Beamer |
| Title | `Large`, medium weight, BQBlue; left aligned; no title rule |
| Body | Normal size, black; do not shrink an entire frame to fit |
| Subitems | `small`; one useful nesting level |
| Notes and sources | `footnotesize`; keep readable at projected scale |
| Side margins | 3mm on both sides |
| Blue | RGB (.2, .2, .7), hex #3333B2 |
| Optional red | #B22C2C |
| Main item gaps | `BQList`: 18pt; `BQCompact`: 13pt; 9--12pt for equation-heavy slides |
| Subitem gaps | 5pt, top separation 3pt; no extra paragraph glue |
| Backup spacing | `BQList`: 15pt; compact: 9pt; subitems: 4pt |
| Navigation | Underlined small blue text, inline or bottom-right; contextual return |
| Excluded chrome | No header/progress strip, horizontal title rule, frame counters, rounded buttons, shadows, cards |

Use measured typography, not screenshot pixel sizes. Default Beamer math and font sizes can
vary with the toolchain; inspect the compiled reference/starter side by side when adapting.

## Page Types

**Title.** Center the actual title in blue, then equal-width author blocks. Each author gets
their own affiliation directly below, even when shared. Use two rows for many authors. Event
and date follow with breathing space. Preserve approved affiliations and disclaimers; never
add an institution from memory. The starter has three equal blocks, not fixed author names.

**Agenda.** Plain, widely spaced section names. Current section blue, remaining sections pale
blue. Use at major transitions, normally four for a full research seminar. No mini-roadmap on
every slide. Agenda headings should describe the new paper, not inherit tourism/network labels.

**Reasoning.** Claim or question title, then 2--4 steps. A parent states the operation or claim;
a child gives a reason, definition, implication, or limitation. A slide with just two substantive
points is not underfilled. Use active, literal language. Avoid unexplained coined labels.

**Derivation.** State the setup and relevant restriction, write the object being optimized or
transformed, show the key cancellation or implication, then state what this buys. Split market
clearing and the consequence into separate reveals. Do not show a matrix result before its maps
and indices are introduced. Use underbraces only when they reduce decoding effort.

**Result exhibit.** One short lead item, large figure, one or two interpretation items, concise
source/uncertainty note. On the first reveal establish the comparison or experiment. Show the
estimate before broad interpretation. Use result headlines only as strong as the evidence.

**Calibration/data.** Organize by what each source supplies: household budgets, production,
external accounts, spatial allocation, etc. Put support/sample sizes in the relevant source's
description, not a second dense summary table. Link official source names and years; identify
restricted extracts without fabricating public links. Separate data from maintained closure.

**Backup.** Self-contained question or derivation, consistent notation, source and assumptions,
and return to the calling main slide. Prefer an additional backup frame over unreadably tiny
text. Retain valuable previous diagnostics only as explicitly historical or diagnostic.

## Emphasis and Math

- Blue already encodes structure. Use bold for the crucial operation or contrast, usually a
  phrase rather than a sentence. Avoid a forest of bold labels.
- Assign an accent to an economic object, not to whatever is currently emphasized. Repeat the
  same color in prose, formulas, figure labels, and legends. Do not imply blue means observed
  and red means recovered unless that legend is explicitly adopted throughout.
- Define indices, hats, units, acronyms, and normalizations at first use. Explain the economic
  meaning of a scalar before introducing its stacked vector or matrix.
- State identities, identifying restrictions, approximations, and estimates differently. A
  baseline share is not automatically a derivative; a conditional local result is not a global
  model. Do not color away these distinctions.
- Use a box around at most the one key formula when that helps. No equation cards or banners.

## Figures, Maps, and Tables

- For an exhibit with a lead and brief interpretation, reserve about .54--.65 of `textheight`;
  a nearly figure-only frame can use .68--.73. Width usually .90--1.00 of the text region.
  These are starting dimensions, not excuses to crop data or overlap notes.
- Export tight vector figures from source; remove duplicate internal titles. Enlarge the
  plotting area, not invisible margins in an existing PDF. Keep `keepaspectratio`.
- Use fixed axes and panel geometry across overlays. A binned scatter comparing predictions
  needs named axes, matched units/sample/weights, and a one-for-one line; its fit statistics
  must describe this comparison rather than a different regression.
- For model comparisons, show levels/magnitudes as well as spatial correlation or fit. Match
  overall versus component price indices, denominators, shock, and period before plotting.
- Prefer outline histograms, consistent line weights, light horizontal guides, a labeled
  benchmark line, and a compact legend. Do not stretch a narrow histogram across the page just
  because horizontal space exists; the reference's tax histogram uses about .80 width.
- Maps need common projection, extent, units, support, and comparable color limits. A right-side
  vertical legend often permits a larger map; use it when it improves space. A right-legend
  variant is optional, not required for slides without maps. Do not change values or scales.
- For a residual/wedge, show both component measures before interpreting the difference.
  Negative residuals are not necessarily negative levels or beneficial externalities.
- Tables use `booktabs`, no vertical rules, aligned values, SEs and sample information. Show
  R-squared only when its definition and source are verified; distinguish within/adjusted fit.

## Stable Reveals and Handouts

Use `item<k->`/`uncover` to reserve space. Use `overlayarea` for replacing figures or lead text.
Avoid `pause` inside complicated nested environments. Reveal groups that make one inference,
not every sentence, symbol, or footnote separately.

For mutually exclusive states, specify which survives handout mode:

```tex
\begin{overlayarea}{\textwidth}{.58\textheight}
\only<1|handout:0>{\BQFigure{.56\textheight}{figures/baseline.pdf}}
\only<2-|handout:1>{\BQFigure{.56\textheight}{figures/full-response.pdf}}
\end{overlayarea}
```

The final state must preserve the comparisons needed to understand the whole slide. If a
sequence's earlier states are indispensable and absent from the final panel, make a dedicated
composite reading state. Do not obtain a handout by naively stacking replacement overlays.

The starter exposes `BQList`, `BQCompact`, `BQSub`, `BQLead`, `BQNote`, `BQSource`, `BQFigure`,
`backupbtn`, `BQBottomLinks`, `BQAppendix`, and `setappendixreturn`. `BQSource` does not parse
links: put footer links in the explicit `BQBottomLinks` command. This simpler interface avoids
copying the original deck's legacy macro dependencies.
