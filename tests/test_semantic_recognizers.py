from edt.layout_model import LayoutBlock
from edt.semantic_recognizers import recognize_semantic_kind


def test_recognize_definition_prefix():
    block = LayoutBlock(block_id="b1", kind="paragraph", text="Definition. A group is ...")
    assert recognize_semantic_kind(block) == "definition"


def test_recognize_heading_kind():
    block = LayoutBlock(block_id="h1", kind="heading", text="Chapter 1")
    assert recognize_semantic_kind(block) == "heading"


def test_recognize_chapter_prefix():
    block = LayoutBlock(block_id="c1", kind="paragraph", text="Chapter 1 Introduction")
    assert recognize_semantic_kind(block) == "chapter"


def test_recognize_bibliography_prefix():
    block = LayoutBlock(block_id="biblio", kind="paragraph", text="Bibliography")
    assert recognize_semantic_kind(block) == "bibliography"


def test_recognize_lemma_prefix():
    block = LayoutBlock(block_id="lem1", kind="paragraph", text="Lemma. Let x be...")
    assert recognize_semantic_kind(block) == "lemma"


def test_recognize_corollary_prefix():
    block = LayoutBlock(block_id="cor1", kind="paragraph", text="Corollary 2.1")
    assert recognize_semantic_kind(block) == "corollary"
