import re

from .semantic_blocks import SemanticBlock


NUMBER_RE = re.compile(r"\b(?P<kind>Figure|Table|Theorem)\s+(?P<number>\d+(?:\.\d+)*)", re.IGNORECASE)


def reference_number_from_text(text: str, semantic_kind: str) -> str:
    for match in NUMBER_RE.finditer(text):
        if match.group("kind").lower() == semantic_kind.lower():
            return match.group("number")
    return ""


def add_reference_number_metadata(block: SemanticBlock) -> SemanticBlock:
    if "number" not in block.metadata and block.semantic_kind in {"figure", "table", "theorem"}:
        number = reference_number_from_text(block.text, block.semantic_kind)
        if number:
            block.metadata["number"] = number
    return block
