from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SECTION_KINDS = {"theorem", "proof", "definition", "example", "exercise", "algorithm"}


def _text(node: dict[str, Any]) -> str:
    return str(node.get("text", "")).strip()


def render_edom_node_to_markdown(node: dict[str, Any]) -> str:
    kind = str(node.get("kind", "block"))
    text = _text(node)
    children = [render_edom_node_to_markdown(child) for child in node.get("children", []) if isinstance(child, dict)]
    children = [child for child in children if child.strip()]
    child_text = "\n\n".join(children)

    if kind == "document":
        return child_text
    if kind == "page":
        return child_text
    if kind == "title":
        return f"# {text}" if text else child_text
    if kind == "heading":
        return f"## {text}" if text else child_text
    if kind == "caption":
        return f"*{text}*" if text else child_text
    if kind == "equation":
        return f"$$\n{text}\n$$" if text else child_text
    if kind in SECTION_KINDS:
        label = kind.title()
        body = f"**{label}.** {text}".strip()
        return f"{body}\n\n{child_text}".strip()
    if kind == "figure":
        return f"[Figure: {text}]\n\n{child_text}".strip() if text else child_text
    if kind == "table":
        return f"[Table]\n\n{text}\n\n{child_text}".strip()
    if text:
        return text
    return child_text


def edom_document_to_markdown(document_payload: dict[str, Any]) -> str:
    root = document_payload.get("root", document_payload)
    if not isinstance(root, dict):
        return ""
    markdown = render_edom_node_to_markdown(root).strip()
    return markdown + ("\n" if markdown else "")


def write_edom_markdown(document_edom: Path, output_markdown: Path) -> Path:
    payload = json.loads(document_edom.read_text(encoding="utf-8"))
    output_markdown.parent.mkdir(parents=True, exist_ok=True)
    output_markdown.write_text(edom_document_to_markdown(payload), encoding="utf-8")
    return output_markdown
