from dataclasses import dataclass
from pathlib import Path


@dataclass
class PdfPageImage:
    pdf_path: Path
    page_number: int
    image_path: Path


def page_image_path(output_dir: Path, page_number: int, suffix: str = ".png") -> Path:
    return output_dir / f"page-{page_number:04d}{suffix}"
