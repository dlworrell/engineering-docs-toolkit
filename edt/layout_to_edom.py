from .edom import EdomNode
from .layout_model import LayoutBlock, LayoutPage
from .reading_order import top_left_order


KIND_MAP = {
    "paragraph": "paragraph",
    "heading": "heading",
    "caption": "caption",
    "table": "table",
    "figure": "figure",
    "image": "figure",
    "math": "equation",
    "equation": "equation",
}


def block_to_edom(block: LayoutBlock) -> EdomNode:
    return EdomNode(kind=KIND_MAP.get(block.kind, "block"), text=block.text, node_id=block.block_id)


def page_to_edom(page: LayoutPage) -> EdomNode:
    root = EdomNode(kind="page", node_id=f"page-{page.page_number}")
    for block in top_left_order(page.blocks):
        root.add(block_to_edom(block))
    return root
