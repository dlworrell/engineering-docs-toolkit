# OpenDocument Format

## Purpose

The OpenDocument Format (ODF) is an open, XML-based format for text documents, spreadsheets, presentations, drawings, charts, formulas, and related office content.

For EDT, ODF is an office-document interchange boundary. EDT imports ODF into EDOM for semantic processing and may publish ODF when an editable, standards-based office deliverable is required.

## Current Standard

The current OASIS Standard is **OpenDocument Version 1.4**, approved in October 2025.

ODF 1.4 has four parts:

- Introduction.
- Packages.
- OpenDocument schema.
- OpenFormula.

ODF also exists in the ISO/IEC 26300 family. OASIS and ISO publication cycles do not necessarily align, so an EDT profile must identify the exact OASIS version or ISO/IEC part and edition it targets.

## Adoption Decision

EDT classifies ODF as **Adopt** for open office-document interchange and **Bridge** for desktop office suites, archives, and institutional workflows.

## Architectural Boundary

```text
EDOM owns canonical semantic structure, identity, and provenance.
ODF carries an editable office-document representation.
Profiles define reversible mappings and application compatibility.
```

ODF paragraphs, spans, sections, styles, pages, and drawing objects are source-format structures and must not automatically become equivalent EDOM semantic nodes.

## Package Model

ODF documents are commonly ZIP packages containing:

- `content.xml`.
- `styles.xml`.
- `meta.xml`.
- `settings.xml`.
- `META-INF/manifest.xml`.
- Images, media, scripts, thumbnails, signatures, and embedded objects.

ODF also supports flat XML representations for some document families.

## Document Families

| Family | Common extensions | EDT use |
| --- | --- | --- |
| Text | `.odt`, `.ott` | Editable text documents and templates |
| Spreadsheet | `.ods`, `.ots` | Tabular models and calculations |
| Presentation | `.odp`, `.otp` | Slide presentations and templates |
| Drawing | `.odg`, `.otg` | Drawings and page-based graphics |
| Formula | `.odf` | Mathematical formula documents |
| Master document | `.odm` | Collections of linked text documents |

## Mapping to EDOM

Representative mappings include:

| ODF construct | EDOM interpretation |
| --- | --- |
| Paragraph | Candidate block refined by style and context |
| Heading | Heading candidate with level evidence |
| Span | Inline text or formatting fragment |
| List | Semantic list candidate |
| Bookmark | Stable anchor candidate |
| Hyperlink | Reference-graph edge |
| Note | Footnote or endnote object |
| Table | Table object requiring structural validation |
| Frame | Container for image, text box, or object |
| Change tracking | Proposed or recorded editorial change |
| Field | Generated or computed content instruction |

Style names provide evidence, not semantic truth by themselves.

## Spreadsheets and OpenFormula

EDT should preserve formulas, cached values, value types, number formats, dates, merged cells, hidden content, named expressions, and external references separately.

Cached values may be stale. A profile should declare whether EDT recalculates formulas, trusts stored values, or reports them as unverified.

## Styles and Layout

ODF separates named styles, automatic styles, default styles, page layouts, master pages, and presentation styles.

EDT should preserve style identifiers, inheritance, list behavior, direct formatting, page layouts, headers, footers, columns, frames, and positioning as typed evidence.

Pages remain provenance and layout. They do not define EDOM semantic hierarchy.

## Metadata

EDT should preserve and reconcile title, description, creators, language, timestamps, keywords, rights, identifiers, generator information, and RDF metadata where present.

Conflicting metadata sources must be reported rather than silently merged.

## Change Tracking and Comments

Profiles should declare whether EDT preserves, accepts, rejects, or imports tracked changes as proposed revisions. Comments should remain editorial annotations.

Every review decision must be recorded as provenance.

## Security

ODF packages may contain encryption, digital signatures, scripts, macros, event listeners, linked resources, and embedded objects.

EDT must not execute active content during import. Profiles should define preservation, removal, trust, encryption, and signature policies explicitly.

## Import Strategy

An ODF importer should:

1. Preserve the original package and digest.
2. Detect the document family and declared version.
3. Validate package structure, manifest entries, media types, and XML.
4. Parse content, styles, metadata, settings, formulas, and relationships.
5. Preserve extensions, assets, comments, changes, signatures, and active-content findings.
6. Map source structures into EDOM using a declared profile.
7. Record parser versions, warnings, confidence, and transformation decisions.

## Export Strategy

An ODF publisher should:

1. Select a declared ODF version, family, and compatibility profile.
2. Map validated EDOM structures to ODF XML.
3. Generate stable identifiers, references, styles, and metadata.
4. Package assets and manifest entries correctly.
5. Apply formula, review, signature, encryption, script, and extension policies.
6. Validate package and schema conformance.
7. Round-trip representative files in target applications.
8. Preserve the generated package and validation evidence.

## Validation

EDT validation may include:

- Invalid ZIP package structure.
- Missing or incorrect manifest entries.
- Media-type mismatches.
- Missing or inconsistent version declarations.
- XML or schema errors.
- Broken links or bookmarks.
- Missing styles, list definitions, or master pages.
- Formula and cached-value inconsistencies.
- Missing embedded resources.
- Unsupported extensions.
- Active-content policy violations.
- Metadata conflicts.
- Signature or encryption errors.
- Round-trip loss in target applications.

Schema validity alone does not prove semantic fidelity, accessibility, or application interoperability.

## Relationship to OOXML

ODF and OOXML are separate standards with different vocabularies, package models, formula languages, and extension mechanisms.

Conversion between them is a transformation. EDT should normalize into EDOM before cross-format publication and report losses involving formulas, styles, revisions, charts, fields, macros, layout, or embedded objects.

## Profiles

An EDT ODF profile may specify:

- OASIS version or ISO/IEC part and edition.
- Document family.
- Target applications and versions.
- Flat XML or package representation.
- Allowed extensions.
- Style-to-EDOM mappings.
- OpenFormula support.
- Change-tracking policy.
- Active-content policy.
- Encryption and signature policy.
- Accessibility requirements.
- Validation and round-trip test matrix.

## Design Rule

```text
Use ODF as an open office-document interchange format.
Normalize semantics into EDOM before transformation.
Generate ODF from validated semantics, not formatting guesses.
Test target applications before claiming compatibility.
```

## References

- OASIS, *Open Document Format for Office Applications (OpenDocument) Version 1.4*: https://docs.oasis-open.org/office/OpenDocument/v1.4/
- ISO, *ISO/IEC 26300-1:2015 — OpenDocument v1.2 — Part 1*: https://www.iso.org/standard/66363.html
