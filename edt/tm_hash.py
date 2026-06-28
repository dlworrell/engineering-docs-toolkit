from pathlib import Path

from .hash_cache import hash_text
from .translation_memory import lookup_term


def lookup_text_hash(path: Path, text: str) -> str | None:
    return lookup_term(path, hash_text(text))
