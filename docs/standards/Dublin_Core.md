# Dublin Core

## Purpose

Dublin Core is a widely adopted metadata standard for describing digital resources. It provides a small, interoperable vocabulary for identifying, discovering, organizing, and preserving documents.

## Where EDT Uses Dublin Core

- Document metadata.
- Publication metadata.
- Archive packages.
- Repository interoperability.
- Search and discovery.
- Export to standards-based publishing targets.

## Where EDT Does Not Use Dublin Core

Dublin Core describes documents but does not model their internal semantic structure. EDOM remains responsible for document hierarchy, semantic objects, references, validation, and provenance.

## Mapping to EDOM

EDOM document metadata maps naturally to Dublin Core fields such as:

| Dublin Core | EDOM |
| --- | --- |
| title | Document title |
| creator | Author(s) |
| subject | Keywords or taxonomy |
| description | Abstract or summary |
| publisher | Publication metadata |
| date | Creation/publication dates |
| language | Document language |
| identifier | Stable document identifier |
| rights | Licensing metadata |

## Design Notes

EDT adopts Dublin Core as a metadata interchange standard rather than an internal document model. The goal is to maximize interoperability with repositories, digital libraries, and publishing systems while preserving the richer semantic information available within EDOM.