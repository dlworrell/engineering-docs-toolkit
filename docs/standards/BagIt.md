# BagIt

## Purpose

BagIt is a hierarchical file-packaging format for the reliable storage and transfer of arbitrary digital content.

For EDT, BagIt is a transport and deposit container for source files, generated publications, metadata, validation reports, and provenance artifacts. It does not define the semantics of the files it carries.

## Current Standard

EDT targets **BagIt 1.0**, published as RFC 8493 in October 2018.

RFC 8493 is an Informational RFC rather than an Internet Standards Track specification. EDT still adopts it because it provides a stable, widely implemented packaging convention.

## Adoption Decision

EDT classifies BagIt as **Adopt** for transfer packages and **Bridge** for repository deposit workflows.

## Core Structure

A bag contains:

- `bagit.txt`, declaring the BagIt version and tag-file encoding.
- `data/`, containing payload files.
- One or more payload manifests such as `manifest-sha512.txt`.

Optional tag files may include:

- `bag-info.txt`.
- Tag manifests.
- `fetch.txt`.
- Project-specific metadata and reports.

## Architectural Boundary

```text
EDOM owns document semantics.
BagIt packages opaque files for transfer and verification.
Manifests prove fixity, not meaning or authenticity.
```

## EDT Package Policy

An EDT BagIt profile should declare:

- Required checksum algorithms.
- Payload-directory layout.
- Required tag files.
- Metadata field vocabulary.
- Whether remote payload retrieval through `fetch.txt` is permitted.
- File-name normalization rules.
- Size, path, and security limits.

SHA-256 or SHA-512 should be preferred over legacy digest algorithms for new packages.

## Validation

EDT validation may include:

- Missing declaration or payload directory.
- Missing, duplicate, or conflicting manifest entries.
- Checksum mismatch.
- Payload files absent from manifests.
- Manifest paths that escape the bag root.
- Unsupported encodings or algorithms.
- Unsafe or unauthorized `fetch.txt` URLs.
- Declared file sizes inconsistent with retrieved files.
- Tag files omitted from tag manifests where the profile requires them.

A complete bag contains every referenced payload file. A valid bag is complete and passes checksum verification.

## Security

BagIt fixity checks detect accidental change but do not establish who created a bag or whether malicious content is safe.

EDT should:

- Treat file paths and remote URLs as untrusted.
- Prevent directory traversal and link attacks.
- Limit network destinations, file sizes, and redirects.
- Scan payloads according to repository policy.
- Use signatures or trusted provenance separately when authenticity is required.

## Provenance

EDT should record the bag profile, creation tool, creation time, payload and tag-manifest digests, source project revision, and validation results.

## Design Rule

```text
Use BagIt to move and verify files.
Do not confuse fixity with authenticity.
Do not confuse packaging with semantic modeling.
```

## References

- RFC 8493, *The BagIt File Packaging Format (V1.0)*: https://www.rfc-editor.org/rfc/rfc8493.html
