from __future__ import annotations

from pathlib import Path

from .config import ConfigError, load_project_config


def materialize_import_manifest(root: Path) -> Path:
    """Write a legacy-compatible import manifest from ``edt.toml``.

    The importer still consumes its established YAML-shaped manifest. This
    adapter keeps that implementation stable while making the unified project
    configuration authoritative for the CLI product path.
    """

    project = load_project_config(root)
    pdf_source = project.first_source("pdf")
    if pdf_source is None:
        raise ConfigError(
            'edt.toml must define a source with type = "pdf" for edt import'
        )

    manifest = root / project.paths.work / "import-project.yml"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        "source:\n"
        f"  primary_pdf: {pdf_source.path.as_posix()}\n"
        f"  start: {project.import_settings.first_page}\n"
        f"  end: {project.import_settings.last_page}\n"
        "import:\n"
        f"  engine: {project.import_settings.ocr_engine}\n"
        f"  language: {project.import_settings.ocr_language}\n"
        "outputs:\n"
        f"  edom: {(project.paths.output / 'import' / 'edom').as_posix()}\n"
        f"  reports: {(project.paths.reports / 'import').as_posix()}\n"
        f"  pages: {(project.paths.work / 'pages').as_posix()}\n",
        encoding="utf-8",
    )
    return manifest
