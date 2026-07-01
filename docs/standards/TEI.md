# TEI

## Purpose

The Text Encoding Initiative (TEI) Guidelines define a modular XML vocabulary for representing textual sources, editions, manuscripts, linguistic material, correspondence, drama, dictionaries, critical apparatus, and other scholarly documents.

TEI is especially valuable when a document must preserve editorial interpretation, textual variation, source structure, and scholarly annotation rather than only its published appearance.

## Current Standard

EDT should target the current TEI P5 Guidelines unless a project profile explicitly requires an older release for compatibility or archival reproducibility.

As of February 2026, the current published TEI P5 release is 4.11.0.

## Where EDT Uses TEI

- Import of scholarly and humanities XML.
- Preservation of manuscript and source-document structure.
- Critical editions and textual variants.
- Named entities, quotations, notes, correspondence, and editorial annotations.
- Export to TEI-based repositories and scholarly workflows.
- Prior art for extensible semantic text encoding.

## Where EDT Does Not Use TEI

TEI is not EDT's universal internal model. EDOM remains authoritative because EDT must represent technical, scientific, engineering, publishing, and provenance semantics beyond TEI's primary scope.

EDT also does not require all imported text to adopt TEI's editorial conventions when another vocabulary or profile provides a clearer domain model.

## Mapping to EDOM

Representative TEI structures map approximately as follows:

| TEI | EDOM |
| --- | --- |
| `TEI` / `text` | `document` |
| `front`, `body`, `back` | document divisions |
| `div` | `section` |
| `p` | `paragraph` |
| `head` | heading metadata |
| `figure` | `figure` |
| `table` | `table` |
| `note` | `note` |
| `q` / `quote` | quotation |
| `list` | `list` |
| `ref` / `ptr` | reference relationship |
| `persName`, `placeName`, `orgName` | typed named entity |
| `app`, `lem`, `rdg` | textual-variant structure |
| `teiHeader` | document metadata and source description |

TEI constructs without a direct EDOM equivalent should be retained through profile-defined nodes, extension metadata, or loss reporting.

## Import Strategy

A TEI importer should preserve:

- Element and attribute semantics.
- Stable identifiers and references.
- Header metadata.
- Editorial responsibility statements.
- Textual variants and critical apparatus.
- Named-entity typing.
- Source locations and provenance.
- The TEI release and customization used by the source document.

Import must not flatten editorial distinctions merely because two constructs render similarly.

## Export Strategy

A TEI bridge should use a declared TEI customization rather than assuming unrestricted `tei_all` output. The selected schema, modules, constraints, and release should be recorded so the export can be reproduced and validated.

Any EDOM semantics that require approximation or extension must be reported explicitly.

## Profiles and ODD

TEI's ODD customization mechanism is relevant prior art for EDT profiles. Both permit a project or domain to constrain and extend a broader semantic system.

They are not identical:

- ODD primarily defines and documents TEI schema customizations.
- EDT profiles may additionally define import mappings, validation policies, reference behavior, quality rules, and publisher behavior.

An EDT TEI profile may therefore include or reference an ODD customization while also specifying the surrounding document-engineering workflow.

## Design Notes

TEI demonstrates how a mature semantic vocabulary can preserve complex textual meaning across generations of tools. EDT should bridge to TEI where it is the appropriate domain standard, preserve TEI-specific semantics during import, and avoid replacing established scholarly conventions with proprietary equivalents.

## References

- TEI Consortium, *TEI P5: Guidelines for Electronic Text Encoding and Interchange*: https://tei-c.org/guidelines/p5/
- Version-independent concept DOI for the latest TEI P5 release: https://doi.org/10.5281/zenodo.3413524
