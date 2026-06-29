from .accessibility_aria import AriaAnnotation
from .figure_alt_text import FigureAltText
from .layout_model import LayoutBlock
from .table_accessibility import AccessibleTable


def aria_for_block(block: LayoutBlock) -> AriaAnnotation:
    role_map = {
        "figure": "figure",
        "image": "img",
        "table": "table",
        "heading": "heading",
        "math": "math",
        "equation": "math",
    }
    return AriaAnnotation(role=role_map.get(block.kind, "group"), label=block.text.strip())


def alt_text_for_figure(block: LayoutBlock) -> FigureAltText:
    return FigureAltText(figure_id=block.block_id, alt_text=block.text.strip())


def accessible_table_for_block(block: LayoutBlock) -> AccessibleTable:
    rows = [line for line in block.text.splitlines() if line.strip()]
    headers = rows[0].replace("|", "\t").split("\t") if rows else []
    return AccessibleTable(table_id=block.block_id, headers=[item.strip() for item in headers if item.strip()])
