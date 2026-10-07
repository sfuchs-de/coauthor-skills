# TeX and Slide Integration

## TeX Figures

- Prefer PDF exports for maps, line art, and charts.
- Remove embedded plot titles and subtitles when TeX supplies `\caption` or `\subcaption`.
- Use TeX for mathematical panel headings and subtitles.
- Keep panel letters and captions outside raster assets.
- Crop only blank margins. Never stretch an image to fill both width and height.
- Use stable panel widths and `\hfill` or a controlled grid; avoid hand-tuned offsets that break after asset updates.

Caption structure:

1. Short declarative title.
2. What each panel displays.
3. Units, sign convention, sample/scenario, transformations, and weighting.
4. Model/support status where relevant.
5. Source and construction reference.

Do not use the caption as a second results paragraph.

## Slides

- Give each slide one job and one principal exhibit.
- Use a short `Experiment`/`Results` hierarchy for quantitative slides when it aids comprehension.
- Place experiment bullets before revealing the map or result in stepped decks.
- Vertically center the complete composition, not each element independently.
- Keep figure notes minimal; move construction details to linked backup slides.
- Use direct labels and larger plot text than in papers.
- For side-by-side maps, use matching crops and scales. For stacked maps, align their plot regions exactly.
- Avoid titles inside the graphic when the slide title already names the result.

## Panel Decisions

- Combine panels when they answer one comparison and share a scale.
- Split panels when each requires a different legend, geographic extent, or reveal sequence.
- Put the main comparison in the main text and the complete scenario set in the appendix.
- Keep diagnostic plots linked but visually subordinate to headline results.
