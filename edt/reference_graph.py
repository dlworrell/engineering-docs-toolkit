from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


UNREFERENCED_OK = {"document", "page", "chapter", "section", "frontmatter", "title", "subtitle", "copyright", "toc", "appendix", "bibliography", "index", "glossary", "caption", "proof"}
REFERENCE_EXPECTED = {"figure", "table", "equation", "theorem", "definition", "lemma", "corollary"}


@dataclass
class ReferenceGraphNode:
    node_id: str
    kind: str
    page: int | None = None
    incoming: list[str] = field(default_factory=list)
    outgoing: list[str] = field(default_factory=list)
    broken: list[str] = field(default_factory=list)
    orphan: bool = False


@dataclass
class ReferenceGraph:
    nodes: dict[str, ReferenceGraphNode] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "summary": {
                "nodes": len(self.nodes),
                "edges": sum(len(node.outgoing) for node in self.nodes.values()),
                "broken": sum(len(node.broken) for node in self.nodes.values()),
                "orphans": sum(1 for node in self.nodes.values() if node.orphan),
            },
            "nodes": [asdict(node) for node in self.nodes.values()],
        }

    def to_markdown(self) -> str:
        payload = self.to_dict()
        summary = payload["summary"]
        lines = [
            "# EDT Reference Index",
            "",
            f"Nodes: {summary['nodes']}",
            f"Edges: {summary['edges']}",
            f"Broken references: {summary['broken']}",
            f"Orphans: {summary['orphans']}",
            "",
            "| ID | Kind | Page | Incoming | Outgoing | Broken | Orphan |",
            "|---|---|---:|---:|---:|---:|---|",
        ]
        for node in self.nodes.values():
            page = "" if node.page is None else str(node.page)
            lines.append(f"| {node.node_id} | {node.kind} | {page} | {len(node.incoming)} | {len(node.outgoing)} | {len(node.broken)} | {node.orphan} |")
        return "\n".join(lines) + "\n"

    def write_json(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return path

    def write_markdown(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.to_markdown(), encoding="utf-8")
        return path


def _walk_nodes(node: dict[str, Any], page: int | None = None) -> list[tuple[dict[str, Any], int | None]]:
    kind = str(node.get("kind", ""))
    current_page = page
    if kind == "page":
        node_id = str(node.get("id", ""))
        if node_id.startswith("page-"):
            try:
                current_page = int(node_id.removeprefix("page-"))
            except ValueError:
                current_page = page
    nodes = [(node, current_page)]
    children = node.get("children", [])
    if isinstance(children, list):
        for child in children:
            if isinstance(child, dict):
                nodes.extend(_walk_nodes(child, current_page))
    return nodes


def _node_references(node: dict[str, Any]) -> list[str]:
    metadata = node.get("metadata", {})
    if not isinstance(metadata, dict):
        return []
    value = metadata.get("references", metadata.get("reference", metadata.get("target_id", "")))
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    return []


def _is_unreferenced_ok(node: dict[str, Any]) -> bool:
    metadata = node.get("metadata", {})
    kind = str(node.get("kind", ""))
    return kind in UNREFERENCED_OK or (isinstance(metadata, dict) and metadata.get("unreferenced_ok") is True)


def build_reference_graph(document_payload: dict[str, object]) -> ReferenceGraph:
    root = document_payload.get("root", document_payload)
    graph = ReferenceGraph()
    if not isinstance(root, dict):
        return graph

    source_nodes = _walk_nodes(root)
    for node, page in source_nodes:
        node_id = str(node.get("id", ""))
        if not node_id:
            continue
        graph.nodes[node_id] = ReferenceGraphNode(node_id=node_id, kind=str(node.get("kind", "")), page=page)

    for node, _page in source_nodes:
        node_id = str(node.get("id", ""))
        if node_id not in graph.nodes:
            continue
        for target_id in _node_references(node):
            if target_id in graph.nodes:
                graph.nodes[node_id].outgoing.append(target_id)
                graph.nodes[target_id].incoming.append(node_id)
            else:
                graph.nodes[node_id].broken.append(target_id)

    for node, _page in source_nodes:
        node_id = str(node.get("id", ""))
        if node_id not in graph.nodes:
            continue
        kind = str(node.get("kind", ""))
        if kind in REFERENCE_EXPECTED and not graph.nodes[node_id].incoming and not _is_unreferenced_ok(node):
            graph.nodes[node_id].orphan = True

    return graph
