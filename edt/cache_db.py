import sqlite3
from pathlib import Path


def init_cache(path: Path) -> None:
    with sqlite3.connect(path) as db:
        db.execute("create table if not exists cache (key text primary key, value text)")


def cache_get(path: Path, key: str) -> str | None:
    init_cache(path)
    with sqlite3.connect(path) as db:
        row = db.execute("select value from cache where key = ?", (key,)).fetchone()
    return None if row is None else str(row[0])


def cache_put(path: Path, key: str, value: str) -> None:
    init_cache(path)
    with sqlite3.connect(path) as db:
        db.execute("insert or replace into cache values (?, ?)", (key, value))
