# PDF

## Purpose

Portable Document Format (PDF) is a fixed-layout document format standardized by ISO 32000.

For EDT, PDF is a publication and preservation target, not the canonical semantic document model. EDT should generate PDF from validated EDOM while preserving structure, metadata, identifiers, provenance, accessibility semantics, and conformance evidence.

## Current Standard

The current PDF specification is **ISO 32000-2:2020**, the second edition of PDF 2.0.

EDT profiles should declare:

- PDF version.
- Conformance subset, such as PDF/A, PDF/UA, PDF/X, or PDF/E.
- Tagged-PDF policy.
- Font-embedding policy.
- Color-management policy.
- Encryption and signature policy.
- Metadata requirements.
- Validation tools and versions.

## Adoption Decision

EDT classifies PDF as **Adopt** for fixed-layout publication and **Bridge** for archival, accessibility, print, engineering, and regulatory ecosystems.

Rationale:

- PDF is the dominant fixed-layout interchange format.
- ISO 32000 provides an open standard for writers and readers.
- Specialized ISO subsets provide stronger requirements for archiving, accessibility, print production, and engineering workflows.
- PDF can preserve visual fidelity, but visual fidelity alone does not preserve document semantics.

## Architectural Boundary

```text
EDOM owns semantic document structure and provenance.
The PDF publisher renders a fixed-layout artifact.
Tagged PDF carries selected structural semantics.
PDF profiles define purpose-specific conformance.
```

Pages are native to PDF layout, but page boundaries must not become the semantic structure of EDOM.

## Where EDT Uses PDF

- Fixed-layout publication.
- Print-ready output.
- Archival deliverables.
- Accessible PDF output.
- Engineering and regulatory packages.
- Signed release artifacts.
- Page-level source comparison.
- Visual regression testing.
- Preservation of final rendered editions.

## Where EDT Does Not Use PDF

PDF does not replace:

- EDOM semantic hierarchy.
- Source-format provenance.
- Reusable structured authoring.
- Profile-independent metadata.
- Localization exchange.
- Terminology management.
- The reference graph.
- Build configuration and validation reports.

A PDF may be an input source, but EDT should recover semantics into EDOM rather than treating page objects as canonical structure.

## Core PDF Model

A PDF file may contain:

- Indirect objects and object streams.
- Page trees and page content streams.
- Fonts and character maps.
- Images and graphics.
- Annotations and links.
- Outlines and destinations.
- Embedded files.
- Metadata streams.
- Structure trees for tagged PDF.
- AcroForm fields.
- Digital signatures.
- Optional content groups.

EDT should expose only the features permitted by the selected publication profile.

## Tagged PDF

Tagged PDF represents logical structure independently from page painting operations.

An EDT publisher should derive the structure tree from validated EDOM semantics and preserve:

- Heading hierarchy.
- Paragraphs and lists.
- Tables and headers.
- Figures and captions.
- Notes and references.
- Reading order.
- Language metadata.
- Alternative text.
- Actual text where required.
- Associations between structure elements and page content.

A tagged file is not automatically accessible. The tags must be semantically correct and aligned with visible content.

## Reading Order

Reading order should come from EDOM, not from geometric sorting of page objects.

Validation should detect:

- Content absent from the structure tree.
- Decorative content included incorrectly.
- Reading order inconsistent with semantic order.
- Repeated headers or footers announced as body content.
- Notes, captions, or sidebars placed incorrectly.
- Multi-column content linearized incorrectly.

## Fonts and Text Extraction

EDT should embed fonts as required by profile and preserve reliable Unicode mapping.

Validation should detect:

- Missing required embedded fonts.
- Invalid or incomplete character maps.
- Text that renders correctly but extracts incorrectly.
- Substitution that changes metrics or meaning.
- Glyph-only equations or symbols without recoverable text semantics.

Text extraction should be tested separately from visual rendering.

## Metadata

PDF metadata may include the document information dictionary, XMP metadata, identifiers, conformance declarations, and profile-specific metadata.

EDT should generate metadata from authoritative EDOM and build data. Conflicting metadata representations must be detected and reported.

Relevant metadata may include:

- Title.
- Authors and contributors.
- Subject and keywords.
- Language.
- Creation and modification times.
- Document and instance identifiers.
- Producer and creator-tool versions.
- Rights and license information.
- Conformance profile identifiers.

## Links, Destinations, and Outlines

EDT should generate internal destinations, external links, outlines, and cross-references from the validated reference graph.

Validation should detect:

- Broken internal destinations.
- Links to missing pages or structure elements.
- Outline hierarchy inconsistent with headings.
- External links prohibited by profile.
- Annotations that obscure content or lack accessible descriptions.

## Forms and Interactive Content

Interactive PDF features require explicit profile support.

EDT should reject or constrain:

