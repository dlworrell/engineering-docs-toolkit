import json

from edt.validation import ValidationFinding, ValidationReport, validate_document_edom


def test_validation_report_counts_and_serializes():
    report = ValidationReport()
    report.add(ValidationFinding("EDOM001", "error", "structure", "Bad root", node_id="document"))
    report.add(ValidationFinding("SEM001", "warning", "semantic", "Missing proof", page=3))

    payload = report.to_dict()

    assert payload["summary"]["findings"] == 2
    assert payload["summary"]["errors"] == 1
    assert payload["summary"]["warnings"] == 1
    assert "EDOM001" in report.to_markdown()


def test_validate_document_edom_accepts_minimal_document():
    report = validate_document_edom({"root": {"id": "document", "kind": "document", "children": [{"id": "page-1", "kind": "page"}]}})

    assert report.error_count == 0
    assert report.warning_count == 0


def test_validate_document_edom_reports_missing_root():
    report = validate_document_edom({})

    assert report.error_count == 1
    assert report.findings[0].rule == "EDOM001"


def test_validation_report_writes_files(tmp_path):
    report = ValidationReport([ValidationFinding("EDOM001", "error", "structure", "Bad root")])

    json_path = report.write_json(tmp_path / "validation.json")
    md_path = report.write_markdown(tmp_path / "validation.md")

    assert json.loads(json_path.read_text(encoding="utf-8"))["summary"]["errors"] == 1
    assert "EDT Validation Report" in md_path.read_text(encoding="utf-8")
