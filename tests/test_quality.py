import json

from edt.quality import build_quality_report
from edt.reference_graph import build_reference_graph
from edt.validation import ValidationFinding, ValidationReport


def test_build_quality_report_scores_clean_document():
    validation = ValidationReport()
    graph = build_reference_graph({"root": {"id": "document", "kind": "document", "children": [{"id": "page-1", "kind": "page"}]}})

    report = build_quality_report(validation, graph)

    assert report.structural_score == 100.0
    assert report.semantic_score == 100.0
    assert report.reference_score == 100.0
    assert report.overall_score == 100.0
    assert report.publication_ready is True


def test_build_quality_report_penalizes_findings_and_broken_refs():
    validation = ValidationReport(
        [
            ValidationFinding("EDOM010", "error", "structure", "Duplicate id"),
            ValidationFinding("SEM020", "warning", "semantic", "Missing caption"),
            ValidationFinding("REF001", "warning", "reference", "Broken ref"),
        ]
    )
    graph = build_reference_graph(
        {
            "root": {
                "id": "document",
                "kind": "document",
                "children": [
                    {
                        "id": "page-1",
                        "kind": "page",
                        "children": [{"id": "p1", "kind": "paragraph", "text": "See missing", "metadata": {"references": "missing"}}],
                    }
                ],
            }
        }
    )

    report = build_quality_report(validation, graph)

    assert report.structural_score == 75.0
    assert report.semantic_score == 95.0
    assert report.reference_score == 95.0
    assert report.broken_references == 1
    assert report.publication_ready is False


def test_quality_report_writes_files(tmp_path):
    validation = ValidationReport()
    graph = build_reference_graph({"root": {"id": "document", "kind": "document", "children": [{"id": "page-1", "kind": "page"}]}})
    report = build_quality_report(validation, graph)

    json_path = report.write_json(tmp_path / "quality.json")
    md_path = report.write_markdown(tmp_path / "quality.md")

    assert json.loads(json_path.read_text(encoding="utf-8"))["overall_score"] == 100.0
    assert "EDT Quality Report" in md_path.read_text(encoding="utf-8")
