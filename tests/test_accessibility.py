from edt.accessibility import check_html_accessibility


def test_math_alttext_check(tmp_path):
    page = tmp_path / "page.html"
    page.write_text('<math alttext="x"><mtext>x</mtext></math>', encoding="utf-8")
    assert check_html_accessibility(page) == []


def test_img_alt_check(tmp_path):
    page = tmp_path / "page.html"
    page.write_text('<img src="x.png">', encoding="utf-8")
    assert check_html_accessibility(page)
