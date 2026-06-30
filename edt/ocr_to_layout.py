from __future__ import annotations

from .layout_model import LayoutBlock, LayoutPage
from .ocr_model import OcrPage


def ocr_page_to_layout(page: OcrPage) -> LayoutPage:
    layout = LayoutPage(page_number=page.page_number, width=page.width, height=page.height)
    for index, block in enumerate(page.blocks, start=1):
        text = block.text.strip()
        kind = "paragraph"
        if text.lower().startswith(("figure", "fig.")):
            kind = "caption"
        elif text.lower().startswith("table"):
            kind = "caption"
        elif len(text) <= 80 and text.isupper():
            kind = "heading"
        layout.add_block(
            LayoutBlock(
                block_id=f"p{page.page_number:04d}-b{index:04d}",
                kind=kind,
                text=text,
                bbox=block.bbox,
                confidence=block.confidence,
            )
        )
    return layout
