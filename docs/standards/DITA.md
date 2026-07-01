# DITA

## Purpose

DITA (Darwin Information Typing Architecture) is an OASIS standard for topic-oriented authoring, reuse, specialization, and publishing. It is especially well suited to product documentation, procedures, reference material, and large documentation sets assembled from reusable components.

## Where EDT Uses DITA

- Import of structured topic-based documentation.
- Export to DITA-based publishing ecosystems.
- Reuse of modular content across multiple publications.
- Conditional processing and audience-specific variants.
- Comparison point for EDT profiles and semantic specialization.

## Where EDT Does Not Use DITA

DITA is not EDT's canonical internal representation. EDOM remains authoritative because EDT also preserves source regions, provenance, validation state, reference-graph data, processing history, and semantics that may originate outside DITA.

EDT also does not require all documents to be decomposed into DITA topics when a continuous book, article, archival source, or another domain vocabulary is the better fit.

## Mapping to EDOM

Common DITA structures map into EDOM approximately as follows:

| DITA | EDOM |
| --- | --- |
| topic | document fragment or section |
| concept | profile-qualified section |
| task | procedure or task node |
| reference | reference section or structured data node |
| map | publication assembly and ordering |
| topicref | reference relationship |
| key / keyref | stable identifier and indirect reference |
| conref | reusable-content relationship |
| conditional attributes | profile or publication conditions |

DITA specialization can map to EDT profiles, but the two mechanisms are not identical. A profile may define validation rules, semantic kinds, import mappings, and publication behavior beyond XML vocabulary specialization.

## Import Strategy

A DITA importer should preserve topic boundaries, maps, identifiers, keys, references, reuse relationships, conditional attributes, and specialization metadata. Imported content should retain provenance back to the original XML elements and source files.

Unsupported specializations should be retained as extension metadata or reported explicitly instead of being silently flattened.

## Export Strategy

A DITA bridge should export only semantics that have a defined DITA mapping. It should report approximations and losses when EDOM concepts cannot be represented faithfully in the selected DITA vocabulary or specialization.

## Design Notes

DITA provides strong prior art for modular authoring, content reuse, and domain specialization. EDT should interoperate with DITA and learn from its architecture while retaining a broader model capable of handling heterogeneous source documents, provenance-rich transformation, semantic validation, and multiple publication families.

## Reference

- OASIS, *Darwin Information Typing Architecture (DITA) Version 1.3* and approved errata: https://docs.oasis-open.org/dita/dita/v1.3/errata02/os/