# Fuchs NBER/Cowles Slide Style

## Visual system

- Format: Beamer, 16:9.
- Standard body size: 9pt for NBER-style conference decks; 10pt only when the deck is materially shorter and less dense.
- Theme: `SimplePlus`.
- Canvas: white.
- Margins: 4 mm left and right.
- Body font: Latin Modern sans; mathematics uses the serif math theme.
- Navigation symbols: suppressed.
- Footline: dark-blue current frame and total frame count at lower right.
- Frame title: bold dark blue, `\normalsize`, followed immediately by a 0.4pt dark-blue rule.

## Semantic palette

| Object | Color | Hex/RGB |
|---|---|---|
| Structure, titles, main labels | Dark blue | `#173B63` |
| Secondary blue / links | Medium blue | `#2F5D7C` |
| Strategic exposure / traffic | Purple | `RGB(112,48,160)` |
| Geographic disruption | Brick | `RGB(206,96,72)` |
| Operational disruption | Burgundy | `#91353B` |
| Policy wedge | Teal | `RGB(0,122,114)` |
| Demand or network object | Green | `#4B8A6A` |
| Secondary text / inactive tabs | Mid-gray | `RGB(110,110,110)` |

Use color to encode economic objects, not decoration. Do not change an object's color between theory, measurement, and results.

## Typography and hierarchy

- Default body: `\footnotesize`.
- Top-level topic marker: bold, usually dark blue.
- Nested bullets: `\scriptsize`; third level only when unavoidable.
- Citations and provenance: `\scriptsize` and gray.
- No oversized titles inside compact slides.
- Avoid paragraphs. A bullet may wrap to a second line but should still express one idea.
- Use ordinary capitalization for slide titles; do not write all-caps titles.

Use the `itemize2` environment for compact lists. It provides about 5pt between items and restrained paragraph spacing. Increase whitespace around section headings and between economic blocks rather than inserting empty decorative elements.

## Titles and progress strips

Titles state the object or conclusion:

- `Traffic Does Not Predict Bypass Difficulty`
- `GE/ToT Effects Often Offset Exposure`
- `Different Shipping Lanes Matter for the U.S. and China`

Avoid titles such as `Results`, `Data`, `Model Results`, or `Additional Analysis`.

Use the progress strip only where it clarifies an internal sequence. Place it directly below the title rule. Active text is bold and semantically colored; inactive text is mid-gray. Keep labels short enough to fit on one line.

## Section dividers

Section dividers are plain, unnumbered frames with:

- small gray uppercase `Section N`;
- centered dark-blue section name;
- a short gray rule;
- no footer.

Within a long quantitative section, a lighter sub-block divider may identify `Strategic Exposure`, `Geographic Disruption`, or `Operational Disruption / Policy` without creating another formal section.

## Standard layouts

### Text and figure

- Use `[T,onlytextwidth]` columns.
- Text: 34--40 percent.
- Figure: 57--63 percent.
- Align the first baseline of both columns.
- Do not nest figures inside decorative cards.

### Two comparable figures

- Use 49/49 columns.
- Match height, crop, scale, and labeling.
- State the shared experiment above the pair.
- Put the comparative result below the pair.

### Equation slide

- Define notation before or next to first use.
- Center display equations.
- Use underbraces only for economically meaningful components.
- Introduce equations in logical sequence, with prose between distinct steps.
- Color exposure, disruption, and incidence terms consistently.

### Results slide

Use `\resultlabel{Experiment}` and `\resultlabel{Results}`. The experiment specifies the shock, comparison, unit, and equilibrium response. Results report magnitudes and economic interpretation rather than narrating every graphical element.

### Stylized-fact box

Use a very light gray fill, thin gray border, 2pt corners, and one sentence. Place it at the bottom of the relevant text column or below the relevant figure. Do not stretch it across the slide when it belongs to only one panel.

## Figures

- Prefer `tabfig_2` before `tabfig` when both exist.
- Use explicit width and maximum height with `keepaspectratio`.
- Remove internal titles and embedded footnotes from slide-ready exports.
- Keep source/scope notes in Beamer text through `\figleg`.
- State sign conventions and units directly.
- For maps, preserve geographic extent, avoid clipped continents, and use the same projection across comparisons.
- For tables, use `booktabs`, limited precision, and emphasis on headline cells rather than shaded grids.

## Reveals

- Reveal the setup or experiment before the map or result.
- Introduce bullets one at a time only when the spoken explanation genuinely follows that sequence.
- Show tightly related experiment bullets together.
- Hold the figure's bounding box fixed across overlays.
- Literature slides normally appear all at once.

## Backup navigation

- Main slides link from the lower-left corner with `Backup:` followed by short descriptive labels.
- Backup slides are unnumbered.
- Every backup slide has `Roadmap`, a contextual `Back` link, and optional adjacent technical links.
- Link labels should describe the destination (`Routing proof`, `Fee accounting`), not say `More` or `Details`.

## Prohibited patterns

- Generic marketing language or AI-style summaries.
- Repeated gray commentary that merely narrates the slide.
- Multiple unrelated palettes.
- Tiny explanatory prose under already dense figures.
- Internal chart titles that repeat frame titles.
- Cards inside cards or boxed page sections.
- A figure shown before its experiment without a deliberate motivating purpose.
- Shrinking text to rescue an overfilled slide.
