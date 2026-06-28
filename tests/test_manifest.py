import json
from edt.manifest import write_manifest


def test_write_manifest(tmp_path):
    path = write_manifest(tmp_path, {"title": "Book"})
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["title"] == "Book"
