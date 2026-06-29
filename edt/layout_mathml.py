from .layout_equations import looks_like_equation
from .layout_model import LayoutBlock
from .semantic_mathml import mathml, mi, mn, mo, mrow


def simple_equation_mathml(block: LayoutBlock) -> str:
    text = block.text.strip()
    if not looks_like_equation(block) or "=" not in text:
        return mathml(mi(text))
    left, right = [part.strip() for part in text.split("=", 1)]
    right_node = mn(right) if right.replace(".", "", 1).isdigit() else mi(right)
    return mathml(mrow(mi(left), mo("="), right_node))
