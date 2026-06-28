from .edom import EdomNode


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
