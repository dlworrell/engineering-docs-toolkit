from pathlib import Path

from .config import load_config
from .hash_cache import hash_file, hash_text
from .html import markdown_to_html, write_edom_html
from .manifest import write_manifest
from .pandoc import run_pandoc
from .plugin import ProjectContext
from .plugin_registry import default_plugins


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
    book_md = out / "book.md"
    book_html = out / "book.html"
    canonical_edom = (
        out / "import" / "edom" / "canonical-document.edom.json"
    )

    book_md.write_text(book_text, encoding="utf-8")
    if canonical_edom.exists():
        fingerprint = hash_file(canonical_edom)
        write_edom_html(canonical_edom, book_html, title=config.title)
        source_mode = "canonical-edom"
    else:
        fingerprint = hash_text(book_text)
        book_html.write_text(
            markdown_to_html(book_text, config.title),
            encoding="utf-8",
        )
        source_mode = "markdown"

    (out / "book.hash").write_text(fingerprint + "\n", encoding="utf-8")

    print(f"wrote {book_md}")
    print(f"wrote {book_html}")

    if "docx" in config.outputs:
        if run_pandoc(book_md, out / "book.docx"):
            print(f"wrote {out / 'book.docx'}")
    if "epub" in config.outputs:
        if run_pandoc(book_md, out / "book.epub"):
            print(f"wrote {out / 'book.epub'}")

    context = ProjectContext(root=root, output=out)
    for plugin in default_plugins():
        plugin.run(context)

    manifest = {
        "title": config.title,
        "chapters": len(chapters),
        "fingerprint": fingerprint,
        "outputs": config.outputs,
        "source_mode": source_mode,
    }
    if canonical_edom.exists():
        manifest["canonical_edom"] = str(canonical_edom.relative_to(root))
    write_manifest(out, manifest)
