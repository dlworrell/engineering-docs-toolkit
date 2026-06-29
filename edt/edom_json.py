import json
from pathlib import Path

from .edom import EdomNode


def node_to_dict(node: EdomNode) -> dict:
    return {
        "id": node.node_id,
        "kind": node.kind,
        "text": node.text,
        "fingerprint": node.fingerprint,
        "children": [node_to_dict(child) for child in node.children],
    }


def dict_to_node(data: dict) -> EdomNode:
    node = EdomNode(kind=str(data["kind"]), text=str(data.get("text", "")), node_id=str(data["id"]))
    return node


def write_edom_json(node: EdomNode, path: Path) -> None:
    path.write_text(json.dumps(node_to_dict(node), indent=2) + "\n", encoding="utf-8")
