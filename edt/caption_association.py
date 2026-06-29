from dataclasses import dataclass

from .layout_figures import caption_blocks, figure_blocks
from .layout_model import LayoutBlock, LayoutPage
from .layout_tables import table_blocks
from .reading_order import top_left_order


@dataclass
class CaptionAssociation:
    content_id: str
    caption_id: str
    caption_text: str


def nearest_caption(block: LayoutBlock, captions: list[LayoutBlock]) -> LayoutBlock | None:
    if block.bbox is None:
        return captions[0] if captions else None
    _x0, y0, _x1, _y1 = block.bbox
    return min(captions, key=lambda caption: abs((caption.bbox or (0, y0, 0, y0))[1] - y0), default=None)


def associate_figures_with_captions(page: LayoutPage) -> list[CaptionAssociation]:
    captions = caption_blocks(page.blocks)
    return [CaptionAssociation(figure.block_id, caption.block_id, caption.text) for figure in figure_blocks(page.blocks) if (caption := nearest_caption(figure, captions))]


def associate_tables_with_captions(page: LayoutPage) -> list[CaptionAssociation]:
    captions = caption_blocks(page.blocks)
    return [CaptionAssociation(table.block_id, caption.block_id, caption.text) for table in table_blocks(page.blocks) if (caption := nearest_caption(table, captions))]
