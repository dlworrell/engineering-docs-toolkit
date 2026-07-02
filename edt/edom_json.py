import json
from pathlib import Path
from typing import Any

from .edom import EdomNode
from .source_region import SourceRegion


def node_to_dict(node: EdomNode) -> dict[str, object]:
    return {
        "id": node.node_id,
        "kind": node.kind,
        "text": node.text,
        "metadata": node.metadata,
        "source_regions": [
            region.to_dict() for region in node.source_regions
        ],
        "fingerprint": node.fingerprint,
        "children": [node_to_dict(child) for child in node.children],
    }


def dict_to_node(data: dict[str, Any]) -> EdomNode:
    metadata = data.get("metadata", {})
    if not isinstance(metadata, dict):
        raise ValueError("EDOM metadata must be an object")

    regions = data.get("source_regions", [])
    if not isinstance(regions, list):
        raise ValueError("EDOM source_regions must be an array")

    node = EdomNode(
        kind=str(data["kind"]),
        text=str(data.get("text", "")),
        node_id=str(data["id"]),
        metadata=dict(metadata),
        source_regions=[
            SourceRegion.from_dict(region)
            for region in regions
            if isinstance(region, dict)
        ],
    )
    for child in data.get("children", []):
        if not isinstance(child, dict):
            raise ValueError("EDOM children must be objects")
        node.add(dict_to_node(child))
    return node


def read_edom_json(path: Path) -> EdomNode:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("EDOM JSON root must be an object")
    return dict_to_node(payload)


def write_edom_json(node: EdomNode, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(node_to_dict(node), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
