# WAI-ARIA

## Purpose

WAI-ARIA (Accessible Rich Internet Applications) defines roles, states, and properties that expose user-interface and document semantics to assistive technologies through accessibility APIs.

For EDT, WAI-ARIA is the accessibility-semantics layer for generated HTML, EPUB content documents, SVG-based interfaces, and other host languages that support ARIA. It supplements native host-language semantics when those semantics are insufficient.

## Current Standard

The stable production target is **WAI-ARIA 1.2**, published as a W3C Recommendation on 6 June 2023.

**WAI-ARIA 1.3** is under active development. The 4 June 2026 publication is a Working Draft and must be treated as work in progress.

EDT therefore:

- Adopts WAI-ARIA 1.2 for production output.
- Evaluates WAI-ARIA 1.3 in experimental profiles only.
- Requires profiles to declare the ARIA version and host language.
- Rejects draft-only roles or properties in a WAI-ARIA 1.2 target.

## Adoption Decision

EDT classifies WAI-ARIA as **Adopt** for web accessibility semantics and **Bridge** for accessibility API interoperability.

Rationale:

- It is the W3C standard for exposing roles, states, and properties to assistive technologies.
- It complements HTML and SVG semantics.
- It enables accessible representation of custom widgets and structures.
- It provides a validation target for semantic publishers.
- It must remain subordinate to correct native host-language semantics.

## First Rule of ARIA

Native host-language semantics should be used whenever they provide the required meaning and behavior.

For example:

- Use an HTML `button` instead of a generic element with `role="button"`.
- Use native headings instead of recreating heading semantics with ARIA.
- Use native form controls where they meet the requirement.
- Use table elements for data tables rather than reconstructing table semantics manually.

ARIA should refine or supply missing semantics. It should not conceal poor host-language structure.

## Where EDT Uses WAI-ARIA

- HTML publication output.
- EPUB content documents.
- Interactive examples and widgets.
- Navigation landmarks.
- Live regions and status messages.
- Accessible names and descriptions.
- Expanded, selected, checked, pressed, and disabled state.
- Relationships among controls, labels, descriptions, and owned content.
- SVG or custom controls that lack sufficient native semantics.
- Accessibility validation and regression testing.

## Where EDT Does Not Use WAI-ARIA

WAI-ARIA does not replace:

- EDOM semantic structure.
- Native HTML or SVG semantics.
- Keyboard behavior.
- Focus management.
- Visual contrast and layout accessibility.
- Alternative text authoring.
- Captions, transcripts, or audio description.
- WCAG conformance.
- PDF tagging or PDF/UA.
- EPUB Accessibility conformance.

The architectural boundary is:

```text
EDOM owns semantic intent.
The host language owns native structure and behavior.
WAI-ARIA supplements missing accessibility semantics.
Assistive technologies consume the resulting accessibility tree.
```

## Mapping from EDOM

Representative mappings include:

| EDOM concept | Preferred output |
| --- | --- |
| Heading | Native heading element |
| Navigation region | Native `nav`, optionally named with ARIA |
| Main content | Native `main` |
| Complementary content | Native `aside` where appropriate |
| Button action | Native `button` |
| Data table | Native table structure |
| Figure | Native `figure` and `figcaption` |
| Status message | Suitable live-region or status semantics |
| Custom tree widget | Host structure plus ARIA tree roles and states |
| Custom tab interface | Host structure plus ARIA tab pattern |
| Dialog | Native dialog support where available, otherwise a validated ARIA pattern |
| Expandable control | Native disclosure pattern or `aria-expanded` with a valid control relationship |

The publisher should select the strongest native representation before adding ARIA.

## Roles

ARIA roles identify the type or purpose of an accessible object.

Role categories include:

- Widget roles.
- Document-structure roles.
- Landmark roles.
- Live-region roles.
- Window roles.
- Composite-widget roles.
- Abstract roles used by the specification rather than authors.

EDT must validate:

- Whether a role is allowed on the selected host element.
- Whether the role conflicts with native semantics.
- Whether required child or context roles are present.
- Whether prohibited states or properties are used.
- Whether the role may receive an accessible name.
- Whether the role requires keyboard and focus behavior.

Abstract roles must never be emitted as author-facing roles.

## States and Properties

ARIA states and properties describe accessibility-relevant conditions and relationships.

Examples include:

