from pathlib import Path

from .cache_db import cache_get, cache_put
from .hash_cache import hash_file


def get_ocr_text(cache: Path, source: Path) -> str | None:
    return cache_get(cache, hash_file(source))


def put_ocr_text(cache: Path, source: Path, text: str) -> None:
    cache_put(cache, hash_file(source), text)
