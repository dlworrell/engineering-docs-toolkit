import json
import sys

from edt.cli import main


def test_initialized_project_imports_and_builds(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(sys, "argv", ["edt", "init"])
    main()

    monkeypatch.setattr(sys, "argv", ["edt", "import"])
    main()

    monkeypatch.setattr(sys, "argv", ["edt", "build"])
    main()

    import_report = tmp_path / "reports" / "import" / "import-report.json"
    canonical = tmp_path / "output" / "import" / "edom" / "canonical-document.edom.json"
    import_html = tmp_path / "output" / "import" / "document.html"
    book_html = tmp_path / "output" / "book.html"
    manifest = tmp_path / "output" / "build-manifest.json"

    assert import_report.exists()
    assert canonical.exists()
    assert import_html.exists()
    assert book_html.exists()
    assert manifest.exists()

    build_manifest = json.loads(manifest.read_text(encoding="utf-8"))
    assert build_manifest["source_mode"] == "canonical-edom"
    assert build_manifest["canonical_edom"] == "output/import/edom/canonical-document.edom.json"
    assert build_manifest["document_reports"] is not None

    output = capsys.readouterr().out
    assert f"wrote {import_report}" in output
    assert f"wrote {book_html}" in output
