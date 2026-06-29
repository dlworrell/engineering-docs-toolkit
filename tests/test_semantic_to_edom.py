from edt.layout_model import LayoutBlock, LayoutPage
from edt.semantic_document import SemanticDocument, semantic_page_from_layout
from edt.semantic_to_edom import semantic_document_to_edom


def test_semantic_document_to_edom_preserves_semantic_kind():
    page = LayoutPage(page_number=1)
    page.add_block(LayoutBlock(block_id="thm1", kind="paragraph", text="Theorem. A result."))
    document = SemanticDocument(pages=[semantic_page_from_layout(page)])
    edom = semantic_document_to_edom(document)
    assert edom.children[0].children[0].kind == "theorem"


def test_semantic_document_to_edom_preserves_metadata():
    page = LayoutPage(page_number=1)
    page.add_block(LayoutBlock(block_id="eq1", kind="equation", text="x = 1 (2.3)"))
    document = SemanticDocument(pages=[semantic_page_from_layout(page)])
    edom = semantic_document_to_edom(document)
    assert edom.children[0].children[0].metadata["equation_number"] == "2.3"


def test_semantic_document_to_edom_applies_reference_metadata():
    page = LayoutPage(page_number=1)
    page.add_block(LayoutBlock(block_id="eq1", kind="equation", text="x = 1 (2.3)"))
    page.add_block(LayoutBlock(block_id="p1", kind="paragraph", text="Equation (2.3) is used here."))
    document = SemanticDocument(pages=[semantic_page_from_layout(page)])
    document.infer_relationships()
    edom = semantic_document_to_edom(document)
    paragraph = edom.children[0].children[1]
    assert paragraph.metadata["references"] == "eq1"
