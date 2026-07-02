import pytest

from edt.source_region import SourceRegion, SourceRegionError


def test_source_region_round_trip():
    region = SourceRegion("document", page=14, bbox=(72, 310, 522, 650))
    assert SourceRegion.from_dict(region.to_dict()) == region


def test_source_region_optional_coordinates():
    assert SourceRegion("chapters").to_dict() == {"source_id": "chapters"}
    assert SourceRegion("document", page=2).to_dict() == {
        "source_id": "document",
        "page": 2,
    }


def test_source_region_normalizes_bbox_numbers():
    region = SourceRegion.from_dict(
        {"source_id": "document", "page": 3, "bbox": [1, 2.5, 3, 4]}
    )
    assert region.bbox == (1.0, 2.5, 3.0, 4.0)


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"source_id": ""}, "non-empty"),
        ({"source_id": "document", "page": 0}, "at least 1"),
        ({"source_id": "document", "bbox": (10, 0, 5, 20)}, "right"),
        ({"source_id": "document", "bbox": (0, 20, 10, 5)}, "bottom"),
    ],
)
def test_source_region_rejects_invalid_values(kwargs, message):
    with pytest.raises(SourceRegionError, match=message):
        SourceRegion(**kwargs)


def test_source_region_rejects_non_numeric_bbox_payload():
    with pytest.raises(SourceRegionError, match="numeric"):
        SourceRegion.from_dict(
            {"source_id": "document", "bbox": [0, "top", 10, 20]}
        )
