from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .simple_yaml import read_simple_yaml


class ConfigError(ValueError):
    """Raised when an EDT project configuration is invalid."""


@dataclass(frozen=True)
class SourceConfig:
    source_id: str
    source_type: str
    path: Path


@dataclass(frozen=True)
class ProjectMetadata:
    title: str = "Untitled Engineering Document"
    language: str = "en"


@dataclass(frozen=True)
class ProjectPaths:
    work: Path = Path(".edt/work")
    reports: Path = Path("reports")
    output: Path = Path("output")


@dataclass(frozen=True)
class ImportSettings:
    first_page: int = 1
    last_page: int = 1
    ocr_engine: str = "null"
    ocr_language: str = "eng"


@dataclass(frozen=True)
class ValidationSettings:
    fail_on: str = "error"


@dataclass(frozen=True)
class PublishSettings:
    formats: tuple[str, ...] = ("html",)


@dataclass(frozen=True)
class ProjectConfig:
    schema_version: int = 1
    project: ProjectMetadata = field(default_factory=ProjectMetadata)
    paths: ProjectPaths = field(default_factory=ProjectPaths)
    sources: tuple[SourceConfig, ...] = field(
        default_factory=lambda: (
            SourceConfig(
                source_id="chapters",
                source_type="markdown",
                path=Path("source/english"),
            ),
        )
    )
    import_settings: ImportSettings = field(default_factory=ImportSettings)
    validation: ValidationSettings = field(default_factory=ValidationSettings)
    publish: PublishSettings = field(default_factory=PublishSettings)

    def first_source(self, source_type: str) -> SourceConfig | None:
        normalized = source_type.strip().lower()
        return next(
            (source for source in self.sources if source.source_type == normalized),
            None,
        )


@dataclass
class BookConfig:
    title: str = "Untitled Engineering Book"
    source_dir: Path = Path("source/english")
    output_dir: Path = Path("output")
    outputs: list[str] = field(default_factory=lambda: ["md", "html"])


def _mapping(value: object, name: str) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ConfigError(f"{name} must be a TOML table")
    return value


def _string(table: dict[str, Any], key: str, default: str, name: str) -> str:
    value = table.get(key, default)
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{name}.{key} must be a non-empty string")
    return value.strip()


def _integer(table: dict[str, Any], key: str, default: int, name: str) -> int:
    value = table.get(key, default)
    if type(value) is not int:
        raise ConfigError(f"{name}.{key} must be an integer")
    return value


def _parse_sources(raw: object) -> tuple[SourceConfig, ...]:
    if raw is None:
        return ProjectConfig().sources
    if not isinstance(raw, list) or not raw:
        raise ConfigError("sources must be a non-empty array of tables")

    sources: list[SourceConfig] = []
    identifiers: set[str] = set()
    supported_types = {"markdown", "pdf"}

    for index, entry in enumerate(raw, start=1):
        name = f"sources[{index}]"
        table = _mapping(entry, name)
        source_id = _string(table, "id", "", name)
        source_type = _string(table, "type", "", name).lower()
        source_path = Path(_string(table, "path", "", name))

        if source_id in identifiers:
            raise ConfigError(f"duplicate source id: {source_id}")
        if source_type not in supported_types:
            supported = ", ".join(sorted(supported_types))
            raise ConfigError(
                f"{name}.type must be one of: {supported}; got {source_type}"
            )

        identifiers.add(source_id)
        sources.append(
            SourceConfig(
                source_id=source_id,
                source_type=source_type,
                path=source_path,
            )
        )

    return tuple(sources)


