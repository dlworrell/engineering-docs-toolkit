# Profile Architecture

Profiles define document-family-specific semantics without changing EDT's core platform.

EDOM provides the common semantic foundation. Profiles extend that foundation for specialized document families such as service manuals, mathematics texts, engineering standards, scholarly papers, legal documents, and project-specific books.

## Purpose

Different technical documents use different semantic conventions.

A mathematics text may require theorem numbering, proof validation, definitions, lemmas, corollaries, examples, and exercises.

A service manual may require warnings, cautions, procedures, tools, parts, torque specifications, exploded diagrams, and inspection steps.

Profiles allow EDT to support these domains without hard-coding every document family into the core engine.

## Responsibilities

A profile may define:

- Additional semantic kinds
- Numbering rules
- Validation rules
- Publisher labels and rendering conventions
- Reference patterns
- Glossary behavior
- Indexing behavior
- Quality thresholds
- Metadata expectations

## Core Principle

Profiles extend EDT. They do not fork EDT.

The platform remains stable while profiles describe domain-specific semantics and policies.

## Relationship to EDOM

EDOM defines the common object model. Profiles define how a particular document family uses and extends that model.

For example:

```text
EDOM kind: figure
Profile convention: exploded-view diagram

EDOM kind: table
Profile convention: torque specification table

EDOM kind: warning
Profile convention: safety warning, caution, or note
```

## Validation Integration

Profiles may add validation rules such as:

- Every theorem must have a proof.
- Every procedure must have ordered steps.
- Every torque specification must include units.
- Every warning must have a severity.
- Every part number must match a profile-defined pattern.

Core validation remains generic. Profile validation adds domain-specific policy.

## Publisher Integration

Profiles may influence rendering without requiring publisher rewrites.

Examples include:

- Labeling figures as diagrams, plates, or illustrations.
- Rendering warnings with service-manual styling.
- Formatting theorem environments.
- Generating specialized indexes.
- Emitting standards-specific metadata.

## Candidate Profiles

Planned or likely profile families include:

- Generic technical document
- Mathematics text
- Service manual
- Bentley-style workshop manual
- Engineering standard
- IEEE-style paper
- Legal document
- HERKULES project profile

## Long-Term Direction

Profiles are the primary mechanism by which EDT becomes broadly useful without becoming a collection of special cases.

Future work should make profiles declarative where possible, testable, versioned, and suitable for reuse across projects.