from xml.etree import ElementTree as ET

from edt.tmx import export_tmx, import_tmx, parse_tmx_units, tmx_date, tmx_header, tmx_lang, validate_tmx
from edt.translation_memory import add_term_pair, lookup_term


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


def test_parse_tmx_units(tmp_path):
    source = tmp_path / "source.tmx"
    source.write_text("<tmx><body><tu><tuv><seg>A</seg></tuv><tuv><seg>B</seg></tuv></tu></body></tmx>", encoding="utf-8")
    assert parse_tmx_units(source) == [("A", "B")]


def test_import_tmx_stores_units(tmp_path):
    source = tmp_path / "source.tmx"
    db = tmp_path / "memory.sqlite"
    source.write_text("<tmx><body><tu><tuv><seg>A</seg></tuv><tuv><seg>B</seg></tuv></tu></body></tmx>", encoding="utf-8")
    import_tmx(source, db)
    assert lookup_term(db, "A") == "B"


def test_tmx_header_builder():
    assert "creationtool" in tmx_header("sv-SE")


def test_tmx_language_reader():
    element = ET.fromstring('<tuv xml:lang="en-US" />')
    assert tmx_lang(element) == "en-US"


def test_tmx_date_helper():
    assert tmx_date().endswith("Z")


def test_tmx_header_dates():
    assert "creationdate" in tmx_header()


def test_tmx_header_required_attrs():
    header = tmx_header()
    assert "o-tmf" in header
