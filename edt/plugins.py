from .plugin import Plugin, ProjectContext


class GlossaryPlugin(Plugin):
    name = "glossary"

    def run(self, context: ProjectContext) -> None:
        glossary_dir = context.root / "reference" / "glossary"
        if not glossary_dir.exists():
            return None
        summary = context.output / "glossary-summary.txt"
        entries = sorted(path.name for path in glossary_dir.iterdir() if path.is_file())
        summary.write_text("\n".join(entries) + ("\n" if entries else ""), encoding="utf-8")
        return None


class IndexSummaryPlugin(Plugin):
    name = "index-summary"

    def run(self, context: ProjectContext) -> None:
        indexes_dir = context.root / "reference" / "indexes"
        if not indexes_dir.exists():
            return None
        summary = context.output / "index-summary.txt"
        entries = sorted(path.name for path in indexes_dir.iterdir() if path.is_file())
        summary.write_text("\n".join(entries) + ("\n" if entries else ""), encoding="utf-8")
        return None
