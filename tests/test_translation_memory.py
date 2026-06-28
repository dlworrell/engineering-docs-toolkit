import sqlite3

from edt.translation_memory import add_term, init_memory, lookup_term


def test_translation_memory_add_term(tmp_path):
    db = tmp_path / "memory.sqlite"
    init_memory(db)
    add_term(db, "Motorblock", "Engine block")
    with sqlite3.connect(db) as conn:
        rows = conn.execute("select source, target from terms").fetchall()
    assert rows == [("Motorblock", "Engine block")]
