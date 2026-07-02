# Research Organization Registry

## Purpose

The Research Organization Registry (ROR) provides open persistent identifiers and metadata for research organizations.

For EDT, ROR identifies affiliations, publishers, funders, repositories, laboratories, universities, companies, government bodies, and other organizations connected to documents and research outputs.

## Current Schema

EDT targets **ROR Metadata Schema 2.1** for current integrations.

Schema 2.1 includes organization identifiers, names, locations, domains, links, external identifiers, organization types, status, and inter-organization relationships.

## Adoption Decision

EDT classifies ROR as **Adopt** for research-organization identity and **Bridge** for DataCite, Crossref, ORCID, JATS, and repository workflows.

## Architectural Boundary

```text
ROR identifies organizations.
EDOM records the organization's role in a document or project.
External deposit schemas carry selected ROR references.
```

A ROR record does not replace project-specific affiliation text, historical context, contracts, departments, or local organization authority records.

## Identifier Policy

EDT should store ROR identifiers as full HTTPS URIs.

An identifier should be accepted only when:

- The record resolves.
- The organization matches the intended entity.
- The record status is understood.
- Historical affiliation policy has been applied.
- The identifier was not selected solely from fuzzy name matching.

## Names

ROR supports multiple names, including display names, labels, aliases, and acronyms.

EDT should preserve:

- The ROR identifier.
- The publication-specific organization name.
- Language and script where available.
- The ROR display name used during verification.
- Verification time and record revision evidence.

The current display name must not overwrite a historically correct affiliation name in an older publication.

## Status and Relationships

ROR records may be active, inactive, or withdrawn and may identify parent, child, related, predecessor, or successor organizations.

EDT should preserve historical organization identity. A successor relationship is useful for discovery but does not authorize silently rewriting prior affiliations.

Withdrawn records require review before new use.

## Import Strategy

A ROR importer should:

1. Pin the API and schema version.
2. Preserve the complete identifier URI.
3. Preserve names, locations, types, status, external identifiers, and relationships.
4. Record retrieval time and source response digest.
5. Detect inactive or withdrawn records.
6. Retain the local affiliation text separately from registry metadata.

## Export Strategy

An EDT exporter should include ROR identifiers only where the target schema supports them and the organization match has been verified.

The exported name should follow the publication or deposit profile while preserving the identifier as the stable identity reference.

## Validation

EDT validation may include:

- Invalid ROR identifier syntax.
- Identifier that does not resolve.
- Name or location inconsistent with the selected record.
- Withdrawn record used without review.
- Active affiliation rewritten to a successor incorrectly.
- Missing ROR identifier where a profile requires one.
- Schema-version mismatch.
- Organization role missing from EDOM.

## Relationship to Other Identifiers

ROR may map to identifiers such as ISNI, GRID, Wikidata, and funder identifiers. These mappings are useful evidence but remain typed external identifiers rather than interchangeable strings.

ORCID identifies people. ROR identifies organizations. DataCite, Crossref, JATS, and ORCID records may carry ROR affiliations.

## Profiles

An EDT ROR profile may specify:

- ROR schema and API version.
- Matching and human-review thresholds.
- Historical-affiliation policy.
- Status handling.
- Required organization roles.
- Target-schema mappings.
- Cache and refresh policy.

## Design Rule

```text
Use ROR to identify the organization.
Preserve the name and role used in the publication.
Do not rewrite history when organizations change.
```

## References

- ROR Data Structure, Schema 2.1: https://ror.readme.io/docs/ror-data-structure
- ROR Identifier Pattern: https://ror.readme.io/docs/identifier
