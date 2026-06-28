from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProjectContext:
    root: Path
    output: Path


class Plugin:
    name = "plugin"

    def run(self, context: ProjectContext) -> None:
        return None
