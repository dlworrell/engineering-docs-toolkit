# METS

## Purpose

METS (Metadata Encoding and Transmission Standard) is an XML standard for packaging and linking descriptive, administrative, and structural metadata about digital objects.

For EDT, METS is a preservation and repository-interchange container. It can describe how files, representations, metadata records, and structural components belong together without replacing the richer document semantics held in EDOM.

## Current Standard

METS Version 2 is the current major revision. It simplifies the schema, improves consistency, and removes the METS 1 dependency on XLink while preserving a migration path for common METS 1 use cases.

METS Version 1 remains supported, with schema version 1.12.1 published as the current METS 1 schema.

An EDT profile must declare which METS major version it targets. It must not emit a hybrid document that assumes METS 1 and METS 2 semantics are interchangeable.

## Adoption Decision

EDT classifies METS as **Bridge**.

Rationale:

- METS is useful for repository packages, archival interchange, and representation-level structure.
- It complements PREMIS, descriptive metadata standards, and technical metadata vocabularies.
- It is not suitable as EDT's canonical semantic document model.
- Repository profiles vary widely, so EDT should support declared mappings rather than assume one universal METS package.

## Where EDT Uses METS

- Repository-ingest packages.
- Archival information packages.
- Structural maps for compound digital objects.
- Linking descriptive, administrative, technical, rights, source, and preservation metadata.
- Linking source files, normalized EDOM serializations, generated publications, and supporting assets.
- Recording file groups and alternate representations.
- Bridging EDT packages into institutional digital-library workflows.

## Where EDT Does Not Use METS

METS is not EDT's canonical semantic representation. EDOM remains authoritative for chapters, sections, paragraphs, equations, figures, tables, references, profiles, source regions, validation findings, and document-level semantics.

METS also does not replace:

- PREMIS for preservation events, agents, rights, and fixity history.
- W3C PROV for general provenance graphs.
- Dublin Core, MODS, or other descriptive metadata vocabularies.
- Format-specific technical metadata.
- BagIt, OCFL, or repository-specific storage and transport conventions.

METS binds these records and files into a package; it does not own every metadata domain contained within that package.

## Core Structural Concepts

Representative METS concepts map into EDT approximately as follows:

| METS concept | EDT meaning |
| --- | --- |
| METS document | Package-level structural metadata record |
| Descriptive metadata section | Linked or embedded descriptive metadata |
| Administrative metadata section | Technical, rights, source, and preservation metadata |
| File section | Inventory of files and representations |
| Structural map | Logical or physical hierarchy of a digital object |
| Structural links | Explicit links among structural components |
| Behavior metadata | Processing or service association, when used by a profile |
| File group | Related files, renditions, or representation components |
| Division | Structural component in a logical or physical hierarchy |
| File pointer | Link from structure to one or more package files |

The exact element names and link mechanisms differ between METS 1 and METS 2. EDT implementations must follow the declared target version.

## Mapping to EDT Artifacts

A typical EDT preservation package may map as follows:

| EDT artifact | METS role |
| --- | --- |
| Original source PDF, XML, HTML, image, or office file | File inventory entry |
| Normalized EDOM serialization | File inventory entry and derived representation |
| EPUB, HTML, PDF, or other publication output | File inventory entry and publication representation |
| Validation report | Administrative or linked metadata artifact |
| Quality report | Administrative or linked metadata artifact |
| PREMIS record | Preservation metadata section or linked metadata file |
| W3C PROV record | Provenance metadata section or linked metadata file |
| Dublin Core or MODS record | Descriptive metadata section or linked metadata file |
| Page images, figures, media, fonts, and stylesheets | File inventory entries grouped by representation or function |
| Logical EDOM hierarchy | Logical structural map projection |
| Source-page or source-region hierarchy | Physical or source-oriented structural map projection |

METS identifiers should connect these records without replacing EDOM identifiers or repository identifiers.

## Logical and Physical Structure

EDT distinguishes semantic structure from source provenance. METS packages may need both:

- A logical structure describing chapters, sections, articles, or components.
- A physical structure describing pages, image files, scans, sheets, or file sequence.

These structures should remain separate when they express different facts.

For example, an EDOM theorem may span two source pages. EDT should not split the theorem semantically merely to match a physical page hierarchy. The METS package may instead link the logical theorem-bearing section to the relevant files or regions while preserving page order separately.

## Metadata Sections

A METS profile should identify which metadata vocabulary owns each metadata domain.

Typical choices include:

| Metadata domain | Likely standard |
| --- | --- |
| Descriptive metadata | Dublin Core, MODS, DataCite, JATS, TEI header, or profile-specific XML |
| Preservation metadata | PREMIS |
| General provenance | W3C PROV |
| Rights and licenses | PREMIS Rights, RightsStatements.org, Creative Commons, or repository policy |
| Image technical metadata | MIX or repository-specific technical metadata |
| Text technical metadata | textMD or repository-specific technical metadata |
| Audio or video technical metadata | format-specific technical vocabularies |
| EDOM package metadata | EDT-defined schema or JSON serialization |

EDT should avoid copying the same assertion into multiple metadata sections unless a target profile requires it. When duplication is required, generation rules and source precedence must be explicit.

