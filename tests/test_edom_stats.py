from edt.edom import EdomNode
from edt.edom_stats import count_kind, count_nodes


def test_count_nodes():
    node = EdomNode(kind="document")
    node.add(EdomNode(kind="paragraph"))
    assert count_nodes(node) == 2


def test_count_kind():
    node = EdomNode(kind="document")
    node.add(EdomNode(kind="paragraph"))
    assert count_kind(node, "paragraph") == 1
