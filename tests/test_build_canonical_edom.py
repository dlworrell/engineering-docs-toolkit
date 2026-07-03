import json

from edt.build import build_project


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
    canonical.parent.mkdir(parents=True)
    canonical.write_text(
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

    build_project(tmp_path)

    html = (tmp_path / "output" / "book.html").read_text(encoding="utf-8")
    manifest = json.loads(
        (tmp_path / "output" / "build-manifest.json").read_text(
            encoding="utf-8"
        )
    )

    assert "Canonical semantic content." in html
    assert "This text must not drive HTML output." not in html
    assert manifest["source_mode"] == "canonical-edom"
    assert manifest["canonical_edom"] == (
        "output/import/edom/canonical-document.edom.json"
    )
