from dataclasses import dataclass, field


@dataclass
class AriaAnnotation:
    role: str
    label: str = ""
    described_by: str = ""
    properties: dict[str, str] = field(default_factory=dict)


def aria_attributes(annotation: AriaAnnotation) -> dict[str, str]:
    attrs = {"role": annotation.role}
    if annotation.label:
        attrs["aria-label"] = annotation.label
    if annotation.described_by:
        attrs["aria-describedby"] = annotation.described_by
    attrs.update(annotation.properties)
    return attrs
