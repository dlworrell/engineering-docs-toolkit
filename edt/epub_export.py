from __future__ import annotations

import json
import zipfile
from html import escape
from pathlib import Path

from .html import edom_document_to_html


CONTAINER_XML = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""


STYLESHEET = """body { font-family: serif; line-height: 1.5; margin: 2em; }
.edt-page { margin-bottom: 2em; }
.edt-theorem, .edt-proof, .edt-definition, .edt-example, .edt-exercise, .edt-algorithm { margin: 1em 0; }
.edt-equation { margin: 1em 0; text-align: center; }
"""


def _xhtml_from_html(html: str) -> str:
    return html.replace("<!doctype html>", '<?xml version="1.0" encoding="utf-8"?>')


def _content_opf(title: str) -> str:
    safe_title = escape(title)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="book-id">urn:uuid:edt-document</dc:identifier>
    <dc:title>{safe_title}</dc:title>
    <dc:language>en</dc:language>
    <meta property="dcterms:modified">2026-01-01T00:00:00Z</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="index" href="index.xhtml" media-type="application/xhtml+xml"/>
    <item id="style" href="stylesheet.css" media-type="text/css"/>
  </manifest>
  <spine>
    <itemref idref="index"/>
  </spine>
</package>
"""


def _nav_xhtml(title: str) -> str:
    safe_title = escape(title)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head><title>{safe_title}</title></head>
<body>
<nav epub:type="toc" id="toc">
  <h1>{safe_title}</h1>
  <ol>
    <li><a href="index.xhtml">{safe_title}</a></li>
  </ol>
</nav>
</body>
</html>
"""


def write_epub(document_edom: Path, output_epub: Path, title: str = "EDT Document") -> Path:
    payload = json.loads(document_edom.read_text(encoding="utf-8"))
    html = edom_document_to_html(payload, title=title)
    index_xhtml = _xhtml_from_html(html)
    output_epub.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output_epub, "w") as archive:
        archive.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        archive.writestr("META-INF/container.xml", CONTAINER_XML)
        archive.writestr("OEBPS/content.opf", _content_opf(title))
        archive.writestr("OEBPS/nav.xhtml", _nav_xhtml(title))
        archive.writestr("OEBPS/index.xhtml", index_xhtml)
        archive.writestr("OEBPS/stylesheet.css", STYLESHEET)

    return output_epub
