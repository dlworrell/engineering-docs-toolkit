from edt.layout_model import LayoutBlock
from edt.semantic_recognizers import recognize_semantic_kind


def test_recognize_definition_prefix():
    block = LayoutBlock(block_id="b1", kind="paragraph", text="Definition. A group is ...")
    assert recognize_semantic_kind(block) == "definition"


def test_recognize_heading_kind():
    block = LayoutBlock(block_id="h1", kind="heading", text="Chapter 1")
    assert recognize_semantic_kind(block) == "heading"
