# Standards Handbook

The Engineering Documents Toolkit (EDT) is a standards-first semantic document engineering platform.

Whenever practical, EDT adopts established open standards instead of inventing new formats, identifiers, vocabularies, or protocols. New abstractions are introduced only when existing standards cannot adequately represent required semantics or provenance.

## Purpose

This handbook documents the external standards that influence EDT's architecture, data model, validation rules, importers, publishers, accessibility support, preservation strategy, and interoperability boundaries.

Each overview answers four questions:

1. What problem does the standard solve?
2. Where does EDT use it?
3. Where does EDT intentionally not use it?
4. How does it map into EDOM and EDT profiles?

## Classification

EDT classifies standards and external specifications as:

| Classification | Meaning |
| --- | --- |
| Adopt | Preferred production standard for the stated purpose |
| Adapt | Used with an explicit EDT profile or constrained mapping |
| Bridge | Supported primarily for interoperability with external ecosystems |
| Evaluate | Monitored or supported experimentally, but not a stable production dependency |
| Reject | Intentionally excluded for a documented reason |

A standard may receive more than one classification when its role differs by workflow.

## Semantic and Linked Data

- [RDF](RDF.md)
- [OWL](OWL.md)
- [SHACL](SHACL.md)
- [SKOS](SKOS.md)
- [Schema.org](Schema.org.md)
- [Dublin Core](Dublin_Core.md)
- [W3C PROV](W3C_PROV.md)

## Web, Publishing, and Accessibility

- [HTML5](HTML5.md)
- [EPUB 3](EPUB3.md)
- [EPUB Accessibility](EPUB-Accessibility.md)
- [WCAG](WCAG.md)
- [WAI-ARIA](WAI-ARIA.md)
- [PDF](PDF.md)
- [PDF/UA](PDF-UA.md)
- [MathML](MathML.md)
- [SVG](SVG.md)

## Structured Authoring and Scholarly Content

- [DocBook](DocBook.md)
- [DITA](DITA.md)
- [TEI](TEI.md)
- [JATS](JATS.md)

## Office Documents

- [Office Open XML](OOXML.md)
- [OpenDocument Format](ODF.md)

## Localization and Terminology

- [XLIFF](XLIFF.md)
- [TMX](TMX.md)
- [SRX](SRX.md)
- [TBX](TBX.md)
- [ITS 2.0](ITS20.md)

## Citation, Identity, and Research Metadata

- [CSL](CSL.md)
- [BibTeX](BibTeX.md)
- [Crossref](Crossref.md)
- [DataCite](DataCite.md)
- [ORCID](ORCID.md)
- [ROR](ROR.md)
- [COAR Controlled Vocabularies](COAR.md)

## Preservation and Packaging

- [PREMIS](PREMIS.md)
- [METS](METS.md)
- [BagIt](BagIt.md)
- [OCFL](OCFL.md)
- [RO-Crate](RO-Crate.md)

## Images and Compound Digital Objects

- [IIIF](IIIF.md)

## Architectural Rule

```text
Standards define interoperable boundaries.
EDOM unifies semantic meaning across those boundaries.
Profiles constrain mappings for specific workflows.
Provenance records every transformation and decision.
```

EDT does not claim that every standard is interchangeable or losslessly convertible. Importers and publishers must report approximations, unsupported constructs, version dependencies, and information loss.

## Versioning Policy

Every production profile should pin:

- Standard or specification version.
- Schema, vocabulary, or context version.
- Processor or validator version.
- EDT mapping-profile version.
- Compatibility target where application behavior matters.

Unversioned references are insufficient for reproducible document engineering.

## Validation Policy

Schema validity is necessary but rarely sufficient. EDT validation may also require:

- Semantic constraints.
- Reference integrity.
- Accessibility evaluation.
- Fixity checks.
- Runtime behavior tests.
- Target-application round trips.
- Repository or registration-service reconciliation.
- Human review.

## Philosophy

Standards are adopted to improve interoperability, longevity, accessibility, auditability, and portability.

EDT's goal is not to replace these standards. It provides a common semantic model that can import, validate, transform, and publish across them while preserving provenance and enabling reproducible builds.
