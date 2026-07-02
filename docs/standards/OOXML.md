# Office Open XML

## Purpose

Office Open XML (OOXML) is the ISO/IEC and Ecma standardized family of XML-based formats used for word-processing documents, spreadsheets, presentations, drawings, charts, equations, and related package content.

For EDT, OOXML is an office-document interchange boundary. EDT imports OOXML into EDOM for semantic processing and may publish OOXML when an editable Microsoft Office-compatible deliverable is required.

## Governing Standards

OOXML is standardized as the **ISO/IEC 29500** family and as **ECMA-376**.

The standards are divided into multiple parts, including:

- Fundamentals and markup-language reference.
- Open Packaging Conventions.
- Markup Compatibility and Extensibility.
- Transitional migration features.

The editions of individual ISO/IEC 29500 parts do not always advance together. An EDT profile must therefore identify the exact part editions, conformance class, and application compatibility target rather than referring only to “OOXML.”

## Adoption Decision

EDT classifies OOXML as **Bridge** for import and export, with selective **Adopt** status for controlled office-delivery profiles.

Rationale:

- OOXML is widely used for editable business, engineering, academic, and government documents.
- Its package structure preserves rich document features and embedded resources.
- Real-world files often contain application-specific extensions and Transitional markup.
- OOXML structure reflects office-application behavior and is not a suitable canonical semantic model for EDT.
- Reliable interchange requires explicit compatibility testing with target applications.

## Architectural Boundary

```text
EDOM owns canonical semantic structure, identity, and provenance.
OOXML carries an editable office-document representation.
Profiles define reversible mappings and application compatibility.
```

EDT must not treat WordprocessingML paragraphs, runs, sections, or page layout as automatically equivalent to EDOM semantic nodes.

## Package Model

Most OOXML documents are ZIP-based packages governed by Open Packaging Conventions.

A package contains:

- Parts.
- Relationships.
- Content-type declarations.
- Core and extended properties.
- Main document, workbook, or presentation parts.
- Styles, numbering, themes, fonts, media, charts, and diagrams.
- Comments, notes, custom XML, and application-specific extension parts.

An EDT importer should validate both the package structure and the markup inside each part.

## Primary Document Families

| OOXML family | Common extension | EDT use |
| --- | --- | --- |
| WordprocessingML | `.docx`, `.docm`, `.dotx`, `.dotm` | Editable text documents and templates |
| SpreadsheetML | `.xlsx`, `.xlsm`, `.xltx`, `.xltm` | Tabular models, workbooks, and calculations |
| PresentationML | `.pptx`, `.pptm`, `.potx`, `.potm` | Slide presentations and templates |
| DrawingML | Embedded across formats | Shapes, images, charts, diagrams, and layout |
| Office Math Markup Language | Embedded in WordprocessingML | Office-native mathematical expressions |

Macro-enabled files require separate security and profile treatment.

## Strict and Transitional Conformance

OOXML distinguishes **Strict** and **Transitional** conformance.

Strict is the cleaner standards-oriented target. Transitional includes legacy compatibility constructs intended to preserve behavior from earlier Microsoft Office formats and implementations.

EDT policy should be:

- Prefer Strict for newly generated controlled documents when the target toolchain supports it.
- Accept Transitional on import when required for real-world compatibility.
- Record the detected conformance class.
- Report Transitional-only constructs.
- Never claim Strict output unless the generated package validates as Strict.

Application defaults may still produce Transitional documents, so file extension alone does not identify conformance class.

## Markup Compatibility and Extensibility

OOXML supports extension markup and alternate content through Markup Compatibility and Extensibility mechanisms.

An importer must preserve:

- Ignorable namespaces.
- Alternate-content choices and fallbacks.
- Process-content declarations.
- Extension lists.
- Application-specific namespace content.

Unsupported extension content must not disappear silently. EDT should retain it as opaque extension data where possible and report any semantic or visual risk.

## WordprocessingML Mapping

