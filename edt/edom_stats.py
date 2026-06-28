from .edom import EdomNode


def count_nodes(node: EdomNode) -> int:
    return 1 + sum(count_nodes(child) for child in node.children)


def count_kind(node: EdomNode, kind: str) -> int:
    own = 1 if node.kind == kind else 0
    return own + sum(count_kind(child, kind) for child in node.children)
