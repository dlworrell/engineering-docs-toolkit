import json
import sys

from edt.cli import main


def test_import_command_uses_edt_toml(tmp_path, monkeypatch, capsys):
    (tmp_path / "edt.toml").write_text(
        'schema_version = 1\n'
        '\n'
        '[project]\n'
        'title = "HERKULES 1934 English"\n'
        'language = "en"\n'
        '\n'
        '[paths]\n'
        'work = ".edt/herkules-work"\n'
        'reports = "build/reports"\n'
        'output = "build/output"\n'
        '\n'
        '[[sources]]\n'
        'id = "primary"\n'
        'type = "pdf"\n'
        'path = "source/original/herkules-1934.pdf"\n'
        '\n'
        '[import]\n'
        'first_page = 2\n'
        'last_page = 3\n'
        'ocr_engine = "tesseract"\n'
        'ocr_language = "swe"\n'
        '\n'
        '[validation]\n'
        'fail_on = "error"\n'
        '\n'
        '[publish]\n'
        'formats = ["html"]\n',
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["edt", "import"])

    main()

    generated_manifest = (
        tmp_path / ".edt" / "herkules-work" / "import-project.yml"
    )
    import_report = tmp_path / "build" / "reports" / "import" / "import-report.json"
    canonical = (
        tmp_path
        / "build"
        / "output"
        / "import"
        / "edom"
        / "canonical-document.edom.json"
    )
    published_html = tmp_path / "build" / "output" / "import" / "document.html"

    assert generated_manifest.exists()
    manifest_text = generated_manifest.read_text(encoding="utf-8")
    assert "primary_pdf: source/original/herkules-1934.pdf" in manifest_text
    assert "start: 2" in manifest_text
    assert "end: 3" in manifest_text
    assert "engine: tesseract" in manifest_text
    assert "language: swe" in manifest_text

    assert canonical.exists()
    assert published_html.exists()
    assert import_report.exists()
    assert (
        tmp_path
        / ".edt"
        / "herkules-work"
        / "pages"
        / "0002"
        / "manifest.json"
    ).exists()
    assert (
        tmp_path
        / ".edt"
        / "herkules-work"
        / "pages"
        / "0003"
        / "manifest.json"
    ).exists()

    report = json.loads(import_report.read_text(encoding="utf-8"))
    assert report["source_pdf"] == "source/original/herkules-1934.pdf"
    assert report["page_range"] == {"start": 2, "end": 3}
    assert report["status"] == "waiting_for_source_pdf"
    assert capsys.readouterr().out == f"wrote {import_report}\n"
