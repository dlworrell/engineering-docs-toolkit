from edt.reference_index import build_reference_index, reference_key_for_block
from edt.semantic_blocks import SemanticBlock


def test_reference_key_for_equation_number():
    block = SemanticBlock(block_id="eq1", semantic_kind="equation", text="x = 1", metadata={"equation_number": "2.3"})
    assert reference_key_for_block(block) == "equation:2.3"


def test_build_reference_index_for_figure():
    block = SemanticBlock(block_id="fig1", semantic_kind="figure", text="", metadata={"number": "1.2"})
    assert build_reference_index([block]) == {"figure:1.2": "fig1"}
