from .edom import EdomNode
from .edom_traverse import preorder


def fingerprint_map(root: EdomNode) -> dict[str, str]:
    return {node.node_id: node.fingerprint for node in preorder(root)}


def dirty_node_ids(previous: dict[str, str], current: dict[str, str]) -> set[str]:
    return {node_id for node_id, fingerprint in current.items() if previous.get(node_id) != fingerprint}