Representative mappings include:

| WordprocessingML | EDOM interpretation |
| --- | --- |
| Paragraph | Candidate block, refined by style and context |
| Run | Text span or formatting fragment |
| Paragraph style | Semantic evidence, not semantic truth by itself |
| Numbering definition | List and outline evidence |
| Section properties | Page-layout and section-boundary evidence |
| Bookmark | Candidate stable anchor |
| Hyperlink | Reference-graph edge |
| Footnote or endnote | Note object and backlink relationship |
| Table | Table candidate requiring structural validation |
| Drawing or image | Figure, decoration, or embedded object |
| Structured document tag | Semantic or workflow annotation |
| Field code | Generated or dynamic content instruction |

A heading-looking paragraph is not automatically a heading. The importer should combine styles, outline levels, numbering, neighboring structure, bookmarks, and application metadata.

## SpreadsheetML Mapping

Representative mappings include:

| SpreadsheetML | EDOM interpretation |
| --- | --- |
| Workbook | Spreadsheet publication or source package |
| Worksheet | Named tabular region |
| Cell | Typed value, formula, or display value |
| Shared string | Text storage mechanism |
| Formula | Computation expression with cached result |
| Defined name | Stable semantic or computational reference |
| Table | Structured tabular object |
| Chart | Visualization linked to data ranges |
| Comment or note | Annotation |
| Style | Presentation and number-format evidence |

EDT should preserve formulas, cached values, number formats, dates, merged cells, hidden rows or columns, and defined names separately. Displayed text alone is insufficient to preserve spreadsheet semantics.

## PresentationML Mapping

Representative mappings include:

| PresentationML | EDOM interpretation |
| --- | --- |
| Presentation | Slide publication |
| Slide | Ordered presentation unit |
| Slide layout | Layout template |
| Slide master | Reusable theme and placement rules |
| Shape | Text, image, diagram, or decorative object |
| Notes slide | Presenter-note content |
| Transition or animation | Presentation behavior |
| Embedded media | Asset with playback semantics |

Reading order must not be inferred solely from object coordinates. EDT should inspect placeholder hierarchy, creation order, accessibility order where available, and semantic relationships.

## Styles and Themes

OOXML styles and themes carry strong authoring intent but do not guarantee semantic correctness.

EDT should preserve:

- Style identifiers and names.
- Based-on and inheritance relationships.
- Numbering and outline behavior.
- Theme colors and fonts.
- Direct formatting overrides.
- Locale and script-specific formatting.

Semantic profiles may map named styles to EDOM kinds, but such mappings must be explicit and versioned.

## Page Layout

OOXML supports margins, sections, headers, footers, columns, page breaks, paper sizes, and positioning.

EDT should preserve layout as source or publication provenance while keeping semantic structure independent from pagination.

Manual page breaks may be meaningful editorial evidence, but they must not split a semantic node automatically.

## Fields and Generated Content

WordprocessingML fields may represent page numbers, references, dates, document properties, tables of contents, equations, and other generated values.

An importer should preserve:

- Field instruction.
- Stored result.
- Lock and dirty state.
- Nested field structure.
- Relationship to EDOM references or generated content.

The stored result may be stale. EDT should not treat it as authoritative without evaluating the instruction under a declared policy.

## Revisions, Comments, and Collaboration

OOXML can contain tracked insertions, deletions, moves, comments, authorship, and revision identifiers.

EDT profiles should define whether to:

- Preserve all revisions.
- Accept revisions into a clean view.
- Reject revisions.
- Import revisions as proposed changes.
- Preserve comments as editorial annotations.

Review decisions must be recorded as provenance. Silent acceptance or rejection is not acceptable.

## Embedded and Linked Content

OOXML packages may contain or reference:

- Images.
- Audio and video.
- Charts and diagrams.
- Embedded spreadsheets or documents.
- OLE objects.
- External links.
- Custom XML.
- Fonts.

