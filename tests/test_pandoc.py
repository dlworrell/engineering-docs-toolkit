from edt.pandoc import pandoc_available


def test_pandoc_available_returns_bool():
    assert isinstance(pandoc_available(), bool)
