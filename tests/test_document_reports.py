import json

from edt.document_reports import generate_document_reports


def test_generate_document_reports_writes_complete_report_set(tmp_path):
    payload = {
        "root": {
            "id": "document",
            "kind": "document",
            "children": [
                {
                    "id": "eq1",
                    "kind": "equation",
                    "text": "x = 1",
                    "metadata": {"equation_number": "2.3"},
                    "source_regions": [
                        {"source_id": "primary", "page": 4}
                    ],
                    "children": [],
                },
                {
                    "id": "p1",
                    "kind": "paragraph",
                    "text": "Equation (2.3) is used here.",
                    "metadata": {"references": "eq1"},
                    "source_regions": [
                        {"source_id": "primary", "page": 5}
                    ],
                    "children": [],
                },
            ],
        }
    }

    report_dir = tmp_path / "reports"
    result = generate_document_reports(payload, report_dir)

    expected_files = {
        "validation.json",
        "validation.md",
        "reference-graph.json",
        "reference-graph.md",
        "quality.json",
        "quality.md",
    }
    assert {path.name for path in report_dir.iterdir()} == expected_files

    validation = json.loads(
        (report_dir / "validation.json").read_text(encoding="utf-8")
    )
    assert validation["summary"] == {
        "findings": 0,
        "errors": 0,
        "warnings": 0,
        "info": 0,
    }

    reference_graph = json.loads(
        (report_dir / "reference-graph.json").read_text(encoding="utf-8")
    )
    nodes = {node["node_id"]: node for node in reference_graph["nodes"]}
    assert reference_graph["summary"] == {
        "nodes": 3,
        "edges": 1,
        "broken": 0,
        "orphans": 0,
    }
    assert nodes["eq1"]["page"] == 4
    assert nodes["p1"]["page"] == 5
    assert nodes["eq1"]["incoming"] == ["p1"]

    quality = json.loads(
        (report_dir / "quality.json").read_text(encoding="utf-8")
    )
    assert quality["overall_score"] == 100.0
    assert quality["publication_ready"] is True
    assert result.to_dict()["quality"]["publication_ready"] is True


def test_generate_document_reports_blocks_broken_references(tmp_path):
    payload = {
        "root": {
            "id": "document",
            "kind": "document",
            "children": [
                {
                    "id": "p1",
                    "kind": "paragraph",
                    "text": "See the missing target.",
                    "metadata": {"references": "missing"},
                    "source_regions": [
                        {"source_id": "primary", "page": 8}
                    ],
                    "children": [],
                }
            ],
        }
    }

    result = generate_document_reports(payload, tmp_path / "reports")

    assert result.validation.warning_count == 1
    assert result.reference_graph.nodes["p1"].broken == ["missing"]
    assert result.quality.broken_references == 1
    assert result.quality.publication_ready is False
