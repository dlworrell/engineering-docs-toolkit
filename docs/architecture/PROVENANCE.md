# Provenance Architecture

Provenance is the chain of evidence that connects every semantic object in EDOM back to its originating source material.

In EDT, provenance is a first-class architectural concern rather than optional metadata.

## Purpose

Provenance enables engineers, editors, reviewers, and automated tooling to determine where information originated, how it was transformed, and whether published output can be reproduced from its sources.

## Design Principles

- Preserve source evidence.
- Record transformations.
- Support deterministic rebuilds.
- Enable audit and review.
- Never discard recoverable source context without explicit policy.

## Provenance Model

Each EDOM object may retain provenance describing:

- Source document
- Source page(s)
- Source region(s)
- Import method
- OCR participation
- Transformation history
- Processing timestamps where appropriate

Page boundaries are provenance, not semantic structure.

## Pipeline Integration

```text
Source
  -> Import
  -> OCR
  -> Layout
  -> Semantic recognition
  -> EDOM
  -> Validation
  -> Publishing
```

Each stage should preserve or extend provenance rather than replace it.

## Uses

Provenance supports:

- Validation diagnostics
- OCR review
- Editorial review
- Side-by-side comparison
- Semantic diffing
- Reproducible publishing
- Long-term archival
- Evidence-preserving workflows

## Relationship to Publishers

Publishers generally consume provenance indirectly, but may emit traceability information, anchors, review artifacts, or audit reports when requested.

## Long-Term Direction

Future versions of EDT may support richer provenance graphs, transformation histories, cryptographic verification, web snapshot capture, and standards-based provenance interchange. Regardless of implementation details, preserving the chain of evidence remains a core architectural principle.