from dataclasses import dataclass

from .layout_model import LayoutBlock


@dataclass
class SemanticBlock:
    block_id: str
    semantic_kind: str
    text: str
    source_kind: str = ""


def semantic_block_from_layout(block: LayoutBlock, semantic_kind: str) -> SemanticBlock:
    return SemanticBlock(block_id=block.block_id, semantic_kind=semantic_kind, text=block.text, source_kind=block.kind)
