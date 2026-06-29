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


def test_semantic_page_from_layout_adds_equation_metadata():
    page = LayoutPage(page_number=1)
    page.add_block(LayoutBlock(block_id="eq1", kind="equation", text="x = 1 (2.3)"))
    semantic = semantic_page_from_layout(page)
    assert semantic.blocks[0].metadata["equation_number"] == "2.3"


def test_semantic_document_infers_proof_relationships():
    page = LayoutPage(page_number=1)
    page.add_block(LayoutBlock(block_id="thm1", kind="paragraph", text="Theorem. A result."))
    page.add_block(LayoutBlock(block_id="proof1", kind="paragraph", text="Proof. Therefore."))
    doc = SemanticDocument(pages=[semantic_page_from_layout(page)])
    relationships = doc.infer_relationships()
    assert relationships[0].relationship == "has_proof"


def test_semantic_document_resolves_reference_relationships():
    page = LayoutPage(page_number=1)
    page.add_block(LayoutBlock(block_id="eq1", kind="equation", text="x = 1 (2.3)"))
    page.add_block(LayoutBlock(block_id="p1", kind="paragraph", text="Equation (2.3) is used here."))
    doc = SemanticDocument(pages=[semantic_page_from_layout(page)])
    relationships = doc.infer_relationships()
    assert any(rel.relationship == "references" and rel.target_id == "eq1" for rel in relationships)
