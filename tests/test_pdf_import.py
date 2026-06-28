from edt.pdf_import import import_pdf


def test_import_pdf_writes_notes(tmp_path):
    result = import_pdf(tmp_path / "book.pdf", tmp_path / "out")
    assert result.output.exists()
    assert (tmp_path / "out" / "import-notes.md").exists()
