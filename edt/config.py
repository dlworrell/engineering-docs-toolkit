from dataclasses import dataclass, field
from pathlib import Path

from .simple_yaml import read_simple_yaml


@dataclass
class BookConfig:
    title: str = "Untitled Engineering Book"
    source_dir: Path = Path("source/english")
    output_dir: Path = Path("output")
    outputs: list[str] = field(default_factory=lambda: ["md", "html"])


def load_config(root: Path) -> BookConfig:
    path = root / "book.yaml"
    cfg = BookConfig()
    if not path.exists():
        return cfg
    raw = read_simple_yaml(path)
    title = raw.get("title")
    if isinstance(title, str):
        cfg.title = title
    return cfg
