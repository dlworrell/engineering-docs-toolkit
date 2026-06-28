from pathlib import Path


def generate_index_summary(root: Path) -> Path | None:
    index_dir = root / "reference" / "indexes"
    if not index_dir.exists():
        return None

    out = root / "output"
    out.mkdir(exist_ok=True)
    target = out / "index-summary.md"

    with target.open("w", encoding="utf-8") as handle:
        handle.write("# Index Summary\n\n")
        for path in sorted(index_dir.glob("*.csv")):
            handle.write(f"- {path.name}\n")

    return target
