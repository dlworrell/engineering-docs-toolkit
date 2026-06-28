from edt.incremental import file_changed, remember_file


def test_incremental_cache(tmp_path):
    cache = tmp_path / "cache.sqlite"
    doc = tmp_path / "doc.txt"
    doc.write_text("one", encoding="utf-8")
    assert file_changed(cache, doc)
    remember_file(cache, doc)
    assert not file_changed(cache, doc)
