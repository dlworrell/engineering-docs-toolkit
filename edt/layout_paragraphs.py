from .layout_model import LayoutBlock
from .reading_order import top_left_order


def paragraph_blocks(blocks: list[LayoutBlock]) -> list[LayoutBlock]:
    return [block for block in top_left_order(blocks) if block.kind == "paragraph"]


def paragraph_text(blocks: list[LayoutBlock]) -> str:
    return "\n\n".join(block.text.strip() for block in paragraph_blocks(blocks) if block.text.strip())
