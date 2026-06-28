from pathlib import Path

from .config import load_config
from .html import markdown_to_html


def build_project(root: Path | None = None) -> None:
    root = root or Path.cwd()
    config = load_config(root)
    source = root / config.source_dir
    out = root / config.output_dir
    out.mkdir(exist_ok=True)

    chapters = sorted(source.glob("*.md")) if source.exists() else []
    parts = []
    for chapter in chapters:
        if chapter.name == "README.md":
            continue
        parts.append(chapter.read_text(encoding="utf-8").strip())

    book_text = "\n\n".join(parts) + "\n"
    (out / "book.md").write_text(book_text, encoding="utf-8")
    (out / "book.html").write_text(markdown_to_html(book_text, config.title), encoding="utf-8")

    print(f"wrote {out / 'book.md'}")
    print(f"wrote {out / 'book.html'}")
