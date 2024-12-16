import importlib

from zenplate.plugins.plugin_manager import PluginManager
from zenplate.plugins import (
    Plugin,
    plugin_wrapper,
    DataPlugin,
    JinjaTestPlugin,
    JinjaFilterPlugin,
)

from config_fixtures import fixtures


@plugin_wrapper("decorated_function", Plugin)
def decorated_function(unique_signature: str):
    return f"{unique_signature}"


@plugin_wrapper("data_plugin", DataPlugin)
def data_plugin(*args, **kwargs):
    return {"test": "test"}


@plugin_wrapper("jinja_test_plugin", JinjaTestPlugin)
def jinja_test_plugin(string: str):
    return string is not None and len(string) > 1


@plugin_wrapper("jinja_filter_plugin", JinjaFilterPlugin)
def jinja_filter_plugin(a_list: list):
    return ",".join(a_list)


def test_plugin_manager_find_plugins_by_module_name():
    plugin_manager = PluginManager(DataPlugin)
    plugins = plugin_manager.find_plugins_by_module_name(
        "zenplate_plugin_test.data_plugins"
    )
    assert "data" in plugins.keys()


def test_plugin_manager_find_matching_plugins():
    plugin_manager = PluginManager(DataPlugin)
    plugins = plugin_manager.find_matching_plugins()
    assert "data" in plugins.keys()


def test_plugin_manager_find_plugins_from_path():
    path_to_module = (
        fixtures / "plugin_module_for_matched_import" / "zenplate_plugin_test"
    )
    plugin_manager = PluginManager(DataPlugin)
    plugins = plugin_manager.find_plugins_from_path(str(path_to_module))
    assert "data" in plugins.keys()


def test_plugin_manager_find_plugins_from_module():
    plugin_manager = PluginManager(DataPlugin)
    module = importlib.import_module("zenplate_plugin_test.data_plugins")
    plugins = plugin_manager.find_plugins_from_module(module)
    assert "data" in plugins.keys()


def test_plugin_manager_specificity():
    plugin_manager = PluginManager(JinjaTestPlugin)
    module = importlib.import_module("zenplate_plugin_test.jinja_plugins")
    plugins = plugin_manager.find_plugins_from_module(module)
    assert "jinja_test" in plugins.keys()
    assert "jinja_filter" not in plugins.keys()


def test_multiple_plugin_managers():
    plugin_config = {
        "named_modules": [
            "zenplate_plugin_test.data_plugins",
            "zenplate_plugin_test.jinja_plugins",
        ],
    }
    data_plugin_manager = PluginManager(DataPlugin)
    data_plugin_manager.load_plugins(plugin_config)
    data_plugin_class = data_plugin_manager.plugins.get("data")
    data_plugin_result = data_plugin_class()

    assert data_plugin_result == "test"

    jinja_test_manager = PluginManager(JinjaTestPlugin)
    jinja_test_manager.load_plugins(plugin_config)
    jinja_test_plugin_class = jinja_test_manager.plugins.get("jinja_test")
    jinja_test_plugin_result = jinja_test_plugin_class("test")
    assert jinja_test_plugin_result

    jinja_filter_manager = PluginManager(JinjaFilterPlugin)
    jinja_filter_manager.load_plugins(plugin_config)
    jinja_filter_plugin_class = jinja_filter_manager.plugins.get("jinja_filter")
    jinja_filter_plugin_result = jinja_filter_plugin_class(["abc", "ab", "a"])

    assert jinja_filter_plugin_result == ["abc", "ab"]


def test_plugin_manager_construct_plugins_dict():
    plugin_manager = PluginManager(DataPlugin)
    plugin_manager.construct_plugins_dict({"test": data_plugin})

    assert "data_plugin" in plugin_manager.plugins.keys()


if __name__ == "__main__":
    test_plugin_manager_find_plugins_by_module_name()
    test_plugin_manager_find_matching_plugins()
    test_plugin_manager_find_plugins_from_path()
    test_plugin_manager_find_plugins_from_module()
    test_plugin_manager_specificity()
    test_multiple_plugin_managers()
    test_plugin_manager_construct_plugins_dict()
