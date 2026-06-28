from .plugin import Plugin
from .plugins import GlossaryPlugin, IndexSummaryPlugin


def default_plugins() -> list[Plugin]:
    return [GlossaryPlugin(), IndexSummaryPlugin()]
