import logging
from pathlib import Path
from typing import List, Optional

import yaml

from zenplate.plugins.plugin_manager import PluginManager
from zenplate.plugins import DataPlugin


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
                data = {
                    k: data_plugin_manager.invoke_plugin(k)
                    for k, v in data_plugin_manager.plugins.items()
                }

                self.vars.update(data)

            except Exception as e:
                logger.error(f"Error loading data plugins: {e}")
                raise

    def load_files(self, var_files: Optional[List[Path]] = None):
        for var_file in var_files:
            if Path(var_file).exists():
                try:
                    with open(var_file, "r") as file:
                        self.vars.update(yaml.safe_load(file))
                except Exception as e:
                    logger.error(e)

    def load(self, variables: Optional[List[str]] = None):
        if variables:
            for v in variables:
                try:
                    if "=" not in v:
                        logger.warning(
                            f"Variable '{v}' is not parsable as a key:value pair, skipping."
                        )
                        continue
                    split_var = v.split("=")
                    if len(split_var) > 1 and r"\," in split_var[1]:
                        split_var[1] = split_var[1].split(r"\,")
                    self.vars[split_var[0]] = split_var[1]
                except ValueError as e:
                    logger.error(f"Variable {v} could not be parsed\n\t{e}")