- `aria-expanded`.
- `aria-selected`.
- `aria-checked`.
- `aria-pressed`.
- `aria-disabled`.
- `aria-current`.
- `aria-live`.
- `aria-controls`.
- `aria-describedby`.
- `aria-labelledby`.
- `aria-owns`.

EDT should emit only values supported by the selected role and ARIA version. Dynamic values must remain synchronized with visible state and application behavior.

## Accessible Names and Descriptions

Interactive controls, landmarks, and other named objects require meaningful accessible names where the role permits or requires them.

EDT should prefer naming sources in this order when appropriate:

1. Native visible labels.
2. Native host-language associations.
3. `aria-labelledby` referencing visible text.
4. `aria-label` when no suitable visible label exists.

Descriptions should add useful information rather than repeat the name.

The publisher must validate:

- Broken ID references.
- Empty names.
- Duplicate or ambiguous names within a context.
- Names hidden from the accessibility tree.
- Roles that prohibit naming.
- Descriptions that contain essential instructions not available visually.

Accessible-name computation depends on the host language and the W3C Accessible Name and Description Computation specification. EDT should test computed results rather than inspecting attributes alone.

## Landmarks

Landmarks support efficient navigation by assistive-technology users.

EDT publishers should generate landmarks from semantic structure, including main content, navigation, complementary content, search, banners, and content information where appropriate.

When multiple landmarks share the same role, each should receive a distinct accessible name when needed for disambiguation.

Landmarks must reflect meaningful page regions rather than wrapping every container in a role.

## Document Structure

ARIA includes document-structure roles, but native HTML elements should normally express headings, paragraphs, lists, tables, figures, and sections.

EDT may use ARIA document roles when:

- The host language lacks an equivalent.
- A custom rendering layer obscures native semantics.
- A specialized interactive structure requires additional meaning.

The publisher must not use ARIA to repair ordering or hierarchy problems that originate in EDOM or malformed host markup.

## Interactive Patterns

A role declaration alone does not create an accessible widget.

Custom widgets must implement:

- Keyboard interaction.
- Focus movement.
- State synchronization.
- Accessible naming.
- Required parent-child relationships.
- Expected events and announcements.
- Pointer and touch behavior.
- Disabled and error states.

EDT should maintain tested publisher components for supported patterns rather than emitting arbitrary role combinations.

## Focus Management

EDT validation should detect:

- Interactive elements that cannot receive focus.
- Non-interactive elements added unnecessarily to the tab order.
- Positive `tabindex` values unless explicitly allowed by profile.
- Composite widgets without a valid focus-management strategy.
- Focus trapped unintentionally.
- Dialogs that fail to restore focus.
- Hidden or disabled content that remains keyboard reachable.
- `aria-activedescendant` relationships that do not resolve.

Focus behavior requires runtime testing; static markup checks are not sufficient.

## Relationships and Ownership

ARIA relationship attributes use ID references to connect accessible objects.

EDT should validate that referenced IDs:

- Exist.
- Are unique.
- Resolve within the correct document context.
- Refer to valid target objects.
- Do not create ownership cycles.
- Do not contradict native structure.

`aria-owns` changes the accessibility-tree relationship and should be used sparingly. Native DOM ownership is preferable whenever practical.

## Hidden Content

`aria-hidden="true"` removes content from the accessibility tree but does not visually hide it and does not necessarily prevent keyboard focus.

EDT must reject configurations where:

- Focusable descendants remain reachable inside hidden content.
- Essential visible text is hidden from assistive technologies.
- The document root is hidden.
- A control's accessible name depends entirely on content made unavailable by the selected profile.

Visual hiding, DOM removal, inertness, and accessibility-tree exclusion are different mechanisms and must not be treated as interchangeable.

## Live Regions

Live regions communicate dynamic updates without moving focus.

EDT profiles should define:

- Which updates require announcement.
- Politeness level.
- Atomicity.
- Relevant change types.
- Duplicate-announcement suppression.
- Error and status-message behavior.

Live regions should not be used for routine visual changes that do not require interruption or notification.

## Host-Language Semantics

ARIA output must be validated together with the host language.

A role or property may be valid in the ARIA vocabulary but invalid or conflicting on a particular HTML or SVG element. Publisher validation should therefore include:

- Host-language conformance.
- ARIA conformance.
- HTML Accessibility API Mappings behavior where relevant.
- Browser accessibility-tree inspection.
- Assistive-technology testing for supported profiles.

## Import Strategy

