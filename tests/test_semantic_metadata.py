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


def test_figure_number_metadata():
    block = LayoutBlock(block_id="fig1", kind="figure", text="Figure 1.2 Engine diagram")
    metadata = semantic_metadata_for_layout(block, "figure")
    assert metadata["number"] == "1.2"


def test_table_number_metadata():
    block = LayoutBlock(block_id="table1", kind="table", text="Table 3.4 Values")
    metadata = semantic_metadata_for_layout(block, "table")
    assert metadata["number"] == "3.4"


def test_theorem_number_metadata():
    block = LayoutBlock(block_id="thm1", kind="paragraph", text="Theorem 4.1")
    metadata = semantic_metadata_for_layout(block, "theorem")
    assert metadata["number"] == "4.1"
