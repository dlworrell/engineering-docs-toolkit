from .equation_numbers import equation_number
from .layout_model import LayoutBlock
from .proof_markers import proof_end_marker
from .semantic_blocks import SemanticBlock, semantic_block_from_layout


def semantic_metadata_for_layout(block: LayoutBlock, semantic_kind: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    if semantic_kind == "equation" and (number := equation_number(block)):
        metadata["equation_number"] = number
    if semantic_kind == "proof" and (marker := proof_end_marker(block)):
        metadata["proof_end_marker"] = marker
    return metadata


def semantic_block_with_metadata(block: LayoutBlock, semantic_kind: str) -> SemanticBlock:
    semantic = semantic_block_from_layout(block, semantic_kind)
    semantic.metadata.update(semantic_metadata_for_layout(block, semantic_kind))
    return semantic
