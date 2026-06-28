from html import escape


def markdown_to_html(text: str, title: str) -> str:
    lines = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        f"<title>{escape(title)}</title>",
        "</head>",
        "<body>",
    ]
    for line in text.splitlines():
        if line.startswith("# "):
            lines.append(f"<h1>{escape(line[2:])}</h1>")
        elif line.startswith("## "):
            lines.append(f"<h2>{escape(line[3:])}</h2>")
        elif line.startswith("### "):
            lines.append(f"<h3>{escape(line[4:])}</h3>")
        elif line.strip():
            lines.append(f"<p>{escape(line)}</p>")
        else:
            lines.append("")
    lines.extend(["</body>", "</html>"])
    return "\n".join(lines)
