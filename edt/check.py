from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .accessibility import check_html_accessibility
from .hash_cache import hash_file

OUTPUT_ARTIFACTS = {
    "md": "output/book.md",
    "html": "output/book.html",
    "docx": "output/book.docx",
    "epub": "output/book.epub",
}


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def _as_int(value: Any) -> int:
    if type(value) is int:
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return 0
    return 0


def _load_report_file(
    path: Path,
    label: str,
    display_path: str | None = None,
) -> tuple[dict[str, Any] | None, list[str]]:
    report_path = display_path or str(path)
    if not path.exists():
        return None, [f"missing {label}: {report_path}"]
    payload = _load_json(path)
    if payload is None:
        return None, [f"invalid {label}: {report_path}"]
    return payload, []


def _summary_payload(
    payload: dict[str, Any],
    label: str,
) -> tuple[dict[str, Any], list[str]]:
    summary = payload.get("summary")
    if not isinstance(summary, dict):
        return {}, [f"{label} is missing summary"]
    return summary, []


def _check_requested_outputs(root: Path, manifest: dict[str, Any]) -> list[str]:
    outputs = manifest.get("outputs", [])
    if not isinstance(outputs, list):
        return ["build manifest has invalid outputs list"]

    issues: list[str] = []
    for output in outputs:
        if not isinstance(output, str):
            issues.append("build manifest contains invalid output name")
            continue
        artifact = OUTPUT_ARTIFACTS.get(output)
        if artifact is None:
            issues.append(f"unknown requested output: {output}")
            continue
        if not (root / artifact).exists():
            issues.append(f"missing requested output: {artifact}")
    return issues


def _check_fingerprint(
    root: Path,
    manifest: dict[str, Any],
    source_path: str,
    source_label: str,
) -> list[str]:
    fingerprint = manifest.get("fingerprint")
    if not isinstance(fingerprint, str) or not fingerprint:
        return ["build manifest is missing source fingerprint"]

    path = root / source_path
    if not path.exists():
        return [f"missing {source_label}: {source_path}"]

    current_fingerprint = hash_file(path)
    if current_fingerprint != fingerprint:
        return [f"stale build manifest: {source_label} changed since build"]
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

    loaded_reports: dict[str, dict[str, Any] | None] = {
        "validation report": None,
        "reference graph report": None,
        "quality report": None,
    }
    for label, report in (
        ("validation report", validation),
        ("reference graph report", reference_graph),
        ("quality report", quality),
    ):
        report_path = report.get("json")
        if isinstance(report_path, str):
            payload, report_issues = _load_report_file(
                root / report_path,
                label,
                display_path=report_path,
            )
            issues.extend(report_issues)
            loaded_reports[label] = payload
        else:
            issues.append(f"canonical EDOM build is missing {label} path")

    validation_payload = loaded_reports["validation report"]
    if validation_payload is not None:
        validation_summary, summary_issues = _summary_payload(
            validation_payload,
            "validation report",
        )
        issues.extend(summary_issues)
        validation_errors = _as_int(validation_summary.get("errors", 0))
        if validation_errors:
            issues.append(f"validation errors: {validation_errors}")

    reference_payload = loaded_reports["reference graph report"]
    if reference_payload is not None:
        reference_summary, summary_issues = _summary_payload(
            reference_payload,
            "reference graph report",
        )
        issues.extend(summary_issues)
        broken_references = _as_int(reference_summary.get("broken", 0))
        if broken_references:
            issues.append(f"broken references: {broken_references}")

    quality_payload = loaded_reports["quality report"]
    if quality_payload is not None:
        publication_ready = quality_payload.get("publication_ready")
        if publication_ready is False:
            issues.append("document is not publication ready")
        elif publication_ready is not True:
            issues.append("quality report is missing publication readiness")

    if manifest.get("validation_passed") is False:
        fail_on = manifest.get("validation_fail_on", "configured threshold")
        issues.append(f"canonical EDOM validation failed at severity {fail_on}")

    return issues


def check_project(root: Path) -> list[str]:
    issues: list[str] = []
    output = root / "output"
    if not output.exists():
        return ["missing output directory: output"]

    for html in output.glob("*.html"):
        issues.extend(check_html_accessibility(html))

    manifest_path = output / "build-manifest.json"
    manifest = _load_json(manifest_path)
    if manifest is None:
        if manifest_path.exists():
            issues.append("invalid build manifest: output/build-manifest.json")
        else:
            issues.append("missing build manifest: output/build-manifest.json")
        return issues

    issues.extend(_check_requested_outputs(root, manifest))

    if manifest.get("source_mode") == "canonical-edom":
        canonical_path = manifest.get("canonical_edom")
        if isinstance(canonical_path, str):
            if (root / canonical_path).exists():
                issues.extend(
                    _check_fingerprint(
                        root,
                        manifest,
                        canonical_path,
                        "canonical EDOM",
                    )
                )
            else:
                issues.append(f"missing canonical EDOM: {canonical_path}")
        else:
            issues.append("canonical EDOM build is missing canonical path")
        issues.extend(_check_document_reports(root, manifest))

    return issues
