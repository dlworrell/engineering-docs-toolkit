import json
import os
import shutil
import sys
from pathlib import Path

import pytest

from edt.cli import main


def _first_existing(paths):
    for path in paths:
        if path.is_file():
            return path
    return None


def _herkules_source_pdf() -> Path | None:
    configured = os.environ.get("EDT_HERKULES_SOURCE_PDF")
    if configured:
        path = Path(configured)
        if path.is_file():
            return path

    checked_in_sources = sorted((Path.cwd() / "source" / "original").glob("*.pdf"))
    source = _first_existing(checked_in_sources)
    if source is not None:
        return source

    fixture = Path(__file__).parent / "fixtures" / "herkules-manual.pdf"
    if fixture.is_file():
        return fixture

    return None


def _replace_setting(text: str, key: str, value: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.strip().startswith(f"{key} ="):
            indent = line[: len(line) - len(line.lstrip())]
            lines.append(f"{indent}{key} = {value}")
        else:
            lines.append(line)
    return "\n".join(lines) + "\n"


def _configure_herkules_project(root: Path, source_pdf: Path) -> None:
    target_pdf = root / "source" / "original" / "document.pdf"
    target_pdf.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_pdf, target_pdf)

    first_page = os.environ.get("EDT_HERKULES_FIRST_PAGE", "1")
    last_page = os.environ.get("EDT_HERKULES_LAST_PAGE", first_page)
    ocr_engine = os.environ.get("EDT_HERKULES_OCR_ENGINE", "tesseract")

    config_path = root / "edt.toml"
    config = config_path.read_text(encoding="utf-8")
    config = _replace_setting(config, "title", '"HERKULES"')
    config = _replace_setting(config, "first_page", first_page)
    config = _replace_setting(config, "last_page", last_page)
    config = _replace_setting(config, "ocr_engine", f'"{ocr_engine}"')
    config_path.write_text(config, encoding="utf-8")


def _run_cli(monkeypatch, *args: str) -> None:
    monkeypatch.setattr(sys, "argv", ["edt", *args])
    main()


def test_herkules_acceptance_import_build_check(tmp_path, monkeypatch):
    source_pdf = _herkules_source_pdf()
    if source_pdf is None:
        pytest.skip(
            "HERKULES acceptance source missing; set EDT_HERKULES_SOURCE_PDF"
        )

    monkeypatch.chdir(tmp_path)

    _run_cli(monkeypatch, "init")
    _configure_herkules_project(tmp_path, source_pdf)
    _run_cli(monkeypatch, "import")
    _run_cli(monkeypatch, "build")

    with pytest.raises(SystemExit) as check_exit:
        _run_cli(monkeypatch, "check")
    assert check_exit.value.code == 0

    import_report_path = tmp_path / "reports" / "import" / "import-report.json"
    canonical_path = tmp_path / "output" / "import" / "edom" / "canonical-document.edom.json"
    manifest_path = tmp_path / "output" / "build-manifest.json"
    validation_path = tmp_path / "reports" / "document" / "validation.json"
    reference_graph_path = tmp_path / "reports" / "document" / "reference-graph.json"
    quality_path = tmp_path / "reports" / "document" / "quality.json"

    assert import_report_path.exists()
    assert canonical_path.exists()
    assert manifest_path.exists()
    assert validation_path.exists()
    assert reference_graph_path.exists()
    assert quality_path.exists()

    import_report = json.loads(import_report_path.read_text(encoding="utf-8"))
    canonical = json.loads(canonical_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    quality = json.loads(quality_path.read_text(encoding="utf-8"))

    assert import_report["source_exists"] is True
    assert import_report["status"] == "imported"
    assert import_report["canonical_document_edom"]["pages"] >= 1
    assert canonical["page_count"] >= 1
    assert manifest["source_mode"] == "canonical-edom"
    assert manifest["document_reports"] is not None
    assert quality["publication_ready"] is True
