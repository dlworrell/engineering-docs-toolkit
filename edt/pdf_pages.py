from dataclasses import dataclass
from pathlib import Path


@dataclass
class PdfPageImage:
    pdf_path: Path
    page_number: int
    image_path: Path


def page_image_path(output_dir: Path, page_number: int, suffix: str = ".png") -> Path:
    return output_dir / f"page-{page_number:04d}{suffix}"


def pdftoppm_args(pdf_path: Path, output_prefix: Path, first_page: int, last_page: int, dpi: int = 300) -> list[str]:
    return ["pdftoppm", "-r", str(dpi), "-png", "-f", str(first_page), "-l", str(last_page), str(pdf_path), str(output_prefix)]
