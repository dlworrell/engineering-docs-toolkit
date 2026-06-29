from edt.edom import EdomNode
from edt.edom_validate import duplicate_ids, heading_jumps, heading_level, missing_references, reference_targets


def test_duplicate_ids_empty():
    root = EdomNode(kind="document")
    assert duplicate_ids(root) == []


def test_duplicate_ids_detected():
    root = EdomNode(kind="document", node_id="same")
    root.add(EdomNode(kind="paragraph", node_id="same"))
    assert duplicate_ids(root) == ["same"]


def test_heading_level():
    assert heading_level("heading2") == 2


def test_heading_jumps():
    root = EdomNode(kind="document")
    root.add(EdomNode(kind="heading1", text="A"))
    root.add(EdomNode(kind="heading3", text="B"))
    assert heading_jumps(root) == ["B"]


def test_reference_targets():
    root = EdomNode(kind="document")
    root.add(EdomNode(kind="reference", text="x"))
    assert reference_targets(root) == ["x"]


def test_missing_references():
    root = EdomNode(kind="document", node_id="root")
    root.add(EdomNode(kind="reference", text="missing"))
    assert missing_references(root) == ["missing"]
