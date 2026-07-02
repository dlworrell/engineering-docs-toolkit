from edt.layout_model import LayoutBlock, LayoutPage
from edt.semantic_document import SemanticDocument, semantic_page_from_layout
from edt.semantic_to_edom import (
    semantic_document_to_canonical_edom,
    semantic_document_to_edom,
)


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


def test_canonical_edom_removes_page_parents():
    first_page = LayoutPage(page_number=1)
    first_page.add_block(
        LayoutBlock(block_id="p1", kind="paragraph", text="First page.")
    )
    second_page = LayoutPage(page_number=2)
    second_page.add_block(
        LayoutBlock(block_id="p2", kind="paragraph", text="Second page.")
    )
    document = SemanticDocument(
        pages=[
            semantic_page_from_layout(first_page),
            semantic_page_from_layout(second_page),
        ]
    )

    edom = semantic_document_to_canonical_edom(document)

    assert edom.kind == "document"
    assert [child.node_id for child in edom.children] == ["p1", "p2"]
    assert all(child.kind != "page" for child in edom.children)


def test_canonical_edom_preserves_page_provenance():
    page = LayoutPage(page_number=7)
    page.add_block(
        LayoutBlock(block_id="thm7", kind="paragraph", text="Theorem. Result.")
    )
    document = SemanticDocument(pages=[semantic_page_from_layout(page)])

    edom = semantic_document_to_canonical_edom(
        document,
        source_id="primary-pdf",
    )

    theorem = edom.children[0]
    assert theorem.kind == "theorem"
    assert len(theorem.source_regions) == 1
    assert theorem.source_regions[0].source_id == "primary-pdf"
    assert theorem.source_regions[0].page == 7


def test_canonical_edom_applies_reference_metadata():
    page = LayoutPage(page_number=1)
    page.add_block(LayoutBlock(block_id="eq1", kind="equation", text="x = 1 (2.3)"))
    page.add_block(LayoutBlock(block_id="p1", kind="paragraph", text="Equation (2.3) is used here."))
    document = SemanticDocument(pages=[semantic_page_from_layout(page)])
    document.infer_relationships()

    edom = semantic_document_to_canonical_edom(document)

    assert edom.children[1].metadata["references"] == "eq1"
