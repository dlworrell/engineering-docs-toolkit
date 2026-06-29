import sqlite3
from pathlib import Path


def init_memory(path: Path) -> None:
    with sqlite3.connect(path) as db:
        db.execute("create table if not exists terms (source text, target text, note text)")
        columns = {row[1] for row in db.execute("pragma table_info(terms)").fetchall()}
        if "source_lang" not in columns:
            db.execute("alter table terms add column source_lang text default ''")
        if "target_lang" not in columns:
            db.execute("alter table terms add column target_lang text default ''")


def add_term(path: Path, source: str, target: str, note: str = "") -> None:
    init_memory(path)
    with sqlite3.connect(path) as db:
        db.execute("insert into terms (source, target, note) values (?, ?, ?)", (source, target, note))


def add_term_pair(path: Path, source: str, target: str, source_lang: str, target_lang: str) -> None:
    init_memory(path)
    with sqlite3.connect(path) as db:
        db.execute("insert into terms (source, target, source_lang, target_lang) values (?, ?, ?, ?)", (source, target, source_lang, target_lang))


def lookup_term(path: Path, source: str) -> str | None:
    init_memory(path)
    with sqlite3.connect(path) as db:
        row = db.execute("select target from terms where source = ? limit 1", (source,)).fetchone()
    return None if row is None else str(row[0])


def has_term(path: Path, source: str) -> bool:
    return lookup_term(path, source) is not None
