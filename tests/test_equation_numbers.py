from edt.equation_numbers import equation_number, has_equation_number
from edt.layout_model import LayoutBlock


def test_equation_number_reads_trailing_number():
    block = LayoutBlock(block_id="eq1", kind="equation", text="x = 1 (2.3)")
    assert equation_number(block) == "2.3"


def test_has_equation_number_false_without_number():
    block = LayoutBlock(block_id="eq1", kind="equation", text="x = 1")
    assert not has_equation_number(block)
