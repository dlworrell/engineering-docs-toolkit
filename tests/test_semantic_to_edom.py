from edt.layout_model import LayoutBlock, LayoutPage
from edt.semantic_document import SemanticDocument, semantic_page_from_layout
from edt.semantic_to_edom import semantic_document_to_edom


def test_semantic_document_to_edom_preserves_semantic_kind():
    page = LayoutPage(page_number=1)
    page.add_block(LayoutBlock(block_id="thm1", kind="paragraph", text="Theorem. A result."))
    document = SemanticDocument(pages=[semantic_page_from_layout(page)])
    edom = semantic_document_to_edom(document)
    assert edom.children[0].children[0].kind == "theorem"
