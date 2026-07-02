# TMX

TMX is an XML interchange format used by localization tools to exchange bilingual segment records.

EDT treats TMX 1.4b as a compatibility format. EDOM remains the canonical semantic document model, while XLIFF remains the preferred active localization-job format.

Importers and exporters must preserve language identifiers, segment structure, inline markers, tool metadata, stable identifiers where available, and processing provenance. They must report omitted, flattened, duplicated, stale, or unsupported data.

Schema validity does not prove round-trip compatibility with a receiving tool. EDT profiles must declare the TMX version, segmentation policy, supported inline subset, language policy, and tested toolchain.
