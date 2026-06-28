from pathlib import Path

from .accessibility import check_html_accessibility


def check_project(root: Path) -> list[str]:
    issues: list[str] = []
    output = root / "output"
    for html in output.glob("*.html") if output.exists() else []:
        issues.extend(check_html_accessibility(html))
    return issues
