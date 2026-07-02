from __future__ import annotations

import mimetypes
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .hash_cache import hash_file


class SourceAssetError(ValueError):
    """Raised when source asset metadata is invalid."""


@dataclass(frozen=True)
class SourceAsset:
    source_id: str
    path: Path
    media_type: str
    sha256: str
    size_bytes: int

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise SourceAssetError("source_id must be a non-empty string")
        if not str(self.path):
            raise SourceAssetError("path must be non-empty")
        if not self.media_type.strip():
            raise SourceAssetError("media_type must be a non-empty string")
        if len(self.sha256) != 64 or any(
            character not in "0123456789abcdef" for character in self.sha256
        ):
            raise SourceAssetError("sha256 must be a lowercase 64-character hex digest")
        if self.size_bytes < 0:
            raise SourceAssetError("size_bytes must not be negative")

    @classmethod
    def from_path(
        cls,
        source_id: str,
        path: Path,
        media_type: str | None = None,
    ) -> "SourceAsset":
        if not path.is_file():
            raise SourceAssetError(f"source asset does not exist: {path}")

        detected_type = media_type or mimetypes.guess_type(path.name)[0]
        return cls(
            source_id=source_id,
            path=path,
            media_type=detected_type or "application/octet-stream",
            sha256=hash_file(path, "sha256"),
            size_bytes=path.stat().st_size,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "source_id": self.source_id,
            "path": self.path.as_posix(),
            "media_type": self.media_type,
            "sha256": self.sha256,
            "size_bytes": self.size_bytes,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SourceAsset":
        source_id = payload.get("source_id")
        path = payload.get("path")
        media_type = payload.get("media_type")
        sha256 = payload.get("sha256")
        size_bytes = payload.get("size_bytes")

        if not isinstance(source_id, str):
            raise SourceAssetError("source_id must be a string")
        if not isinstance(path, str):
            raise SourceAssetError("path must be a string")
        if not isinstance(media_type, str):
            raise SourceAssetError("media_type must be a string")
        if not isinstance(sha256, str):
            raise SourceAssetError("sha256 must be a string")
        if type(size_bytes) is not int:
            raise SourceAssetError("size_bytes must be an integer")

        return cls(
            source_id=source_id,
            path=Path(path),
            media_type=media_type,
            sha256=sha256,
            size_bytes=size_bytes,
        )
