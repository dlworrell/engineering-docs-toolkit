from edt.semantic_blocks import SemanticBlock
from edt.semantic_relationships import link_adjacent_proofs


def test_link_adjacent_theorem_to_proof():
    theorem = SemanticBlock(block_id="thm1", semantic_kind="theorem", text="Theorem.")
    proof = SemanticBlock(block_id="proof1", semantic_kind="proof", text="Proof.")
    result = link_adjacent_proofs([theorem, proof])
    assert result[0].source_id == "thm1"
    assert result[0].target_id == "proof1"
