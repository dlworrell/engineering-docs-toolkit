# ORCID

## Purpose

ORCID provides unique, persistent identifiers for researchers and contributors. An ORCID iD helps distinguish people with similar names and connects individuals to contributions, affiliations, funding, peer review, and other research activities.

ORCID is an identity and interoperability service, not a document-authoring format.

## Where EDT Uses ORCID

- Contributor identification.
- Author and editor disambiguation.
- Scholarly metadata export.
- Crossref and publisher deposit workflows.
- JATS, TEI, and other structured publication formats.
- Researcher-authorized metadata synchronization.
- Validation of contributor identifiers.

## Where EDT Does Not Use ORCID

ORCID does not replace EDOM contributor metadata. EDOM remains responsible for names as supplied by the document, contributor roles, affiliations, provenance, ordering, and publication-specific attribution.

An ORCID record should not be treated as an infallible authority for every contributor fact. Imported data must preserve its source, visibility, access time, and assertion context.

## Mapping to EDOM

Representative ORCID concepts map approximately as follows:

| ORCID | EDOM |
| --- | --- |
| ORCID iD | Persistent contributor identifier |
| Person name | Structured contributor name |
| Other names | Name variants and aliases |
| Employment / education | Affiliation relationships |
| Works | Contribution relationships |
| Funding | Award and funder relationships |
| Peer review | Contributor activity relationship |
| Research resources | Resource relationship |
| Source assertion | Provenance for imported metadata |
| Visibility | Access and disclosure metadata |

EDOM should preserve the contributor name and role supplied by the source document even when an ORCID record contains different or newer information.

## Collection Strategy

When EDT participates in an interactive authoring, submission, or publication workflow, ORCID iDs should be collected through an authenticated ORCID authorization flow rather than by asking users to type identifiers manually.

A successful authenticated collection should record:

- The normalized ORCID iD.
- That the identifier was authenticated.
- The authorization event and time.
- The integration or client involved.
- The permissions granted.
- The name returned by ORCID when available.
- Relevant provenance without exposing secrets or access tokens.

Access tokens and other credentials must never be stored inside EDOM documents or committed to source repositories.

## Unauthenticated Identifiers

Some imported documents, legacy databases, or curated archives will contain ORCID iDs that were not collected through an authenticated workflow.

EDT should preserve these identifiers, but mark their authentication status explicitly. It should not imply that an unauthenticated identifier was confirmed by the record holder.

Validation may check that:

- The identifier has valid ORCID syntax and checksum.
- The identifier resolves in the ORCID Registry when network validation is enabled.
- The record metadata is plausibly compatible with the local contributor data.
- Obvious conflicts are reported for review.

Name matching alone must not be used to silently assign an ORCID iD.

## Normalization

EDT should normalize ORCID iDs to the full HTTPS URI form:

```text
https://orcid.org/0000-0000-0000-0000
```

Display formatting should follow ORCID's current brand and display guidance. Internal comparison may use a canonical normalized value, but exported metadata should preserve the standard URI form where the destination format permits it.

## Import Strategy

An ORCID-aware importer should preserve:

- The identifier exactly as encountered.
- Its normalized form.
- Whether authentication is known, unknown, or explicitly unauthenticated.
- The source element, field, or metadata record.
- Any associated contributor name and role.
- Retrieval or assertion provenance.

Conflicting identifiers attached to the same contributor should be reported rather than automatically merged.

## Export Strategy

ORCID iDs should be exported with contributor metadata when supported by the target format or registration system, including JATS, Crossref, Schema.org, and other scholarly metadata outputs.

Exporters should distinguish authenticated and unauthenticated identifiers when the target schema supports that distinction. They should never fabricate an authentication claim.

## Synchronization

Where an authorized ORCID integration is available, EDT may read or write permitted metadata through the ORCID APIs.

Synchronization must be deliberate and provenance-preserving:

1. Identify the local EDOM assertion and its source.
2. Retrieve the current ORCID record under the granted permissions.
3. Compare rather than blindly overwrite.
4. Present conflicts for policy-based or human resolution.
5. Record what was read or written, when, and by which integration.
6. Respect visibility settings and the researcher's control of their record.

## Validation

EDT validation may include:

- Syntax and checksum validation.
- Duplicate ORCID iDs assigned to different local contributors.
- Multiple ORCID iDs assigned to one contributor.
- Missing authentication-status metadata.
- Contributor-name or affiliation conflicts requiring review.
- Required ORCID iDs under a publication profile.
- Resolution or API failures when online checks are enabled.
- Export formats that cannot preserve the identifier.

A valid checksum proves only that the identifier is structurally valid; it does not prove that the identifier belongs to the named contributor.

## Profiles

An EDT ORCID profile may specify:

- Whether ORCID iDs are required, recommended, or optional.
- Which contributor roles require them.
- Whether authenticated collection is mandatory.
- Whether online resolution is performed.
- Conflict-handling policy.
- Display requirements.
- Export destinations and synchronization permissions.

## Design Notes

ORCID gives EDT a standards-based way to identify contributors without relying on names alone. EDT should preserve ORCID's trust model by distinguishing authenticated identifiers from imported or curated identifiers and by respecting researcher control.

The architectural boundary is:

```text
EDOM owns contributor semantics, roles, and provenance.
ORCID provides persistent person identifiers and authorized connections.
```

## References

- ORCID, *About ORCID*: https://info.orcid.org/what-is-orcid/
- ORCID, *Collecting and sharing ORCID iDs*: https://info.orcid.org/documentation/collecting-and-sharing-orcid-ids/
- ORCID, *Integration Guide*: https://info.orcid.org/documentation/integration-guide/
