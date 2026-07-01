# Engineering Document Object Model (EDOM)

The Engineering Document Object Model (EDOM) is EDT's canonical semantic representation for technical documents.

EDOM exists so that EDT can reason about document meaning independently of source format, page layout, or publication target.

## Purpose

Source documents arrive in many forms: PDFs, scanned pages, Markdown, HTML, EPUB, office documents, and future web snapshots. Each format represents structure differently, and many formats mix semantic meaning with presentation.

EDOM provides one normalized model for downstream processing.

Once a document is represented as EDOM, validators, reference graph builders, quality reporters, translators, and publishers can operate on the same semantic structure.

## Design Goals

EDOM is designed to be:

- Semantic rather than presentational.
- Deterministic and reproducible.
- Serializable for storage and interchange.
- Extensible through document profiles.
- Suitable for validation, publishing, translation, accessibility, and archival workflows.
- Capable of preserving provenance back to source material.

## Core Principle

Pages are provenance, not structure.

A theorem may span two pages. A table may continue across a page break. A figure may be assembled from multiple source regions. In EDOM these are still single semantic objects. Their page locations are recorded as provenance, not as the primary document hierarchy.

## Conceptual Hierarchy

```text
Document
    Metadata
    Front Matter
    Sections
        Blocks
            Paragraphs
            Figures
            Tables
            Equations
            Definitions
            Theorems
            Proofs
            Examples
            Exercises
    Back Matter
    Assets
    References
    Provenance
```

The tree expresses containment and reading order. Additional relationships are represented through metadata and reference graphs.

## Core Object Shape

Every addressable EDOM object should have:

- A stable identifier.
- A kind.
- Optional text.
- Optional metadata.
- Optional children.
- Optional references.
- Optional provenance.

Conceptually:

```json
{
  "id": "figure-3.2",
  "kind": "figure",
  "text": "",
  "metadata": {
    "number": "3.2",
    "references": []
  },
  "children": [
    {
      "id": "caption-3.2",
      "kind": "caption",
      "text": "Pump assembly overview."
    }
  ]
}
```

## Common Semantic Kinds

EDOM supports general document objects such as:

- document
- page
- section
- paragraph
- title
- subtitle
- caption
- figure
- table
- equation
- definition
- theorem
- lemma
- corollary
- proposition
- proof
- example
- exercise
- algorithm
- quotation
- citation
- bibliography
- index
- glossary

This list is not intended to be the final vocabulary for every document family. Future document profiles will define domain-specific semantics such as technical warnings, torque specifications, service procedures, parts lists, legal clauses, or scholarly apparatus.

## Identity

Identifiers are the foundation for cross references, validation, publishing anchors, provenance lookups, and regression comparison.

An EDOM identifier should be stable across rebuilds whenever the underlying semantic object has not changed.

Stable identifiers make it possible to:

- Resolve internal references.
- Generate reproducible HTML anchors.
- Track semantic changes over time.
- Maintain translation memory alignment.
- Build reference graphs.
- Compare document revisions.

## Relationships

EDOM is a tree augmented by graphs.

The primary EDOM tree records containment and reading order. Additional relationships include:

- Cross references.
- Caption ownership.
- Theorem/proof relationships.
- Equation references.
- Citation references.
- Accessibility relationships.
- Provenance links to source regions.

The reference graph subsystem materializes many of these relationships for validation, reporting, publishing, and future knowledge-graph workflows.

## Provenance

EDOM nodes should retain enough provenance to identify where they came from in the source material.

A node may originate from one or more source regions:

```json
{
  "source": {
    "document": "manual.pdf",
    "regions": [
      {"page": 42, "bbox": [72, 120, 468, 310]},
      {"page": 43, "bbox": [72, 60, 468, 255]}
    ]
  }
}
```

This allows EDT to support review, audit, side-by-side comparison, OCR correction, and evidence-preserving workflows.

## Serialization

EDOM is currently serialized as JSON-compatible data.

JSON is the canonical interchange representation for EDT 1.0 because it is deterministic, testable, easy to inspect, and straightforward for downstream tools to consume.

Future releases may add additional serializations, schemas, or standards bridges without replacing the core semantic model.

## Profiles

EDOM defines the platform's common semantic foundation.

Document-family-specific semantics belong in profiles. A mathematics profile may define theorem numbering and proof requirements. A service-manual profile may define warnings, cautions, procedures, tools, parts, and torque specifications.

Profiles should extend EDOM without requiring changes to the core model.

## Downstream Use

EDOM is consumed by:

- Validators.
- Reference graph builders.
- Quality report generators.
- Translation memory tools.
- Accessibility processors.
- HTML, Markdown, EPUB, and future publishers.
- Regression and semantic-diff tooling.

EDOM is the semantic center of EDT.