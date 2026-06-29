from edt.layout_mathml import simple_equation_mathml
from edt.layout_model import LayoutBlock


def test_simple_equation_mathml_converts_equals_expression():
    block = LayoutBlock(block_id="eq1", kind="equation", text="x = 1")
    output = simple_equation_mathml(block)
    assert "<math" in output
    assert "<mi>x</mi>" in output
    assert "<mn>1</mn>" in output
