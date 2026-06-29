from pathlib import Path

from edt.tesseract_ocr import TesseractOcrEngine


def test_tesseract_engine_defaults():
    engine = TesseractOcrEngine()
    assert engine.name == "tesseract"
    assert engine.language == "eng"
