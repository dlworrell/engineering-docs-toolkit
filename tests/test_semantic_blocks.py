from edt.layout_model import LayoutBlock
from edt.semantic_blocks import semantic_block_from_layout


def test_semantic_block_from_layout_preserves_text():
    block = LayoutBlock(block_id="b1", kind="paragraph", text="Definition. A ring...")
    semantic = semantic_block_from_layout(block, "definition")
    assert semantic.semantic_kind == "definition"
    assert semantic.text == block.text
