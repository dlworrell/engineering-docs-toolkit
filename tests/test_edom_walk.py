from edt.edom import EdomNode
from edt.edom_walk import walk


def test_walk_visits_nodes():
    root = EdomNode(kind="document")
    root.add(EdomNode(kind="paragraph"))
    seen = []
    walk(root, lambda node: seen.append(node.kind))
    assert seen == ["document", "paragraph"]
