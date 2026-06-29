from .accessibility_aria import AriaAnnotation
from .semantic_blocks import SemanticBlock


SEMANTIC_ARIA_ROLES = {
    "title": "heading",
    "chapter": "doc-chapter",
    "section": "doc-part",
    "heading": "heading",
    "figure": "figure",
    "table": "table",
    "equation": "math",
    "proof": "doc-example",
    "theorem": "doc-example",
    "definition": "definition",
    "code_listing": "code",
    "quotation": "blockquote",
    "citation": "doc-biblioentry",
    "bibliography": "doc-bibliography",
    "index": "doc-index",
}


def aria_for_semantic_block(block: SemanticBlock) -> AriaAnnotation:
    role = SEMANTIC_ARIA_ROLES.get(block.semantic_kind, "group")
    return AriaAnnotation(role=role, label=block.text.strip())
