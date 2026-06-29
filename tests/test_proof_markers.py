from edt.layout_model import LayoutBlock
from edt.proof_markers import has_proof_end_marker, proof_end_marker


def test_proof_end_marker_reads_qed():
    block = LayoutBlock(block_id="p1", kind="paragraph", text="Therefore done. qed")
    assert proof_end_marker(block) == "qed"


def test_has_proof_end_marker_reads_square():
    block = LayoutBlock(block_id="p1", kind="paragraph", text="Therefore done. □")
    assert has_proof_end_marker(block)
