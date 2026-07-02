# IIIF

## Purpose

The International Image Interoperability Framework (IIIF) defines interoperable APIs for delivering images, presenting compound digital objects, and exchanging annotations and related services.

For EDT, IIIF is a publication and interoperability layer for scanned documents, page images, manuscripts, photographs, maps, audiovisual resources, and other compound objects.

## Current Standards

EDT targets:

- **IIIF Presentation API 3.0.0**.
- **IIIF Image API 3.0.0**.

Profiles may also declare compatible versions of the IIIF Content Search, Authentication, and Change Discovery APIs where required.

## Adoption Decision

EDT classifies IIIF as **Adopt** for image and compound-object delivery and **Bridge** for libraries, archives, museums, repositories, and annotation systems.

## Architectural Boundary

```text
EDOM owns semantic document structure and provenance.
IIIF Canvases represent presentation surfaces or time extents.
IIIF services deliver images and related content.
Annotations connect content to regions, time spans, and semantic resources.
```

A IIIF Canvas is a presentation surface, not automatically an EDOM page or semantic node.

## Presentation API

The Presentation API describes compound objects through resources such as:

- Collections.
- Manifests.
- Canvases.
- Ranges.
- Annotation Pages.
- Annotations.
- Content resources.

EDT should map logical sequences, page-image evidence, media, structures, labels, metadata, and annotations without allowing presentation order to replace semantic document hierarchy.

## Image API

The Image API provides standardized requests for image regions, sizes, rotations, qualities, and formats.

EDT profiles should declare:

- Image API compliance level.
- Supported formats and qualities.
- Maximum dimensions and request limits.
- Rights and authentication policy.
- Canonical service identifiers.
- Color and derivative-generation policy.

Requested derivatives remain linked to the underlying source image and its provenance.

## Mapping to EDT

Representative mappings include:

| IIIF concept | EDT meaning |
| --- | --- |
| Collection | Group of related publications or objects |
| Manifest | Presentation description for one compound object |
| Canvas | Ordered presentation surface or time extent |
| Range | Structural navigation grouping |
| Annotation Page | Ordered set of annotations |
| Annotation | Relationship between target and body |
| Image service | Derivative-delivery endpoint |
| `seeAlso` | Related machine-readable resource |
| `rendering` | Downloadable alternative representation |
| `partOf` | Membership relationship |

EDT page-region provenance may target a Canvas fragment while the corresponding EDOM node spans several Canvases.

## Labels and Metadata

IIIF labels and metadata values are intended primarily for human presentation. EDT should preserve language maps and should link to richer machine-readable metadata through identified resources.

A display metadata entry must not replace authoritative EDOM, Dublin Core, DataCite, or repository metadata.

## Structural Navigation

Ranges may represent chapters, sections, articles, scenes, or other navigation structures.

EDT should generate Ranges from validated semantic structure and should validate ordering, nesting, Canvas references, and stable identifiers.

## Annotations

IIIF uses the Web Annotation model for painting content onto Canvases and for supplemental annotations such as transcription, commentary, tagging, and links.

EDT should preserve:

- Annotation motivation.
- Body and target identifiers.
- Spatial or temporal selectors.
- Language and format.
- Creator and creation time where available.
- Provenance and confidence.

Annotations must not silently overwrite canonical EDOM content.

## Import Strategy

A IIIF importer should:

1. Pin the API and JSON-LD context versions.
2. Preserve identifiers, types, language maps, structures, services, and annotations.
3. Resolve relative and linked resources under controlled network policy.
4. Map Canvases and fragments into source-region provenance.
5. Map recognized structures into EDOM and the reference graph.
6. Preserve unknown extensions.
7. Record retrieval times, response digests, warnings, and mapping decisions.

## Export Strategy

A IIIF publisher should:

1. Select declared IIIF API versions and a publication profile.
2. Generate stable Manifest, Canvas, Range, Annotation, and service identifiers.
3. Map source images, media, structures, and annotations from validated EDT data.
4. Emit language maps and rights metadata.
5. Link richer metadata and downloadable representations.
6. Validate JSON-LD, required properties, references, and service declarations.
7. Test representative viewers and clients.
8. Preserve generated resources and validation evidence.

## Validation

EDT validation may include:

- Invalid or duplicate identifiers.
- Missing required types or properties.
- Broken Canvas, Range, Annotation, or service references.
- Invalid language maps.
- Presentation order inconsistent with the declared profile.
- Image services that advertise unsupported behavior.
- Region or time selectors outside the target extent.
- Rights or authentication metadata inconsistent with service behavior.
- Extension contexts that cannot be resolved reproducibly.
- Manifest structures inconsistent with EDOM navigation.

JSON syntax validity alone does not prove IIIF interoperability.

## Accessibility

IIIF publications should provide meaningful labels, summaries, language metadata, transcriptions, captions, alternative representations, and navigation structures where applicable.

Image delivery alone does not make scanned content accessible. EDT should connect OCR, transcription, semantic text, and descriptions to the presented resources.

## Profiles

An EDT IIIF profile may specify:

- Presentation and Image API versions.
- Additional IIIF APIs.
- Identifier policy.
- Canvas and Range mapping rules.
- Image-service compliance level.
- Annotation motivations and selectors.
- Rights and authentication policy.
- Accessibility requirements.
- Viewer and client test matrix.

## Provenance

EDT should record source-image digests, derivative-generation parameters, API versions, identifiers, publisher version, JSON-LD contexts, validation results, and viewer interoperability tests.

## Design Rule

```text
Use IIIF to present and deliver compound digital objects.
Keep semantic hierarchy in EDOM.
Treat Canvases as presentation surfaces and provenance targets.
Preserve stable identifiers and reproducible service behavior.
```

## References

- IIIF Presentation API 3.0: https://iiif.io/api/presentation/3.0/
- IIIF Image API 3.0: https://iiif.io/api/image/3.0/
- IIIF API and Documentation Index: https://iiif.io/api/
