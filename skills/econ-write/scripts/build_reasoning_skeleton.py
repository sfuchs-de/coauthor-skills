#!/usr/bin/env python3
r"""Build a deterministic structural skeleton for an academic manuscript.

The script creates nodes and structural edges (containment and sequence). It does
not decide whether the reasoning is good. The `econ-write` author-audit workflow
should enrich the output with semantic roles, logical dependencies, weak edges,
and repairs through close reading.

Supported inputs: .tex, .md/.markdown, .txt, .docx, and .pdf (when pdftotext is
available). LaTeX \input and \include directives are followed recursively.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Iterator, Optional
from xml.etree import ElementTree as ET


HEADING_LEVELS = {
    "part": 1,
    "chapter": 1,
    "section": 1,
    "subsection": 2,
    "subsubsection": 3,
    "paragraph": 4,
    "subparagraph": 5,
}

LATEX_HEADING_RE = re.compile(
    r"^\s*\\(?P<kind>part|chapter|section|subsection|subsubsection|paragraph|subparagraph)\*?\s*\{(?P<title>.+?)\}\s*(?:%.*)?$"
)
MARKDOWN_HEADING_RE = re.compile(r"^(?P<marks>#{1,6})\s+(?P<title>.+?)\s*$")
LATEX_INCLUDE_RE = re.compile(r"\\(?:input|include)\s*\{([^}]+)\}")
LATEX_BEGIN_RE = re.compile(r"\\begin\{([^}]+)\}")
LATEX_END_TEMPLATE = r"\\end\{%s\}"

FORMAL_ENV_KIND = {
    "equation": "equation",
    "equation*": "equation",
    "align": "equation",
    "align*": "equation",
    "aligned": "equation",
    "gather": "equation",
    "gather*": "equation",
    "multline": "equation",
    "multline*": "equation",
    "displaymath": "equation",
    "definition": "definition",
    "assumption": "assumption",
    "lemma": "lemma",
    "proposition": "proposition",
    "theorem": "theorem",
    "corollary": "corollary",
    "proof": "proof",
    "figure": "figure",
    "figure*": "figure",
    "table": "table",
    "table*": "table",
    "algorithm": "algorithm",
    "algorithm*": "algorithm",
}

ROLE_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("definition", re.compile(r"^(let|define|denote|write|call)\b", re.I)),
    ("assumption", re.compile(r"^(assume|suppose|maintain|impose)\b", re.I)),
    ("motivation", re.compile(r"^(to understand|to motivate|the problem|the remaining question|why)\b", re.I)),
    ("derivation", re.compile(r"^(substitut|differentiat|log-linear|premultip|aggregat|rearrang|combining|applying)\w*\b", re.I)),
    ("interpretation", re.compile(r"^(economically|intuitively|the intuition|this means|the first term|the second term)\b", re.I)),
    ("qualification", re.compile(r"^(however|nevertheless|nonetheless|the qualification|this interpretation requires|under)\b", re.I)),
    ("comparison", re.compile(r"^(by contrast|in contrast|relative to|compared with|whereas)\b", re.I)),
    ("evidence", re.compile(r"^(figure|table|the data|the estimates|the results)\b", re.I)),
    ("estimation", re.compile(r"^(we estimate|the regression|our empirical design|identification)\b", re.I)),
    ("transition", re.compile(r"^(we next|next,|the next section|having established|this section now)\b", re.I)),
    ("conclusion", re.compile(r"^(therefore|thus|hence|in sum|in summary|taken together)\b", re.I)),
    ("roadmap", re.compile(r"^(this section|we proceed|the remainder|the rest of)\b", re.I)),
]

ABBREVIATIONS = {
    "e.g.", "i.e.", "et al.", "fig.", "eq.", "prop.", "sec.", "app.",
    "dr.", "mr.", "ms.", "prof.", "vs.", "no.", "pp.", "p.", "cf.",
}


@dataclass
class SourceLine:
    text: str
    file: str
    line: int


@dataclass
class Node:
    id: str
    parent_id: str
    level: str
    order: int
    file: str
    start_line: int
    end_line: int
    title: str
    text: str
    surface_role: str
    semantic_role: str = ""
    inherits: str = ""
    advance: str = ""
    yield_text: str = ""
    flags: str = ""


@dataclass
class Edge:
    source: str
    target: str
    edge_class: str
    relation: str
    explicitness: str = "explicit"
    evidence: str = ""
    strength: str = ""
    issue: str = ""
    repair: str = ""


def strip_latex_comment(line: str) -> str:
    out: list[str] = []
    escaped = False
    for ch in line:
        if ch == "%" and not escaped:
            break
        out.append(ch)
        if ch == "\\" and not escaped:
            escaped = True
        else:
            escaped = False
    return "".join(out)


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def latex_title(text: str) -> str:
    text = re.sub(r"\\label\{[^}]+\}", "", text)
    text = re.sub(r"\\[a-zA-Z@]+\*?(?:\[[^]]*\])?\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"[{}]", "", text)
    return normalize_space(text)


def read_latex(path: Path, seen: Optional[set[Path]] = None) -> list[SourceLine]:
    if seen is None:
        seen = set()
    path = path.resolve()
    if path in seen:
        return []
    if not path.exists():
        raise FileNotFoundError(path)
    seen.add(path)
    result: list[SourceLine] = []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    for idx, raw in enumerate(lines, start=1):
        clean = strip_latex_comment(raw)
        match = LATEX_INCLUDE_RE.search(clean)
        # Follow a simple include even when surrounding whitespace or a trailing label exists.
        if match:
            target = match.group(1).strip()
            candidate = (path.parent / target)
            if candidate.suffix == "":
                candidate = candidate.with_suffix(".tex")
            if candidate.exists():
                prefix = clean[: match.start()].strip()
                suffix = clean[match.end() :].strip()
                if prefix:
                    result.append(SourceLine(prefix, str(path), idx))
                result.extend(read_latex(candidate, seen))
                if suffix:
                    result.append(SourceLine(suffix, str(path), idx))
                continue
        result.append(SourceLine(clean, str(path), idx))
    return result


def read_plain(path: Path) -> list[SourceLine]:
    return [
        SourceLine(line, str(path.resolve()), idx)
        for idx, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1)
    ]


def read_pdf(path: Path) -> list[SourceLine]:
    executable = shutil.which("pdftotext")
    if not executable:
        raise RuntimeError("PDF input requires the `pdftotext` executable. Use editable source or extract text first.")
    with tempfile.TemporaryDirectory() as temp_dir:
        output = Path(temp_dir) / "manuscript.txt"
        subprocess.run([executable, "-layout", str(path), str(output)], check=True)
        return read_plain(output)


def read_docx(path: Path) -> list[SourceLine]:
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    lines: list[SourceLine] = []
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("word/document.xml")
    root = ET.fromstring(xml)
    paragraph_index = 0
    for para in root.findall(".//w:p", ns):
        paragraph_index += 1
        texts = [t.text or "" for t in para.findall(".//w:t", ns)]
        text = "".join(texts).strip()
        style = ""
        style_el = para.find("./w:pPr/w:pStyle", ns)
        if style_el is not None:
            style = style_el.attrib.get(f"{{{ns['w']}}}val", "")
        if style.lower().startswith("heading"):
            digits = re.findall(r"\d+", style)
            level = int(digits[0]) if digits else 1
            text = f"{'#' * max(1, min(level, 6))} {text}"
        lines.append(SourceLine(text, str(path.resolve()), paragraph_index))
        lines.append(SourceLine("", str(path.resolve()), paragraph_index))
    return lines


def load_source(path: Path) -> tuple[list[SourceLine], str]:
    suffix = path.suffix.lower()
    if suffix == ".tex":
        return read_latex(path), "latex"
    if suffix in {".md", ".markdown", ".qmd"}:
        return read_plain(path), "markdown"
    if suffix == ".docx":
        return read_docx(path), "markdown"
    if suffix == ".pdf":
        return read_pdf(path), "plain"
    return read_plain(path), "plain"


def classify_role(text: str) -> str:
    cleaned = normalize_space(re.sub(r"\\[a-zA-Z@]+\*?", "", text)).lstrip("([{“‘\"")
    for role, pattern in ROLE_PATTERNS:
        if pattern.search(cleaned):
            return role
    return "exposition"


def split_sentences(text: str) -> list[str]:
    text = normalize_space(text)
    if not text:
        return []

    protected = text
    placeholders: dict[str, str] = {}
    counter = 0
    for abbreviation in sorted(ABBREVIATIONS, key=len, reverse=True):
        pattern = re.compile(re.escape(abbreviation), re.I)
        for match in list(pattern.finditer(protected)):
            token = f"__ABBR_{counter}__"
            counter += 1
            placeholders[token] = match.group(0)
            protected = protected[: match.start()] + token + protected[match.end() :]
            break
    # Protect decimal points.
    protected = re.sub(r"(?<=\d)\.(?=\d)", "__DECIMAL__", protected)
    pieces = re.split(r"(?<=[.!?])\s+(?=(?:[A-Z0-9]|\\|\(|\[|[“\"]))", protected)
    sentences: list[str] = []
    for piece in pieces:
        for token, value in placeholders.items():
            piece = piece.replace(token, value)
        piece = piece.replace("__DECIMAL__", ".").strip()
        if piece:
            sentences.append(piece)
    return sentences or [text]


class GraphBuilder:
    def __init__(self, include_sentences: bool = True) -> None:
        self.nodes: list[Node] = []
        self.edges: list[Edge] = []
        self.include_sentences = include_sentences
        self.counters: defaultdict[str, int] = defaultdict(int)
        self.order_by_parent: defaultdict[str, int] = defaultdict(int)
        self.last_by_parent_level: dict[tuple[str, str], str] = {}
        self.heading_stack: list[tuple[int, str]] = []
        self.document_id = "DOC"
        self.nodes.append(Node("DOC", "", "document", 1, "", 0, 0, "Document", "", "document"))

    def next_id(self, prefix: str) -> str:
        self.counters[prefix] += 1
        return f"{prefix}{self.counters[prefix]:04d}"

    def current_parent(self) -> str:
        return self.heading_stack[-1][1] if self.heading_stack else self.document_id

    def add_node(
        self,
        level: str,
        parent_id: str,
        file: str,
        start_line: int,
        end_line: int,
        text: str,
        title: str = "",
        node_id: Optional[str] = None,
        surface_role: Optional[str] = None,
    ) -> str:
        prefix_map = {
            "section": "SEC",
            "subsection": "SUB",
            "subsubsection": "SSB",
            "run_in_heading": "RUN",
            "paragraph": "P",
            "sentence": "S",
            "equation": "EQ",
            "definition": "DEF",
            "assumption": "ASM",
            "lemma": "LEM",
            "proposition": "PROP",
            "theorem": "THM",
            "corollary": "COR",
            "proof": "PRF",
            "figure": "FIG",
            "table": "TAB",
            "algorithm": "ALG",
        }
        if node_id is None:
            node_id = self.next_id(prefix_map.get(level, "N"))
        self.order_by_parent[parent_id] += 1
        order = self.order_by_parent[parent_id]
        role = surface_role or classify_role(text)
        self.nodes.append(
            Node(
                id=node_id,
                parent_id=parent_id,
                level=level,
                order=order,
                file=file,
                start_line=start_line,
                end_line=end_line,
                title=title,
                text=normalize_space(text),
                surface_role=role,
            )
        )
        if parent_id:
            self.edges.append(Edge(parent_id, node_id, "structural", "contains"))
        key = (parent_id, level)
        previous = self.last_by_parent_level.get(key)
        if previous:
            self.edges.append(Edge(previous, node_id, "structural", "sequence"))
        self.last_by_parent_level[key] = node_id
        return node_id

    def add_heading(self, rank: int, title: str, source: SourceLine) -> None:
        while self.heading_stack and self.heading_stack[-1][0] >= rank:
            self.heading_stack.pop()
        parent = self.current_parent()
        level = {1: "section", 2: "subsection", 3: "subsubsection"}.get(rank, "run_in_heading")
        node_id = self.add_node(level, parent, source.file, source.line, source.line, title, title=title, surface_role="heading")
        self.heading_stack.append((rank, node_id))

    def add_paragraph(self, lines: list[SourceLine]) -> None:
        if not lines:
            return
        text = normalize_space(" ".join(line.text.strip() for line in lines if line.text.strip()))
        if not text:
            return
        # Skip pure labels and layout commands.
        if re.fullmatch(r"(?:\\label\{[^}]+\}|\\(?:vspace|smallskip|medskip|bigskip|noindent)\b.*)", text):
            return
        parent = self.current_parent()
        paragraph_id = self.add_node(
            "paragraph",
            parent,
            lines[0].file,
            lines[0].line,
            lines[-1].line,
            text,
            surface_role=classify_role(text),
        )
        if self.include_sentences:
            for sentence in split_sentences(text):
                self.add_node(
                    "sentence",
                    paragraph_id,
                    lines[0].file,
                    lines[0].line,
                    lines[-1].line,
                    sentence,
                    surface_role=classify_role(sentence),
                )

    def add_formal(self, kind: str, lines: list[SourceLine]) -> None:
        if not lines:
            return
        parent = self.current_parent()
        text = "\n".join(line.text for line in lines).strip()
        title = ""
        caption = re.search(r"\\caption(?:\[[^]]*\])?\{([^{}]*)\}", text, re.S)
        if caption:
            title = latex_title(caption.group(1))
        self.add_node(kind, parent, lines[0].file, lines[0].line, lines[-1].line, text, title=title, surface_role=kind)


def parse(lines: list[SourceLine], source_type: str, include_sentences: bool) -> GraphBuilder:
    builder = GraphBuilder(include_sentences=include_sentences)
    paragraph_buffer: list[SourceLine] = []
    formal_buffer: list[SourceLine] = []
    formal_env: Optional[str] = None
    in_document = source_type != "latex"

    def flush_paragraph() -> None:
        nonlocal paragraph_buffer
        builder.add_paragraph(paragraph_buffer)
        paragraph_buffer = []

    for source in lines:
        raw = source.text
        if source_type == "latex":
            if "\\begin{document}" in raw:
                in_document = True
                continue
            if "\\end{document}" in raw:
                flush_paragraph()
                break
            if not in_document:
                continue

        if formal_env:
            formal_buffer.append(source)
            if re.search(LATEX_END_TEMPLATE % re.escape(formal_env), raw):
                builder.add_formal(FORMAL_ENV_KIND[formal_env], formal_buffer)
                formal_buffer = []
                formal_env = None
            continue

        if source_type == "latex":
            heading = LATEX_HEADING_RE.match(raw)
            if heading:
                flush_paragraph()
                rank = HEADING_LEVELS[heading.group("kind")]
                builder.add_heading(rank, latex_title(heading.group("title")), source)
                continue
            begin = LATEX_BEGIN_RE.search(raw)
            if begin and begin.group(1) in FORMAL_ENV_KIND:
                flush_paragraph()
                formal_env = begin.group(1)
                formal_buffer = [source]
                if re.search(LATEX_END_TEMPLATE % re.escape(formal_env), raw):
                    builder.add_formal(FORMAL_ENV_KIND[formal_env], formal_buffer)
                    formal_buffer = []
                    formal_env = None
                continue
        elif source_type == "markdown":
            heading = MARKDOWN_HEADING_RE.match(raw)
            if heading:
                flush_paragraph()
                builder.add_heading(len(heading.group("marks")), normalize_space(heading.group("title")), source)
                continue

        if not raw.strip():
            flush_paragraph()
        else:
            paragraph_buffer.append(source)

    flush_paragraph()
    if formal_buffer and formal_env:
        builder.add_formal(FORMAL_ENV_KIND[formal_env], formal_buffer)
    return builder


def write_csv(path: Path, rows: Iterable[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def graphml_escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def write_graphml(path: Path, nodes: list[Node], edges: list[Edge]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        handle.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        handle.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns">\n')
        for key, attr_name in [
            ("d0", "level"), ("d1", "title"), ("d2", "text"), ("d3", "surface_role"),
            ("d4", "file"), ("d5", "start_line"), ("d6", "end_line"),
        ]:
            handle.write(f'  <key id="{key}" for="node" attr.name="{attr_name}" attr.type="string"/>\n')
        handle.write('  <key id="e0" for="edge" attr.name="relation" attr.type="string"/>\n')
        handle.write('  <key id="e1" for="edge" attr.name="edge_class" attr.type="string"/>\n')
        handle.write('  <graph id="G" edgedefault="directed">\n')
        for node in nodes:
            handle.write(f'    <node id="{graphml_escape(node.id)}">\n')
            values = [node.level, node.title, node.text, node.surface_role, node.file, node.start_line, node.end_line]
            for idx, value in enumerate(values):
                handle.write(f'      <data key="d{idx}">{graphml_escape(value)}</data>\n')
            handle.write('    </node>\n')
        for idx, edge in enumerate(edges):
            handle.write(
                f'    <edge id="E{idx}" source="{graphml_escape(edge.source)}" target="{graphml_escape(edge.target)}">\n'
            )
            handle.write(f'      <data key="e0">{graphml_escape(edge.relation)}</data>\n')
            handle.write(f'      <data key="e1">{graphml_escape(edge.edge_class)}</data>\n')
            handle.write('    </edge>\n')
        handle.write('  </graph>\n</graphml>\n')


def write_outputs(builder: GraphBuilder, output_dir: Path, input_path: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    node_rows = [asdict(node) for node in builder.nodes]
    edge_rows = [asdict(edge) for edge in builder.edges]
    write_csv(output_dir / "reasoning_nodes.csv", node_rows, list(Node.__dataclass_fields__.keys()))
    write_csv(output_dir / "reasoning_edges.csv", edge_rows, list(Edge.__dataclass_fields__.keys()))
    payload = {
        "metadata": {
            "input": str(input_path.resolve()),
            "note": "Structural skeleton only. Semantic dependencies and writing judgments require close reading.",
        },
        "nodes": node_rows,
        "edges": edge_rows,
    }
    (output_dir / "reasoning_graph.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_graphml(output_dir / "reasoning_graph.graphml", builder.nodes, builder.edges)

    counts: defaultdict[str, int] = defaultdict(int)
    for node in builder.nodes:
        counts[node.level] += 1
    summary_lines = [
        "# Reasoning Skeleton Summary",
        "",
        f"- Input: `{input_path}`",
        f"- Nodes: {len(builder.nodes)}",
        f"- Edges: {len(builder.edges)}",
        "",
        "## Nodes by level",
        "",
    ]
    for level, count in sorted(counts.items()):
        summary_lines.append(f"- {level}: {count}")
    summary_lines.extend(
        [
            "",
            "## Important limitation",
            "",
            "This output contains deterministic containment and sequence edges plus surface-role hints. "
            "It does not establish argumentative quality. Enrich it with inheritance, advance, yield, "
            "semantic dependency edges, weak-edge diagnoses, and repairs through close reading.",
        ]
    )
    (output_dir / "summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Root manuscript file (.tex, .md, .txt, .docx, or .pdf)")
    parser.add_argument("--output-dir", type=Path, default=Path("writing-review/graph"))
    parser.add_argument("--no-sentences", action="store_true", help="Skip sentence nodes for a smaller graph")
    args = parser.parse_args(argv)

    if not args.input.exists():
        parser.error(f"Input does not exist: {args.input}")
    try:
        lines, source_type = load_source(args.input)
        builder = parse(lines, source_type, include_sentences=not args.no_sentences)
        write_outputs(builder, args.output_dir, args.input)
    except (OSError, RuntimeError, subprocess.CalledProcessError, zipfile.BadZipFile, ET.ParseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote reasoning skeleton to {args.output_dir}")
    print(f"Nodes: {len(builder.nodes)}; edges: {len(builder.edges)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
