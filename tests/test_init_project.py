from edt.config import load_project_config
from edt.init_project import init_project


def test_init_project_creates_book_yaml(tmp_path):
    init_project(tmp_path)

    assert (tmp_path / "book.yaml").exists()
    assert (tmp_path / "edt.toml").exists()
    assert (tmp_path / "source" / "english").exists()
    assert (tmp_path / "source" / "original").exists()

    config = load_project_config(tmp_path)
    pdf_source = config.first_source("pdf")
    markdown_source = config.first_source("markdown")

    assert pdf_source is not None
    assert pdf_source.source_id == "primary"
    assert str(pdf_source.path) == "source/original/document.pdf"
    assert markdown_source is not None
    assert str(markdown_source.path) == "source/english"
