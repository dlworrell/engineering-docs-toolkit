from edt.layout_equations import equation_blocks, looks_like_equation
from edt.layout_model import LayoutBlock


def test_equation_blocks_filters_math_kind():
    block = LayoutBlock(block_id="eq1", kind="math")
    assert equation_blocks([block]) == [block]


def test_looks_like_equation_detects_equals():
    block = LayoutBlock(block_id="p1", kind="paragraph", text="x = 1")
    assert looks_like_equation(block)
