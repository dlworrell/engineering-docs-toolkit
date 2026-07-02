from pathlib import Path

import pytest

from edt.source_asset import SourceAsset, SourceAssetError


def test_source_asset_from_path(tmp_path):
    path = tmp_path / "chapter.md"
    path.write_text("# Chapter\n", encoding="utf-8")

    asset = SourceAsset.from_path("chapters", path)

    assert asset.source_id == "chapters"
    assert asset.path == path
    assert asset.media_type == "text/markdown"
    assert asset.size_bytes == len("# Chapter\n".encode("utf-8"))
    assert len(asset.sha256) == 64
    assert SourceAsset.from_dict(asset.to_dict()) == asset


def test_source_asset_allows_explicit_media_type(tmp_path):
    path = tmp_path / "source.bin"
    path.write_bytes(b"abc")

    asset = SourceAsset.from_path(
        "primary",
        path,
        media_type="application/pdf",
    )

    assert asset.media_type == "application/pdf"


def test_source_asset_uses_octet_stream_for_unknown_extension(tmp_path):
    path = tmp_path / "source.unknown-extension"
    path.write_bytes(b"abc")

    asset = SourceAsset.from_path("primary", path)

    assert asset.media_type == "application/octet-stream"


def test_source_asset_rejects_missing_file(tmp_path):
    with pytest.raises(SourceAssetError, match="does not exist"):
        SourceAsset.from_path("primary", tmp_path / "missing.pdf")


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        (
            {
                "source_id": "",
                "path": Path("source.pdf"),
                "media_type": "application/pdf",
                "sha256": "0" * 64,
                "size_bytes": 1,
            },
            "source_id",
        ),
        (
            {
                "source_id": "primary",
                "path": Path("source.pdf"),
                "media_type": "application/pdf",
                "sha256": "bad",
                "size_bytes": 1,
            },
            "sha256",
        ),
        (
            {
                "source_id": "primary",
                "path": Path("source.pdf"),
                "media_type": "application/pdf",
                "sha256": "0" * 64,
                "size_bytes": -1,
            },
            "size_bytes",
        ),
    ],
)
def test_source_asset_rejects_invalid_values(kwargs, message):
    with pytest.raises(SourceAssetError, match=message):
        SourceAsset(**kwargs)
