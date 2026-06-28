from edt.edom import EdomNode
from edt.edom_traverse import find_by_kind, postorder, preorder


def test_preorder():
    node = EdomNode(kind="document")
    node.add(EdomNode(kind="paragraph"))
    assert [item.kind for item in preorder(node)] == ["document", "paragraph"]


def test_postorder():
    node = EdomNode(kind="document")
    node.add(EdomNode(kind="paragraph"))
    assert [item.kind for item in postorder(node)] == ["paragraph", "document"]


def test_find_by_kind():
    node = EdomNode(kind="document")
    node.add(EdomNode(kind="paragraph"))
    assert len(find_by_kind(node, "paragraph")) == 1
