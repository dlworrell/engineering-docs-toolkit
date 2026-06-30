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


def test_validate_document_edom_reports_duplicate_ids():
    report = validate_document_edom(
        {
            "root": {
                "id": "document",
                "kind": "document",
                "children": [
                    {
                        "id": "page-1",
                        "kind": "page",
                        "children": [
                            {"id": "a", "kind": "paragraph", "text": "One"},
                            {"id": "a", "kind": "paragraph", "text": "Two"},
                        ],
                    }
                ],
            }
        }
    )

    assert any(finding.rule == "EDOM010" for finding in report.findings)
    assert report.error_count == 1


def test_validate_document_edom_reports_empty_leaf_nodes():
    report = validate_document_edom(
        {
            "root": {
                "id": "document",
                "kind": "document",
                "children": [
                    {
                        "id": "page-1",
                        "kind": "page",
                        "children": [{"id": "empty", "kind": "paragraph", "text": ""}],
                    }
                ],
            }
        }
    )

    assert any(finding.rule == "EDOM011" for finding in report.findings)
    assert report.warning_count == 1


def test_validate_document_edom_reports_missing_pages():
    report = validate_document_edom(
        {
            "root": {
                "id": "document",
                "kind": "document",
                "children": [{"id": "page-1", "kind": "page"}, {"id": "page-3", "kind": "page"}],
            }
        }
    )

    assert any(finding.rule == "EDOM013" and finding.page == 2 for finding in report.findings)
    assert report.error_count == 1


def test_validate_document_edom_reports_theorem_without_proof():
    report = validate_document_edom(
        {
            "root": {
                "id": "document",
                "kind": "document",
                "children": [
                    {
                        "id": "page-1",
                        "kind": "page",
                        "children": [
                            {"id": "thm1", "kind": "theorem", "text": "Theorem 1.1"},
                            {"id": "p1", "kind": "paragraph", "text": "Text."},
                        ],
                    }
                ],
            }
        }
    )

    assert any(finding.rule == "SEM001" and finding.node_id == "thm1" for finding in report.findings)
    assert report.warning_count == 1


def test_validate_document_edom_reports_proof_without_theorem():
    report = validate_document_edom(
        {
            "root": {
                "id": "document",
                "kind": "document",
                "children": [
                    {
                        "id": "page-1",
                        "kind": "page",
                        "children": [{"id": "proof1", "kind": "proof", "text": "Proof."}],
                    }
                ],
            }
        }
    )

    assert any(finding.rule == "SEM002" and finding.node_id == "proof1" for finding in report.findings)
    assert report.warning_count == 1


def test_validate_document_edom_reports_duplicate_theorem_numbers():
    report = validate_document_edom(
        {
            "root": {
                "id": "document",
                "kind": "document",
                "children": [
                    {
                        "id": "page-1",
                        "kind": "page",
                        "children": [
                            {"id": "thm1", "kind": "theorem", "text": "Theorem", "metadata": {"number": "1.1"}},
                            {"id": "proof1", "kind": "proof", "text": "Proof."},
                            {"id": "thm2", "kind": "theorem", "text": "Theorem", "metadata": {"number": "1.1"}},
                            {"id": "proof2", "kind": "proof", "text": "Proof."},
                        ],
                    }
                ],
            }
        }
    )

    assert any(finding.rule == "SEM010" and finding.node_id == "thm2" for finding in report.findings)


def test_validate_document_edom_reports_duplicate_figure_table_definition_numbers():
    report = validate_document_edom(
        {
            "root": {
                "id": "document",
                "kind": "document",
                "children": [
                    {
                        "id": "page-1",
                        "kind": "page",
                        "children": [
                            {"id": "fig1", "kind": "figure", "text": "", "metadata": {"number": "1.2"}, "children": [{"id": "cap1", "kind": "caption", "text": "Figure 1.2"}]},
                            {"id": "fig2", "kind": "figure", "text": "", "metadata": {"number": "1.2"}, "children": [{"id": "cap2", "kind": "caption", "text": "Figure 1.2"}]},
                            {"id": "tbl1", "kind": "table", "text": "T", "metadata": {"number": "3.4"}, "children": [{"id": "cap3", "kind": "caption", "text": "Table 3.4"}]},
                            {"id": "tbl2", "kind": "table", "text": "T", "metadata": {"number": "3.4"}, "children": [{"id": "cap4", "kind": "caption", "text": "Table 3.4"}]},
                            {"id": "def1", "kind": "definition", "text": "D", "metadata": {"number": "2.1"}},
                            {"id": "def2", "kind": "definition", "text": "D", "metadata": {"number": "2.1"}},
                        ],
                    }
                ],
            }
        }
    )

    rules = {finding.rule for finding in report.findings}
    assert {"SEM011", "SEM012", "SEM013"}.issubset(rules)


