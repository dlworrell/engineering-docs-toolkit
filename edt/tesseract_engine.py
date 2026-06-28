from pathlib import Path

from .ocr_engine import OcrEngine, OcrResult


class TesseractEngine(OcrEngine):
    name = "tesseract"

    def read(self, source: Path) -> OcrResult:
        return OcrResult(source=source, text="")
