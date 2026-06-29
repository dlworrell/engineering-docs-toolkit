from .layout_model import LayoutBlock


def top_left_order(blocks: list[LayoutBlock]) -> list[LayoutBlock]:
    def key(block: LayoutBlock) -> tuple[int, int]:
        if block.bbox is None:
            return (0, 0)
        x0, y0, _x1, _y1 = block.bbox
        return (y0, x0)

    return sorted(blocks, key=key)
