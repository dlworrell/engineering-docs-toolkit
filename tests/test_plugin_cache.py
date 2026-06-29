from edt.plugin_cache import cache_key, cached_execute


def test_cache_key_contains_plugin_id():
    key = cache_key("plugin-a", "node-a", "hash-a")
    assert key.startswith("plugin-a:")
