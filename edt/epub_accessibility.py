from dataclasses import dataclass, field


@dataclass
class EpubAccessibilityMetadata:
    summary: str = ""
    access_modes: list[str] = field(default_factory=list)
    features: list[str] = field(default_factory=list)
    hazards: list[str] = field(default_factory=list)

    def package_metadata(self) -> dict[str, list[str] | str]:
        return {
            "accessibilitySummary": self.summary,
            "accessMode": self.access_modes,
            "accessibilityFeature": self.features,
            "accessibilityHazard": self.hazards,
        }
