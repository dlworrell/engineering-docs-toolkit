from pathlib import Path

from edt.tesseract_engine import TesseractEngine


def test_tesseract_engine_name():
    engine = TesseractEngine()
    assert engine.name == "tesseract"


def test_tesseract_engine_read():
    result = TesseractEngine().read(Path("page.png"))
    assert result.text == ""
