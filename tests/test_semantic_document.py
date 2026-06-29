from edt.layout_model import LayoutBlock, LayoutPage
from edt.semantic_document import SemanticDocument, semantic_page_from_layout


def test_semantic_page_from_layout_recognizes_blocks():
    page = LayoutPage(page_number=1)
    page.add_block(LayoutBlock(block_id="d1", kind="paragraph", text="Definition. A set..."))
    semantic = semantic_page_from_layout(page)
    assert semantic.blocks[0].semantic_kind == "definition"


def test_semantic_document_flattens_blocks():
    page = LayoutPage(page_number=1)
    page.add_block(LayoutBlock(block_id="p1", kind="paragraph", text="Text"))
    doc = SemanticDocument(pages=[semantic_page_from_layout(page)])
    assert len(doc.blocks) == 1
