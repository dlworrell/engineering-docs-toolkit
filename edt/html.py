from __future__ import annotations

import json
from html import escape
from pathlib import Path
from typing import Any

from .math_parser import replace_math


def render_inline(text: str) -> str:
    rendered = replace_math(text)
    pieces = []
    cursor = 0
    while True:
        start = rendered.find('<math ', cursor)
        if start == -1:
            pieces.append(escape(rendered[cursor:]))
            break
        end = rendered.find('</math>', start)
        if end == -1:
            pieces.append(escape(rendered[cursor:]))
            break
        end += len('</math>')
        pieces.append(escape(rendered[cursor:start]))
        pieces.append(rendered[start:end])
        cursor = end
    return ''.join(pieces)


def markdown_to_html(text: str, title: str) -> str:
    lines = ["<!doctype html>", '<html lang="en">', "<head>", '<meta charset="utf-8">', f"<title>{escape(title)}</title>", "</head>", "<body>", '<main role="main">']
    for line in text.splitlines():
        if line.startswith("# "):
            lines.append(f"<h1>{render_inline(line[2:])}</h1>")
        elif line.startswith("## "):
            lines.append(f"<h2>{render_inline(line[3:])}</h2>")
        elif line.startswith("### "):
            lines.append(f"<h3>{render_inline(line[4:])}</h3>")
        elif line.strip():
            lines.append(f"<p>{render_inline(line)}</p>")
        else:
            lines.append("")
    lines.extend(["</main>", "</body>", "</html>"])
    return "\n".join(lines)


def _attrs(node: dict[str, Any], *classes: str) -> str:
    node_id = escape(str(node.get("id", "")), quote=True)
    kind = escape(str(node.get("kind", "block")), quote=True)
    class_value = " ".join(value for value in classes if value)
    class_attr = f' class="{escape(class_value, quote=True)}"' if class_value else ""
    return f'id="{node_id}" data-edt-kind="{kind}"{class_attr}'


def render_edom_node(node: dict[str, Any]) -> str:
    kind = str(node.get("kind", "block"))
    text = str(node.get("text", ""))
    children = node.get("children", [])
    child_html = "\n".join(render_edom_node(child) for child in children if isinstance(child, dict))

    if kind == "document":
        return child_html
    if kind == "page":
        return f'<section {_attrs(node, "edt-page")}>\n{child_html}\n</section>'
    if kind == "heading":
        return f'<h2 {_attrs(node)}>{render_inline(text)}</h2>'
    if kind == "title":
        return f'<h1 {_attrs(node)}>{render_inline(text)}</h1>'
    if kind == "caption":
        return f'<figcaption {_attrs(node)}>{render_inline(text)}</figcaption>'
    if kind == "figure":
        return f'<figure {_attrs(node)}>{child_html}</figure>'
    if kind == "table":
        return f'<div {_attrs(node, "edt-table")} role="table">{render_inline(text)}{child_html}</div>'
    if kind == "equation":
        return f'<div {_attrs(node, "edt-equation")} role="math">{render_inline(text)}</div>'
    if kind == "theorem":
        return f'<section {_attrs(node, "edt-theorem")}><strong>Theorem.</strong> {render_inline(text)}</section>'
    if kind == "proof":
        return f'<section {_attrs(node, "edt-proof")}><strong>Proof.</strong> {render_inline(text)}</section>'
    if kind in {"definition", "example", "exercise", "algorithm"}:
        return f'<section {_attrs(node, f"edt-{kind}")}><strong>{escape(kind.title())}.</strong> {render_inline(text)}</section>'
    if text:
        return f'<p {_attrs(node)}>{render_inline(text)}</p>'
    return f'<div {_attrs(node)}>{child_html}</div>'


def edom_document_to_html(document_payload: dict[str, Any], title: str = "EDT Document") -> str:
    root = document_payload.get("root", document_payload)
    body = render_edom_node(root) if isinstance(root, dict) else ""
    lines = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{escape(title)}</title>",
        "</head>",
        "<body>",
        '<main role="main">',
        body,
        "</main>",
        "</body>",
        "</html>",
    ]
    return "\n".join(lines)


def write_edom_html(document_edom: Path, output_html: Path, title: str = "EDT Document") -> Path:
    payload = json.loads(document_edom.read_text(encoding="utf-8"))
    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_html.write_text(edom_document_to_html(payload, title=title), encoding="utf-8")
    return output_html
