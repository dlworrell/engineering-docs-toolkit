from pathlib import Path
from types import SimpleNamespace

from edt.tesseract_ocr import TesseractOcrEngine


def test_tesseract_engine_defaults():
    engine = TesseractOcrEngine()
    assert engine.name == "tesseract"
    assert engine.language == "eng"


def test_tesseract_engine_calls_runner(monkeypatch):
    calls = []

    def fake_run(args, check, capture_output, text):
        calls.append(args)
        return SimpleNamespace(stdout="Hello\n")

    monkeypatch.setattr("edt.tesseract_ocr.subprocess.run", fake_run)
    page = TesseractOcrEngine().recognize_image(Path("page.png"))
    assert page.text == "Hello"
    assert calls[0][0] == "tesseract"
