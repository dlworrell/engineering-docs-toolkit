from .edom import EdomNode
from .reference_exports import ResolvedLink


def find_edom_node(root: EdomNode, node_id: str) -> EdomNode | None:
    if root.node_id == node_id:
        return root
    for child in root.children:
        found = find_edom_node(child, node_id)
        if found is not None:
            return found
    return None


def add_reference_metadata(root: EdomNode, links: list[ResolvedLink]) -> EdomNode:
    for link in links:
        node = find_edom_node(root, link.source_id)
        if node is None:
            continue
        existing = node.metadata.get("references", "")
        targets = [target for target in existing.split(",") if target]
        targets.append(link.target_id)
        node.metadata["references"] = ",".join(targets)
    return root
