# EPUB Accessibility

## Purpose

EPUB Accessibility defines conformance and discoverability requirements for accessible EPUB publications.

For EDT, it governs how EPUB output is evaluated, described, certified, and distributed so readers can determine whether a publication meets their accessibility needs.

## Current Standard

The current W3C Recommendation is **EPUB Accessibility 1.1**, published on 17 October 2024. It is accompanied by **EPUB Accessibility Techniques 1.1**.

EDT profiles should declare the EPUB Accessibility version, EPUB version, WCAG target, metadata policy, certification policy, and validation procedure.

## Adoption Decision

EDT classifies EPUB Accessibility 1.1 as **Adopt** for accessible EPUB publication and **Bridge** for retailer, library, certification, and reading-system ecosystems.

## Architectural Boundary

```text
EDOM owns semantic intent and source provenance.
The EPUB publisher renders accessible structures.
EPUB Accessibility defines conformance, discoverability, and reporting requirements.
```

## Core Requirements

EDT should support and validate:

- Accessibility metadata.
- WCAG conformance claims.
- Publication-wide navigation.
- Page navigation when source pagination is represented.
- Correct reading order.
- Alternative text and descriptions.
- Accessible tables and mathematics.
- Language and direction metadata.
- Keyboard-accessible interactive content.
- Captions, transcripts, and media alternatives.
- Complete and ordered media overlays.
- Certification metadata and evaluator reports.

## Discoverability

Accessibility metadata must describe the generated publication accurately. It may include access modes, sufficient access modes, accessibility features, hazards, summaries, conformance claims, certifier identity, credentials, and report links.

Metadata must not be copied from a template without verification.

## Page Navigation

Where an EPUB represents pages from another source, EDT should generate stable page-break markers, a page-list navigation structure, and pagination-source metadata where required.

Pages remain provenance, not semantic structure. A paragraph or theorem must not be split semantically merely because it crosses a page boundary.

## Native Semantics

Publishers should prefer native HTML and SVG semantics for headings, lists, tables, figures, notes, links, language, and navigation.

WAI-ARIA should supplement native semantics only when required.

## Certification

A conformance claim should record the certifier, credentials, report, evaluation date, conformance target, and exact publication revision evaluated.

Material changes to content, navigation, scripting, media, or packaging require re-evaluation.

## Import Strategy

When importing an EPUB, EDT should preserve package accessibility metadata, conformance claims, navigation, page lists, landmarks, alternative text, language, media overlays, and source provenance.

Imported claims are assertions to verify, not automatic proof of conformance.

## Export Strategy

An accessible EPUB publisher should:

1. Select a declared EPUB and accessibility profile.
2. Publish validated EDOM semantics using native structures.
3. Generate navigation, landmarks, and page lists.
4. Preserve language, direction, alternatives, and descriptions.
5. Generate accurate accessibility metadata.
6. Run EPUB, HTML, ARIA, and accessibility checks.
7. Perform required manual evaluation.
8. Preserve reports, tool versions, and artifact hashes.

## Validation

EDT validation may include:

- Missing or inaccurate accessibility metadata.
- Broken navigation or page-list targets.
- Incorrect reading order.
- Missing headings or landmarks.
- Images without required alternatives.
- Table-header failures.
- Language or direction errors.
- Invalid ARIA.
- Inaccessible scripted controls.
- Media without required alternatives.
- Incomplete media overlays.
- Certification attached to the wrong publication revision.

Automated validation alone does not establish conformance.

## Design Rule

```text
Build accessibility from semantics, not repair markup.
Describe accessibility honestly.
Preserve evidence for every conformance claim.
```

## References

- W3C, *EPUB Accessibility 1.1*: https://www.w3.org/TR/epub-a11y-11/
- W3C, *EPUB Accessibility Techniques 1.1*: https://www.w3.org/TR/epub-a11y-tech-11/
- W3C, *EPUB 3.3*: https://www.w3.org/TR/epub-33/
