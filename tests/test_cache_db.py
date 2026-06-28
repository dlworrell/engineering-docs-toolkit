from edt.cache_db import cache_get, cache_put


def test_cache_round_trip(tmp_path):
    db = tmp_path / "cache.sqlite"
    cache_put(db, "abc", "value")
    assert cache_get(db, "abc") == "value"
    assert cache_get(db, "missing") is None
