from edt.edom import EdomNode
from edt.edom_validate import duplicate_ids


def test_duplicate_ids_empty():
    root = EdomNode(kind="document")
    assert duplicate_ids(root) == []
