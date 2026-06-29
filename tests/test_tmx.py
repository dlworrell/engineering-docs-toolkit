from edt.tmx import export_tmx, import_tmx
from edt.translation_memory import add_term_pair


def test_export_tmx(tmp_path):
    db = tmp_path / "memory.sqlite"
    out = tmp_path / "memory.tmx"
    add_term_pair(db, "A", "B", "sv", "en")
    export_tmx(db, out)
    assert "<tmx" in out.read_text(encoding="utf-8")


def test_import_tmx_skeleton(tmp_path):
    source = tmp_path / "source.tmx"
    db = tmp_path / "memory.sqlite"
    source.write_text("<tmx><body /></tmx>", encoding="utf-8")
    import_tmx(source, db)
    assert db.exists()
