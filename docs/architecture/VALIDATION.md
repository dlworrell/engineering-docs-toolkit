# Validation Architecture

Validation is one of EDT's core semantic services. It operates on the Engineering Document Object Model (EDOM), not on source files or rendered output.

## Objectives

Validation verifies that a document is structurally sound, semantically consistent, internally coherent, accessible, and ready for publication.

Its purpose is to evaluate document meaning and integrity rather than visual formatting.

## Validation Pipeline

```text
EDOM
  -> Structural validation
  -> Semantic validation
  -> Reference validation
  -> Accessibility validation
  -> Quality metrics
  -> Validation report
```

## Validation Categories

- Structural integrity
- Semantic consistency
- Cross-reference integrity
- Numbering consistency
- Caption and ownership checks
- Accessibility requirements
- Profile-specific rules

## Findings

Each finding records a rule identifier, severity, category, message, affected node, and provenance where available. Reports should be deterministic and reproducible.

## Rule Philosophy

The EDT core defines platform-wide rules. Document profiles extend the rule set without modifying the validation engine.

## Relationship to EDOM

Validation consumes EDOM as the canonical semantic model. It does not infer semantics from layout or rendering.

## Relationship to Quality Reports

Validation findings are one input to quality reports. Quality reports summarize publication readiness rather than replacing detailed validation output.

## Long-Term Direction

Future releases may add profile-aware validation, standards compliance modules, richer diagnostics, and automated remediation suggestions while preserving deterministic validation behavior.