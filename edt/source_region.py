from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class SourceRegionError(ValueError):
    """Raised when source provenance coordinates are invalid."""


@dataclass(frozen=True)
class SourceRegion:
    source_id: str
    page: int | None = None
    bbox: tuple[float, float, float, float] | None = None

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise SourceRegionError("source_id must be a non-empty string")
        if self.page is not None and self.page < 1:
            raise SourceRegionError("page must be at least 1")
        if self.bbox is not None:
            if len(self.bbox) != 4:
                raise SourceRegionError("bbox must contain four coordinates")
            left, top, right, bottom = self.bbox
            if right < left:
                raise SourceRegionError("bbox right must be greater than or equal to left")
            if bottom < top:
                raise SourceRegionError("bbox bottom must be greater than or equal to top")

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {"source_id": self.source_id}
        if self.page is not None:
            payload["page"] = self.page
        if self.bbox is not None:
            payload["bbox"] = list(self.bbox)
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SourceRegion":
        source_id = payload.get("source_id")
        if not isinstance(source_id, str):
            raise SourceRegionError("source_id must be a string")

        page_value = payload.get("page")
        if page_value is not None and type(page_value) is not int:
            raise SourceRegionError("page must be an integer")

        bbox_value = payload.get("bbox")
        bbox: tuple[float, float, float, float] | None = None
        if bbox_value is not None:
            if not isinstance(bbox_value, (list, tuple)) or len(bbox_value) != 4:
                raise SourceRegionError("bbox must contain four numeric coordinates")
            if not all(isinstance(value, (int, float)) for value in bbox_value):
                raise SourceRegionError("bbox coordinates must be numeric")
            bbox = tuple(float(value) for value in bbox_value)

        return cls(source_id=source_id, page=page_value, bbox=bbox)
