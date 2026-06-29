from .layout_model import LayoutBlock, LayoutPage


def header_band(page: LayoutPage, ratio: float = 0.1) -> int:
    return int(page.height * ratio)


def footer_band(page: LayoutPage, ratio: float = 0.1) -> int:
    return int(page.height * (1.0 - ratio))


def header_blocks(page: LayoutPage) -> list[LayoutBlock]:
    limit = header_band(page)
    return [block for block in page.blocks if block.bbox is not None and block.bbox[1] <= limit]


def footer_blocks(page: LayoutPage) -> list[LayoutBlock]:
    limit = footer_band(page)
    return [block for block in page.blocks if block.bbox is not None and block.bbox[1] >= limit]
