from edt.epub_accessibility import EpubAccessibilityMetadata


def test_epub_accessibility_package_metadata():
    metadata = EpubAccessibilityMetadata(summary="Readable", access_modes=["textual"])
    package = metadata.package_metadata()
    assert package["accessibilitySummary"] == "Readable"
    assert "textual" in package["accessMode"]
