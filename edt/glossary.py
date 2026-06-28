import csv
from pathlib import Path


def generate_glossary(root: Path) -> Path | None:
    source = root / "reference" / "glossary" / "terms.csv"
    if not source.exists():
        return None

    out = root / "output"
    out.mkdir(exist_ok=True)
    target = out / "glossary.md"

    with source.open(newline="", encoding="utf-8") as src, target.open("w", encoding="utf-8") as dst:
        reader = csv.DictReader(src)
        dst.write("# Glossary\n\n")
        for row in reader:
            dst.write(f"- **{row.get('swedish', '')}**: {row.get('english', '')}\n")

    return target
