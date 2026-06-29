from pathlib import Path

from edt.pdf_pages import page_image_path


def test_page_image_path_is_padded():
    path = page_image_path(Path("out"), 3)
    assert str(path).endswith("page-0003.png")
