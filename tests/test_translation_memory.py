import sqlite3

from edt.translation_memory import add_quality_term, add_reviewed_term, add_term, add_term_pair, has_term, init_memory, lookup_term, lookup_term_pair


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


def test_has_term(tmp_path):
    db = tmp_path / "memory.sqlite"
    add_term(db, "A", "B")
    assert has_term(db, "A")


def test_lookup_missing(tmp_path):
    db = tmp_path / "memory.sqlite"
    assert lookup_term(db, "A") is None


def test_language_columns(tmp_path):
    db = tmp_path / "memory.sqlite"
    init_memory(db)
    with sqlite3.connect(db) as conn:
        names = [row[1] for row in conn.execute("pragma table_info(terms)")]
    assert "source_lang" in names


def test_add_term_pair(tmp_path):
    db = tmp_path / "memory.sqlite"
    add_term_pair(db, "A", "B", "sv", "en")
    with sqlite3.connect(db) as conn:
        rows = conn.execute("select source_lang, target_lang from terms").fetchall()
    assert rows == [("sv", "en")]


def test_lookup_term_pair(tmp_path):
    db = tmp_path / "memory.sqlite"
    add_term_pair(db, "A", "B", "sv", "en")
    assert lookup_term_pair(db, "A", "sv", "en") == "B"


def test_review_columns(tmp_path):
    db = tmp_path / "memory.sqlite"
    init_memory(db)
    with sqlite3.connect(db) as conn:
        names = [row[1] for row in conn.execute("pragma table_info(terms)")]
    assert "reviewer" in names


def test_add_reviewed_term(tmp_path):
    db = tmp_path / "memory.sqlite"
    add_reviewed_term(db, "A", "B", "D", "approved")
    with sqlite3.connect(db) as conn:
        rows = conn.execute("select reviewer, status from terms").fetchall()
    assert rows == [("D", "approved")]


def test_quality_columns(tmp_path):
    db = tmp_path / "memory.sqlite"
    init_memory(db)
    with sqlite3.connect(db) as conn:
        names = [row[1] for row in conn.execute("pragma table_info(terms)")]
    assert "confidence" in names


def test_add_quality_term(tmp_path):
    db = tmp_path / "memory.sqlite"
    add_quality_term(db, "A", "B", 0.9, "mt")
    with sqlite3.connect(db) as conn:
        rows = conn.execute("select confidence, origin from terms").fetchall()
    assert rows == [(0.9, "mt")]
