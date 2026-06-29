from edt.plugin_cache import cache_key, cached_execute


def test_cache_key_contains_plugin_id():
    key = cache_key("plugin-a", "node-a", "hash-a")
    assert key.startswith("plugin-a:")


def test_cached_execute_reuses_value():
    cache = {}
    calls = []

    def action():
        calls.append("called")
        return "result"

    key = cache_key("plugin-a", "node-a", "hash-a")
    first = cached_execute(cache, key, action)
    second = cached_execute(cache, key, action)
    assert first == second
    assert len(calls) == 1
