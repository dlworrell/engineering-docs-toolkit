from __future__ import annotations

import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

from .config import ProjectConfig, load_project_config


@dataclass(frozen=True)
class DependencyStatus:
    name: str
    required: bool
    available: bool
    detail: str


@dataclass(frozen=True)
class DoctorReport:
    dependencies: tuple[DependencyStatus, ...]

    @property
    def ready(self) -> bool:
        return all(item.available for item in self.dependencies if item.required)

    @property
    def missing_required(self) -> tuple[DependencyStatus, ...]:
        return tuple(
            item
            for item in self.dependencies
            if item.required and not item.available
        )

    def to_text(self) -> str:
        lines = ["EDT dependency report", ""]
        width = max((len(item.name) for item in self.dependencies), default=0)
        for item in self.dependencies:
            if item.available:
                state = "found"
            elif item.required:
                state = "missing"
            else:
                state = "not required"
            lines.append(f"{item.name.ljust(width)}  {state}  {item.detail}")
        lines.append("")
        lines.append("Project ready" if self.ready else "Project blocked")
        return "\n".join(lines) + "\n"


def _executable_status(
    name: str,
    *,
    required: bool,
    purpose: str,
) -> DependencyStatus:
    resolved = shutil.which(name)
    available = resolved is not None
    if available:
        detail = f"{purpose}; {resolved}"
    elif required:
        detail = f"required for {purpose}"
    else:
        detail = f"not configured for {purpose}"
    return DependencyStatus(
        name=name,
        required=required,
        available=available,
        detail=detail,
    )


def dependency_requirements(config: ProjectConfig) -> dict[str, bool]:
    has_pdf_source = config.first_source("pdf") is not None
    formats = set(config.publish.formats)
    return {
        "pdftoppm": has_pdf_source,
        "tesseract": (
            has_pdf_source
            and config.import_settings.ocr_engine == "tesseract"
        ),
        "pandoc": bool(formats.intersection({"docx", "epub"})),
    }


def inspect_dependencies(config: ProjectConfig) -> DoctorReport:
    requirements = dependency_requirements(config)
    dependencies = (
        DependencyStatus(
            name="python",
            required=True,
            available=sys.version_info >= (3, 11),
            detail=(
                f"{sys.version_info.major}.{sys.version_info.minor}."
                f"{sys.version_info.micro}; requires 3.11 or later"
            ),
        ),
        _executable_status(
            "pdftoppm",
            required=requirements["pdftoppm"],
            purpose="PDF page rendering",
        ),
        _executable_status(
            "tesseract",
            required=requirements["tesseract"],
            purpose="configured OCR",
        ),
        _executable_status(
            "pandoc",
            required=requirements["pandoc"],
            purpose="configured DOCX or EPUB publishing",
        ),
    )
    return DoctorReport(dependencies=dependencies)


def doctor_project(root: Path | None = None) -> DoctorReport:
    root = root or Path.cwd()
    return inspect_dependencies(load_project_config(root))
