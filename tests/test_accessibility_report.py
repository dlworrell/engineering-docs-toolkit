from edt.accessibility_report import basic_accessibility_report
from edt.figure_alt_text import FigureAltText
from edt.table_accessibility import AccessibleTable


def test_basic_accessibility_report_detects_missing_alt_text():
    report = basic_accessibility_report([FigureAltText(figure_id="fig1", alt_text="")], [])
    assert "fig1" in report.missing_alt_text


def test_basic_accessibility_report_passes_complete_content():
    report = basic_accessibility_report([FigureAltText(figure_id="fig1", alt_text="Diagram")], [AccessibleTable(table_id="t1", headers=["A"])])
    assert report.passes_basic_checks
