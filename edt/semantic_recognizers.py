from .layout_model import LayoutBlock


PREFIX_KIND = {
    "definition": "definition",
    "theorem": "theorem",
    "lemma": "lemma",
    "corollary": "corollary",
    "proposition": "proposition",
    "proof": "proof",
    "example": "example",
    "exercise": "exercise",
    "algorithm": "algorithm",
    "chapter": "chapter",
    "section": "section",
    "bibliography": "bibliography",
    "index": "index",
}


KIND_KIND = {
    "title": "title",
    "author": "author",
    "heading": "heading",
    "caption": "caption",
    "table": "table",
    "figure": "figure",
    "equation": "equation",
}


def recognize_semantic_kind(block: LayoutBlock) -> str:
    text = block.text.strip().lower()
    for prefix, kind in PREFIX_KIND.items():
        if text.startswith(prefix):
            return kind
    if block.kind in KIND_KIND:
        return KIND_KIND[block.kind]
    return "paragraph"
