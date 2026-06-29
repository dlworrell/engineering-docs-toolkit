from dataclasses import dataclass, field


BBox = tuple[int, int, int, int]


@dataclass
class LayoutBlock:
    block_id: str
    kind: str
    text: str = ""
    bbox: BBox | None = None
    confidence: float = 0.0


@dataclass
class LayoutPage:
    page_number: int
    width: int = 0
    height: int = 0
    blocks: list[LayoutBlock] = field(default_factory=list)

    def add_block(self, block: LayoutBlock) -> LayoutBlock:
        self.blocks.append(block)
        return block
