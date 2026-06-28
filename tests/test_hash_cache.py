from edt.hash_cache import hash_file, hash_text


def test_hash_text_stable():
    assert hash_text("abc") == hash_text("abc")


def test_hash_file_stable(tmp_path):
    path = tmp_path / "x.txt"
    path.write_text("abc", encoding="utf-8")
    assert hash_file(path) == hash_file(path)
