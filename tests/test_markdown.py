from edt.markdown import parse_markdown


def test_parse_headings():
    doc = parse_markdown("# Chapter\nText\n## Section\nMore")
    assert len(doc.sections) == 2
    assert doc.sections[0].title == "Chapter"
    assert doc.sections[1].level == 2
