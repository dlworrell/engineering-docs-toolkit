from pathlib import Path

from .cache_db import cache_get, cache_put
from .hash_cache import hash_file


def file_changed(cache: Path, path: Path) -> bool:
    digest = hash_file(path)
    key = str(path)
    return cache_get(cache, key) != digest


def remember_file(cache: Path, path: Path) -> None:
    cache_put(cache, str(path), hash_file(path))
