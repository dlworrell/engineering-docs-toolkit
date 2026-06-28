import hashlib
from pathlib import Path


def hash_bytes(data: bytes, algorithm: str = "blake2b") -> str:
    if algorithm == "sha256":
        return hashlib.sha256(data).hexdigest()
    return hashlib.blake2b(data, digest_size=32).hexdigest()


def hash_text(text: str, algorithm: str = "blake2b") -> str:
    return hash_bytes(text.encode("utf-8"), algorithm)


def hash_file(path: Path, algorithm: str = "blake2b") -> str:
    return hash_bytes(path.read_bytes(), algorithm)
