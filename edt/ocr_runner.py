from pathlib import Path

from .ocr_cache import get_ocr_text, put_ocr_text
from .ocr_engine import OcrEngine, OcrResult


def read_with_cache(engine: OcrEngine, source: Path, cache: Path) -> OcrResult:
    cached = get_ocr_text(cache, source)
    if cached is not None:
        return OcrResult(source=source, text=cached)
    result = engine.read(source)
    put_ocr_text(cache, source, result.text)
    return result