- JavaScript.
- Rich media.
- Launch actions.
- External file references.
- Dynamic forms.
- Unsupported annotation types.

Where forms are permitted, fields require correct names, roles, states, tab order, labels, and validation behavior.

## Embedded Files

Embedded files may support source packages, data attachments, associated files, or archival workflows.

An EDT profile should define:

- Permitted attachment types.
- Relationship metadata.
- File names and media types.
- Checksums.
- Accessibility implications.
- Archival and security policy.

Embedded files must not become an undocumented substitute for semantic content.

## Color and Graphics

A PDF profile may constrain:

- Output intents.
- ICC profiles.
- Device-dependent color spaces.
- Transparency.
- Overprint.
- Spot colors.
- Image resolution.
- Rendering intents.

These requirements belong to the selected output profile rather than the core EDOM model.

## Security

PDF supports encryption, permissions, signatures, actions, embedded files, and external references.

EDT should treat imported PDFs as untrusted input and should:

- Disable active content during analysis.
- Enforce resource limits.
- Inspect embedded files and actions.
- Record encryption and signature state.
- Preserve original file fixity.
- Distinguish signature validity from document trust.

Encryption may conflict with archival or accessibility profiles and must be controlled by profile policy.

## Import Strategy

A PDF importer should preserve:

- Original file bytes and digest.
- Declared PDF version.
- Page geometry and page labels.
- Text, fonts, images, graphics, annotations, and links.
- Structure tree and role mappings.
- Metadata and identifiers.
- Embedded files.
- Signatures and encryption state.
- Parser warnings and unsupported features.

The importer should separate:

- Recovered semantic structure.
- Page-layout evidence.
- Original PDF objects.
- Inferred reading order.
- Confidence and validation findings.

Pages and coordinates remain source provenance. They should not define EDOM hierarchy.

## Export Strategy

A PDF publisher should:

1. Select a declared PDF version and conformance profile.
2. Render validated EDOM content.
3. Generate a structure tree when required.
4. Embed fonts and preserve Unicode mappings.
5. Generate metadata, identifiers, outlines, and destinations.
6. Apply color, attachment, security, and signature policy.
7. Validate syntax and profile conformance.
8. Test visual rendering, text extraction, and accessibility behavior.
9. Preserve the PDF, configuration, and validation reports as build artifacts.

## Validation

EDT validation may include:

- Syntax and cross-reference errors.
- Unsupported PDF version or feature.
- Missing required metadata.
- Conflicting document identifiers.
- Missing embedded fonts.
- Invalid Unicode mapping.
- Broken links, destinations, or outlines.
- Structure-tree errors.
- Incorrect reading order.
- Missing alternative text.
- Profile-prohibited actions, encryption, or attachments.
- Invalid color-management configuration.
- Signature validation failures.
- Visual or extraction regressions.

A PDF that opens successfully is not necessarily conforming, accessible, trustworthy, or semantically complete.

## Relationship to PDF/UA

PDF/UA defines accessibility requirements for PDF. EDT should apply the repository's PDF/UA profile when accessible fixed-layout output is required.

Tagged PDF is necessary for most PDF/UA workflows, but correct tagging, reading order, language, alternative text, and semantic relationships must also be validated.

## Relationship to PDF/A

PDF/A defines archival profiles that restrict features and require stronger self-containment and metadata behavior.

EDT should select a specific PDF/A part and conformance level rather than using the label "PDF/A" generically.

Archival conformance does not automatically establish accessibility, and accessibility conformance does not automatically establish archival conformance.

## Relationship to PDF/X and PDF/E

PDF/X supports print-production exchange. PDF/E supports engineering-document workflows.

EDT should treat each as a separate profile with its own required metadata, permitted features, color or engineering constraints, and validation tools.

## Profiles

An EDT PDF profile may specify:

- ISO 32000 version.
- Specialized conformance standard and level.
- Tagged-PDF requirements.
- Role-map policy.
- Font and Unicode policy.
- Color-management policy.
- Image-resolution requirements.
- Attachment policy.
- Encryption and signature policy.
- Metadata requirements.
- Validator and renderer test matrix.
- Accessibility and extraction tests.

## Provenance

EDT should record:

- Source EDOM revision.
- Publisher and library versions.
- PDF profile.
- Font and color-profile dependencies.
- Build configuration.
- Generated artifact digest.
- Validation tools and results.
- Signature and certification information.
- Human review and waivers.

## Design Rule

```text
Treat PDF as a rendered publication artifact.
Generate structure from EDOM, not from page geometry.
Validate semantics, rendering, extraction, and profile conformance separately.
Preserve the exact build evidence for every released PDF.
```

## References

- ISO, *ISO 32000-2:2020 — Document management — Portable document format — Part 2: PDF 2.0*: https://www.iso.org/standard/75839.html
- PDF Association, *PDF Specification Index*: https://pdfa.org/resource/pdf-specification-index/
