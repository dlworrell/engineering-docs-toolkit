from pathlib import Path


def init_project(root: Path) -> None:
    (root / "source" / "english").mkdir(parents=True, exist_ok=True)
    (root / "reference" / "glossary").mkdir(parents=True, exist_ok=True)
    (root / "reference" / "indexes").mkdir(parents=True, exist_ok=True)
    book = root / "book.yaml"
    if not book.exists():
        book.write_text("title: Untitled Engineering Book\noutputs:\n  - md\n  - html\n", encoding="utf-8")
