import re

from .mathml import display_mathml, inline_mathml

DISPLAY = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
INLINE = re.compile(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)")


def replace_math(text: str) -> str:
    text = DISPLAY.sub(lambda m: display_mathml(m.group(1).strip()), text)
    text = INLINE.sub(lambda m: inline_mathml(m.group(1).strip()), text)
    return text
