from pathlib import Path

from edt.ocr_engine import NullOcrEngine


def test_null_ocr_engine_read():
    result = NullOcrEngine().read(Path("page.png"))
    assert result.text == ""


def test_null_ocr_engine_returns_page():
    page = NullOcrEngine().recognize_image(Path("page.png"), page_number=2)
    assert page.page_number == 2
