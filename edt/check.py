from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .accessibility import check_html_accessibility


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def _check_report_file(path: Path, label: str) -> list[str]:
    if not path.exists():
        return [f"missing {label}: {path}"]
    if _load_json(path) is None:
        return [f"invalid {label}: {path}"]
    return []


def _check_document_reports(root: Path, manifest: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    reports = manifest.get("document_reports")
    if not isinstance(reports, dict):
        return ["canonical EDOM build is missing document report metadata"]

    validation = reports.get("validation")
    reference_graph = reports.get("reference_graph")
    quality = reports.get("quality")
    if not isinstance(validation, dict):
        issues.append("canonical EDOM build is missing validation report")
        validation = {}
    if not isinstance(reference_graph, dict):
        issues.append("canonical EDOM build is missing reference graph report")
        reference_graph = {}
    if not isinstance(quality, dict):
        issues.append("canonical EDOM build is missing quality report")
        quality = {}

    for label, report in (
        ("validation report", validation),
        ("reference graph report", reference_graph),
        ("quality report", quality),
    ):
        report_path = report.get("json")
        if isinstance(report_path, str):
            issues.extend(_check_report_file(root / report_path, label))
        else:
            issues.append(f"canonical EDOM build is missing {label} path")

    validation_errors = int(validation.get("errors", 0))
    if validation_errors:
        issues.append(f"validation errors: {validation_errors}")

    broken_references = int(reference_graph.get("broken", 0))
    if broken_references:
        issues.append(f"broken references: {broken_references}")

    if quality.get("publication_ready") is False:
        issues.append("document is not publication ready")

    return issues


def check_project(root: Path) -> list[str]:
    issues: list[str] = []
    output = root / "output"
    for html in output.glob("*.html") if output.exists() else []:
        issues.extend(check_html_accessibility(html))

    manifest_path = output / "build-manifest.json"
    manifest = _load_json(manifest_path)
    if manifest is None:
        return issues

    if manifest.get("source_mode") == "canonical-edom":
        canonical_path = manifest.get("canonical_edom")
        if isinstance(canonical_path, str):
            if not (root / canonical_path).exists():
                issues.append(f"missing canonical EDOM: {canonical_path}")
        else:
            issues.append("canonical EDOM build is missing canonical path")
        issues.extend(_check_document_reports(root, manifest))

    return issues
