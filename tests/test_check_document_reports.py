import json

from edt.check import check_project
from edt.hash_cache import hash_file


def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def write_canonical_build(
    root,
    validation_payload,
    reference_payload,
    quality_payload,
):
    output = root / "output"
    report_dir = root / "reports" / "document"
    canonical = output / "import" / "edom" / "canonical-document.edom.json"
    canonical.parent.mkdir(parents=True, exist_ok=True)
    canonical.write_text(
        json.dumps(
            {
                "root": {
                    "id": "document",
                    "kind": "document",
                    "children": [
                        {
                            "id": "p1",
                            "kind": "paragraph",
                            "text": "Canonical content.",
                            "children": [],
                        }
                    ],
                }
            }
        ),
        encoding="utf-8",
    )
    (output / "book.md").write_text("# Canonical\n", encoding="utf-8")
    (output / "book.html").write_text(
        "<html><body>Canonical</body></html>\n",
        encoding="utf-8",
    )

    write_json(report_dir / "validation.json", validation_payload)
    write_json(report_dir / "reference-graph.json", reference_payload)
    write_json(report_dir / "quality.json", quality_payload)
    (report_dir / "validation.md").write_text("# validation\n", encoding="utf-8")
    (report_dir / "reference-graph.md").write_text(
        "# reference graph\n",
        encoding="utf-8",
    )
    (report_dir / "quality.md").write_text("# quality\n", encoding="utf-8")

    write_json(
        output / "build-manifest.json",
        {
            "title": "Canonical",
            "chapters": 1,
            "fingerprint": hash_file(canonical),
            "outputs": ["md", "html"],
            "source_mode": "canonical-edom",
            "canonical_edom": "output/import/edom/canonical-document.edom.json",
            "document_reports": {
                "validation": {
                    "errors": 0,
                    "warnings": 0,
                    "info": 0,
                    "json": "reports/document/validation.json",
                    "markdown": "reports/document/validation.md",
                },
                "reference_graph": {
                    "nodes": 1,
                    "edges": 0,
                    "broken": 0,
                    "orphans": 0,
                    "json": "reports/document/reference-graph.json",
                    "markdown": "reports/document/reference-graph.md",
                },
                "quality": {
                    "structural_score": 100.0,
                    "semantic_score": 100.0,
                    "reference_score": 100.0,
                    "overall_score": 100.0,
                    "publication_ready": True,
                    "errors": 0,
                    "warnings": 0,
                    "broken_references": 0,
                    "orphan_references": 0,
                    "json": "reports/document/quality.json",
                    "markdown": "reports/document/quality.md",
                },
            },
        },
    )
    return canonical


def test_check_reads_document_report_files_not_manifest_summaries(tmp_path):
    write_canonical_build(
        tmp_path,
        validation_payload={
            "summary": {
                "findings": 1,
                "errors": 1,
                "warnings": 0,
                "info": 0,
            },
            "findings": [],
        },
        reference_payload={
            "summary": {
                "nodes": 2,
                "edges": 1,
                "broken": 2,
                "orphans": 0,
            },
            "nodes": [],
        },
        quality_payload={
            "structural_score": 75.0,
            "semantic_score": 100.0,
            "reference_score": 50.0,
            "overall_score": 75.0,
            "publication_ready": False,
            "errors": 1,
            "warnings": 0,
            "broken_references": 2,
            "orphan_references": 0,
        },
    )

    issues = check_project(tmp_path)

    assert "validation errors: 1" in issues
    assert "broken references: 2" in issues
    assert "document is not publication ready" in issues


def test_check_reports_stale_canonical_edom_fingerprint(tmp_path):
    canonical = write_canonical_build(
        tmp_path,
        validation_payload={
            "summary": {
                "findings": 0,
                "errors": 0,
                "warnings": 0,
                "info": 0,
            },
            "findings": [],
        },
        reference_payload={
            "summary": {
                "nodes": 1,
                "edges": 0,
                "broken": 0,
                "orphans": 0,
            },
            "nodes": [],
        },
        quality_payload={
            "structural_score": 100.0,
            "semantic_score": 100.0,
            "reference_score": 100.0,
            "overall_score": 100.0,
            "publication_ready": True,
            "errors": 0,
            "warnings": 0,
            "broken_references": 0,
            "orphan_references": 0,
        },
    )
    payload = json.loads(canonical.read_text(encoding="utf-8"))
    payload["root"]["children"][0]["text"] = "Changed after build."
    canonical.write_text(json.dumps(payload), encoding="utf-8")

    issues = check_project(tmp_path)

    assert "stale build manifest: canonical EDOM changed since build" in issues
