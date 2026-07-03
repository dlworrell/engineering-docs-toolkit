import json

import pytest

from edt.build import build_project


def write_canonical_edom(path):
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            {
                "root": {
                    "id": "document",
                    "kind": "document",
                    "children": [
                        {
                            "id": "title",
                            "kind": "title",
                            "text": "HERKULES",
                            "children": [],
                        },
                        {
                            "id": "p1",
                            "kind": "paragraph",
                            "text": "Canonical semantic content.",
                            "children": [],
                        },
                    ],
                }
            }
        ),
        encoding="utf-8",
    )


def test_build_uses_canonical_edom_when_available(tmp_path):
    source = tmp_path / "source" / "english"
    source.mkdir(parents=True)
    (source / "01-stale.md").write_text(
        "# Stale Markdown\n\nThis text must not drive HTML output.\n",
        encoding="utf-8",
    )
    (tmp_path / "book.yaml").write_text(
        "title: HERKULES\n"
        "source_dir: source/english\n"
        "output_dir: output\n"
        "outputs:\n"
        "  - md\n"
        "  - html\n",
        encoding="utf-8",
    )

    canonical = (
        tmp_path
        / "output"
        / "import"
        / "edom"
        / "canonical-document.edom.json"
    )
    write_canonical_edom(canonical)

    build_project(tmp_path)

    markdown = (tmp_path / "output" / "book.md").read_text(encoding="utf-8")
    html = (tmp_path / "output" / "book.html").read_text(encoding="utf-8")
    manifest = json.loads(
        (tmp_path / "output" / "build-manifest.json").read_text(
            encoding="utf-8"
        )
    )

    assert "Canonical semantic content." in markdown
    assert "This text must not drive HTML output." not in markdown
    assert "Canonical semantic content." in html
    assert "This text must not drive HTML output." not in html
    assert manifest["source_mode"] == "canonical-edom"
    assert manifest["canonical_edom"] == (
        "output/import/edom/canonical-document.edom.json"
    )


def test_build_uses_canonical_markdown_for_pandoc_outputs(tmp_path, monkeypatch):
    source = tmp_path / "source" / "english"
    source.mkdir(parents=True)
    (source / "01-stale.md").write_text(
        "# Stale Markdown\n\nThis text must not drive DOCX output.\n",
        encoding="utf-8",
    )
    (tmp_path / "book.yaml").write_text(
        "title: HERKULES\n"
        "source_dir: source/english\n"
        "output_dir: output\n"
        "outputs:\n"
        "  - html\n"
        "  - docx\n",
        encoding="utf-8",
    )

    canonical = (
        tmp_path
        / "output"
        / "import"
        / "edom"
        / "canonical-document.edom.json"
    )
    write_canonical_edom(canonical)
    pandoc_sources = []

    def fake_pandoc(source_path, output_path):
        pandoc_sources.append(source_path.read_text(encoding="utf-8"))
        output_path.write_text("converted", encoding="utf-8")
        return True

    monkeypatch.setattr("edt.build.run_pandoc", fake_pandoc)

    build_project(tmp_path)

    assert pandoc_sources == ["# HERKULES\n\nCanonical semantic content.\n"]
    assert (tmp_path / "output" / "book.docx").exists()
    assert "This text must not drive DOCX output." not in pandoc_sources[0]


def test_build_fails_when_requested_pandoc_output_is_unavailable(
    tmp_path,
    monkeypatch,
):
    source = tmp_path / "source" / "english"
    source.mkdir(parents=True)
    (source / "01.md").write_text("# Book\n\nBody.\n", encoding="utf-8")
    (tmp_path / "book.yaml").write_text(
        "title: Book\n"
        "source_dir: source/english\n"
        "output_dir: output\n"
        "outputs:\n"
        "  - html\n"
        "  - docx\n",
        encoding="utf-8",
    )
    monkeypatch.setattr("edt.build.run_pandoc", lambda source_path, output_path: False)

    with pytest.raises(RuntimeError, match="requested docx output"):
        build_project(tmp_path)

    assert not (tmp_path / "output" / "book.docx").exists()
