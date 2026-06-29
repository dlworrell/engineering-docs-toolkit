from dataclasses import dataclass


@dataclass
class FigureAltText:
    figure_id: str
    alt_text: str
    long_description: str = ""
    confidence: float = 0.0

    @property
    def is_complete(self) -> bool:
        return bool(self.alt_text.strip())
