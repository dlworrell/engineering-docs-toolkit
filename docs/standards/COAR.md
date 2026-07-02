# COAR Controlled Vocabularies

## Purpose

The Confederation of Open Access Repositories (COAR) publishes controlled vocabularies for repository metadata, including resource types, access rights, and version types.

For EDT, COAR vocabularies provide interoperable classification values for repository deposits and scholarly communication metadata.

## Current Vocabulary

EDT targets **COAR Resource Types 3.2** and should pin the exact published version of every COAR vocabulary used by a profile.

## Adoption Decision

EDT classifies COAR controlled vocabularies as **Adopt** for repository classification and **Bridge** for institutional and open-access repository workflows.

## Architectural Boundary

```text
EDOM owns rich semantic type and lifecycle metadata.
COAR supplies shared repository-facing classification terms.
Profiles map EDOM values to versioned COAR concept URIs.
```

COAR terms should narrow or classify metadata for exchange; they should not erase more specific EDT semantics.

## Vocabulary Use

Relevant COAR vocabularies include:

- Resource types.
- Access rights.
- Version types.

EDT should store concept URIs rather than labels alone. Labels are language-dependent display values; the URI identifies the concept.

## Mapping Policy

A mapping should record:

- EDOM source type or state.
- COAR concept URI.
- Vocabulary version.
- Mapping relation and confidence.
- Profile that authorized the mapping.

When no exact concept exists, EDT should use the nearest profile-approved broader term and report the loss of specificity.

## Resource Types

Resource-type mappings may cover publications, datasets, software, images, audiovisual works, learning objects, patents, workflows, reports, and other repository objects.

A repository-facing resource type is not necessarily the same as an EDOM node type or MIME media type.

## Access Rights

Access-rights metadata should reflect actual distribution policy and technical access state.

EDT must not infer open access merely because a file is publicly reachable during processing. Embargoes, restricted access, metadata-only records, and closed access require explicit policy values.

## Version Types

Version terminology should be generated from editorial and publication provenance, not guessed from a file name.

Examples may distinguish submitted, accepted, published, updated, or other version states according to the selected vocabulary and repository profile.

## Import Strategy

A COAR-aware importer should preserve concept URIs, source labels, vocabulary version, language, and any local repository extensions.

Unknown or deprecated concepts should be retained and reported rather than silently replaced.

## Export Strategy

An exporter should:

1. Select a pinned COAR vocabulary version.
2. Map authoritative EDOM values to concept URIs.
3. Emit labels only as supplemental display text.
4. Validate that each URI belongs to the declared vocabulary.
5. Report broad, approximate, or missing mappings.

## Validation

EDT validation may include:

- Label supplied without a concept URI.
- Concept URI absent from the pinned vocabulary.
- Deprecated concept used for new output.
- Resource type inconsistent with the deposited artifact.
- Access-rights value inconsistent with distribution policy.
- Version type inconsistent with provenance.
- Mapping that discards required EDOM specificity without warning.

## Relationship to SKOS

COAR vocabularies are published as controlled concept schemes and align naturally with EDT's SKOS strategy.

EDT may import them as external SKOS schemes while preserving COAR ownership, versioning, identifiers, and labels.

## Profiles

An EDT COAR profile may specify:

- Vocabulary names and versions.
- Required concept schemes.
- EDOM-to-COAR mappings.
- Fallback concepts.
- Deprecation policy.
- Repository-specific constraints.
- Language and label policy.

## Design Rule

```text
Exchange stable concept URIs, not free-text labels.
Preserve richer EDOM semantics behind repository classifications.
Version every vocabulary dependency.
```

## References

- COAR Controlled Vocabularies for Repositories: https://vocabularies.coar-repositories.org/
- COAR Resource Types 3.2: https://vocabularies.coar-repositories.org/resource_types/
