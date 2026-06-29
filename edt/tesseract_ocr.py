import subprocess
from pathlib import Path

from .ocr_model import OcrBlock, OcrPage


class TesseractOcrEngine:
    name = "tesseract"

    def __init__(self, command: str = "tesseract", language: str = "eng") -> None:
        self.command = command
        self.language = language

    def recognize_image(self, image_path: Path, page_number: int = 1) -> OcrPage:
        result = subprocess.run(
            [self.command, str(image_path), "stdout", "-l", self.language],
            check=True,
            capture_output=True,
            text=True,
        )
        page = OcrPage(page_number=page_number)
        page.blocks.append(OcrBlock(text=result.stdout.strip()))
        return page
