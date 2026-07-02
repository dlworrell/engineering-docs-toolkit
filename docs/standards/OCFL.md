# Oxford Common File Layout

## Purpose

The Oxford Common File Layout (OCFL) defines an application-independent method for storing versioned digital objects in a transparent filesystem hierarchy.

For EDT, OCFL is a preservation-storage layout for source packages, normalized EDOM, publications, metadata, validation reports, and provenance artifacts across object versions.

## Current Standard

EDT targets **OCFL 1.1**.

## Adoption Decision

EDT classifies OCFL as **Adopt** for preservation repositories and **Bridge** for institutional storage systems.

## Architectural Boundary

```text
EDOM owns semantic document state.
OCFL stores versioned object files and inventories.
Repository policy owns retention, replication, and custody.
```

OCFL preserves filesystem objects and version history; it does not define document semantics or editorial workflow.

## Core Model

An OCFL repository contains versioned objects. Each object has:

- A stable object identifier.
- An inventory describing content state and versions.
- Fixity digests.
- Version directories.
- A logical-state mapping from content paths to stored files.
- Optional extensions governed by repository policy.

Content-addressed deduplication may allow unchanged files to be referenced across versions without unnecessary duplication.

## EDT Object Policy

An EDT OCFL object may preserve:

- Original source files.
- Normalized EDOM snapshots.
- Imported assets.
- Build configuration.
- Published PDF, EPUB, HTML, or office documents.
- Quality and validation reports.
- Reference-graph exports.
- Provenance records.
- Release manifests and signatures.

Profiles should distinguish authoritative files from reproducible derivatives.

## Versioning

Each meaningful deposited state should receive a new OCFL version. EDT should record the project revision, build identifier, actor, time, and reason for change.

OCFL version labels must not be confused with semantic document edition numbers or software versions. Those remain explicit metadata.

## Validation

EDT validation may include:

- Missing or invalid repository declarations.
- Invalid object or inventory structure.
- Inventory digest mismatch.
- Content state referencing missing files.
- Mutable content inside completed versions.
- Invalid version sequence.
- Duplicate or ambiguous object identifiers.
- Unsupported or undeclared extensions.
- Logical paths that violate project policy.

Repository conformance must be checked independently from EDOM and publication conformance.

## Fixity and Authenticity

OCFL inventories provide fixity evidence. They do not independently establish authenticity, authorization, or chain of custody.

EDT repositories may add signatures, W3C PROV records, audit logs, and external custody controls when stronger trust assertions are required.

## Relationship to BagIt

BagIt is suited to transfer and deposit packages. OCFL is suited to persistent versioned storage.

A common workflow is:

```text
EDT project or release
        ↓
BagIt transfer package
        ↓
Validated repository ingest
        ↓
OCFL preservation object
```

The BagIt package may be preserved intact or unpacked according to repository policy, but that decision must be recorded.

## Extensions

OCFL extensions must be declared, documented, versioned, and tested. Essential object semantics should not depend on a private extension that other conforming implementations cannot interpret.

## Provenance

EDT should record object identifiers, OCFL version identifiers, inventory digests, ingest and validation tools, source project revisions, extension declarations, and migration events.

## Design Rule

```text
Use OCFL for transparent, versioned preservation storage.
Keep semantic editions explicit in EDOM metadata.
Preserve fixity, provenance, and repository decisions separately.
```

## References

- OCFL 1.1 Specification: https://ocfl.io/1.1/spec/
- OCFL Extensions: https://ocfl.github.io/extensions/
