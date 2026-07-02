import json
import sys

from edt.cli import main


def test_report_command_generates_document_reports(tmp_path, monkeypatch, capsys):
    document = tmp_path / "canonical-document.edom.json"
    document.write_text(
        json.dumps(
            {
                "root": {
                    "id": "document",
                    "kind": "document",
                    "children": [
                        {
                            "id": "eq1",
                            "kind": "equation",
                            "text": "x = 1",
                            "metadata": {"equation_number": "1.1"},
                            "source_regions": [
                                {"source_id": "primary", "page": 2}
                            ],
                            "children": [],
                        },
                        {
                            "id": "p1",
                            "kind": "paragraph",
                            "text": "Equation (1.1) is used here.",
                            "metadata": {"references": "eq1"},
                            "source_regions": [
                                {"source_id": "primary", "page": 3}
                            ],
                            "children": [],
                        },
                    ],
                }
            }
        ),
        encoding="utf-8",
    )
    output = tmp_path / "reports"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "edt",
            "report",
            "--document",
            str(document),
            "--output",
            str(output),
        ],
    )

    main()

    assert (output / "validation.json").exists()
    assert (output / "reference-graph.json").exists()
    assert (output / "quality.json").exists()
    quality = json.loads(
        (output / "quality.json").read_text(encoding="utf-8")
    )
    assert quality["publication_ready"] is True
    assert capsys.readouterr().out == f"wrote {output}\n"
