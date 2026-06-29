from dataclasses import dataclass, field


@dataclass
class OcrBlock:
    text: str
    confidence: float = 0.0
    bbox: tuple[int, int, int, int] | None = None


@dataclass
class OcrPage:
    page_number: int
    width: int = 0
    height: int = 0
    blocks: list[OcrBlock] = field(default_factory=list)

    @property
    def text(self) -> str:
        return "\n".join(block.text for block in self.blocks)
