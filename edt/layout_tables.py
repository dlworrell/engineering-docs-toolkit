from .layout_model import LayoutBlock


TABLE_KINDS = {"table", "table_cell", "table_row"}


def table_blocks(blocks: list[LayoutBlock]) -> list[LayoutBlock]:
    return [block for block in blocks if block.kind in TABLE_KINDS]


def looks_like_table(block: LayoutBlock) -> bool:
    text = block.text.strip()
    return "\t" in text or " | " in text
