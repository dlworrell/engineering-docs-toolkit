# W3C PROV

## Purpose

W3C PROV is the World Wide Web Consortium recommendation for representing provenance information. It provides a standard model for describing entities, activities, and agents involved in producing data or documents.

## Where EDT Uses W3C PROV

- Conceptual model for provenance architecture.
- Traceability from source artifacts to EDOM.
- Transformation history.
- Audit and review workflows.
- Reproducible publishing.
- Future standards-based provenance interchange.

## Where EDT Does Not Use W3C PROV

EDT does not require its internal provenance representation to mirror PROV syntax exactly. EDOM remains the canonical internal model. Where interchange is needed, EDOM provenance can be mapped to PROV.

## Mapping to EDOM

EDOM provenance aligns naturally with PROV concepts:

| W3C PROV | EDT |
| --- | --- |
| Entity | Source document, asset, or EDOM node |
| Activity | Import, OCR, layout analysis, semantic recognition, validation, publication |
| Agent | User, plugin, importer, OCR engine, publisher |

This mapping allows provenance to be preserved internally while remaining compatible with external standards.

## Design Notes

EDT treats provenance as a first-class architectural concern. Adoption of W3C PROV provides a well-established vocabulary for interoperability while allowing EDT to optimize its internal representation for deterministic processing and semantic document engineering.