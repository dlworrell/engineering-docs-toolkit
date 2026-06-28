from pathlib import Path

from edt.ocr_engine import OcrEngine


def test_ocr_engine_read():
    result = OcrEngine().read(Path("page.png"))
    assert result.text == ""
