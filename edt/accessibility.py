from pathlib import Path


def check_html_accessibility(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    issues: list[str] = []
    if "<math" in text and "alttext=" not in text:
        issues.append("MathML is missing alttext")
    if "<img" in text and "alt=" not in text:
        issues.append("Image is missing alt text")
    return issues
