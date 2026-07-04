# P0 Remediation Status

Date: 2026-07-03

## Status

P0 remediation is functionally complete as of tests 608, 610, 611, and 612 passing.

The Engineering Docs Toolkit is no longer only a collection of isolated components. The current product path supports a user-visible workflow from project initialization through import, canonical EDOM generation, validation/report generation, and publication output.

The P0 goal was not to finish every long-term exporter or architecture cleanup item. The P0 goal was to make the core workflow truthful, reproducible, and failure-aware enough that real integration work can safely begin.

## P0 outcomes

### Integrated product path

The integrated product path is now covered at CLI/integration level:

```text
edt init
  -> edt import
  -> canonical EDOM
  -> validation / reference graph / quality reports
  -> edt build
  -> Markdown / HTML / Pandoc-backed outputs where available
  -> edt check
```

The initialized workflow now has regression coverage. Canonical EDOM drives the build path when present. HTML and Markdown are generated from canonical EDOM rather than stale source Markdown.

### Output truthfulness

The build path now rejects unsupported outputs instead of silently pretending they were produced.

Pandoc-backed outputs fail explicitly when the requested output cannot be generated. DOCX and EPUB are allowed only through the canonical Markdown path, so they no longer silently diverge from canonical EDOM while HTML is built from canonical content.

This preserves the core EDT rule:

```text
normalize once, publish many
```

### Validation and publication readiness

Canonical EDOM builds generate document reports:

- validation report
- reference graph report
- quality report

Validation thresholds are enforced during canonical builds. Empty canonical documents are no longer considered publication-ready.

`edt check` now inspects the generated report files themselves instead of trusting only manifest summaries. It reports validation errors, broken references, failed publication readiness, missing reports, invalid reports, missing requested outputs, and stale canonical EDOM fingerprints.

### Staleness detection

The build manifest fingerprint is checked against the current canonical EDOM. If canonical EDOM changes after build, `edt check` reports the build as stale.

This closes the most important P0 failure mode: a generated output set that appears valid but no longer corresponds to the current canonical source.

## Known architectural debt

The following items are intentionally not considered P0 blockers:

1. **Native importer consumption of `edt.toml`**

   Unified configuration is currently bridged through an import manifest adapter. This is acceptable for P0 because the user-facing workflow is working and legacy importer compatibility is preserved. Native consumption by `project_import.py` remains a cleanup item.

2. **Exporter architecture beyond the canonical Markdown bridge**

   Canonical EDOM to Markdown is now the safe bridge into Pandoc-backed formats. Native or richer exporters for PDF, ODT, LaTeX, TEI, JATS, DocBook, and profile-specific outputs remain future work.

3. **Full dependency graph semantics**

   P0 now checks the source fingerprint for canonical EDOM builds. More detailed dependency tracking across imported assets, OCR caches, report inputs, plugins, and project-specific resources belongs in later architecture work.

4. **HERKULES acceptance harness**

   HERKULES should become the serious regression corpus, but it belongs after the P0 product path is stable. That makes it early P1 work rather than a P0 blocker.

## P0 completion criteria

P0 can be treated as functionally complete because EDT now satisfies the following criteria:

- An initialized project can be imported and built through the CLI.
- The import path produces canonical EDOM.
- The build path uses canonical EDOM when available.
- Markdown and HTML outputs are generated from canonical EDOM.
- Pandoc-backed outputs fail explicitly when unavailable.
- Unsupported outputs are rejected.
- Canonical builds generate validation, reference, and quality reports.
- Validation thresholds are enforced.
- Publication readiness is represented in the quality report.
- `edt check` verifies requested outputs, canonical EDOM existence, report file validity, report contents, publication readiness, and canonical source freshness.

## Recommendation

Move to P1.

The next phase should use HERKULES as the acceptance and regression corpus. P1 should focus on real-source integration pressure rather than more synthetic P0 scaffolding.

Recommended first P1 steps:

1. Build a HERKULES acceptance harness.
2. Capture expected import, report, and publication artifacts.
3. Run the initialized project workflow against HERKULES material.
4. Promote failures into specific importer, EDOM, validation, or exporter issues.
5. Keep the adapter-based unified config bridge until native importer integration can be done safely.

## Decision

P0 remediation is closed subject to continued green CI on the recorded commits. New failures discovered by HERKULES should be handled as P1 integration findings unless they expose a regression in the P0 product path itself.
