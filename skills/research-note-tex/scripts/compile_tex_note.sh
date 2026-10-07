#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  echo "Usage: compile_tex_note.sh path/to/note.tex [output-dir]" >&2
  exit 2
fi

tex_path="$1"
if [ ! -f "$tex_path" ]; then
  echo "TeX file not found: $tex_path" >&2
  exit 1
fi

tex_dir="$(cd "$(dirname "$tex_path")" && pwd)"
tex_file="$(basename "$tex_path")"
base_name="${tex_file%.tex}"

if [ "$#" -eq 2 ]; then
  out_dir="$2"
else
  out_dir="$tex_dir/build"
fi

mkdir -p "$out_dir"

if command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir="$out_dir" "$tex_path"
else
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="$out_dir" "$tex_path"
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="$out_dir" "$tex_path"
fi

pdf_path="$out_dir/$base_name.pdf"
if [ ! -f "$pdf_path" ]; then
  echo "Build completed but PDF was not found: $pdf_path" >&2
  exit 1
fi

echo "$pdf_path"
