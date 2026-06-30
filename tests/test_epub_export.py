import zipfile

from edt.epub_export import write_epub


def test_write_epub_creates_epub_package(tmp_path):
    document = tmp_path / "document.edom.json"
    document.write_text(
        '{"root":{"id":"document","kind":"document","children":[{"id":"page-1","kind":"page","children":[{"id":"h1","kind":"heading","text":"HERKULES","children":[]}]}]}}',
        encoding="utf-8",
    )
    output = tmp_path / "book.epub"

    write_epub(document, output, title="HERKULES")

    assert output.exists()
    with zipfile.ZipFile(output) as archive:
        names = archive.namelist()
        assert names[0] == "mimetype"
        assert archive.read("mimetype") == b"application/epub+zip"
        assert "META-INF/container.xml" in names
        assert "OEBPS/content.opf" in names
        assert "OEBPS/nav.xhtml" in names
        assert "OEBPS/index.xhtml" in names
        assert "OEBPS/stylesheet.css" in names
        assert b"HERKULES" in archive.read("OEBPS/index.xhtml")
