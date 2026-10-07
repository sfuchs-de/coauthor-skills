# Visual Contract

## Priority Order

1. Existing project-wide style helper.
2. Established colors and typography in the target paper or deck.
3. The fallback conventions below.

Never introduce a second house style into an established project.

## Typography

- Let TeX typeset titles, subtitles, panel labels, captions, and source notes.
- Match plot labels to the document's TeX font. Prefer Latin Modern or the project's existing serif family for papers; use the deck's established sans family for slides.
- Use TeX math for symbols and equations. Do not imitate TeX with Unicode glyphs in plot titles.
- Use three text levels at most: axis/legend, annotation, and figure-level caption managed by TeX.
- Ensure the smallest rendered text remains legible at the final insertion size. A large standalone PNG with tiny labels is not acceptable.

## Fallback Palette

Use these only when the project has no semantic palette:

| Meaning | Color | Hex |
|---|---|---|
| Primary/baseline | blue | `#0072B2` |
| Counterfactual/reroute | orange | `#E69F00` |
| Disruption/closure/harm | vermillion | `#D55E00` |
| Secondary comparison | green | `#009E73` |
| Additional category | purple | `#7B3294` |
| Neutral/unclassified | grey | `#8C8C8C` |
| Main text | charcoal | `#263238` |
| Land | light grey | `#D9DEE2` |
| Sea | very pale blue | `#EEF6FA` |

For signed outcomes, use a diverging blue-white-red scale centered at zero. State which side is harm. For sequential magnitudes, use a perceptually uniform single-hue scale such as viridis. Do not mix categorical and continuous color semantics.

## Line and Fill Hierarchy

- Background network: thin, light grey-blue, low alpha.
- Baseline route: solid blue, medium weight.
- Counterfactual route: solid orange, medium-to-heavy weight.
- Closed area or denied edge: vermillion/red, clearly bounded; use hatching when grayscale reproduction matters.
- Country or region boundary: light neutral line subordinate to data.
- Selected observation: saturated foreground color and, where useful, a shape or line-style distinction.

## Statistical Integrity

- Label transformed scales, caps, logarithms, percentiles, and truncation directly.
- Center diverging scales at the economically meaningful null, usually zero.
- Do not use area or width encodings without stating the transformation.
- Use fixed baseline weights when comparing counterfactual compositions unless the purpose is explicitly to show reweighting.
- Show missing or unsupported observations as missing, never as zero.
