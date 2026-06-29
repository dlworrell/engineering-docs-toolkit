from collections.abc import Callable

from .edom import EdomNode
from .edom_traverse import preorder


def walk(root: EdomNode, visitor: Callable[[EdomNode], None]) -> None:
    for node in preorder(root):
        visitor(node)
