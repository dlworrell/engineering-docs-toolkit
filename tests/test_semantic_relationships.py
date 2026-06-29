from edt.semantic_blocks import SemanticBlock
from edt.semantic_relationships import infer_semantic_relationships, link_adjacent_captions, link_adjacent_proofs


def test_link_adjacent_theorem_to_proof():
    theorem = SemanticBlock(block_id="thm1", semantic_kind="theorem", text="Theorem.")
    proof = SemanticBlock(block_id="proof1", semantic_kind="proof", text="Proof.")
    result = link_adjacent_proofs([theorem, proof])
    assert result[0].source_id == "thm1"
    assert result[0].target_id == "proof1"


def test_link_adjacent_figure_to_caption():
    figure = SemanticBlock(block_id="fig1", semantic_kind="figure", text="")
    caption = SemanticBlock(block_id="cap1", semantic_kind="caption", text="Figure 1. Engine")
    result = link_adjacent_captions([figure, caption])
    assert result[0].relationship == "has_caption"
    assert result[0].target_id == "cap1"


def test_infer_semantic_relationships_combines_relationships():
    theorem = SemanticBlock(block_id="thm1", semantic_kind="theorem", text="Theorem.")
    proof = SemanticBlock(block_id="proof1", semantic_kind="proof", text="Proof.")
    figure = SemanticBlock(block_id="fig1", semantic_kind="figure", text="")
    caption = SemanticBlock(block_id="cap1", semantic_kind="caption", text="Figure 1. Engine")
    result = infer_semantic_relationships([theorem, proof, figure, caption])
    assert {relationship.relationship for relationship in result} == {"has_proof", "has_caption"}
