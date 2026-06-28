from html import escape

from .math_parser import replace_math


def render_inline(text: str) -> str:
    rendered = replace_math(text)
    pieces = []
    cursor = 0
    while True:
        start = rendered.find('<math ', cursor)
        if start == -1:
            pieces.append(escape(rendered[cursor:]))
            break
        end = rendered.find('</math>', start)
        if end == -1:
            pieces.append(escape(rendered[cursor:]))
            break
        end += len('</math>')
        pieces.append(escape(rendered[cursor:start]))
        pieces.append(rendered[start:end])
        cursor = end
    return ''.join(pieces)


def markdown_to_html(text: str, title: str) -> str:
    lines = ["<!doctype html>", '<html lang="en">', "<head>", '<meta charset="utf-8">', f"<title>{escape(title)}</title>", "</head>", "<body>"]
    for line in text.splitlines():
        if line.startswith("# "):
            lines.append(f"<h1>{render_inline(line[2:])}</h1>")
        elif line.startswith("## "):
            lines.append(f"<h2>{render_inline(line[3:])}</h2>")
        elif line.startswith("### "):
            lines.append(f"<h3>{render_inline(line[4:])}</h3>")
        elif line.strip():
            lines.append(f"<p>{render_inline(line)}</p>")
        else:
            lines.append("")
    lines.extend(["</body>", "</html>"])
    return "\n".join(lines)
