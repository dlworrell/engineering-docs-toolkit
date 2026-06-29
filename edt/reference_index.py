from .semantic_blocks import SemanticBlock


INDEXED_KINDS = {"equation", "figure", "table", "theorem"}


def reference_key_for_block(block: SemanticBlock) -> str:
    if block.semantic_kind == "equation" and (number := block.metadata.get("equation_number", "")):
        return f"equation:{number}"
    number = block.metadata.get("number", "")
    if block.semantic_kind in INDEXED_KINDS and number:
        return f"{block.semantic_kind}:{number}"
    return ""


def build_reference_index(blocks: list[SemanticBlock]) -> dict[str, str]:
    index: dict[str, str] = {}
    for block in blocks:
        key = reference_key_for_block(block)
        if key:
            index[key] = block.block_id
    return index
