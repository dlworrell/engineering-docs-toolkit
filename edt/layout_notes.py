from .layout_model import LayoutBlock, LayoutPage


def footnote_blocks(page: LayoutPage) -> list[LayoutBlock]:
    return [block for block in page.blocks if block.kind == "footnote"]


def marginalia_blocks(page: LayoutPage, margin_width: int = 80) -> list[LayoutBlock]:
    result: list[LayoutBlock] = []
    for block in page.blocks:
        if block.bbox is None:
            continue
        x0, _y0, x1, _y1 = block.bbox
        if x0 <= margin_width or x1 >= page.width - margin_width:
            result.append(block)
    return result
