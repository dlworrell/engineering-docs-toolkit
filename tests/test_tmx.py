from xml.etree import ElementTree as ET
import sqlite3

from edt.tmx import child_elements, export_tmx, import_tmx, parse_tmx_props, parse_tmx_units, parse_tmx_units_with_props, tmx_date, tmx_header, tmx_lang, tmx_prop, validate_tmx, xml_name
from edt.translation_memory import add_reviewed_term, add_term_pair, lookup_term


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


def test_validate_tmx_ok(tmp_path):
    source = tmp_path / "source.tmx"
    source.write_text("<tmx><body /></tmx>", encoding="utf-8")
    assert validate_tmx(source) == []


def test_validate_tmx_body(tmp_path):
    source = tmp_path / "source.tmx"
    source.write_text("<tmx />", encoding="utf-8")
    assert validate_tmx(source) == ["missing-body"]


def test_validate_tmx_segments(tmp_path):
    source = tmp_path / "source.tmx"
    source.write_text("<tmx><body><tu /></body></tmx>", encoding="utf-8")
    assert validate_tmx(source) == ["missing-seg"]


def test_tmx_property_writer():
    assert tmx_prop("status", "approved") == '<prop type="status">approved</prop>'


def test_export_tmx_metadata_props(tmp_path):
    db = tmp_path / "memory.sqlite"
    out = tmp_path / "memory.tmx"
    add_reviewed_term(db, "A", "B", "D", "approved")
    export_tmx(db, out)
    assert '<prop type="status">approved</prop>' in out.read_text(encoding="utf-8")


def test_parse_tmx_props():
    unit = ET.fromstring('<tu><prop type="status">approved</prop></tu>')
    assert parse_tmx_props(unit) == {"status": "approved"}


def test_parse_tmx_units_with_props(tmp_path):
    source = tmp_path / "source.tmx"
    source.write_text('<tmx><body><tu><prop type="status">approved</prop><tuv><seg>A</seg></tuv><tuv><seg>B</seg></tuv></tu></body></tmx>', encoding="utf-8")
    assert parse_tmx_units_with_props(source) == [("A", "B", {"status": "approved"})]


def test_import_tmx_metadata(tmp_path):
    source = tmp_path / "source.tmx"
    db = tmp_path / "memory.sqlite"
    source.write_text('<tmx><body><tu><prop type="status">approved</prop><tuv><seg>A</seg></tuv><tuv><seg>B</seg></tuv></tu></body></tmx>', encoding="utf-8")
    import_tmx(source, db)
    with sqlite3.connect(db) as conn:
        rows = conn.execute("select status from terms").fetchall()
    assert rows == [("approved",)]


def test_metadata_round_trip(tmp_path):
    source_db = tmp_path / "source.sqlite"
    out = tmp_path / "memory.tmx"
    target_db = tmp_path / "target.sqlite"
    add_reviewed_term(source_db, "A", "B", "D", "approved")
    export_tmx(source_db, out)
    import_tmx(out, target_db)
    with sqlite3.connect(target_db) as conn:
        rows = conn.execute("select reviewer, status from terms").fetchall()
    assert rows == [("D", "approved")]


def test_xml_name_strips_namespace():
    assert xml_name("{urn:test}tu") == "tu"


def test_parse_tmx_namespaced_units(tmp_path):
    source = tmp_path / "source.tmx"
    source.write_text('<tmx xmlns="urn:test"><body><tu><tuv><seg>A</seg></tuv><tuv><seg>B</seg></tuv></tu></body></tmx>', encoding="utf-8")
    assert parse_tmx_units(source) == [("A", "B")]
