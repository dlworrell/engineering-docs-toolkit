import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

from .translation_memory import init_memory


def tmx_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def tmx_header(source_lang: str = "und") -> str:
    date = tmx_date()
    return f'<header creationtool="engineering-docs-toolkit" creationtoolversion="0" datatype="PlainText" segtype="sentence" adminlang="en" srclang="{escape(source_lang)}" creationdate="{date}" changedate="{date}" o-tmf="edt" tool-id="engineering-docs-toolkit" creationid="edt" changeid="edt" />'


def xml_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def child_elements(element: ET.Element, name: str) -> list[ET.Element]:
    return [child for child in list(element) if xml_name(child.tag) == name]


def descendant_elements(element: ET.Element, name: str) -> list[ET.Element]:
    return [child for child in element.iter() if xml_name(child.tag) == name]


def read_tmx_root(tmx_path: Path) -> ET.Element:
    try:
        return ET.fromstring(tmx_path.read_text(encoding="utf-8"))
    except ET.ParseError as exc:
        raise ValueError(f"malformed TMX XML: {exc}") from exc


def tmx_lang(element: ET.Element) -> str:
    return element.attrib.get("{http://www.w3.org/XML/1998/namespace}lang", element.attrib.get("lang", "und"))


def tmx_prop(name: str, value: str) -> str:
    return f'<prop type="{escape(name)}">{escape(value)}</prop>'


def parse_tmx_props(unit: ET.Element) -> dict[str, str]:
    return {prop.attrib.get("type", ""): prop.text or "" for prop in child_elements(unit, "prop")}


def export_tmx(db_path: Path, out_path: Path) -> None:
    init_memory(db_path)
    with sqlite3.connect(db_path) as db:
        rows = db.execute("select source, target, source_lang, target_lang, reviewer, status, confidence, origin, reviewed_at from terms").fetchall()
    body = []
    for source, target, source_lang, target_lang, reviewer, status, confidence, origin, reviewed_at in rows:
        props = "".join(tmx_prop(k, str(v)) for k, v in {"reviewer": reviewer, "status": status, "confidence": confidence, "origin": origin, "reviewed_at": reviewed_at}.items() if v not in (None, "", 0))
        body.append(f'<tu>{props}<tuv xml:lang="{escape(source_lang or "und")}"><seg>{escape(source)}</seg></tuv><tuv xml:lang="{escape(target_lang or "und")}"><seg>{escape(target)}</seg></tuv></tu>')
    out_path.write_text("<tmx version=\"1.4\">" + tmx_header() + "<body>" + "".join(body) + "</body></tmx>\n", encoding="utf-8")


def segment_text(tuv: ET.Element) -> str:
    segments = child_elements(tuv, "seg")
    return "" if not segments else "".join(segments[0].itertext())


def unit_segments(unit: ET.Element) -> list[str]:
    return [segment_text(tuv) for tuv in child_elements(unit, "tuv")]


def parse_tmx_units(tmx_path: Path) -> list[tuple[str, str]]:
    root = read_tmx_root(tmx_path)
    return [(segments[0], segments[1]) for tu in descendant_elements(root, "tu") if len(segments := unit_segments(tu)) >= 2]


def parse_tmx_units_with_props(tmx_path: Path) -> list[tuple[str, str, dict[str, str]]]:
    root = read_tmx_root(tmx_path)
    return [(segments[0], segments[1], parse_tmx_props(tu)) for tu in descendant_elements(root, "tu") if len(segments := unit_segments(tu)) >= 2]


def validate_tmx(tmx_path: Path) -> list[str]:
    try:
        root = read_tmx_root(tmx_path)
    except ValueError as exc:
        return [str(exc)]
    issues: list[str] = []
    if xml_name(root.tag) != "tmx":
        issues.append("root-not-tmx")
    if not descendant_elements(root, "body"):
        issues.append("missing-body")
    for tu in descendant_elements(root, "tu"):
        if not descendant_elements(tu, "seg"):
            issues.append("missing-seg")
    return issues


def import_tmx(tmx_path: Path, db_path: Path) -> None:
    init_memory(db_path)
    with sqlite3.connect(db_path) as db:
        for source, target, props in parse_tmx_units_with_props(tmx_path):
            db.execute("insert into terms (source, target, reviewer, status, confidence, origin, reviewed_at) values (?, ?, ?, ?, ?, ?, ?)", (source, target, props.get("reviewer", ""), props.get("status", ""), float(props.get("confidence", 0) or 0), props.get("origin", ""), props.get("reviewed_at", "")))
