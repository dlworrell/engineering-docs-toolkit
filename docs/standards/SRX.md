# SRX

## Purpose

SRX (Segmentation Rules eXchange) is an XML-based standard for exchanging language-specific text segmentation rules between localization tools.

For EDT, SRX defines how localizable text may be split into linguistic segments before entering XLIFF or translation-memory workflows. EDOM remains authoritative for document semantics and structure.

## Adoption Decision

EDT classifies SRX as **Adopt** for segmentation-rule interchange and **Bridge** for localization-tool compatibility.

## Architectural Boundary

```text
EDOM defines semantic document units.
SRX defines linguistic segmentation rules.
XLIFF carries active localization content.
TMX stores reusable translated segments.
```

Pages and visual line breaks must never define linguistic segmentation. They are source provenance, not semantic boundaries.

## Core Concepts

An SRX profile should define:

- Language-rule groups.
- Language-map patterns.
- Break rules.
- Non-break rules.
- Rule ordering.
- Cascade behavior.
- Regular-expression assumptions.

Break and non-break rules are evaluated according to the selected profile and implementation policy. EDT must preserve the exact rule order because changing it can change segmentation results.

## Where EDT Uses SRX

- Reproducible sentence segmentation.
- XLIFF export preparation.
- TMX import and export reconciliation.
- Localization regression testing.
- Toolchain migration.
- Segmentation provenance.

## Where EDT Does Not Use SRX

SRX does not define:

- EDOM node boundaries.
- Translation-unit identity.
- Translation state.
- Inline-code semantics.
- Terminology.
- Publication layout.
- Source-page structure.

A sentence boundary produced by SRX is not automatically a paragraph, list item, heading, or other EDOM node.

## Import Strategy

An SRX importer should preserve:

- Declared version.
- Rule-group names.
- Language-map patterns.
- Rule order.
- Break and non-break expressions.
- Cascade setting.
- Source file and digest.
- Tool and profile provenance.

Unknown extensions should be retained when possible and reported when they may affect compatibility.

## Export Strategy

An SRX exporter should:

1. Select a declared SRX profile.
2. Emit stable rule-group names.
3. Preserve deterministic rule order.
4. Declare cascade behavior.
5. Validate the generated XML.
6. Test representative language fixtures.
7. Preserve the file, profile, and test results as build artifacts.

## Validation

EDT validation may include:

- XML or schema errors.
- Missing language maps.
- Duplicate rule groups.
- Invalid regular expressions.
- Conflicting break and non-break rules.
- Unreachable rules.
- Unsupported cascade behavior.
- Segmentation output that differs from approved fixtures.
- XLIFF or TMX profiles that reference a different SRX revision.

Schema validity alone does not prove that two tools will segment text identically. EDT profiles should include expected segmentation fixtures for representative abbreviations, punctuation, numbers, markup boundaries, and language-specific cases.

## Provenance

Every segmentation run should record:

- SRX file and digest.
- Profile version.
- Segmentation engine and version.
- Input language.
- Input text revision.
- Generated segment boundaries.
- Warnings and overrides.

## Design Rule

```text
Segment linguistically with SRX.
Structure semantically with EDOM.
Preserve both decisions and their provenance.
```
