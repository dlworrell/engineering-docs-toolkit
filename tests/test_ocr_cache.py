from edt.ocr_cache import get_ocr_text, put_ocr_text


def test_ocr_cache_round_trip(tmp_path):
    cache = tmp_path / "cache.sqlite"
    page = tmp_path / "page.txt"
    page.write_text("image", encoding="utf-8")
    put_ocr_text(cache, page, "text")
    assert get_ocr_text(cache, page) == "text"
