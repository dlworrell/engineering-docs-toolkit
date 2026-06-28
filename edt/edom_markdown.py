from .edom import EdomNode


def markdown_to_edom(text: str, title: str = "Document") -> EdomNode:
    root = EdomNode(kind="document", text=title)
    current = root
    for line in text.splitlines():
        if line.startswith("#"):
            marks = len(line) - len(line.lstrip("#"))
            heading = line[marks:].strip()
            current = root.add(EdomNode(kind=f"heading{marks}", text=heading))
        elif line.strip():
            current.add(EdomNode(kind="paragraph", text=line.strip()))
    return root
