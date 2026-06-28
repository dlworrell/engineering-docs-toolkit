from .model import Document, Section


def parse_markdown(text: str, title: str = "Untitled") -> Document:
    doc = Document(title=title)
    current: Section | None = None
    for line in text.splitlines():
        if line.startswith("#"):
            marks = len(line) - len(line.lstrip("#"))
            heading = line[marks:].strip()
            current = Section(level=marks, title=heading)
            doc.sections.append(current)
        elif current is not None:
            current.body.append(line)
    return doc
