# WCAG

## Purpose

The Web Content Accessibility Guidelines (WCAG) define testable requirements for making web content more accessible to people with disabilities.

For EDT, WCAG is the baseline accessibility standard for HTML, EPUB content documents, web-based documentation, and interactive publication components.

## Current Standard

EDT targets **WCAG 2.2** for new publication profiles. Profiles must declare the conformance level—A, AA, or AAA—and the exact artifact scope evaluated.

## Adoption Decision

EDT classifies WCAG as **Adopt** for digital publication accessibility.

## Architectural Boundary

```text
EDOM owns semantic intent.
Publishers render accessible structures and behavior.
WCAG defines the accessibility outcomes to validate.
```

WCAG does not replace format-specific requirements such as EPUB Accessibility, WAI-ARIA, PDF/UA, HTML conformance, or manual assistive-technology testing.

## Principles

WCAG requirements are organized under four principles:

- Perceivable.
- Operable.
- Understandable.
- Robust.

EDT profiles should map each applicable success criterion to generated structures, automated checks, manual checks, and retained evidence.

## Where EDT Uses WCAG

- HTML and EPUB publication profiles.
- Alternative-text requirements.
- Heading, landmark, list, and table semantics.
- Keyboard operation and focus behavior.
- Color contrast and non-color cues.
- Language identification.
- Captions, transcripts, and media alternatives.
- Error identification and form instructions.
- Reflow, zoom, orientation, spacing, and target-size checks.
- Accessibility quality reports and release gates.

## Validation Strategy

Automated validation can detect only part of WCAG. EDT should combine:

1. Static format validation.
2. Automated accessibility rules.
3. Keyboard and interaction testing.
4. Accessibility-tree inspection.
5. Screen-reader and magnification testing where required.
6. Human review of meaning, sequence, alternatives, and usability.

A passing automated scan is not a WCAG conformance claim.

## Conformance Claims

A conformance claim should record:

- WCAG version and level.
- Publication revision and artifact digest.
- Pages, resources, and embedded content included.
- Technologies relied upon.
- Validators and versions.
- Manual evaluator and date.
- Findings, waivers, and unresolved limitations.

Material publication changes require re-evaluation.

## Relationship to WAI-ARIA

WAI-ARIA supplies accessibility semantics where native host-language semantics are insufficient. WCAG defines broader outcomes, including keyboard access, focus, contrast, alternatives, error handling, and understandable behavior.

Correct ARIA can support WCAG conformance; invalid or unnecessary ARIA can cause failures.

## Relationship to EPUB and PDF

EPUB Accessibility builds on WCAG and adds publication-specific discoverability, navigation, and reporting requirements.

PDF accessibility is evaluated through PDF/UA and related guidance rather than by treating a fixed-layout PDF as an ordinary web page.

## Design Rule

```text
Build accessibility from semantics and behavior.
Use automation to find defects, not to manufacture conformance claims.
Preserve evidence for every released accessibility assertion.
```

## References

- W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*: https://www.w3.org/TR/WCAG22/
- W3C, *Understanding WCAG 2.2*: https://www.w3.org/WAI/WCAG22/Understanding/
