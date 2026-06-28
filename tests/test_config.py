from edt.config import load_config


def test_load_title(tmp_path):
    (tmp_path / "book.yaml").write_text("title: Test Book\n", encoding="utf-8")
    assert load_config(tmp_path).title == "Test Book"


def test_load_outputs(tmp_path):
    (tmp_path / "book.yaml").write_text("outputs:\n  - html\n  - epub\n", encoding="utf-8")
    assert load_config(tmp_path).outputs == ["html", "epub"]
