from .edom import EdomNode
from .edom_reference_metadata import add_reference_metadata
from .reference_exports import resolved_links_from_relationships
from .semantic_blocks import SemanticBlock
from .semantic_document import SemanticDocument, SemanticPage


SEMANTIC_TO_EDOM = {
    "definition": "definition",
    "theorem": "theorem",
    "proof": "proof",
    "example": "example",
    "exercise": "exercise",
    "algorithm": "algorithm",
    "heading": "heading",
    "caption": "caption",
    "table": "table",
    "figure": "figure",
    "equation": "equation",
    "paragraph": "paragraph",
}


def semantic_block_to_edom(block: SemanticBlock) -> EdomNode:
    return EdomNode(kind=SEMANTIC_TO_EDOM.get(block.semantic_kind, "block"), text=block.text, node_id=block.block_id, metadata=dict(block.metadata))


def semantic_page_to_edom(page: SemanticPage) -> EdomNode:
    root = EdomNode(kind="page", node_id=f"page-{page.page_number}")
    for block in page.blocks:
        root.add(semantic_block_to_edom(block))
    return root


def semantic_document_to_edom(document: SemanticDocument) -> EdomNode:
    root = EdomNode(kind="document", node_id="document")
    for page in document.pages:
        root.add(semantic_page_to_edom(page))
    add_reference_metadata(root, resolved_links_from_relationships(document.relationships))
    return root
