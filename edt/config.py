from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class BookConfig:
    title: str = "Untitled Engineering Book"
    source_dir: Path = Path("source/english")
    output_dir: Path = Path("output")
    outputs: list[str] = field(default_factory=lambda: ["md", "html"])


def load_config(root: Path) -> BookConfig:
    return BookConfig()
