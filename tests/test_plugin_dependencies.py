from edt.plugin_dependencies import PluginDependencySet


def test_plugin_dependency_set_records_input():
    deps = PluginDependencySet(plugin_id="plugin-a")
    deps.add_input("node-a")
    result = deps.inputs
    assert "node-a" in result
