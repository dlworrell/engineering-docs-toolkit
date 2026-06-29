from edt.edom import EdomNode
from edt.edom_validate import duplicate_ids, heading_jumps, heading_level


def test_duplicate_ids_empty():
    root = EdomNode(kind="document")
    assert duplicate_ids(root) == []


def test_duplicate_ids_detected():
    root = EdomNode(kind="document", node_id="same")
    root.add(EdomNode(kind="paragraph", node_id="same"))
    assert duplicate_ids(root) == ["same"]


def test_heading_level():
    assert heading_level("heading2") == 2
