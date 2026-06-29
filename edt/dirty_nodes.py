from .edom import EdomNode
from .edom_traverse import preorder


def fingerprint_map(root: EdomNode) -> dict[str, str]:
    return {node.node_id: node.fingerprint for node in preorder(root)}
