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
        if "reviewer" not in columns:
            db.execute("alter table terms add column reviewer text default ''")
        if "status" not in columns:
            db.execute("alter table terms add column status text default ''")
        if "confidence" not in columns:
            db.execute("alter table terms add column confidence real default 0")
        if "origin" not in columns:
            db.execute("alter table terms add column origin text default ''")
        if "reviewed_at" not in columns:
            db.execute("alter table terms add column reviewed_at text default ''")


def add_term(path: Path, source: str, target: str, note: str = "") -> None:
    init_memory(path)
    with sqlite3.connect(path) as db:
        db.execute("insert into terms (source, target, note) values (?, ?, ?)", (source, target, note))


def add_term_pair(path: Path, source: str, target: str, source_lang: str, target_lang: str) -> None:
    init_memory(path)
    with sqlite3.connect(path) as db:
        db.execute("insert into terms (source, target, source_lang, target_lang) values (?, ?, ?, ?)", (source, target, source_lang, target_lang))


def add_reviewed_term(path: Path, source: str, target: str, reviewer: str, status: str) -> None:
    init_memory(path)
    with sqlite3.connect(path) as db:
        db.execute("insert into terms (source, target, reviewer, status) values (?, ?, ?, ?)", (source, target, reviewer, status))


def add_quality_term(path: Path, source: str, target: str, confidence: float, origin: str) -> None:
    init_memory(path)
    with sqlite3.connect(path) as db:
        db.execute("insert into terms (source, target, confidence, origin) values (?, ?, ?, ?)", (source, target, confidence, origin))


def lookup_term(path: Path, source: str) -> str | None:
    init_memory(path)
    with sqlite3.connect(path) as db:
        row = db.execute("select target from terms where source = ? limit 1", (source,)).fetchone()
    return None if row is None else str(row[0])


def lookup_term_pair(path: Path, source: str, source_lang: str, target_lang: str) -> str | None:
    init_memory(path)
    with sqlite3.connect(path) as db:
        row = db.execute("select target from terms where source = ? and source_lang = ? and target_lang = ? limit 1", (source, source_lang, target_lang)).fetchone()
    return None if row is None else str(row[0])


def has_term(path: Path, source: str) -> bool:
    return lookup_term(path, source) is not None