EDT should inventory these resources, validate relationships, preserve media types and hashes, and apply profile-specific security rules.

External links should not be resolved automatically in untrusted documents.

## Macros and Active Content

Macro-enabled formats may contain VBA projects and other active content.

EDT should treat active content as untrusted and should:

- Detect macro-enabled packages.
- Preserve macro binaries only when profile policy permits.
- Never execute macros during import.
- Report signatures and trust status.
- Isolate embedded executables or active objects.
- Strip active content only through an explicit, provenance-recorded transformation.

A macro-free extension does not prove that all external or active behaviors are absent.

## Import Strategy

An OOXML importer should:

1. Preserve the original package and digest.
2. Validate ZIP and Open Packaging Conventions structure.
3. Identify document family, conformance class, and application metadata.
4. Parse relationships and content types.
5. Preserve supported markup, extension content, assets, and metadata.
6. Map document structures into EDOM using a declared profile.
7. Preserve styles, numbering, fields, revisions, comments, and layout as typed evidence.
8. Detect macros, external links, embedded objects, and unsupported features.
9. Record parser versions, warnings, confidence, and transformation decisions.

## Export Strategy

An OOXML publisher should:

1. Select a document family, conformance class, and compatibility profile.
2. Map validated EDOM structures to OOXML parts.
3. Generate stable identifiers and relationships.
4. Generate styles, numbering, references, notes, and metadata.
5. Package assets and content types correctly.
6. Emit only allowed extensions and active features.
7. Validate package and markup conformance.
8. Open and round-trip representative files in target applications.
9. Preserve the generated package and validation evidence.

## Validation

EDT validation may include:

- Invalid ZIP package structure.
- Missing or conflicting content types.
- Broken internal relationships.
- Unsupported external relationships.
- Incorrect Strict or Transitional declarations.
- Schema or markup errors.
- Unknown extension content.
- Duplicate identifiers.
- Broken bookmarks, fields, hyperlinks, notes, or drawings.
- Missing style or numbering definitions.
- Formula and cached-value inconsistencies.
- Missing embedded resources.
- Macro or active-content policy violations.
- Metadata conflicts.
- Round-trip loss in target applications.

Schema validity alone does not prove semantic fidelity or application interoperability.

## Accessibility

OOXML can carry accessibility-relevant semantics, including headings, table structure, alternative text, language, reading order, titles, descriptions, and document properties.

EDT should preserve and validate these features, but office-application accessibility must be tested in the target application and exported formats.

An accessible DOCX does not automatically produce an accessible PDF or EPUB; each publication path requires its own validation.

## Profiles

An EDT OOXML profile may specify:

- WordprocessingML, SpreadsheetML, or PresentationML.
- ISO/IEC 29500 part editions.
- Strict or Transitional conformance.
- Target applications and versions.
- Allowed extensions.
- Style-to-EDOM mappings.
- Field evaluation policy.
- Revision and comment policy.
- Macro and embedded-object policy.
- External-link policy.
- Accessibility requirements.
- Validation and round-trip test matrix.

## Provenance

EDT should record:

- Original or generated package digest.
- OOXML family and conformance class.
- Standard-part editions.
- Application producer metadata.
- Importer or publisher version.
- Profile and mapping version.
- Extension and compatibility decisions.
- Active-content findings.
- Validation and round-trip results.

## Design Rule

```text
Use OOXML as an office-document interchange format.
Normalize semantics into EDOM before transformation.
Generate OOXML from validated semantics, not from presentation guesses.
Test the actual target applications before claiming compatibility.
```

## References

- Ecma International, *ECMA-376 Office Open XML File Formats*: https://ecma-international.org/publications-and-standards/standards/ecma-376/
- ISO, *ISO/IEC 29500 Office Open XML File Formats*: https://www.iso.org/standard/71691.html
- Microsoft, *Open XML SDK documentation*: https://learn.microsoft.com/office/open-xml/open-xml-sdk
