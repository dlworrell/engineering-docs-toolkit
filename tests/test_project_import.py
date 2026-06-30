import json
from pathlib import Path

from edt.ocr_model import OcrBlock, OcrPage
from edt.pdf_pages import PdfPageImage
from edt.project_import import import_project, load_project_import_config


def test_project_import_reports_missing_source(tmp_path):
    manifest_dir = tmp_path / "edt"
    manifest_dir.mkdir()
    (manifest_dir / "project.yml").write_text(
        "source:\n"
        "  primary_pdf: source/original/herkules-manual.pdf\n"
        "  start: 1\n"
        "  end: 3\n"
        "outputs:\n"
        "  edom: output/pilot/edom\n"
        "  reports: reports/pilot\n"
        "  pages: pages\n",
        encoding="utf-8",
    )

    result = import_project(tmp_path)

    assert result.source_exists is False
    assert result.fingerprint == "missing"
    assert result.report_path.exists()
    report = json.loads(result.report_path.read_text(encoding="utf-8"))
    assert report["status"] == "waiting_for_source_pdf"
    assert report["page_range"] == {"start": 1, "end": 3}
    assert len(report["pages"]) == 3
    assert (tmp_path / "source" / "original" / "SHA256SUMS").exists()
    assert (tmp_path / "source" / "original" / "provenance.md").exists()
    assert (tmp_path / "pages" / "0001" / "manifest.json").exists()
    assert (tmp_path / "pages" / "0003" / "manifest.json").exists()


def test_project_import_hashes_existing_source(tmp_path):
    source = tmp_path / "source" / "original" / "herkules-manual.pdf"
    source.parent.mkdir(parents=True)
    source.write_text("fake pdf content", encoding="utf-8")

    result = import_project(tmp_path)

    assert result.source_exists is True
    assert result.fingerprint != "missing"
    assert (tmp_path / "output" / "import" / "edom" / "import-notes.md").exists()
    page_manifest = json.loads((tmp_path / "pages" / "0001" / "manifest.json").read_text(encoding="utf-8"))
    assert page_manifest["status"] == "initialized"
    assert page_manifest["image_status"] == "skipped_not_pdf"
    assert page_manifest["ocr_status"] == "waiting_for_image"
    assert page_manifest["layout_status"] == "waiting_for_ocr"
    assert page_manifest["semantic_status"] == "waiting_for_layout"
    assert page_manifest["edom_status"] == "waiting_for_semantic"


def test_project_import_extracts_pdf_page_images(tmp_path, monkeypatch):
    source = tmp_path / "source" / "original" / "herkules-manual.pdf"
    source.parent.mkdir(parents=True)
    source.write_bytes(b"%PDF-1.7\n")

    def fake_extract(pdf_path: Path, output_dir: Path, first_page: int, last_page: int):
        output_dir.mkdir(parents=True)
        rendered = output_dir / "page-0001.png"
        rendered.write_bytes(b"png")
        return [PdfPageImage(pdf_path=pdf_path, page_number=1, image_path=rendered)]

    monkeypatch.setattr("edt.project_import.extract_pdf_pages", fake_extract)
    result = import_project(tmp_path)

    assert result.source_exists is True
    assert (tmp_path / "pages" / "0001" / "image.png").read_bytes() == b"png"
    page_manifest = json.loads((tmp_path / "pages" / "0001" / "manifest.json").read_text(encoding="utf-8"))
    assert page_manifest["image_status"] == "extracted"


def test_project_import_writes_ocr_artifact(tmp_path, monkeypatch):
    source = tmp_path / "source" / "original" / "herkules-manual.pdf"
    source.parent.mkdir(parents=True)
    source.write_bytes(b"%PDF-1.7\n")

    def fake_extract(pdf_path: Path, output_dir: Path, first_page: int, last_page: int):
        output_dir.mkdir(parents=True)
        rendered = output_dir / "page-0001.png"
        rendered.write_bytes(b"png")
        return [PdfPageImage(pdf_path=pdf_path, page_number=1, image_path=rendered)]

    class FakeOcrEngine:
        name = "fake"

        def recognize_image(self, image_path: Path, page_number: int = 1):
            return OcrPage(page_number=page_number, blocks=[OcrBlock(text="Herkules", confidence=0.9)])

    monkeypatch.setattr("edt.project_import.extract_pdf_pages", fake_extract)
    monkeypatch.setattr("edt.project_import.make_ocr_engine", lambda config: FakeOcrEngine())
    import_project(tmp_path)

    ocr_payload = json.loads((tmp_path / "pages" / "0001" / "ocr.json").read_text(encoding="utf-8"))
    assert ocr_payload["engine"] == "fake"
    assert ocr_payload["text"] == "Herkules"
    page_manifest = json.loads((tmp_path / "pages" / "0001" / "manifest.json").read_text(encoding="utf-8"))
    assert page_manifest["ocr_status"] == "complete"


