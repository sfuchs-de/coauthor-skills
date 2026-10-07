# Maps and Route Networks

## Layer Order

Build maps in this order:

1. Sea background.
2. Land polygons.
3. Coastlines and borders.
4. Background route network or cells.
5. Traffic, exposure, or outcome layer.
6. Closures, exercise zones, or denied cells.
7. Baseline and counterfactual highlighted routes.
8. Labels, legend, and scale notes.

Never color land and sea with the same family. Verify their distinction from the rendered PDF, not only the plotting window.

## Geographic Framing

- Use one projection and geographic extent across comparable panels.
- Choose the extent to show both the intervention and economically relevant alternatives. For rerouting, include the nearest substitute corridor; do not crop away Malacca, Sunda, Lombok, or the Cape when they are part of the mechanism.
- Handle the dateline explicitly before drawing global routes.
- Remove longitude/latitude axes unless they aid interpretation.
- Use high-resolution coastlines appropriate to the final display size.

## Traffic and Routes

- Distinguish observed routes, model routes, and counterfactual routes visually and in the note.
- If line width represents traffic, use a documented monotone transformation and include interpretable reference widths.
- Use low alpha for the full network and high contrast for selected routes.
- Show the blocked geography and its route consequence in the same exhibit or in tightly linked panels.
- For before/after maps, preserve the same crop, scale, background, and legend.
- Distinguish rerouted traffic from traffic that loses network support. Do not draw disconnected traffic as if it had a finite route.

## Closures and Jurisdictions

- Draw closed cells or polygons above the background network but below route labels.
- State whether the intervention is a one-cell disruption, corridor cut, selective denial, or complete closure.
- For selective closures, state whose traffic is denied and do not visually imply a common closure.
- Describe EEZ contact as jurisdictional exposure unless the legal authority or effective control is separately established.

## Map QA

- Check that no counterfactual route crosses a prohibited cell or edge.
- Check route continuity and port endpoints.
- Check that labels do not cover the key corridor.
- Check that panel colorbars have identical limits when comparisons require them.
- Check that the map remains interpretable in grayscale and at 50 percent display size.
