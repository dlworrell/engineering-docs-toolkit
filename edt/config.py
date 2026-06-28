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
    source_dir = raw.get("source_dir")
    output_dir = raw.get("output_dir")
    if isinstance(title, str):
        cfg.title = title
    if isinstance(source_dir, str):
        cfg.source_dir = Path(source_dir)
    if isinstance(output_dir, str):
        cfg.output_dir = Path(output_dir)
    return cfg
