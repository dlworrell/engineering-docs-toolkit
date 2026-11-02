<!--
SPDX-FileCopyrightText: 2026 Donovan Worrell

SPDX-License-Identifier: Apache-2.0
Catalyst-File-ID: urn:uuid:2f970f28-a5f2-4976-a29a-c691b8d51d76
-->

# MathML Accessibility

Math textbook conversion must preserve mathematical structure, not only visual appearance.

The toolkit will support a math accessibility pipeline:

1. Extract text and math from source PDF pages.
2. Preserve reading order.
3. Convert formulas to MathML.
4. Preserve source LaTeX when available.
5. Add alt text for every math expression.
6. Export accessible HTML and EPUB.
7. Keep page references for review.

Early support stores LaTeX-like source in MathML `mtext` nodes as a safe placeholder. Later versions should replace this with semantic MathML conversion.
