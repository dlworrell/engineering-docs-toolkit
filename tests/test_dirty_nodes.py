from edt.dirty_nodes import fingerprint_map
from edt.edom import EdomNode


def test_fingerprint_map_contains_node_id():
    root = EdomNode(kind="document", node_id="root")
    result = fingerprint_map(root)
    assert "root" in result
