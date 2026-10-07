# Imported Economics Presentation Guidance

This material was moved from the economics-writing reference so presentation ownership remains in
`design-econ-seminar`.

- Reach the main result early; do not begin with an extended literature review or generic preview.
- Consider result-first openings built around the central table, figure, or equation when the object
  is intelligible without excessive setup.
- Let equations, tables, and graphs carry evidence; do not write a spoken manuscript as slide bullets.
- Leave a slide visible long enough for the audience to inspect it. One slide per minute is usually
  too fast for substantive economics evidence.
- Speak clearly and at a measured pace, and hear a question fully before answering it.

These are heuristics associated with the economics-writing sources summarized in `econ-write`, not
universal presentation rules. Adapt them to the audience, interruption norm, and format.

## Beamer implementation lead

When the project has no stronger local convention, a minimal starting point is:

```latex
\documentclass{beamer}
\usetheme{metropolis}
\setbeamertemplate{navigation symbols}{}
```

Use `\pause` sparingly. Put backup frames after `\appendix`, label them clearly, and connect relevant
main slides with explicit `\hyperlink{backup1}{\beamerbutton{Detail}}` buttons. Preserve an existing
theme and navigation system rather than imposing this example on an established deck.
