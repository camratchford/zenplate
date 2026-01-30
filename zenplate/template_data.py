import logging
from pathlib import Path
from typing import List, Optional

import yaml

from zenplate.plugins import DataPlugin
from zenplate.plugins.plugin_manager import PluginManager

logger = logging.getLogger(__name__)


class TemplateData(object):
    def __init__(self, config):
        self.config = config
        self.vars = {}
        if config.jinja_global_vars:
            self.vars.update(config.jinja_global_vars)
        self.load_plugins()

    def load_plugins(self):
        if self.config.plugin_config:
            try:
                data_plugin_manager = PluginManager(DataPlugin)
                data_plugin_manager.load_plugins(self.config.plugin_config)
                data = {k: data_plugin_manager.invoke_plugin(k) for k, v in data_plugin_manager.plugins.items()}

                self.vars.update(data)

            except Exception as e:
                logger.error(
                    "An unhandled exception occurred while loading template variable plugin(s):"
                    f" {', '.join(self.config.plugin_config.get('path_modules'))}"
                    f" {', '.join(self.config.plugin_config.get('named_modules'))}"
                )
                raise e

    def load_files(self, var_files: Optional[List[Path]] = None):
        for var_file in var_files:
            logger.debug(f"Loading variables from file: {var_file}")
            if Path(var_file).exists():
                try:
                    with open(var_file, "r") as file:
                        file_vars = yaml.safe_load(file)
                        logger.debug(f"Loaded variables: {file_vars}")
                        self.vars.update(file_vars)
                except Exception as e:
                    logger.error(f"An unhandled exception occurred while loading variable file(s): {var_files}")
                    raise e

    def load(self, variables: Optional[List[str]] = None):
        if variables:
            for v in variables:
                try:
                    if "=" not in v:
                        logger.warning(f"Variable '{v}' is not parsable as a key:value pair, skipping.")
                        continue
                    split_var = v.split("=")

                    if len(split_var) > 1:
                        var_key = split_var[0]
                        var_value = split_var[1]

                        if r"\," in split_var[1]:
                            var_value = split_var[1].split(r"\,")

                        self.vars[var_key] = var_value

                except ValueError as e:
                    raise ValueError(f"Variable '{v}' could not be parsed: {e}") from e

                except Exception as e:
                    logger.error(f"An unhandled exception occurred while loading template variable(s): {variables}")
                    raise e
