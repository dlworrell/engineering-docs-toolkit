from collections.abc import Callable


def cache_key(plugin_id: str, node_id: str, fingerprint: str) -> str:
    return f"{plugin_id}:{node_id}:{fingerprint}"


def cached_execute(cache: dict[str, str], key: str, action: Callable[[], str]) -> str:
    if key not in cache:
        cache[key] = action()
    return cache[key]
