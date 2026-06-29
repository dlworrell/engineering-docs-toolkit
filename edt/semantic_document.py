from dataclasses import dataclass, field

from .layout_model import LayoutPage
from .reading_order import top_left_order
from .semantic_blocks import SemanticBlock
from .semantic_metadata import semantic_block_with_metadata
from .semantic_recognizers import recognize_semantic_kind
from .semantic_relationships import SemanticRelationship, infer_semantic_relationships


@dataclass
class SemanticPage:
    page_number: int
    blocks: list[SemanticBlock] = field(default_factory=list)


@dataclass
class SemanticDocument:
    pages: list[SemanticPage] = field(default_factory=list)
    relationships: list[SemanticRelationship] = field(default_factory=list)

    @property
    def blocks(self) -> list[SemanticBlock]:
        return [block for page in self.pages for block in page.blocks]

    def infer_relationships(self) -> list[SemanticRelationship]:
        self.relationships = infer_semantic_relationships(self.blocks)
        return self.relationships


def semantic_page_from_layout(page: LayoutPage) -> SemanticPage:
    semantic = SemanticPage(page_number=page.page_number)
    for block in top_left_order(page.blocks):
        kind = recognize_semantic_kind(block)
        semantic.blocks.append(semantic_block_with_metadata(block, kind))
    return semantic
