from edt.table_accessibility import AccessibleTable


def test_accessible_table_has_headers():
    table = AccessibleTable(table_id="table-1", headers=["Part", "Value"])
    assert table.has_headers
