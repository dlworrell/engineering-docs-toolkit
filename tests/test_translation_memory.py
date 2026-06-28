import sqlite3

from edt.translation_memory import add_term, init_memory, lookup_term


def test_translation_memory_add_term(tmp_path):
    db = tmp_path / "memory.sqlite"
    init_memory(db)
    add_term(db, "A", "B")
    with sqlite3.connect(db) as conn:
        rows = conn.execute("select source, target from terms").fetchall()
    assert rows == [("A", "B")]


def test_lookup_term(tmp_path):
    db = tmp_path / "memory.sqlite"
    add_term(db, "A", "B")
    assert lookup_term(db, "A") == "B"
