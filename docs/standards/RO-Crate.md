# RO-Crate

## Purpose

Research Object Crate (RO-Crate) is a JSON-LD-based packaging and metadata specification for describing research objects, their files, contextual entities, provenance, and relationships.

For EDT, RO-Crate is a portable research-object exchange layer for source materials, semantic documents, data, software, workflows, publications, metadata, and provenance.

## Current Standard

EDT targets **RO-Crate Metadata Specification 1.3**, published as a community Recommendation on 22 June 2026.

Profiles must pin both the RO-Crate specification version and any domain-specific RO-Crate profile.

## Adoption Decision

EDT classifies RO-Crate as **Adopt** for research-object exchange and **Bridge** for FAIR data, workflow, repository, and computational-research ecosystems.

## Architectural Boundary

```text
EDOM owns canonical document semantics.
RO-Crate describes a portable graph of files and contextual entities.
Packaging and repository layers preserve the physical files.
```

RO-Crate metadata is a derived exchange view, not a replacement for EDOM or complete repository provenance.

## Core Structure

An RO-Crate normally includes:

- `ro-crate-metadata.json`, containing JSON-LD metadata.
- A root data entity representing the crate.
- Data entities for files, directories, datasets, workflows, or other payload objects.
- Contextual entities such as people, organizations, licenses, places, and instruments.
- Optional human-readable preview content.

Entities are identified by IRIs or relative identifiers and typed primarily with Schema.org and profile vocabularies.

## EDT Mapping

Representative mappings include:

| EDT concept | RO-Crate representation |
| --- | --- |
| Project or release package | Root data entity |
| Source or generated file | Data entity |
| EDOM publication | CreativeWork or profile-specific entity |
| Person | Contextual Person entity with ORCID where verified |
| Organization | Contextual Organization entity with ROR where verified |
| License | Identified license entity |
| Build or transformation | Provenance action or profile-defined activity |
| Reference-graph relationship | Typed JSON-LD relationship |
| Software dependency | SoftwareApplication or SoftwareSourceCode entity |
| Dataset | Dataset entity with DataCite-compatible metadata where appropriate |

## Profiles

RO-Crate profiles narrow the general specification for particular communities or workflows.

An EDT profile should declare:

- RO-Crate version.
- Profile URI and version.
- Required entity types and properties.
- Vocabulary dependencies.
- Identifier policy.
- Validation rules.
- Packaging expectations.

Profile conformance must not be inferred merely from the presence of a profile URI.

## Import Strategy

An importer should:

1. Preserve the original crate and digest.
2. Parse JSON-LD under the pinned context.
3. Identify the root data entity and declared profiles.
4. Preserve all data and contextual entities.
5. Resolve relative identifiers without escaping the crate root.
6. Map recognized entities and relationships into EDOM, provenance, and the reference graph.
7. Preserve unknown properties as extension data.
8. Report missing files, duplicate identifiers, invalid types, and unresolved relationships.

Remote context retrieval should be controlled, cached, and versioned for reproducibility.

## Export Strategy

An exporter should:

1. Select the RO-Crate and domain-profile versions.
2. Select files and contextual entities for the crate.
3. Generate stable identifiers and relationships.
4. Include verified ORCID, ROR, DOI, license, and vocabulary identifiers where available.
5. Preserve file media types, sizes, and checksums according to profile policy.
6. Validate JSON-LD and profile requirements.
7. Preserve the generated metadata graph and validation report.

## Validation

EDT validation may include:

- Missing or invalid metadata descriptor.
- Missing root data entity.
- Duplicate or ambiguous identifiers.
- Referenced payload files that do not exist.
- Files absent from the metadata graph where the profile requires enumeration.
- Invalid or unpinned JSON-LD context.
- Missing required types or properties.
- Broken relationships.
- Profile declaration inconsistent with actual content.
- External identifiers that do not resolve or match the entity.
- Paths that escape the crate root.

JSON syntax validity alone does not prove RO-Crate or profile conformance.

## Relationship to BagIt and OCFL

RO-Crate describes research-object semantics and context. BagIt supports transfer fixity. OCFL supports persistent versioned storage.

They may be combined deliberately:

```text
RO-Crate metadata describes the research object.
BagIt packages it for transfer.
OCFL preserves versioned repository states.
```

Each layer must retain its own validation and provenance evidence.

## Relationship to Schema.org, RDF, and W3C PROV

RO-Crate uses JSON-LD and commonly relies on Schema.org terms. EDT should preserve the RDF graph interpretation rather than treating the metadata as arbitrary nested JSON.

W3C PROV or profile-specific provenance terms may supplement RO-Crate's entity and action descriptions when stronger provenance modeling is required.

## Provenance

EDT should record the source EDOM revision, exporter or importer version, RO-Crate and profile versions, JSON-LD contexts, payload digests, validation results, and any mapping or normalization decisions.

## Design Rule

```text
Use RO-Crate to describe a portable research object.
Keep EDOM as the canonical document model.
Pin contexts and profiles.
Validate both the graph and the packaged files.
```

## References

- RO-Crate Metadata Specification 1.3: https://www.researchobject.org/ro-crate/specification/1.3/
- RO-Crate Profiles: https://www.researchobject.org/ro-crate/profiles.html
