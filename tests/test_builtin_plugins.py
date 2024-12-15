import datetime
from pathlib import Path
from zenplate.plugins.plugin_manager import PluginManager

import os

plugin_manager = PluginManager()

plugin_config = {
    "named_modules": [
        "zenplate.plugins.default_plugins.data_plugins",
        "zenplate.plugins.default_plugins.jinja_plugins",
    ],
}


def test_data_default_variables():
    plugin_manager.load_plugins(plugin_config)
    assert plugin_manager.invoke_plugin("defaults")
    assert plugin_manager.invoke_plugin("defaults")["os"]["name"] == os.name


def test_list_path_contents():
    plugin_manager.load_plugins(plugin_config)
    assert plugin_manager.invoke_plugin("ls", Path(__file__).parent) is not None
    assert plugin_manager.invoke_plugin("ls", Path(__file__).parent)


def test_jinja_test_path_exists():
    plugin_manager.load_plugins(plugin_config)
    assert (
        plugin_manager.invoke_plugin("path_exists", Path(__file__).resolve())
        is not None
    )
    assert plugin_manager.invoke_plugin("path_exists", Path(__file__).resolve())


def test_jinja_filter_now():
    plugin_manager.load_plugins(plugin_config)
    output = plugin_manager.invoke_plugin("now", fmt="%Y-%m-%d")
    assert output is not None
    assert output == datetime.datetime.now().strftime("%Y-%m-%d")


def test_jinja_filter_datetime_format():
    plugin_manager.load_plugins(plugin_config)
    output = plugin_manager.invoke_plugin(
        "datetime_format", datetime.datetime.now(), fmt="%Y-%m-%d"
    )
    assert output is not None
    assert output == datetime.datetime.now().strftime("%Y-%m-%d")


def test_jinja_filter_to_yaml():
    plugin_manager.load_plugins(plugin_config)
    output = plugin_manager.invoke_plugin("to_yaml", {"test": "test"})
    assert output is not None
    assert output == "test: test\n"


if __name__ == "__main__":
    test_data_default_variables()
    test_list_path_contents()
    test_jinja_test_path_exists()
    test_jinja_filter_now()
    test_jinja_filter_datetime_format()
    test_jinja_filter_to_yaml()
