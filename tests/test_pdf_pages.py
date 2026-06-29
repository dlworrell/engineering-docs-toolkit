from pathlib import Path

from edt.pdf_pages import page_image_path, pdftoppm_args


def test_page_image_path_is_padded():
    path = page_image_path(Path("out"), 3)
    assert str(path).endswith("page-0003.png")


def test_pdftoppm_args_contains_page_range():
    args = pdftoppm_args(Path("book.pdf"), Path("out/page"), 2, 4)
    assert "-f" in args
    assert "2" in args
    assert "4" in args
