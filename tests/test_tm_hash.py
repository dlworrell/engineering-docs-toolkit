from edt.hash_cache import hash_text
from edt.tm_hash import lookup_text_hash
from edt.translation_memory import add_term


def test_lookup_text_hash(tmp_path):
    db = tmp_path / "memory.sqlite"
    add_term(db, hash_text("A"), "B")
    assert lookup_text_hash(db, "A") == "B"
