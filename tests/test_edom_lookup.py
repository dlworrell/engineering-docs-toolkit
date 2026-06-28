from edt.edom import EdomNode
from edt.edom_lookup import find_by_id


def test_find_by_id():
    root = EdomNode(kind="document", node_id="root")
    root.add(EdomNode(kind="paragraph", node_id="p1"))
    assert find_by_id(root, "p1") is not None
