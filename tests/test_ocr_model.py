from edt.ocr_model import OcrBlock, OcrPage


def test_ocr_page_text_join():
    page = OcrPage(page_number=1)
    page.blocks.append(OcrBlock(text="Hello"))
    page.blocks.append(OcrBlock(text="World"))
    assert page.text == "Hello\nWorld"
