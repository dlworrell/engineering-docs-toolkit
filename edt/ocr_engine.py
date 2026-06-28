from dataclasses import dataclass
from pathlib import Path


@dataclass
class OcrResult:
    source: Path
    text: str


class OcrEngine:
    name = "ocr"

    def read(self, source: Path) -> OcrResult:
        return OcrResult(source=source, text="")
