from pathlib import Path

from edt.glossary import generate_glossary
from edt.plugin import Plugin, ProjectContext


class GlossaryPlugin(Plugin):
    name = "glossary"

    def run(self, context: ProjectContext) -> None:
        generate_glossary(context.root)
