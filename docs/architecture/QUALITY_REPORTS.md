# Quality Reports Architecture

Quality reports summarize EDT validation and reference graph results into publication-readiness metrics.

They do not replace detailed validation reports. Instead, they provide a concise assessment of document health for maintainers, CI systems, and downstream publication workflows.

## Purpose

Technical document builds need both detailed diagnostics and high-level readiness signals.

Validation reports answer: what is wrong?

Quality reports answer: is this document ready to publish?

## Inputs

Quality reports consume existing EDT artifacts:

- Validation reports
- Reference graph data
- Structural findings
- Semantic findings
- Reference findings
- Accessibility findings where available

Quality reporting should not rediscover document structure or re-run semantic inference.

## Metrics

Initial EDT quality reports include:

- Structural score
- Semantic score
- Reference score
- Overall score
- Error count
- Warning count
- Broken reference count
- Orphaned reference count
- Publication-ready flag

Future versions may add accessibility score, provenance coverage, profile conformance, glossary coverage, translation readiness, and standards compliance metrics.

## Publication Readiness

Publication readiness is a policy decision derived from quality metrics.

For EDT 1.0, publication readiness is based on validation errors, broken references, and the overall quality score.

Document profiles may eventually define stricter or domain-specific readiness policies.

## Output Formats

Quality reports should be generated in both machine-readable and human-readable forms:

```text
reports/quality.json
reports/quality.md
```

The JSON report supports automation and dashboards. The Markdown report supports review by authors, editors, and maintainers.

## CI Integration

Quality reports are intended to support continuous integration. A CI workflow may choose to fail a build when publication readiness is false, when score thresholds are missed, or when new findings exceed a configured baseline.

## Relationship to Validation

Validation produces findings. Quality reporting interprets those findings.

This separation keeps validation deterministic and diagnostic while allowing quality policies to evolve independently.

## Relationship to the Reference Graph

The Reference Graph provides graph-level health metrics such as broken references and orphaned objects. Quality reports summarize those metrics alongside validation findings.

## Long-Term Direction

Quality reporting will become the primary document-health dashboard for EDT projects. Future reports may include trend analysis, regression comparison, standards conformance, accessibility readiness, and release gating for production technical publications.
