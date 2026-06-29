from dataclasses import dataclass, field

from .figure_alt_text import FigureAltText
from .table_accessibility import AccessibleTable


@dataclass
class AccessibilityReport:
    missing_alt_text: list[str] = field(default_factory=list)
    tables_without_headers: list[str] = field(default_factory=list)

    @property
    def passes_basic_checks(self) -> bool:
        return not self.missing_alt_text and not self.tables_without_headers


def basic_accessibility_report(figures: list[FigureAltText], tables: list[AccessibleTable]) -> AccessibilityReport:
    return AccessibilityReport(
        missing_alt_text=[figure.figure_id for figure in figures if not figure.is_complete],
        tables_without_headers=[table.table_id for table in tables if not table.has_headers],
    )
