from pathlib import Path


PROJECT_CONFIG = """schema_version = 1

[project]
title = "Untitled Engineering Document"
language = "en"

[paths]
work = ".edt/work"
reports = "reports"
output = "output"

[[sources]]
id = "primary"
type = "pdf"
path = "source/original/document.pdf"

[[sources]]
id = "chapters"
type = "markdown"
path = "source/english"

[import]
first_page = 1
last_page = 1
ocr_engine = "null"
ocr_language = "eng"

[validation]
fail_on = "error"

[publish]
formats = ["html"]
"""


LEGACY_BOOK_CONFIG = """title: Untitled Engineering Book
outputs:
  - md
  - html
"""


PROJECT_README = """# EDT Project

This project was initialized by Engineering Documents Toolkit.

Edit `edt.toml` to configure sources, paths, validation policy, and publication formats. Markdown chapters belong in `source/english/` and are processed in lexical filename order.

Build the current project with:

```bash
edt build
```
"""


SAMPLE_CHAPTER = """# Introduction

Replace this chapter with the first section of your engineering document.
"""


PROJECT_DIRECTORIES = (
    "source/english",
    "source/original",
    "assets",
    "profiles",
    "reference/glossary",
    "reference/indexes",
    ".edt/work",
    ".edt/cache",
    "reports",
    "output",
)


def _write_if_missing(path: Path, content: str) -> None:
    if path.exists():
        return
    path.write_text(content, encoding="utf-8")


def init_project(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)

    for relative_path in PROJECT_DIRECTORIES:
        (root / relative_path).mkdir(parents=True, exist_ok=True)

    _write_if_missing(root / "edt.toml", PROJECT_CONFIG)
    _write_if_missing(root / "book.yaml", LEGACY_BOOK_CONFIG)
    _write_if_missing(root / "README.md", PROJECT_README)

    chapter_dir = root / "source" / "english"
    if not any(chapter_dir.glob("*.md")):
        _write_if_missing(chapter_dir / "01-introduction.md", SAMPLE_CHAPTER)
