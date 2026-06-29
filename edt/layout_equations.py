from .layout_model import LayoutBlock


EQUATION_KINDS = {"equation", "math", "formula"}


def equation_blocks(blocks: list[LayoutBlock]) -> list[LayoutBlock]:
    return [block for block in blocks if block.kind in EQUATION_KINDS]


def looks_like_equation(block: LayoutBlock) -> bool:
    text = block.text.strip()
    return "=" in text and any(char.isalpha() for char in text)
