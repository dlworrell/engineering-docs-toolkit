import sqlite3
from pathlib import Path


def init_memory(path: Path) -> None:
    with sqlite3.connect(path) as db:
        db.execute("create table if not exists terms (source text, target text, note text)")


def add_term(path: Path, source: str, target: str, note: str = "") -> None:
    init_memory(path)
    with sqlite3.connect(path) as db:
        db.execute("insert into terms values (?, ?, ?)", (source, target, note))


def lookup_term(path: Path, source: str) -> str | None:
    init_memory(path)
    with sqlite3.connect(path) as db:
        row = db.execute("select target from terms where source = ? limit 1", (source,)).fetchone()
    return None if row is None else str(row[0])
