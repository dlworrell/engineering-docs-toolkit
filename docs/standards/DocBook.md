# DocBook

## Purpose

DocBook is an open XML vocabulary for semantic technical documentation. It provides structured elements for books, articles, chapters, sections, procedures, figures, tables, examples, code listings, glossaries, bibliographies, indexes, and related publishing content.

## Where EDT Uses DocBook

- Interchange with existing technical publishing systems.
- Import of semantically structured technical documents.
- Export for downstream XML publishing workflows.
- Terminology and design guidance for common technical document objects.
- Comparison point for EDOM's technical publishing semantics.

## Where EDT Does Not Use DocBook

DocBook is not EDT's internal canonical model. EDOM remains the authoritative representation because EDT must also preserve provenance, source regions, validation state, reference graph data, profile extensions, and processing metadata that do not map cleanly to a single publishing vocabulary.

EDT also does not require every document family to conform to DocBook's vocabulary when another standard or profile is a better semantic fit.

## Mapping to EDOM

Many DocBook elements map directly or approximately to EDOM kinds:

| DocBook | EDOM |
| --- | --- |
| `book` / `article` | `document` |
| `chapter` / `section` | `section` |
| `para` | `paragraph` |
| `figure` | `figure` |
| `table` | `table` |
| `equation` | `equation` |
| `procedure` | profile-defined procedure |
| `example` | `example` |
| `glossary` | `glossary` |
| `bibliography` | `bibliography` |
| `index` | `index` |

Identifiers and cross-references can map into EDOM identifiers and reference relationships. DocBook metadata maps into EDOM document metadata where equivalent fields exist.

## Import Strategy

A DocBook importer should preserve explicit source semantics rather than re-infer them from presentation. Source element names, attributes, identifiers, and locations should remain available through provenance metadata.

Unsupported or profile-specific constructs should be retained through extension metadata or loss-reporting rather than silently discarded.

## Export Strategy

A DocBook publisher or bridge should emit standards-conforming XML from validated EDOM content. The export should document any EDOM semantics that require approximation, extension elements, or profile-specific mapping.

## Design Notes

DocBook demonstrates that semantic technical publishing has substantial prior art. EDT should reuse its vocabulary and ecosystem where practical while retaining EDOM as the broader semantic and provenance-preserving platform model.