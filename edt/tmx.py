import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

from .translation_memory import add_term, init_memory


def tmx_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def tmx_header(source_lang: str = "und") -> str:
    return f'<header creationtool="engineering-docs-toolkit" creationtoolversion="0" datatype="PlainText" segtype="sentence" adminlang="en" srclang="{escape(source_lang)}" />'


def tmx_lang(element: ET.Element) -> str:
    return element.attrib.get("{http://www.w3.org/XML/1998/namespace}lang", element.attrib.get("lang", "und"))


def export_tmx(db_path: Path, out_path: Path) -> None:
    init_memory(db_path)
    with sqlite3.connect(db_path) as db:
        rows = db.execute("select source, target, source_lang, target_lang from terms").fetchall()
    body = []
    for source, target, source_lang, target_lang in rows:
        body.append(f'<tu><tuv xml:lang="{escape(source_lang or "und")}"><seg>{escape(source)}</seg></tuv><tuv xml:lang="{escape(target_lang or "und")}"><seg>{escape(target)}</seg></tuv></tu>')
    out_path.write_text("<tmx version=\"1.4\">" + tmx_header() + "<body>" + "".join(body) + "</body></tmx>\n", encoding="utf-8")


def parse_tmx_units(tmx_path: Path) -> list[tuple[str, str]]:
    root = ET.fromstring(tmx_path.read_text(encoding="utf-8"))
    return [(tu[0].findtext("seg", ""), tu[1].findtext("seg", "")) for tu in root.findall(".//tu") if len(tu) >= 2]


def import_tmx(tmx_path: Path, db_path: Path) -> None:
    init_memory(db_path)
    for source, target in parse_tmx_units(tmx_path):
        add_term(db_path, source, target)
