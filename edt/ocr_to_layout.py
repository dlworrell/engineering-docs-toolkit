from __future__ import annotations

from .layout_equations import looks_like_equation
from .layout_model import LayoutBlock, LayoutPage
from .ocr_model import OcrPage


def ocr_page_to_layout(page: OcrPage) -> LayoutPage:
    layout = LayoutPage(
        page_number=page.page_number,
        width=page.width,
        height=page.height,
    )
    for index, block in enumerate(page.blocks, start=1):
        text = block.text.strip()
        layout_block = LayoutBlock(
            block_id=f"p{page.page_number:04d}-b{index:04d}",
            kind="paragraph",
            text=text,
            bbox=block.bbox,
            confidence=block.confidence,
        )
        if text.lower().startswith(("figure", "fig.")):
            layout_block.kind = "caption"
        elif text.lower().startswith("table"):
            layout_block.kind = "caption"
        elif looks_like_equation(layout_block):
            layout_block.kind = "equation"
        elif len(text) <= 80 and text.isupper():
            layout_block.kind = "heading"
        layout.add_block(layout_block)
    return layout
