from .edom import EdomNode
from .edom_traverse import preorder


def find_by_id(root: EdomNode, node_id: str) -> EdomNode | None:
    for node in preorder(root):
        if node.node_id == node_id:
            return node
    return None