def test_project_import_writes_layout_artifact(tmp_path, monkeypatch):
    source = tmp_path / "source" / "original" / "herkules-manual.pdf"
    source.parent.mkdir(parents=True)
    source.write_bytes(b"%PDF-1.7\n")

    def fake_extract(pdf_path: Path, output_dir: Path, first_page: int, last_page: int):
        output_dir.mkdir(parents=True)
        rendered = output_dir / "page-0001.png"
        rendered.write_bytes(b"png")
        return [PdfPageImage(pdf_path=pdf_path, page_number=1, image_path=rendered)]

    class FakeOcrEngine:
        name = "fake"

        def recognize_image(self, image_path: Path, page_number: int = 1):
            return OcrPage(page_number=page_number, blocks=[OcrBlock(text="HERKULES", confidence=0.9)])

    monkeypatch.setattr("edt.project_import.extract_pdf_pages", fake_extract)
    monkeypatch.setattr("edt.project_import.make_ocr_engine", lambda config: FakeOcrEngine())
    import_project(tmp_path)

    layout_payload = json.loads((tmp_path / "pages" / "0001" / "layout.json").read_text(encoding="utf-8"))
    assert layout_payload["blocks"][0]["kind"] == "heading"
    assert layout_payload["blocks"][0]["text"] == "HERKULES"
    page_manifest = json.loads((tmp_path / "pages" / "0001" / "manifest.json").read_text(encoding="utf-8"))
    assert page_manifest["layout_status"] == "complete"


def test_project_import_writes_semantic_artifact(tmp_path, monkeypatch):
    source = tmp_path / "source" / "original" / "herkules-manual.pdf"
    source.parent.mkdir(parents=True)
    source.write_bytes(b"%PDF-1.7\n")

    def fake_extract(pdf_path: Path, output_dir: Path, first_page: int, last_page: int):
        output_dir.mkdir(parents=True)
        rendered = output_dir / "page-0001.png"
        rendered.write_bytes(b"png")
        return [PdfPageImage(pdf_path=pdf_path, page_number=1, image_path=rendered)]

    class FakeOcrEngine:
        name = "fake"

        def recognize_image(self, image_path: Path, page_number: int = 1):
            return OcrPage(page_number=page_number, blocks=[OcrBlock(text="Theorem 1.1", confidence=0.9), OcrBlock(text="Proof.", confidence=0.9)])

    monkeypatch.setattr("edt.project_import.extract_pdf_pages", fake_extract)
    monkeypatch.setattr("edt.project_import.make_ocr_engine", lambda config: FakeOcrEngine())
    import_project(tmp_path)

    semantic_payload = json.loads((tmp_path / "pages" / "0001" / "semantic.json").read_text(encoding="utf-8"))
    assert semantic_payload["blocks"][0]["semantic_kind"] == "theorem"
    assert semantic_payload["blocks"][1]["semantic_kind"] == "proof"
    assert semantic_payload["relationships"][0]["relationship"] == "has_proof"
    page_manifest = json.loads((tmp_path / "pages" / "0001" / "manifest.json").read_text(encoding="utf-8"))
    assert page_manifest["semantic_status"] == "complete"


def test_project_import_writes_edom_artifact(tmp_path, monkeypatch):
    source = tmp_path / "source" / "original" / "herkules-manual.pdf"
    source.parent.mkdir(parents=True)
    source.write_bytes(b"%PDF-1.7\n")

    def fake_extract(pdf_path: Path, output_dir: Path, first_page: int, last_page: int):
        output_dir.mkdir(parents=True)
        rendered = output_dir / "page-0001.png"
        rendered.write_bytes(b"png")
        return [PdfPageImage(pdf_path=pdf_path, page_number=1, image_path=rendered)]

    class FakeOcrEngine:
        name = "fake"

        def recognize_image(self, image_path: Path, page_number: int = 1):
            return OcrPage(page_number=page_number, blocks=[OcrBlock(text="Theorem 1.1", confidence=0.9), OcrBlock(text="Proof.", confidence=0.9)])

    monkeypatch.setattr("edt.project_import.extract_pdf_pages", fake_extract)
    monkeypatch.setattr("edt.project_import.make_ocr_engine", lambda config: FakeOcrEngine())
    import_project(tmp_path)

    edom_payload = json.loads((tmp_path / "pages" / "0001" / "edom.json").read_text(encoding="utf-8"))
    assert edom_payload["root"]["kind"] == "page"
    assert edom_payload["root"]["children"][0]["kind"] == "theorem"
    assert edom_payload["root"]["children"][1]["kind"] == "proof"
    page_manifest = json.loads((tmp_path / "pages" / "0001" / "manifest.json").read_text(encoding="utf-8"))
    assert page_manifest["edom_status"] == "complete"


def test_load_project_import_config_uses_manifest_values(tmp_path):
    manifest = tmp_path / "edt" / "project.yml"
    manifest.parent.mkdir()
    manifest.write_text(
        "source:\n"
        "  primary_pdf: source/original/book.pdf\n"
        "  start: 4\n"
        "  end: 6\n"
        "ocr:\n"
        "  engine: tesseract\n"
        "  language: swe\n"
        "outputs:\n"
        "  edom: output/custom/edom\n"
        "  reports: reports/custom\n"
        "  pages: import-pages\n",
        encoding="utf-8",
    )

    config = load_project_import_config(tmp_path)

    assert config.source_pdf == tmp_path / "source" / "original" / "book.pdf"
    assert config.output_dir == tmp_path / "output" / "custom" / "edom"
    assert config.report_dir == tmp_path / "reports" / "custom"
    assert config.pages_dir == tmp_path / "import-pages"
    assert config.first_page == 4
    assert config.last_page == 6
    assert config.ocr_engine == "tesseract"
    assert config.ocr_language == "swe"
