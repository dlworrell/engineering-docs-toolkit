import re

from .layout_model import LayoutBlock


EQUATION_NUMBER_RE = re.compile(r"\((\d+(?:\.\d+)*)\)\s*$")


def equation_number(block: LayoutBlock) -> str:
    match = EQUATION_NUMBER_RE.search(block.text.strip())
    return "" if match is None else match.group(1)


def has_equation_number(block: LayoutBlock) -> bool:
    return bool(equation_number(block))