## METS 2 Strategy

METS 2 should be the preferred target for new EDT-controlled integrations when the receiving repository supports it.

A METS 2 exporter should:

1. Use the official METS 2 namespace and schema.
2. Avoid METS 1 XLink assumptions.
3. Preserve file inventory, structural hierarchy, metadata links, and representation relationships.
4. Record the exact schema revision used.
5. Validate output against the declared schema and repository profile.
6. Report any METS 1 feature or local extension that lacks a direct METS 2 equivalent.

Because METS 2 is a major revision, repository compatibility must be confirmed rather than assumed.

## METS 1 Compatibility

METS 1 remains important because many repositories and legacy packages depend on it.

An EDT METS 1 profile should:

- Target a declared schema revision, normally 1.12.1 unless the repository requires another version.
- Use XLink consistently where required.
- Preserve profile-specific conventions.
- Validate against both the official schema and any institutional Schematron or business rules.
- Record deviations and local extensions.

METS 1 support should be treated as deliberate compatibility work, not as the default for new repositories that accept METS 2.

## Import Strategy

A METS importer should preserve:

- METS major version and schema revision.
- Package identifiers.
- File inventory and checksums.
- File groups and representation roles.
- Logical and physical structural maps.
- Metadata-section identifiers and link targets.
- External and embedded metadata records.
- Structural links.
- Profile declarations and local extensions.
- Source locations and import provenance.

The importer should not assume that a METS structural map is equivalent to EDOM semantic hierarchy. It should classify each map by declared purpose and map it into EDOM or provenance structures accordingly.

Unknown metadata vocabularies or local extensions should be retained as opaque, typed artifacts with warnings rather than discarded.

## Export Strategy

A METS exporter should:

1. Select a declared METS version and repository profile.
2. Inventory every included file.
3. Assign stable package-local identifiers.
4. Record checksums and MIME types where required.
5. Group files into representations or functional sets.
6. Generate logical and physical structural maps from validated EDT data.
7. Attach or link descriptive, administrative, technical, rights, provenance, and preservation metadata.
8. Validate schema conformance.
9. Validate repository-specific business rules.
10. Preserve the generated METS file, validation output, and package manifest as build artifacts.

Export must fail or warn explicitly when required files, identifiers, checksums, metadata records, or structural links are missing.

## Profiles

METS implementations are commonly governed by profiles or institutional conventions. An EDT METS profile may specify:

- METS major version and schema revision.
- Required package identifier policy.
- Required metadata vocabularies.
- Allowed embedded versus external metadata.
- File-group roles and naming rules.
- Logical and physical structural-map requirements.
- Checksum algorithms.
- MIME-type policy.
- Repository-specific extension elements.
- Validation schemas, Schematron rules, and business rules.
- Packaging convention such as BagIt or OCFL.
- Required PREMIS events and relationships.

Profiles should be versioned and preserved with the package so future validation is reproducible.

## Validation

EDT validation may include:

- Schema conformance.
- Missing package or file identifiers.
- Duplicate identifiers.
- Broken file pointers or metadata links.
- Missing files referenced by the METS document.
- Files present in the package but absent from the inventory.
- Checksum mismatches.
- Unsupported or undeclared checksum algorithms.
- Invalid MIME types.
- Empty or cyclic structural maps.
- Logical structures incorrectly derived from page order alone.
- Physical structures inconsistent with file sequence.
- Metadata sections with undeclared vocabularies.
- PREMIS, descriptive, or provenance records that fail their own validation.
- Violations of repository-specific profile rules.

Schema validity alone is not enough. A package can be valid XML while still being incomplete, internally inconsistent, or unusable by the target repository.

## Relationship to PREMIS

METS and PREMIS should be used together with a clear division of responsibility:

```text
METS describes package structure and binds files to metadata.
PREMIS describes preservation objects, events, agents, rights, and fixity history.
```

A PREMIS record may be embedded in or linked from a METS administrative metadata section. Identifiers should connect PREMIS objects to METS file entries and representations.

## Relationship to EDOM

METS may expose selected views of EDOM, but it should not become a second semantic source of truth.

Recommended boundary:

```text
EDOM owns semantic document structure.
METS owns repository package structure.
PREMIS owns preservation metadata.
W3C PROV owns general provenance interchange.
```

Any generated structural map should be reproducible from a declared EDOM version, profile, and publisher configuration.

## Migration Between METS Versions

METS 1 to METS 2 migration should be handled as a transformation with explicit provenance.

A migration process should record:

- Source and target schema versions.
- Transformation software and version.
- Mapping rules.
- Removed or approximated constructs.
- Identifier changes.
- Link conversion decisions.
- Validation results.
- Human review when local extensions are involved.

EDT must not claim lossless migration unless all source constructs and repository requirements were preserved and verified.

## References

- Library of Congress, *Metadata Encoding and Transmission Standard (METS) Official Web Site*: https://www.loc.gov/standards/mets/
- Library of Congress, *METS Version 2*: https://www.loc.gov/standards/mets/mets2.html
- Library of Congress, *METS Version 1 Schema and Documentation*: https://www.loc.gov/standards/mets/mets-schemadocs.html
