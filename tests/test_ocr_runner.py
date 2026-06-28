from pathlib import Path

from edt.ocr_engine import OcrEngine, OcrResult
from edt.ocr_runner import read_with_cache


class StaticEngine(OcrEngine):
    def read(self, source: Path) -> OcrResult:
        return OcrResult(source=source, text="text")


def test_read_with_cache(tmp_path):
    page = tmp_path / "page.txt"
    page.write_text("image", encoding="utf-8")
    result = read_with_cache(StaticEngine(), page, tmp_path / "cache.sqlite")
    assert result.text == "text"
