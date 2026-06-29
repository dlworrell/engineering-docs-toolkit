from edt.edom import EdomNode
from edt.edom_json import dict_to_node, node_to_dict, read_edom_json


def test_node_to_dict_kind():
    data = node_to_dict(EdomNode(kind="document"))
    assert data["kind"] == "document"


def test_node_to_dict_fingerprint():
    data = node_to_dict(EdomNode(kind="document"))
    assert "fingerprint" in data


def test_node_to_dict_children():
    node = EdomNode(kind="document")
    node.add(EdomNode(kind="paragraph"))
    data = node_to_dict(node)
    assert len(data["children"]) == 1


def test_dict_to_node():
    node = dict_to_node({"id": "x", "kind": "document", "text": "Book"})
    assert node.node_id == "x"


def test_dict_to_node_children():
    data = {"id": "x", "kind": "document", "children": [{"id": "y", "kind": "paragraph"}]}
    assert len(dict_to_node(data).children) == 1


def test_read_edom_json(tmp_path):
    path = tmp_path / "edom.json"
    path.write_text('{"id":"x","kind":"document"}', encoding="utf-8")
    assert read_edom_json(path).node_id == "x"