def test_validate_document_edom_reports_missing_figure_and_table_captions():
    report = validate_document_edom(
        {
            "root": {
                "id": "document",
                "kind": "document",
                "children": [
                    {
                        "id": "page-1",
                        "kind": "page",
                        "children": [
                            {"id": "fig1", "kind": "figure", "text": ""},
                            {"id": "tbl1", "kind": "table", "text": "T"},
                        ],
                    }
                ],
            }
        }
    )

    rules = {finding.rule for finding in report.findings}
    assert {"SEM020", "SEM021"}.issubset(rules)


def test_validate_document_edom_reports_caption_without_valid_owner():
    report = validate_document_edom(
        {
            "root": {
                "id": "document",
                "kind": "document",
                "children": [
                    {
                        "id": "page-1",
                        "kind": "page",
                        "children": [
                            {"id": "p1", "kind": "paragraph", "text": "Body", "children": [{"id": "cap1", "kind": "caption", "text": "Figure 1"}]}
                        ],
                    }
                ],
            }
        }
    )

    assert any(finding.rule == "SEM022" and finding.node_id == "cap1" for finding in report.findings)


def test_validate_document_edom_reports_unresolved_reference():
    report = validate_document_edom(
        {
            "root": {
                "id": "document",
                "kind": "document",
                "children": [
                    {
                        "id": "page-1",
                        "kind": "page",
                        "children": [
                            {"id": "p1", "kind": "paragraph", "text": "See missing.", "metadata": {"references": "missing"}}
                        ],
                    }
                ],
            }
        }
    )

    assert any(finding.rule == "REF001" and finding.node_id == "p1" for finding in report.findings)


def test_validate_document_edom_accepts_resolved_reference():
    report = validate_document_edom(
        {
            "root": {
                "id": "document",
                "kind": "document",
                "children": [
                    {
                        "id": "page-1",
                        "kind": "page",
                        "children": [
                            {"id": "fig1", "kind": "figure", "text": "", "children": [{"id": "cap1", "kind": "caption", "text": "Figure 1"}]},
                            {"id": "p1", "kind": "paragraph", "text": "See fig.", "metadata": {"references": ["fig1"]}},
                        ],
                    }
                ],
            }
        }
    )

    assert not any(finding.rule.startswith("REF") for finding in report.findings)


def test_validate_document_edom_reports_circular_reference():
    report = validate_document_edom(
        {
            "root": {
                "id": "document",
                "kind": "document",
                "children": [
                    {
                        "id": "page-1",
                        "kind": "page",
                        "children": [
                            {"id": "a", "kind": "paragraph", "text": "A", "metadata": {"references": "b"}},
                            {"id": "b", "kind": "paragraph", "text": "B", "metadata": {"references": "a"}},
                        ],
                    }
                ],
            }
        }
    )

    assert any(finding.rule == "REF003" for finding in report.findings)


def test_validate_document_edom_reports_orphaned_reference_expected_nodes():
    report = validate_document_edom(
        {
            "root": {
                "id": "document",
                "kind": "document",
                "children": [
                    {
                        "id": "page-1",
                        "kind": "page",
                        "children": [
                            {"id": "fig1", "kind": "figure", "text": "", "children": [{"id": "cap1", "kind": "caption", "text": "Figure 1"}]},
                            {"id": "tbl1", "kind": "table", "text": "T", "children": [{"id": "cap2", "kind": "caption", "text": "Table 1"}]},
                        ],
                    }
                ],
            }
        }
    )

    rules = {finding.rule for finding in report.findings}
    assert "REF002" in rules
    assert any(finding.node_id == "fig1" for finding in report.findings if finding.rule == "REF002")
    assert any(finding.node_id == "tbl1" for finding in report.findings if finding.rule == "REF002")


def test_validate_document_edom_allows_explicitly_unreferenced_nodes():
    report = validate_document_edom(
        {
            "root": {
                "id": "document",
                "kind": "document",
                "children": [
                    {
                        "id": "page-1",
                        "kind": "page",
                        "children": [
                            {"id": "fig1", "kind": "figure", "text": "", "metadata": {"unreferenced_ok": True}, "children": [{"id": "cap1", "kind": "caption", "text": "Figure 1"}]}
                        ],
                    }
                ],
            }
        }
    )

    assert not any(finding.rule == "REF002" for finding in report.findings)


def test_validation_report_writes_files(tmp_path):
    report = ValidationReport([ValidationFinding("EDOM001", "error", "structure", "Bad root")])

    json_path = report.write_json(tmp_path / "validation.json")
    md_path = report.write_markdown(tmp_path / "validation.md")

    assert json.loads(json_path.read_text(encoding="utf-8"))["summary"]["errors"] == 1
    assert "EDT Validation Report" in md_path.read_text(encoding="utf-8")
