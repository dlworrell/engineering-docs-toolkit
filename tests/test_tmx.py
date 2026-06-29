from edt.tmx import export_tmx, import_tmx
from edt.translation_memory import add_term_pair


def test_export_tmx(tmp_path):
    db = tmp_path / "memory.sqlite"
    out = tmp_path / "memory.tmx"
    add_term_pair(db, "A", "B", "sv", "en")
    export_tmx(db, out)
    assert "<tmx" in out.read_text(encoding="utf-8")
