---
name: remarkable-move-render
description: Render Markdown notes and scripts as minimalist PDFs sized for the reMarkable Paper Pro Move, with centered display equations, section-based page breaks, compact typography, PDF integrity checks, and optional contact-sheet QA. Use when Codex is asked to make a reMarkable Move PDF, format Markdown for a small e-ink device, increase or tune the device PDF font size, reproduce Markdown-preview styling in a PDF, or verify that a rendered notes document fits without clipping or broken equations.
---

# reMarkable Move Render

Render Markdown through Pandoc MathML and headless Chrome using the bundled Paper Pro Move stylesheet.

## Quick Start

```bash
python3 "<skill-directory>"/scripts/render_move.py \
  notes.md --output notes_move.pdf --qa-dir /tmp/notes_move_qa
```

Use `--font-size 8.8pt` for a slightly larger body font. Preserve the default unless visual QA shows excess whitespace or poor legibility.

## Workflow

1. Read the Markdown and confirm that `##` headings mark intended page starts.
2. Run `scripts/render_move.py` with an explicit output path.
3. Inspect the reported page count and PDF size.
4. Open the contact sheet when `--qa-dir` is supplied.
5. Inspect the opening, densest page, equation-heavy page, and final page at full resolution.
6. Adjust prose or font size in small increments. Do not solve overflow by making the whole document unreadably small.
7. Rerender and rerun integrity checks.

## Layout Contract

- Page size: 91.8 mm by 163.2 mm.
- Default body size: 8.55 pt with 1.33 line height.
- `##` headings start new pages; `#` is the cover heading.
- Display equations use MathML and are centered.
- Styling is monochrome, low-ink, and close to a native Markdown preview.
- Bullets are compact but visibly separated.
- Avoid decorative boxes, colored backgrounds, running headers, and generated tables of contents unless requested.

## Dependencies

The renderer requires Pandoc and a Chrome or Chromium executable. It uses `qpdf`, `pdfinfo`, and `pdftoppm` when available. Pillow is optional and is used only to assemble the contact sheet.

## QA Rules

- Treat a successful render as incomplete until the PDF is visually inspected.
- Check that equations are centered rather than merely assigned `text-align: center` inside a full-width MathML box.
- Check that a heading is not stranded at the bottom of a page.
- Check that long bullets, URLs, and inline equations do not cross the right margin.
- Check whether a dense backup section should span two pages rather than forcing a smaller global font.
- Report any unavailable validation tools instead of implying that they ran.

