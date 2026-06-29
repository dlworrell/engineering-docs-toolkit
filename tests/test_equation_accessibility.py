from edt.equation_accessibility import equation_aria, equation_aria_label
from edt.semantic_blocks import SemanticBlock


def test_equation_aria_label_includes_number():
    block = SemanticBlock(block_id="eq1", semantic_kind="equation", text="x = 1", metadata={"equation_number": "2.3"})
    assert equation_aria_label(block).startswith("Equation 2.3")


def test_equation_aria_role_is_math():
    block = SemanticBlock(block_id="eq1", semantic_kind="equation", text="x = 1")
    assert equation_aria(block).role == "math"
