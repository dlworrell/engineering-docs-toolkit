from dataclasses import dataclass
from pathlib import Path

from .hash_cache import hash_file


@dataclass
class PdfImportResult:
    source: Path
    output: Path
    pages: int = 0
    fingerprint: str = ""


def import_pdf(source: Path, output: Path) -> PdfImportResult:
    output.mkdir(parents=True, exist_ok=True)
    fingerprint = hash_file(source) if source.exists() else "missing"
    notes = output / "import-notes.md"
    notes.write_text(f"# PDF Import Notes\n\nSource: {source}\nHash: {fingerprint}\n", encoding="utf-8")
    return PdfImportResult(source=source, output=output, fingerprint=fingerprint)
