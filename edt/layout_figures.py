from .layout_model import LayoutBlock


FIGURE_KINDS = {"figure", "image", "diagram"}


def figure_blocks(blocks: list[LayoutBlock]) -> list[LayoutBlock]:
    return [block for block in blocks if block.kind in FIGURE_KINDS]


def caption_blocks(blocks: list[LayoutBlock]) -> list[LayoutBlock]:
    return [block for block in blocks if block.kind == "caption" or block.text.lower().startswith("figure ")]
