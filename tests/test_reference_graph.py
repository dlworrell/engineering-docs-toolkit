import json

from edt.reference_graph import build_reference_graph


def test_build_reference_graph_tracks_edges_and_broken_refs():
    graph = build_reference_graph(
        {
            "root": {
                "id": "document",
                "kind": "document",
                "children": [
                    {
                        "id": "page-1",
                        "kind": "page",
                        "children": [
                            {"id": "fig1", "kind": "figure", "text": "", "children": [{"id": "cap1", "kind": "caption", "text": "Figure 1"}]},
                            {"id": "p1", "kind": "paragraph", "text": "See fig.", "metadata": {"references": ["fig1", "missing"]}},
                        ],
                    }
                ],
            }
        }
    )

    assert graph.nodes["p1"].outgoing == ["fig1"]
    assert graph.nodes["p1"].broken == ["missing"]
    assert graph.nodes["fig1"].incoming == ["p1"]
    assert graph.to_dict()["summary"]["edges"] == 1
    assert graph.to_dict()["summary"]["broken"] == 1


def test_build_reference_graph_marks_orphans():
    graph = build_reference_graph(
        {
            "root": {
                "id": "document",
                "kind": "document",
                "children": [
                    {
                        "id": "page-1",
                        "kind": "page",
                        "children": [
                            {"id": "fig1", "kind": "figure", "text": "", "children": [{"id": "cap1", "kind": "caption", "text": "Figure 1"}]},
                            {"id": "fig2", "kind": "figure", "text": "", "metadata": {"unreferenced_ok": True}, "children": [{"id": "cap2", "kind": "caption", "text": "Figure 2"}]},
                        ],
                    }
                ],
            }
        }
    )

    assert graph.nodes["fig1"].orphan is True
    assert graph.nodes["fig2"].orphan is False
    assert graph.to_dict()["summary"]["orphans"] == 1


def test_reference_graph_writes_reports(tmp_path):
    graph = build_reference_graph({"root": {"id": "document", "kind": "document", "children": [{"id": "page-1", "kind": "page"}]}})

    json_path = graph.write_json(tmp_path / "reference-index.json")
    md_path = graph.write_markdown(tmp_path / "reference-index.md")

    assert json.loads(json_path.read_text(encoding="utf-8"))["summary"]["nodes"] == 2
    assert "EDT Reference Index" in md_path.read_text(encoding="utf-8")
