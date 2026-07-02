# Schema.org

## Purpose

Schema.org is a shared vocabulary for describing people, organizations, creative works, publications, datasets, events, products, places, and other entities in machine-readable web metadata.

For EDT, Schema.org is primarily a discovery and web-interoperability vocabulary. It helps published documents expose structured metadata to search engines, repositories, knowledge graphs, and downstream services.

## Current Standard

Schema.org evolves through published releases and a public development process. EDT should not assume that an undeclared live vocabulary is stable forever.

Each publication profile should record:

- The Schema.org release or vocabulary snapshot used.
- The selected types and properties.
- The serialization, normally JSON-LD for EDT web output.
- Any external vocabularies or profile constraints.
- The validation date and tooling used.

## Where EDT Uses Schema.org

- Structured metadata embedded in HTML publications.
- Description of books, articles, reports, datasets, software, media, and web pages.
- Contributor and organization metadata.
- Persistent identifiers and same-entity links.
- Accessibility metadata for creative works.
- Citation and relationship discovery.
- Search-engine and knowledge-graph interoperability.
- Static web snapshots and site-proof publication packages.

## Where EDT Does Not Use Schema.org

Schema.org is not EDT's canonical document model. It does not represent the complete internal hierarchy, source regions, validation state, detailed provenance, layout evidence, or every domain-specific semantic object required by EDOM.

Schema.org metadata is also not a substitute for target-specific standards such as JATS, TEI, Crossref, Dublin Core, W3C PROV, EPUB, or PDF/UA. EDT should use those standards when they provide the more precise interchange contract.

## Mapping to EDOM

Representative Schema.org concepts map approximately as follows:

| Schema.org | EDOM |
| --- | --- |
| `CreativeWork` | General document or publication entity |
| `Article` / `ScholarlyArticle` | Article document profile |
| `Book` | Book publication profile |
| `TechArticle` | Technical article or documentation profile |
| `Report` | Report document profile |
| `Dataset` | Dataset entity and related metadata |
| `SoftwareSourceCode` | Source-code resource |
| `WebPage` | Published web page |
| `Person` | Contributor or agent |
| `Organization` | Publisher, institution, or agent |
| `author` / `creator` | Contributor relationship |
| `contributor` | Secondary contributor relationship |
| `publisher` | Publisher relationship |
| `citation` | Citation or related-work edge |
| `isPartOf` / `hasPart` | Document composition relationship |
| `about` | Subject relationship |
| `identifier` | Persistent or local identifier |
| `sameAs` | External identity equivalence link |
| `dateCreated` / `dateModified` / `datePublished` | Declared lifecycle dates |
| `license` | Rights or license locator |
| `encoding` / `associatedMedia` | Published representation or media asset |
| `accessibilityFeature` | Accessibility capability metadata |
| `accessibilityHazard` | Accessibility hazard metadata |
| `accessibilitySummary` | Human-readable accessibility statement |

The mapping is intentionally selective. EDOM remains richer and may export only the subset appropriate to the selected Schema.org type and publication profile.

## JSON-LD Publication Strategy

JSON-LD is EDT's preferred Schema.org serialization for HTML publications because it separates structured metadata from presentation markup while retaining web compatibility.

A publisher should:

1. Select the most specific appropriate Schema.org type.
2. Generate metadata from validated EDOM fields.
3. Use stable identifiers and canonical URLs.
4. Connect contributors, organizations, publications, and parts as graph nodes rather than flattening all information into text.
5. Include only assertions supported by EDOM or declared external sources.
6. Preserve the generated JSON-LD as a publication artifact.
7. Record the vocabulary snapshot, publisher version, and validation result in provenance.

Example shape:

```json
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "@id": "https://example.org/manual/chapter-1",
  "headline": "System Architecture",
  "author": {
    "@type": "Person",
    "name": "Example Author",
    "identifier": "https://orcid.org/0000-0000-0000-0000"
  },
  "isPartOf": {
    "@type": "Book",
    "@id": "https://example.org/manual"
  }
}
```

This example is illustrative; project profiles determine required and permitted properties.

## Import Strategy

EDT may import Schema.org metadata from JSON-LD, RDFa, Microdata, or extracted web metadata when processing websites and static snapshots.

An importer should preserve:

- The original serialization.
- The source URL and retrieval time.
- The declared `@context`.
- Types, identifiers, and relationships.
- Literal values and language tags where available.
- The distinction between embedded assertions and EDT-verified facts.
- Extraction warnings and unsupported terms.

Imported metadata must not silently replace stronger project metadata or source-document assertions. Conflicts should be retained and reported for resolution.

## Static Web Snapshots

For future site-proof workflows, Schema.org metadata should be captured with the rendered HTML, linked assets, retrieval headers, timestamps, and content hashes.

The snapshot should distinguish:

- Metadata asserted by the source site.
- Metadata inferred by EDT.
- Metadata added by a project profile.
- Metadata verified against external registries.

That separation is necessary for evidentiary traceability and reproducible re-publication.

## Validation

EDT validation may include:

- Missing or inappropriate `@type` values.
- Missing stable identifiers or canonical URLs.
- Invalid property ranges.
- Contributor records lacking names or identifiers required by a profile.
- Broken `isPartOf`, `hasPart`, `citation`, or `sameAs` targets.
- Conflicting creation, modification, and publication dates.
- Accessibility metadata inconsistent with the generated publication.
- Claims not supported by EDOM provenance.
- Use of terms outside the declared vocabulary snapshot.
- Publication metadata that fails the selected external validator or consumer profile.

Schema.org vocabulary validity and search-engine product eligibility are separate concerns. A graph can be valid Schema.org without satisfying every rule imposed by a particular consumer.

## Profiles

An EDT Schema.org profile may specify:

- Required root type.
- Allowed nested types.
- Required and recommended properties.
- Identifier and canonical-URL policy.
- ORCID, DOI, ISBN, ISSN, or other identifier mappings.
- Accessibility metadata requirements.
- Citation and part-whole relationship policies.
- Whether inferred assertions are permitted.
- Validation tools and consumer-specific rules.
- The declared Schema.org release or snapshot.

## Provenance

Every generated or imported Schema.org assertion should be traceable to one of the following:

- An EDOM semantic field.
- A source-document region.
- Imported web metadata.
- A project-profile rule.
- An external registry lookup.
- A human editorial decision.

EDT should not publish unsupported structured claims merely to increase metadata coverage.

## Design Notes

Schema.org gives EDT a broad web-facing vocabulary for discovery and linked metadata. Its strength is reach and interoperability, not complete document semantics.

The architectural boundary is:

```text
EDOM owns the complete semantic document and its provenance.
Schema.org exposes a selected discovery graph for web consumers.
```

## References

- Schema.org documentation: https://schema.org/docs/documents.html
- Schema.org `CreativeWork`: https://schema.org/CreativeWork
- Schema.org `ScholarlyArticle`: https://schema.org/ScholarlyArticle
- Schema.org `Person`: https://schema.org/Person
- Schema.org vocabulary downloads: https://schema.org/docs/developers.html
