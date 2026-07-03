import json

from edt.check import check_project


def test_check_project_reports_canonical_quality_issues(tmp_path):
    output = tmp_path / "output"
    report_dir = tmp_path / "reports" / "document"
    canonical = output / "import" / "edom" / "canonical-document.edom.json"
    canonical.parent.mkdir(parents=True)
    report_dir.mkdir(parents=True)

    canonical.write_text(
        json.dumps({"root": {"id": "document", "kind": "document"}}),
        encoding="utf-8",
    )
    (report_dir / "validation.json").write_text(
        json.dumps({"summary": {"errors": 1}}),
        encoding="utf-8",
    )
    (report_dir / "reference-graph.json").write_text(
        json.dumps({"summary": {"broken": 2}}),
        encoding="utf-8",
    )
    (report_dir / "quality.json").write_text(
        json.dumps({"publication_ready": False}),
        encoding="utf-8",
    )
    output.mkdir(exist_ok=True)
    (output / "build-manifest.json").write_text(
        json.dumps(
            {
                "source_mode": "canonical-edom",
                "canonical_edom": "output/import/edom/canonical-document.edom.json",
                "document_reports": {
                    "validation": {
                        "errors": 1,
                        "json": "reports/document/validation.json",
                    },
                    "reference_graph": {
                        "broken": 2,
                        "json": "reports/document/reference-graph.json",
                    },
                    "quality": {
                        "publication_ready": False,
                        "json": "reports/document/quality.json",
                    },
                },
            }
        ),
        encoding="utf-8",
    )

    issues = check_project(tmp_path)

    assert "validation errors: 1" in issues
    assert "broken references: 2" in issues
    assert "document is not publication ready" in issues


def test_check_project_reports_missing_canonical_report_files(tmp_path):
    output = tmp_path / "output"
    canonical = output / "import" / "edom" / "canonical-document.edom.json"
    canonical.parent.mkdir(parents=True)
    canonical.write_text(
        json.dumps({"root": {"id": "document", "kind": "document"}}),
        encoding="utf-8",
    )
    output.mkdir(exist_ok=True)
    (output / "build-manifest.json").write_text(
        json.dumps(
            {
                "source_mode": "canonical-edom",
                "canonical_edom": "output/import/edom/canonical-document.edom.json",
                "document_reports": {
                    "validation": {"errors": 0, "json": "reports/document/validation.json"},
                    "reference_graph": {"broken": 0, "json": "reports/document/reference-graph.json"},
                    "quality": {"publication_ready": True, "json": "reports/document/quality.json"},
                },
            }
        ),
        encoding="utf-8",
    )

    issues = check_project(tmp_path)

    assert "missing validation report: reports/document/validation.json" in issues
    assert "missing reference graph report: reports/document/reference-graph.json" in issues
    assert "missing quality report: reports/document/quality.json" in issues