When importing HTML, EPUB content, or SVG containing ARIA, EDT should preserve:

- Explicit roles.
- States and properties.
- ID-reference relationships.
- Host-language element semantics.
- Accessible-name sources.
- Language and direction.
- Source locations and provenance.

The importer should distinguish:

- Native semantics.
- Explicit ARIA overrides.
- Invalid or conflicting ARIA.
- Computed semantic meaning.

Invalid ARIA should not silently become authoritative EDOM semantics.

## Export Strategy

A WAI-ARIA-aware publisher should:

1. Select a declared host-language and ARIA profile.
2. Render correct native semantics first.
3. Add ARIA only where it supplies required missing semantics.
4. Generate stable and unique ID references.
5. Emit required roles, states, and properties.
6. Implement keyboard and focus behavior for interactive patterns.
7. Validate static markup.
8. Inspect the generated accessibility tree.
9. Run automated and manual interaction tests.
10. Preserve validation and test results as build artifacts.

## Validation

EDT validation may include:

- Unknown roles, states, or properties.
- Draft-only ARIA features in a stable profile.
- Abstract roles used in content.
- Roles invalid for the host element.
- Conflicts with native semantics.
- Missing required states or owned elements.
- Prohibited states or properties.
- Invalid values.
- Broken ID references.
- Missing accessible names.
- Names applied to roles that prohibit naming.
- Duplicate landmark names.
- Focusable content hidden from the accessibility tree.
- Interactive roles without keyboard behavior.
- Composite widgets with invalid focus management.
- State values inconsistent with visible or application state.

Static conformance is necessary but not sufficient. Interactive output requires runtime and assistive-technology testing.

## Relationship to WCAG

WAI-ARIA is a technical mechanism, not an accessibility-conformance standard by itself.

Correct ARIA can help satisfy WCAG requirements for name, role, value, relationships, status messages, and keyboard access. Incorrect ARIA can make otherwise usable content inaccessible.

EDT accessibility profiles should identify the WCAG version and conformance target independently from the ARIA version.

## Relationship to EPUB

EPUB content documents use HTML and may use ARIA under EPUB and host-language constraints.

EDT should generate native EPUB semantics first, then add valid ARIA where needed. ARIA validation must be part of the broader EPUB Accessibility workflow, not a substitute for it.

## Relationship to SVG

SVG can expose graphics and interactive controls to accessibility APIs. EDT should use native SVG accessibility features and ARIA together according to the selected SVG and ARIA profiles.

Complex diagrams may also require structured descriptions, alternative representations, data tables, or long descriptions beyond role and name metadata.

## WAI-ARIA 1.3 Readiness

WAI-ARIA 1.3 is a Working Draft as of 4 June 2026. Experimental profiles may evaluate its additions, but production output should remain on WAI-ARIA 1.2 until the profile explicitly changes.

Any experimental profile should:

- Pin the dated draft.
- Identify draft-only roles and properties.
- Test browser and assistive-technology support.
- Provide fallback behavior.
- Prevent draft features from leaking into stable builds.

## Profiles

An EDT WAI-ARIA profile may specify:

- ARIA version.
- Host language and version.
- Allowed roles and properties.
- Supported interactive patterns.
- Native-semantics preference rules.
- Landmark policy.
- Accessible-name policy.
- Keyboard and focus requirements.
- Automated validation tools.
- Browser and assistive-technology test matrix.
- Draft-feature policy.

## Provenance

Accessibility validation should record:

- Publisher and version.
- ARIA and host-language profiles.
- Generated artifact hash.
- Validation tools and versions.
- Accessibility-tree snapshots where practical.
- Browser and platform.
- Assistive technology and version.
- Test results and human review.
- Waivers and unresolved findings.

## Design Rule

```text
Use native semantics first.
Add ARIA only to express missing accessibility semantics.
Validate the computed accessibility tree, not just the markup.
Test behavior as well as structure.
```

## References

- W3C, *Accessible Rich Internet Applications (WAI-ARIA) 1.2*: https://www.w3.org/TR/wai-aria-1.2/
- W3C, *Accessible Rich Internet Applications (WAI-ARIA) 1.3*, Working Draft: https://www.w3.org/TR/wai-aria-1.3/
- W3C, *Core Accessibility API Mappings*: https://www.w3.org/TR/core-aam-1.2/
- W3C, *Accessible Name and Description Computation*: https://www.w3.org/TR/accname-1.2/
