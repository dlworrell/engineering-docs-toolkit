import json
import sys

from edt.cli import main


def test_import_command_generates_document_reports(tmp_path, monkeypatch, capsys):
    manifest = tmp_path / "edt" / "project.yml"
    manifest.parent.mkdir()
    manifest.write_text(
        "source:\n"
        "  primary_pdf: source/original/book.pdf\n"
        "  start: 1\n"
        "  end: 1\n"
        "outputs:\n"
        "  edom: output/import/edom\n"
        "  reports: reports/import\n"
        "  pages: pages\n",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["edt", "import"])

    main()

    import_report = tmp_path / "reports" / "import" / "import-report.json"
    report_dir = tmp_path / "reports" / "import" / "document"
    canonical = (
        tmp_path
        / "output"
        / "import"
        / "edom"
        / "canonical-document.edom.json"
    )
    published_html = tmp_path / "output" / "import" / "document.html"

    assert canonical.exists()
    assert published_html.exists()
    assert import_report.exists()
    assert (report_dir / "validation.json").exists()
    assert (report_dir / "reference-graph.json").exists()
    assert (report_dir / "quality.json").exists()

    html = published_html.read_text(encoding="utf-8")
    assert "<!doctype html>" in html
    assert 'data-edt-kind="document"' not in html
    assert '<main role="main">' in html

    quality = json.loads(
        (report_dir / "quality.json").read_text(encoding="utf-8")
    )
    assert quality["publication_ready"] is False
    assert capsys.readouterr().out == f"wrote {import_report}\n"
