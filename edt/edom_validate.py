from .edom import EdomNode
from .edom_traverse import preorder


def duplicate_ids(root: EdomNode) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []

    def visit(node: EdomNode) -> None:
        if node.node_id in seen:
            duplicates.append(node.node_id)
        seen.add(node.node_id)
        for child in node.children:
            visit(child)

    visit(root)
    return duplicates


def heading_level(kind: str) -> int | None:
    if kind.startswith("heading") and kind[7:].isdigit():
        return int(kind[7:])
    return None


def heading_jumps(root: EdomNode) -> list[str]:
    issues: list[str] = []
    previous = 0
    for node in preorder(root):
        level = heading_level(node.kind)
        if level is None:
            continue
        if previous and level > previous + 1:
            issues.append(node.text)
        previous = level
    return issues
