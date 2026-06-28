from pathlib import Path


def build_project(root: Path | None = None) -> None:
    root = root or Path.cwd()
    out = root / "output"
    out.mkdir(exist_ok=True)
    print(f"engineering-docs-toolkit: output directory is {out}")
