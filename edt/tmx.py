import sqlite3
from pathlib import Path
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
