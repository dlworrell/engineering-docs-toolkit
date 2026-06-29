from dataclasses import dataclass
import unicodedata


@dataclass(frozen=True)
class UnicodeRange:
    name: str
    start: int
    end: int

    def contains(self, char: str) -> bool:
        codepoint = ord(char)
        return self.start <= codepoint <= self.end


MATH_RANGES = [
    UnicodeRange("Greek and Coptic", 0x0370, 0x03FF),
    UnicodeRange("Letterlike Symbols", 0x2100, 0x214F),
    UnicodeRange("Number Forms", 0x2150, 0x218F),
    UnicodeRange("Arrows", 0x2190, 0x21FF),
    UnicodeRange("Mathematical Operators", 0x2200, 0x22FF),
    UnicodeRange("Miscellaneous Technical", 0x2300, 0x23FF),
    UnicodeRange("Geometric Shapes", 0x25A0, 0x25FF),
    UnicodeRange("Miscellaneous Mathematical Symbols-A", 0x27C0, 0x27EF),
    UnicodeRange("Supplemental Arrows-A", 0x27F0, 0x27FF),
    UnicodeRange("Supplemental Arrows-B", 0x2900, 0x297F),
    UnicodeRange("Miscellaneous Mathematical Symbols-B", 0x2980, 0x29FF),
    UnicodeRange("Supplemental Mathematical Operators", 0x2A00, 0x2AFF),
    UnicodeRange("Mathematical Alphanumeric Symbols", 0x1D400, 0x1D7FF),
]


ASCII_MATH_GLYPHS = set("+-=*/^_<>|~")


def math_range_for(char: str) -> str:
    for unicode_range in MATH_RANGES:
        if unicode_range.contains(char):
            return unicode_range.name
    return ""


def is_math_glyph(char: str) -> bool:
    return char in ASCII_MATH_GLYPHS or bool(math_range_for(char)) or unicodedata.category(char) == "Sm"


def contains_math_glyph(text: str) -> bool:
    return any(is_math_glyph(char) for char in text)
