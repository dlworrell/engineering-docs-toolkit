# DataCite Metadata Schema

## Purpose

The DataCite Metadata Schema defines structured metadata for the publication, citation, discovery, and linking of research data and other research outputs.

For EDT, DataCite is a deposit and discovery metadata profile for datasets, software, reports, workflows, presentations, publications, projects, awards, and related research objects.

## Current Standard

EDT targets **DataCite Metadata Schema 4.7**, released on 3 March 2026.

Profiles must pin the schema version because controlled values and relation types evolve between releases.

## Adoption Decision

EDT classifies DataCite as **Adopt** for research-output metadata and **Bridge** for DOI registration and repository deposit workflows.

## Architectural Boundary

```text
EDOM owns complete document and project semantics.
DataCite carries a publication and discovery metadata projection.
DOI registration services own identifier registration state.
```

DataCite metadata must not become the sole source of truth for authorship, provenance, funding, or relationships when richer EDOM records exist.

## Core Mapping

Representative mappings include:

| DataCite property | EDT meaning |
| --- | --- |
| Identifier | DOI or other registered identifier |
| Creator | Primary creator with optional ORCID and affiliation |
| Title | Public resource title |
| Publisher | Publishing or hosting organization |
| Publication year | Public release year |
| Resource type | General and specific output type |
| Contributor | Contributor with typed role |
| Related identifier | Typed reference-graph relationship |
| Rights | License and access terms |
| Funding reference | Funder, award, and grant metadata |
| Geo location | Spatial coverage |
| Description | Abstract, methods, or other typed description |
| Date | Typed lifecycle or coverage date |

## Identifiers

EDT should preserve identifiers as typed values with scheme, canonical form, registration agency, and resolution status.

A DOI string is not proof that the DOI is registered, resolves correctly, or describes the intended resource. Deposit validation and post-registration resolution checks are separate steps.

## Names and Organizations

Creators and contributors should use stable person and organization identifiers where available, including ORCID and ROR.

EDT should preserve the supplied display name as well as the identifier. Identifiers must not be inferred from name similarity alone.

## Relationships

DataCite relation types should be generated from the validated EDT reference graph.

Examples include version, part-whole, metadata, documentation, supplement, translation, derivation, citation, and identity relationships.

Profiles should require reciprocal relationships where the repository workflow supports them and should prevent unsupported free-text relation semantics from being forced into an incorrect controlled value.

## Import Strategy

A DataCite importer should:

1. Identify the schema version and representation.
2. Preserve all supplied identifiers and controlled values.
3. Normalize names, language tags, dates, and identifiers without discarding source values.
4. Map relationships into the EDT reference graph.
5. Preserve unknown future values as extension data where possible.
6. Record source, retrieval time, importer version, and validation results.

## Export Strategy

A DataCite exporter should:

1. Select a pinned schema version and deposit profile.
2. Map authoritative EDOM metadata into required and optional fields.
3. Use ORCID, ROR, funder, award, and related-resource identifiers where verified.
4. Emit controlled values valid for the selected schema.
5. Validate XML or JSON before deposit.
6. Preserve the exact submitted metadata and service response.
7. Reconcile the registered record with the submitted build.

## Validation

EDT validation may include:

- Missing mandatory properties.
- Invalid controlled values.
- Invalid or unverified identifiers.
- Creator or contributor records lacking required names.
- Affiliation identifiers inconsistent with the named organization.
- Invalid date or language values.
- Broken or semantically inconsistent related identifiers.
- Funding records missing required award context.
- Metadata that refers to a different artifact revision.
- Deposit response inconsistent with the requested DOI state.

Schema validity alone does not prove metadata correctness.

## Relationship to Crossref

DataCite and Crossref both register DOI metadata but serve overlapping ecosystems with different schemas, services, and conventions.

EDT should select the registration agency according to publisher and repository policy. Conversion between DataCite and Crossref metadata must be treated as a mapped transformation with explicit loss reporting.

## Relationship to ORCID and ROR

ORCID identifies people; ROR identifies research organizations. EDT should preserve both the persistent identifier and the name used for the specific publication.

Historical affiliations should remain historically correct even when an organization later changes status or name.

## Profiles

An EDT DataCite profile may specify:

- Schema version.
- Resource-type policy.
- Required creator and contributor identifiers.
- Affiliation and funding rules.
- Relationship requirements.
- License and access metadata.
- Deposit service and endpoint.
- DOI state transitions.
- Validation and reconciliation checks.

## Provenance

EDT should record the source EDOM revision, exporter version, schema version, submitted payload digest, registration service response, assigned DOI, timestamps, and later metadata updates.

## Design Rule

```text
Generate DataCite metadata from authoritative semantics.
Validate identifiers and relationships before deposit.
Preserve the exact metadata that was registered.
```

## References

- DataCite, *Metadata Schema 4.7*: https://schema.datacite.org/meta/kernel-4.7/
- DataCite Metadata Schema Documentation: https://datacite-metadata-schema.readthedocs.io/
