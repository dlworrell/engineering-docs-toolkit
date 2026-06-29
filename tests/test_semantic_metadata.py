from edt.layout_model import LayoutBlock
from edt.semantic_metadata import semantic_block_with_metadata, semantic_metadata_for_layout


def test_equation_number_metadata():
    block = LayoutBlock(block_id="eq1", kind="equation", text="x = 1 (2.3)")
    metadata = semantic_metadata_for_layout(block, "equation")
    assert metadata["equation_number"] == "2.3"


def test_proof_end_marker_metadata():
    block = LayoutBlock(block_id="proof1", kind="paragraph", text="Therefore done. qed")
    semantic = semantic_block_with_metadata(block, "proof")
    assert semantic.metadata["proof_end_marker"] == "qed"
