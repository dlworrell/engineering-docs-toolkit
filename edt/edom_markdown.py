from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .edom import EdomNode


def markdown_to_edom(text: str, title: str = "Document") -> EdomNode:
    root = EdomNode(kind="document", text=title)
    current = root
    for line in text.splitlines():
        if line.startswith("#"):
            marks = len(line) - len(line.lstrip("#"))
            heading = line[marks:].strip()
            current = root.add(EdomNode(kind=f"heading{marks}", text=heading))
        elif line.strip():
            current.add(EdomNode(kind="paragraph", text=line.strip()))
    return root


def _heading_level(node: dict[str, Any], default: int = 2) -> int:
    kind = str(node.get("kind", ""))
    if kind.startswith("heading"):
        suffix = kind.removeprefix("heading")
        if suffix.isdigit():
            return max(1, min(6, int(suffix)))
    metadata = node.get("metadata", {})
    if isinstance(metadata, dict):
        level = metadata.get("level")
        if isinstance(level, int):
            return max(1, min(6, level))
    return default


def _node_text(node: dict[str, Any]) -> str:
    return str(node.get("text", "")).strip()


def _children(node: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        child
        for child in node.get("children", [])
        if isinstance(child, dict)
    ]


def _render_children(node: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for child in _children(node):
        rendered = render_edom_node_to_markdown(child)
        if rendered:
            if lines:
                lines.append("")
            lines.extend(rendered)
    return lines


def render_edom_node_to_markdown(node: dict[str, Any]) -> list[str]:
    kind = str(node.get("kind", "block"))
    text = _node_text(node)
    children = _render_children(node)

    if kind == "document":
        return children
    if kind == "page":
        return children
    if kind == "title":
        return [f"# {text}"] if text else children
    if kind == "heading":
        return [f"{'#' * _heading_level(node)} {text}"] if text else children
    if kind.startswith("heading"):
        return [f"{'#' * _heading_level(node)} {text}"] if text else children
    if kind == "caption":
        return [f"*{text}*"] if text else children
    if kind == "equation":
        return ["$$", text, "$$"] if text else children
    if kind in {"theorem", "proof", "definition", "example", "exercise", "algorithm"}:
        heading = kind.title()
        lines = [f"### {heading}"]
        if text:
            lines.extend(["", text])
        if children:
            lines.extend(["", *children])
        return lines
    if text:
        lines = [text]
        if children:
            lines.extend(["", *children])
        return lines
    return children


def edom_document_to_markdown(document_payload: dict[str, Any]) -> str:
    root = document_payload.get("root", document_payload)
    if not isinstance(root, dict):
        return ""
    lines = render_edom_node_to_markdown(root)
    return "\n".join(lines).strip() + "\n"


def write_edom_markdown(document_edom: Path, output_markdown: Path) -> Path:
    payload = json.loads(document_edom.read_text(encoding="utf-8"))
    output_markdown.parent.mkdir(parents=True, exist_ok=True)
    output_markdown.write_text(
        edom_document_to_markdown(payload),
        encoding="utf-8",
    )
    return output_markdown
