from edt.edom import EdomNode


def test_edom_fingerprint_stable():
    a = EdomNode(kind="paragraph", text="hello")
    b = EdomNode(kind="paragraph", text="hello")
    assert a.fingerprint == b.fingerprint


def test_edom_child_changes_fingerprint():
    node = EdomNode(kind="section", text="A")
    before = node.fingerprint
    node.add(EdomNode(kind="paragraph", text="body"))
    assert node.fingerprint != before
