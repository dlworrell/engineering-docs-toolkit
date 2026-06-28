from edt.edom import EdomNode
from edt.edom_json import node_to_dict


def test_node_to_dict():
    data = node_to_dict(EdomNode(kind="document"))
    assert data["kind"] == "document"
