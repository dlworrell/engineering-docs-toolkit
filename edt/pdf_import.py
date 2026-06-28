from dataclasses import dataclass
from pathlib import Path


@dataclass
class PdfImportResult:
    source: Path
    output: Path
    pages: int = 0


def import_pdf(source: Path, output: Path) -> PdfImportResult:
    output.mkdir(parents=True, exist_ok=True)
    notes = output / "import-notes.md"
    notes.write_text(f"# PDF Import Notes\n\nSource: {source}\n", encoding="utf-8")
    return PdfImportResult(source=source, output=output)
