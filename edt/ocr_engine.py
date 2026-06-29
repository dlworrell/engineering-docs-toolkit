from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from .ocr_model import OcrPage


@dataclass
class OcrResult:
    source: Path
    text: str


class OcrEngine(Protocol):
    def recognize_image(self, image_path: Path, page_number: int = 1) -> OcrPage:
        ...


class NullOcrEngine:
    name = "ocr"

    def recognize_image(self, image_path: Path, page_number: int = 1) -> OcrPage:
        return OcrPage(page_number=page_number)

    def read(self, source: Path) -> OcrResult:
        return OcrResult(source=source, text="")
