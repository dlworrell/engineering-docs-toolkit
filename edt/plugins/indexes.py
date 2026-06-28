from edt.indexes import generate_index_summary
from edt.plugin import Plugin, ProjectContext


class IndexSummaryPlugin(Plugin):
    name = "indexes"

    def run(self, context: ProjectContext) -> None:
        generate_index_summary(context.root)
