from dataclasses import dataclass, field


@dataclass
class PluginDependencySet:
    plugin_id: str
    inputs: set[str] = field(default_factory=set)

    def add_input(self, input_id: str) -> None:
        self.inputs.add(input_id)
