from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .hash_cache import hash_file
from .pdf_import import import_pdf


@dataclass
class ProjectImportConfig:
    manifest: Path
    source_pdf: Path
    output_dir: Path
    report_dir: Path


@dataclass
class ProjectImportResult:
    config: ProjectImportConfig
    source_exists: bool
    fingerprint: str
    report_path: Path


def _read_manifest_value(manifest: Path, key: str) -> str | None:
    if not manifest.exists():
        return None
    prefix = f"{key}:"
    for raw_line in manifest.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith(prefix):
            return line[len(prefix) :].strip().strip('"').strip("'")
    return None


def load_project_import_config(root: Path, manifest: Path | None = None) -> ProjectImportConfig:
    manifest_path = manifest or root / "edt" / "project.yml"
    if not manifest_path.is_absolute():
        manifest_path = root / manifest_path

    source_value = _read_manifest_value(manifest_path, "primary_pdf") or "source/original/herkules-manual.pdf"
    edom_value = _read_manifest_value(manifest_path, "edom") or "output/import/edom"
    reports_value = _read_manifest_value(manifest_path, "reports") or "reports/import"

    return ProjectImportConfig(
        manifest=manifest_path,
        source_pdf=root / source_value,
        output_dir=root / edom_value,
        report_dir=root / reports_value,
    )


def write_source_provenance(root: Path, source_pdf: Path, fingerprint: str) -> None:
    source_dir = source_pdf.parent
    source_dir.mkdir(parents=True, exist_ok=True)
    checksum_path = source_dir / "SHA256SUMS"
    provenance_path = source_dir / "provenance.md"

    checksum_path.write_text(f"{fingerprint}  {source_pdf.name}\n", encoding="utf-8")
    provenance_path.write_text(
        "# Source Provenance\n\n"
        f"Canonical source: `{source_pdf.relative_to(root)}`\n\n"
        f"SHA-256: `{fingerprint}`\n\n"
        "This file records the canonical source artifact used by the EDT import pipeline.\n",
        encoding="utf-8",
    )


def import_project(root: Path | None = None, manifest: Path | None = None) -> ProjectImportResult:
    root = root or Path.cwd()
    config = load_project_import_config(root, manifest)
    config.report_dir.mkdir(parents=True, exist_ok=True)
    config.output_dir.mkdir(parents=True, exist_ok=True)

    source_exists = config.source_pdf.exists()
    fingerprint = hash_file(config.source_pdf) if source_exists else "missing"

    write_source_provenance(root, config.source_pdf, fingerprint)

    if source_exists:
        import_pdf(config.source_pdf, config.output_dir)

    report = {
        "manifest": str(config.manifest.relative_to(root)),
        "source_pdf": str(config.source_pdf.relative_to(root)),
        "source_exists": source_exists,
        "sha256": fingerprint,
        "edom_output": str(config.output_dir.relative_to(root)),
        "status": "imported" if source_exists else "waiting_for_source_pdf",
    }
    report_path = config.report_dir / "import-report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    return ProjectImportResult(
        config=config,
        source_exists=source_exists,
        fingerprint=fingerprint,
        report_path=report_path,
    )
