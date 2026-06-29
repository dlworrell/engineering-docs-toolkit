from edt.semantic_accessibility import aria_for_semantic_block
from edt.semantic_blocks import SemanticBlock


def test_semantic_equation_maps_to_math_role():
    block = SemanticBlock(block_id="eq1", semantic_kind="equation", text="x = 1")
    assert aria_for_semantic_block(block).role == "math"


def test_semantic_bibliography_maps_to_doc_role():
    block = SemanticBlock(block_id="b1", semantic_kind="bibliography", text="Bibliography")
    assert aria_for_semantic_block(block).role == "doc-bibliography"
