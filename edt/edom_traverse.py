from collections.abc import Iterator

from .edom import EdomNode


def preorder(node: EdomNode) -> Iterator[EdomNode]:
    yield node
    for child in node.children:
        yield from preorder(child)


def find_by_kind(node: EdomNode, kind: str) -> list[EdomNode]:
    return [item for item in preorder(node) if item.kind == kind]
