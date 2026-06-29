from .accessibility_aria import AriaAnnotation
from .semantic_blocks import SemanticBlock


def equation_aria_label(block: SemanticBlock) -> str:
    number = block.metadata.get("equation_number", "")
    return f"Equation {number}: {block.text}" if number else f"Equation: {block.text}"


def equation_aria(block: SemanticBlock) -> AriaAnnotation:
    return AriaAnnotation(role="math", label=equation_aria_label(block))
