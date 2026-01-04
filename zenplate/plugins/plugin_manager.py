import logging
from pathlib import Path
from typing import Type

import importlib
import importlib.util
import pkgutil
import inspect

from zenplate.plugins.base import Plugin
from zenplate.exceptions import ZenplateException


logger = logging.getLogger(__name__)


class ZenplatePluginManagerException(ZenplateException):
    pass


class PluginManager:
    plugin_config: dict
    plugin_modules: list
    base_class: Type[Plugin] = Plugin
    plugin_config: dict = {}

    def __init__(
        self,
        base_class: Type[Plugin] = Plugin,
        plugin_search_string: str = "zenplate_plugin",
    ):
        self._plugins = {}
        self.plugin_search_string = plugin_search_string
        self.base_class = base_class

    def load_plugins(self, plugin_config: dict):
        self.plugin_config = plugin_config
        path_modules = self.plugin_config.get("path_modules", [])

        found_plugins = {}
        for module in path_modules:
            if not Path(module).exists():
                raise ZenplatePluginManagerException(
                    f"Error loading plugin path module ({module}). Path does not exist."
                )
            found_plugins.update(self.find_plugins_from_path(module))

        named_modules = self.plugin_config.get("named_modules", [])
        for module in named_modules:
            loader = pkgutil.find_loader(module)
            if loader is None:
                raise ZenplatePluginManagerException(
                    f"Error loading plugin named module ({module}). Loader does not exist."
                )
            found_plugins.update(self.find_plugins_by_module_name(module))

        matching_plugins = self.find_matching_plugins()
        if matching_plugins:
            found_plugins.update(matching_plugins)

        if found_plugins:
            self.construct_plugins_dict(found_plugins)

    def find_plugins_by_module_name(self, module: str):
        found_module = importlib.import_module(module)
        plugins = self.find_plugins_from_module(found_module)

        return plugins

    def find_matching_plugins(self):
        matching_modules = [
            importlib.import_module(name)
            for finder, name, is_pkg in pkgutil.iter_modules()
            if name.startswith(self.plugin_search_string)
        ]

        plugins = {}

        # todo: I'm sure there's a better way
        for module in matching_modules:
            for submodule_search_loc in module.__spec__.submodule_search_locations:
                plugins.update(self.find_plugins_from_path(submodule_search_loc))

        return plugins

    def find_plugins_from_path(self, module_path: str):
        plugin_dir = Path(module_path).resolve()
        if not Path(module_path).exists():
            raise ZenplatePluginManagerException(
                f"Plugin module: {module_path} does not exist"
            )
        plugins = {}
        for filename in plugin_dir.iterdir():
            if filename.name.startswith("__"):
                continue
            filename: Path
            if filename.suffix == ".py":
                module_name = (
                    str(filename.relative_to(plugin_dir.parent))
                    .replace("\\", ".")
                    .rstrip(".py")
                )

                spec = importlib.util.spec_from_file_location(
                    module_name, str(filename)
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                plugins.update(self.find_plugins_from_module(module))

        return plugins

    def find_plugins_from_module(self, module) -> dict:
        results = {}
        for name, obj in inspect.getmembers(module):
            if (
                inspect.isclass(obj)
                and issubclass(obj, self.base_class)
                and obj != self.base_class
            ):
                logger.debug(f"Found plugin: {obj.name} in {module.__name__} module")
                results[obj.name] = obj

        return results

    @property
    def plugins(self):
        return {k: v.get("class")() for k, v in self._plugins.items()}

    def construct_plugins_dict(self, found_plugins: dict):
        config_plugins = self.plugin_config.get("plugin_kwargs")
        if found_plugins:
            for name, cls in found_plugins.items():
                registered_name = cls.name
                if issubclass(cls, self.base_class):
                    self._plugins[registered_name] = {"class": cls, "kwargs": {}}
                if config_plugins:
                    matching_config = config_plugins.get(registered_name)
                    if matching_config:
                        self._plugins[registered_name]["kwargs"] = matching_config

    def get_plugin(self, plugin_name: str):
        return self._plugins.get(plugin_name).get("class")

    def invoke_plugin(self, plugin_name: str, *args, **kwargs):
        plugin = self._plugins.get(plugin_name)
        if not plugin:
            raise ZenplatePluginManagerException(
                f"Plugin '{plugin_name}' not found in the plugin manager"
            )

        plugin_kwargs = {}
        if plugin and plugin.get("class") and hasattr(plugin.get("class"), "kwargs"):
            plugin_kwargs.update(plugin.get("class").kwargs)
            plugin_kwargs.update(plugin.get("kwargs"))
        plugin_kwargs.update(kwargs)

        return plugin["class"]()(*args, **plugin_kwargs)
