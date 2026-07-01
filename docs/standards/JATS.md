# JATS

## Purpose

JATS (Journal Article Tag Suite) is the ANSI/NISO XML standard for representing journal articles and related scholarly content. It provides structured models for article metadata, body content, references, figures, tables, equations, supplementary material, and publication history.

## Current Standard

EDT should target JATS 1.4, published as ANSI/NISO Z39.96-2024, unless a project profile explicitly requires another version for compatibility or archival reproducibility.

JATS provides three principal tag sets:

- Journal Archiving and Interchange.
- Journal Publishing.
- Article Authoring.

The selected tag set and version must be recorded with the document profile and provenance.

## Where EDT Uses JATS

- Import of scientific and scholarly journal articles.
- Export to journal-production and repository workflows.
- Preservation of article metadata and references.
- Representation of figures, tables, equations, acknowledgments, and supplementary material.
- Interchange with archives, publishers, and indexing systems.
- Prior art for scientific-document semantics.

## Where EDT Does Not Use JATS

JATS is not EDT's universal internal representation. EDOM remains authoritative because EDT must also model books, engineering documents, standards, websites, archival sources, source-page regions, validation state, provenance, reference graphs, and profile-specific semantics outside the journal-article domain.

EDT also does not assume that all scientific documents should be forced into an article structure when a report, book, standard, dataset description, or another domain model is more appropriate.

## Mapping to EDOM

Representative JATS structures map approximately as follows:

| JATS | EDOM |
| --- | --- |
| `article` | `document` |
| `front` | document metadata and front matter |
| `body` | main document divisions |
| `back` | references and back matter |
| `sec` | `section` |
| `p` | `paragraph` |
| `fig` | `figure` |
| `table-wrap` | `table` |
| `disp-formula` / `inline-formula` | `equation` |
| `xref` | reference relationship |
| `ref-list` | `bibliography` |
| `supplementary-material` | supplemental asset or document |
| `contrib-group` | contributor metadata |
| `article-meta` | document metadata |

JATS elements without a direct EDOM equivalent should be retained through profile-defined nodes, extension metadata, or explicit loss reporting.

## Import Strategy

A JATS importer should preserve:

- The JATS version and selected tag set.
- Article identifiers and publication metadata.
- Contributor names, roles, affiliations, and identifiers.
- Section hierarchy.
- Citations and bibliographic identifiers.
- Figures, tables, equations, and supplementary assets.
- Footnotes, acknowledgments, funding, permissions, and publication history.
- Source XML locations and provenance.

Import must preserve explicit semantics rather than reconstructing them from rendered appearance.

## Export Strategy

A JATS bridge should target a declared tag set, version, and project profile. It should validate output against the corresponding JATS schema and report any EDOM semantics that require approximation, extension, or omission.

Journal Publishing is the likely default for production-oriented output, while Archiving and Interchange may be preferable for preservation and heterogeneous legacy content. Article Authoring may be appropriate for constrained authoring workflows.

## Profiles and Customization

Publishers and repositories commonly apply business rules or constrained JATS profiles beyond schema validity. EDT profiles should represent these requirements explicitly through:

- Allowed and required semantic structures.
- Metadata requirements.
- Identifier policies.
- Reference and citation rules.
- Accessibility constraints.
- Publisher-specific import and export mappings.

Schema validity alone is not sufficient to establish publication readiness.

## Design Notes

JATS is strong prior art for structured scientific publishing and should be treated as a first-class interchange standard. EDT should preserve JATS semantics where available, map them transparently into EDOM, and avoid introducing proprietary equivalents for concepts already established by the standard.

## References

- NISO, *JATS: Journal Article Tag Suite, version 1.4 (ANSI/NISO Z39.96-2024)*: https://www.niso.org/standards-committees/jats
- NLM, *JATS: Journal Publishing Tag Set*: https://jats.nlm.nih.gov/publishing/
