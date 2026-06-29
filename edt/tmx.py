import sqlite3
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

from .translation_memory import init_memory


def export_tmx(db_path: Path, out_path: Path) -> None:
    init_memory(db_path)
    with sqlite3.connect(db_path) as db:
        rows = db.execute("select source, target, source_lang, target_lang from terms").fetchall()
    body = []
    for source, target, source_lang, target_lang in rows:
        body.append(f'<tu><tuv xml:lang="{escape(source_lang or "und")}"><seg>{escape(source)}</seg></tuv><tuv xml:lang="{escape(target_lang or "und")}"><seg>{escape(target)}</seg></tuv></tu>')
    out_path.write_text("<tmx version=\"1.4\"><body>" + "".join(body) + "</body></tmx>\n", encoding="utf-8")


def parse_tmx_units(tmx_path: Path) -> list[tuple[str, str]]:
    root = ET.fromstring(tmx_path.read_text(encoding="utf-8"))
    return [(tu[0].findtext("seg", ""), tu[1].findtext("seg", "")) for tu in root.findall(".//tu") if len(tu) >= 2]


def import_tmx(tmx_path: Path, db_path: Path) -> None:
    init_memory(db_path)
    tmx_path.read_text(encoding="utf-8")
