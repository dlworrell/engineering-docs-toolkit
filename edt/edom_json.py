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
    for child in data.get("children", []):
        node.add(dict_to_node(child))
    return node


def read_edom_json(path: Path) -> EdomNode:
    return dict_to_node(json.loads(path.read_text(encoding="utf-8")))


def write_edom_json(node: EdomNode, path: Path) -> None:
    path.write_text(json.dumps(node_to_dict(node), indent=2) + "\n", encoding="utf-8")
