from edt.edom import EdomNode
from edt.edom_json import dict_to_node, node_to_dict


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
