from edt.layout_model import LayoutBlock
from edt.semantic_blocks import SemanticBlock, semantic_block_from_layout


def test_semantic_block_from_layout_preserves_text():
    block = LayoutBlock(block_id="b1", kind="paragraph", text="Definition. A ring...")
    semantic = semantic_block_from_layout(block, "definition")
    assert semantic.semantic_kind == "definition"
    assert semantic.text == block.text


def test_semantic_block_metadata_default():
    block = SemanticBlock(block_id="b1", semantic_kind="equation", text="x = 1")
    assert block.metadata == {}
