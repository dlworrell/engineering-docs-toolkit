from edt.init_project import init_project


def test_init_project_creates_book_yaml(tmp_path):
    init_project(tmp_path)
    assert (tmp_path / "book.yaml").exists()
    assert (tmp_path / "source" / "english").exists()
