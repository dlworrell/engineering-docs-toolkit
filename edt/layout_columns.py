from .layout_model import LayoutBlock


def block_left(block: LayoutBlock) -> int:
    return 0 if block.bbox is None else block.bbox[0]


def column_index(block: LayoutBlock, split_x: int) -> int:
    return 0 if block_left(block) < split_x else 1


def group_two_columns(blocks: list[LayoutBlock], split_x: int) -> dict[int, list[LayoutBlock]]:
    columns: dict[int, list[LayoutBlock]] = {0: [], 1: []}
    for block in blocks:
        columns[column_index(block, split_x)].append(block)
    return columns
