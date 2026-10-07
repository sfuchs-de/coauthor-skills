# Charts and Tables

## General Chart Style

Use a restrained tidyverse-like presentation:

- White background.
- Charcoal text.
- No enclosing plot box unless needed for a map.
- Thin neutral axes.
- Light major gridlines only when they improve value reading.
- No minor gridlines by default.
- Legend at bottom or direct labels when space permits.
- Sentence-case labels and concise category names.

In Python, reproduce this visual logic rather than using matplotlib defaults. In R, prefer a shared `theme_econ()` derived from `theme_minimal()` or `theme_classic()`.

## Figure Types

### Scatterplots

- Label axes with object, unit, and transformation.
- Show the economically meaningful reference line when relevant.
- Use transparency for dense clouds and label only substantive outliers.
- Report sample restrictions and weighting in the note.

### Event Studies

- Mark the omitted period and event date.
- Use point estimates plus confidence intervals, not connected decorative curves alone.
- Keep pre- and post-event windows visually balanced where feasible.
- State fixed effects, treatment intensity, and clustering in the note or adjacent text.

### Decompositions

- Preserve a common sign convention and scale across components.
- Use stacked bars only when components add exactly.
- If components do not add because of a residual or nonlinear term, display that term explicitly.
- For direct versus GE/terms-of-trade maps, use matched panels and color limits when magnitudes permit; otherwise state that scales differ.

### Heatmaps

- Sort rows and columns by an economic criterion, not alphabetically by default.
- State normalization and denominator.
- Use a neutral color for missing values and distinguish them from zero.
- Avoid printing values in cells when they are unreadable at final size.

### Small Multiples

- Use one shared legend.
- Keep axes, breaks, and panel dimensions fixed.
- Put panel labels in TeX subcaptions or stable plot annotations.
- Limit each panel to one comparison.

## Tables

- Use `booktabs`: `\toprule`, `\midrule`, and `\bottomrule`; no vertical rules.
- Put units in column headers and definitions in notes.
- Align decimals and use consistent precision justified by the data.
- Bold only the result the reader should compare, not whole rows or columns.
- Report missing or unsupported values as `--` with an explanatory note.
- Separate benchmark, robustness, and diagnostic specifications visibly.
- For counterfactual tables, include the baseline, the total outcome, and the increment from the policy or response when that distinction matters.
