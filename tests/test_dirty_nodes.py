from edt.dirty_nodes import dirty_node_ids, fingerprint_map
from edt.edom import EdomNode


def test_fingerprint_map_contains_node_id():
    root = EdomNode(kind="document", node_id="root")
    result = fingerprint_map(root)
    assert "root" in result


def test_dirty_node_ids_detects_change():
    previous = {"root": "before"}
    current = {"root": "after"}
    result = dirty_node_ids(previous, current)
    assert "root" in result
