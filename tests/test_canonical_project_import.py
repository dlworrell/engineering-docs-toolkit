import json
from pathlib import Path

from edt.ocr_model import OcrBlock, OcrPage
from edt.pdf_pages import PdfPageImage
from edt.project_import import import_project


def test_pdf_import_writes_page_independent_canonical_edom(tmp_path, monkeypatch):
    manifest = tmp_path / "edt" / "project.yml"
    manifest.parent.mkdir()
    manifest.write_text(
        "source:\n"
        "  primary_pdf: source/original/book.pdf\n"
        "  start: 1\n"
        "  end: 2\n"
        "outputs:\n"
        "  edom: output/import/edom\n"
        "  reports: reports/import\n"
        "  pages: pages\n",
        encoding="utf-8",
    )

    source = tmp_path / "source" / "original" / "book.pdf"
    source.parent.mkdir(parents=True)
    source.write_bytes(b"%PDF-1.7\n")

    def fake_extract(
        pdf_path: Path,
        output_dir: Path,
        first_page: int,
        last_page: int,
    ):
        output_dir.mkdir(parents=True)
        rendered_pages = []
        for page_number in range(first_page, last_page + 1):
            rendered = output_dir / f"page-{page_number:04d}.png"
            rendered.write_bytes(b"png")
            rendered_pages.append(
                PdfPageImage(
                    pdf_path=pdf_path,
                    page_number=page_number,
                    image_path=rendered,
                )
            )
        return rendered_pages

    class FakeOcrEngine:
        name = "fake"

        def recognize_image(self, image_path: Path, page_number: int = 1):
            if page_number == 1:
                blocks = [OcrBlock(text="x = 1 (2.3)", confidence=0.99)]
            else:
                blocks = [
                    OcrBlock(
                        text="Equation (2.3) is used here.",
                        confidence=0.99,
                    )
                ]
            return OcrPage(page_number=page_number, blocks=blocks)

    monkeypatch.setattr("edt.project_import.extract_pdf_pages", fake_extract)
    monkeypatch.setattr(
        "edt.project_import.make_ocr_engine",
        lambda config: FakeOcrEngine(),
    )

    result = import_project(tmp_path)

    canonical_path = (
        tmp_path
        / "output"
        / "import"
        / "edom"
        / "canonical-document.edom.json"
    )
    payload = json.loads(canonical_path.read_text(encoding="utf-8"))
    root = payload["root"]

    assert payload["page_count"] == 2
    assert root["kind"] == "document"
    assert [child["kind"] for child in root["children"]] == [
        "equation",
        "paragraph",
    ]
    assert all(child["kind"] != "page" for child in root["children"])

    equation, paragraph = root["children"]
    assert equation["source_regions"] == [
        {"source_id": "primary", "page": 1}
    ]
    assert paragraph["source_regions"] == [
        {"source_id": "primary", "page": 2}
    ]
    assert paragraph["metadata"]["references"] == equation["id"]

    report = json.loads(result.report_path.read_text(encoding="utf-8"))
    assert report["canonical_document_edom"] == {
        "status": "complete",
        "document": "output/import/edom/canonical-document.edom.json",
        "pages": 2,
        "nodes": 2,
    }
