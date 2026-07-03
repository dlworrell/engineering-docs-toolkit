import pytest

from edt.build import build_project


def test_build_rejects_unsupported_requested_outputs(tmp_path):
    source = tmp_path / "source" / "english"
    source.mkdir(parents=True)
    (source / "01.md").write_text("# Book\n\nBody.\n", encoding="utf-8")
    (tmp_path / "book.yaml").write_text(
        "title: Book\n"
        "source_dir: source/english\n"
        "output_dir: output\n"
        "outputs:\n"
        "  - html\n"
        "  - pdf\n",
        encoding="utf-8",
    )

    with pytest.raises(RuntimeError, match="unsupported requested outputs: pdf"):
        build_project(tmp_path)

    assert not (tmp_path / "output").exists()