def load_project_config(root: Path) -> ProjectConfig:
    path = root / "edt.toml"
    if not path.exists():
        return ProjectConfig()

    try:
        with path.open("rb") as stream:
            raw = tomllib.load(stream)
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"invalid TOML in {path}: {exc}") from exc

    schema_version = raw.get("schema_version", 1)
    if type(schema_version) is not int:
        raise ConfigError("schema_version must be an integer")
    if schema_version != 1:
        raise ConfigError(f"unsupported schema_version: {schema_version}")

    project_raw = _mapping(raw.get("project"), "project")
    paths_raw = _mapping(raw.get("paths"), "paths")
    import_raw = _mapping(raw.get("import"), "import")
    validation_raw = _mapping(raw.get("validation"), "validation")
    publish_raw = _mapping(raw.get("publish"), "publish")

    project = ProjectMetadata(
        title=_string(
            project_raw,
            "title",
            ProjectMetadata.title,
            "project",
        ),
        language=_string(
            project_raw,
            "language",
            ProjectMetadata.language,
            "project",
        ),
    )

    paths = ProjectPaths(
        work=Path(_string(paths_raw, "work", str(ProjectPaths.work), "paths")),
        reports=Path(
            _string(paths_raw, "reports", str(ProjectPaths.reports), "paths")
        ),
        output=Path(
            _string(paths_raw, "output", str(ProjectPaths.output), "paths")
        ),
    )

    first_page = _integer(
        import_raw,
        "first_page",
        ImportSettings.first_page,
        "import",
    )
    last_page = _integer(
        import_raw,
        "last_page",
        first_page,
        "import",
    )
    if first_page < 1:
        raise ConfigError("import.first_page must be at least 1")
    if last_page < first_page:
        raise ConfigError("import.last_page must be greater than or equal to first_page")

    import_settings = ImportSettings(
        first_page=first_page,
        last_page=last_page,
        ocr_engine=_string(
            import_raw,
            "ocr_engine",
            ImportSettings.ocr_engine,
            "import",
        ).lower(),
        ocr_language=_string(
            import_raw,
            "ocr_language",
            ImportSettings.ocr_language,
            "import",
        ),
    )

    fail_on = _string(
        validation_raw,
        "fail_on",
        ValidationSettings.fail_on,
        "validation",
    ).lower()
    if fail_on not in {"info", "warning", "error"}:
        raise ConfigError("validation.fail_on must be info, warning, or error")
    validation = ValidationSettings(fail_on=fail_on)

    formats_raw = publish_raw.get("formats", list(PublishSettings.formats))
    if not isinstance(formats_raw, list) or not formats_raw:
        raise ConfigError("publish.formats must be a non-empty array of strings")
    formats: list[str] = []
    for index, value in enumerate(formats_raw, start=1):
        if not isinstance(value, str) or not value.strip():
            raise ConfigError(
                f"publish.formats[{index}] must be a non-empty string"
            )
        normalized = value.strip().lower()
        if normalized not in formats:
            formats.append(normalized)
    publish = PublishSettings(formats=tuple(formats))

    return ProjectConfig(
        schema_version=schema_version,
        project=project,
        paths=paths,
        sources=_parse_sources(raw.get("sources")),
        import_settings=import_settings,
        validation=validation,
        publish=publish,
    )


def load_config(root: Path) -> BookConfig:
    unified_path = root / "edt.toml"
    if unified_path.exists():
        project = load_project_config(root)
        markdown_source = project.first_source("markdown")
        return BookConfig(
            title=project.project.title,
            source_dir=(
                markdown_source.path
                if markdown_source is not None
                else Path("source/english")
            ),
            output_dir=project.paths.output,
            outputs=list(project.publish.formats),
        )

    path = root / "book.yaml"
    cfg = BookConfig()
    if not path.exists():
        return cfg
    raw = read_simple_yaml(path)
    title = raw.get("title")
    source_dir = raw.get("source_dir")
    output_dir = raw.get("output_dir")
    outputs = raw.get("outputs")
    if isinstance(title, str):
        cfg.title = title
    if isinstance(source_dir, str):
        cfg.source_dir = Path(source_dir)
    if isinstance(output_dir, str):
        cfg.output_dir = Path(output_dir)
    if isinstance(outputs, list):
        cfg.outputs = [str(item) for item in outputs]
    return cfg
