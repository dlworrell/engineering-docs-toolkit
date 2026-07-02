from pathlib import Path

import pytest

from edt.config import ConfigError, load_config, load_project_config


def test_load_title(tmp_path):
    (tmp_path / "book.yaml").write_text("title: Test Book\n", encoding="utf-8")
    assert load_config(tmp_path).title == "Test Book"


def test_load_outputs(tmp_path):
    (tmp_path / "book.yaml").write_text(
        "outputs:\n  - html\n  - epub\n",
        encoding="utf-8",
    )
    assert load_config(tmp_path).outputs == ["html", "epub"]


def test_load_project_config_defaults(tmp_path):
    config = load_project_config(tmp_path)

    assert config.schema_version == 1
    assert config.project.title == "Untitled Engineering Document"
    assert config.project.language == "en"
    assert config.paths.work == Path(".edt/work")
    assert config.paths.reports == Path("reports")
    assert config.paths.output == Path("output")
    assert config.import_settings.first_page == 1
    assert config.import_settings.last_page == 1
    assert config.import_settings.ocr_engine == "null"
    assert config.validation.fail_on == "error"
    assert config.publish.formats == ("html",)

    source = config.first_source("markdown")
    assert source is not None
    assert source.source_id == "chapters"
    assert source.path == Path("source/english")


def test_load_project_config_from_toml(tmp_path):
    (tmp_path / "edt.toml").write_text(
        'schema_version = 1\n'
        '\n'
        '[project]\n'
        'title = "Herkules Manual"\n'
        'language = "sv"\n'
        '\n'
        '[paths]\n'
        'work = ".edt/custom-work"\n'
        'reports = "build/reports"\n'
        'output = "build/output"\n'
        '\n'
        '[[sources]]\n'
        'id = "primary"\n'
        'type = "pdf"\n'
        'path = "source/original/herkules.pdf"\n'
        '\n'
        '[[sources]]\n'
        'id = "chapters"\n'
        'type = "markdown"\n'
        'path = "source/edited"\n'
        '\n'
        '[import]\n'
        'first_page = 4\n'
        'last_page = 12\n'
        'ocr_engine = "tesseract"\n'
        'ocr_language = "swe"\n'
        '\n'
        '[validation]\n'
        'fail_on = "warning"\n'
        '\n'
        '[publish]\n'
        'formats = ["html", "epub", "html"]\n',
        encoding="utf-8",
    )

    config = load_project_config(tmp_path)

    assert config.project.title == "Herkules Manual"
    assert config.project.language == "sv"
    assert config.paths.work == Path(".edt/custom-work")
    assert config.paths.reports == Path("build/reports")
    assert config.paths.output == Path("build/output")
    assert config.import_settings.first_page == 4
    assert config.import_settings.last_page == 12
    assert config.import_settings.ocr_engine == "tesseract"
    assert config.import_settings.ocr_language == "swe"
    assert config.validation.fail_on == "warning"
    assert config.publish.formats == ("html", "epub")

    pdf_source = config.first_source("pdf")
    assert pdf_source is not None
    assert pdf_source.source_id == "primary"
    assert pdf_source.path == Path("source/original/herkules.pdf")

    markdown_source = config.first_source("MARKDOWN")
    assert markdown_source is not None
    assert markdown_source.path == Path("source/edited")


def test_book_config_uses_unified_project_config(tmp_path):
    (tmp_path / "book.yaml").write_text(
        "title: Legacy Book\noutputs:\n  - md\n",
        encoding="utf-8",
    )
    (tmp_path / "edt.toml").write_text(
        '[project]\n'
        'title = "Unified Book"\n'
        '\n'
        '[paths]\n'
        'output = "build/publication"\n'
        '\n'
        '[[sources]]\n'
        'id = "chapters"\n'
        'type = "markdown"\n'
        'path = "manuscript"\n'
        '\n'
        '[publish]\n'
        'formats = ["html", "docx"]\n',
        encoding="utf-8",
    )

    config = load_config(tmp_path)

    assert config.title == "Unified Book"
    assert config.source_dir == Path("manuscript")
    assert config.output_dir == Path("build/publication")
    assert config.outputs == ["html", "docx"]


def test_rejects_unsupported_schema_version(tmp_path):
    (tmp_path / "edt.toml").write_text(
        "schema_version = 2\n",
        encoding="utf-8",
    )

    with pytest.raises(ConfigError, match="unsupported schema_version"):
        load_project_config(tmp_path)


def test_rejects_duplicate_source_ids(tmp_path):
    (tmp_path / "edt.toml").write_text(
        '[[sources]]\n'
        'id = "primary"\n'
        'type = "pdf"\n'
        'path = "one.pdf"\n'
        '\n'
        '[[sources]]\n'
        'id = "primary"\n'
        'type = "markdown"\n'
        'path = "chapters"\n',
        encoding="utf-8",
    )

    with pytest.raises(ConfigError, match="duplicate source id"):
        load_project_config(tmp_path)


def test_rejects_unsupported_source_type(tmp_path):
    (tmp_path / "edt.toml").write_text(
        '[[sources]]\n'
        'id = "website"\n'
        'type = "html"\n'
        'path = "source.html"\n',
        encoding="utf-8",
    )

    with pytest.raises(ConfigError, match="must be one of"):
        load_project_config(tmp_path)


def test_rejects_invalid_page_range(tmp_path):
    (tmp_path / "edt.toml").write_text(
        '[import]\n'
        'first_page = 8\n'
        'last_page = 3\n',
        encoding="utf-8",
    )

    with pytest.raises(ConfigError, match="greater than or equal"):
        load_project_config(tmp_path)


def test_rejects_invalid_validation_threshold(tmp_path):
    (tmp_path / "edt.toml").write_text(
        '[validation]\n'
        'fail_on = "fatal"\n',
        encoding="utf-8",
    )

    with pytest.raises(ConfigError, match="info, warning, or error"):
        load_project_config(tmp_path)
