import sqlite3

from edt.tmx import export_tmx, import_tmx
from edt.translation_memory import add_term_pair


def round_trip(tmp_path, text: str) -> str:
    source_db = tmp_path / "source.sqlite"
    out = tmp_path / "memory.tmx"
    target_db = tmp_path / "target.sqlite"
    add_term_pair(source_db, text, "ok", "und", "en")
    export_tmx(source_db, out)
    import_tmx(out, target_db)
    with sqlite3.connect(target_db) as conn:
        return conn.execute("select source from terms").fetchone()[0]


def test_tmx_round_trips_emoji(tmp_path):
    assert round_trip(tmp_path, "wrench 🔧") == "wrench 🔧"


def test_tmx_round_trips_supplementary_plane(tmp_path):
    text = "supplementary " + chr(0x1D11E)
    assert round_trip(tmp_path, text) == text


def test_tmx_round_trips_unicode_mark_sequence(tmp_path):
    mark = "\\u0301".encode("ascii").decode("unicode_escape")
    text = "unicode e" + mark
    assert round_trip(tmp_path, text) == text
