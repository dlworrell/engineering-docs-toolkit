from edt.edom import EdomNode
from edt.edom_json import node_to_dict


def test_node_to_dict_kind():
    data = node_to_dict(EdomNode(kind="document"))
    assert data["kind"] == "document"


def test_node_to_dict_fingerprint():
    data = node_to_dict(EdomNode(kind="document"))
    assert "fingerprint" in data
