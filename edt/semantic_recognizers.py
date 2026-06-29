from .layout_model import LayoutBlock


PREFIX_KIND = {
    "definition": "definition",
    "theorem": "theorem",
    "proof": "proof",
    "example": "example",
    "exercise": "exercise",
    "algorithm": "algorithm",
}


def recognize_semantic_kind(block: LayoutBlock) -> str:
    text = block.text.strip().lower()
    for prefix, kind in PREFIX_KIND.items():
        if text.startswith(prefix):
            return kind
    if block.kind in {"heading", "caption", "table", "figure", "equation"}:
        return block.kind
    return "paragraph"
