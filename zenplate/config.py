import json
import logging
import pathlib
from pathlib import Path
from typing import Optional, List
from typing_extensions import Annotated, get_type_hints

import yaml

from zenplate.setup_logging import setup_logging
from zenplate.yaml_extras import pathobj_rep
from zenplate.exceptions import ZenplateException


logger = logging.getLogger(__name__)


class ZenplateConfigException(ZenplateException):
    pass


class Config:
    config_file: Annotated[Path, "exclude"] = None

    template_path: Annotated[Path, "exclude"] = None
    tree_directory: Annotated[Path, "exclude"] = None
    output_path: Annotated[Path, "exclude"] = None

    var_files: Optional[List[Path]] = None
    variables: Optional[List[str]] = []
    plugin_config: dict = {}

    log_path: Optional[Path] = None
    log_level: str = "ERROR"
    stdout: bool = False
    verbose: bool = False

    def __init__(self):
        self.config_file: Annotated[Path, "exclude"] = None
        self.template_path: Annotated[Path, "exclude"] = None
        self.tree_directory: Annotated[Path, "exclude"] = None
        self.output_path: Annotated[Path, "exclude"] = None
        self.var_files = []
        self.jinja_config = {
            "trim_blocks": False,
            "lstrip_blocks": False,
            "keep_trailing_newline": False,
        }
        self.jinja_global_vars: dict = {}
        self.dry_run: bool = False
        self.log_level: str = "ERROR"
        self.log_path: Optional[Path] = None
        self.stdout: bool = False
        self.verbose: bool = False
        self.force_overwrite: bool = False

        default_plugin_config = {
            "path_modules": [],
            "named_modules": [
                "zenplate.plugins.default_plugins.data_plugins",
                "zenplate.plugins.default_plugins.jinja_plugins",
            ],
            "plugin_kwargs": {
                "ls": {
                    "path": ".",
                }
            },
        }
        self.plugin_config = default_plugin_config

        setup_logging(log_path=self.log_path, log_level=self.log_level)
        logger.debug(f"Config initialized with {self.__dict__}")

    def attr_exportable(self, key):
        type_hints = get_type_hints(self, include_extras=True).get(key, None)
        if not type_hints:
            return True

        return (
            not hasattr(type_hints, "__metadata__")
            or type_hints.__metadata__[0] != "exclude"
        )

    @property
    def exportable_attrs(self):
        return [
            k
            for k, v in self.__dict__.items()
            if self.attr_exportable(k)
            and not k.startswith("_")
            and not k == "config_file"
        ]

    def configure_from_path(self, config_file_path):
        """
        - Reads in a yaml/json config file, load top level dictionary keys that match the config class's set of attrs.
        - Will ignore any keys that are contained in the 'self.exportable_attrs' list.
        - Any attrs ending in 'dir','path','file' with be cast into a Path object, then resolved.
        """
        self.config_file = config_file_path

        logger.debug(f"Attempting import of config file {self.config_file}")

        if isinstance(self.config_file, Path) and self.config_file.exists():
            if self.config_file and self.config_file.exists():
                if (
                    ".yaml" in self.config_file.suffixes
                    or ".yml" in self.config_file.suffixes
                ):
                    with open(self.config_file, "r") as file:
                        logger.debug("YAML extension found for config file")
                        loaded_config = yaml.safe_load(file)
                elif ".json" in self.config_file.suffixes:
                    with open(self.config_file, "r") as file:
                        logger.debug("JSON extension found for config file")
                        loaded_config = json.load(file)
                else:
                    raise ZenplateConfigException(
                        f"Config file {self.config_file} is not a valid file type. Must be .yaml or .json"
                    )

                if loaded_config:
                    for attr, value in loaded_config.items():
                        if not hasattr(self, attr):
                            logger.warning(
                                f"Config file contains unknown attribute: {attr}"
                            )
                            continue
                        if hasattr(self, attr) and attr in self.exportable_attrs:
                            if (
                                attr.endswith("dir")
                                or attr.endswith("path")
                                or attr.endswith("file")
                            ):
                                if value is not None:
                                    try:
                                        value = Path(loaded_config[attr]).resolve()
                                    except TypeError as e:
                                        print(f"Error with {attr}: {e}")
                            setattr(self, attr, value)
                            logger.debug(f"Configured {attr} with {str(value)}")

        setup_logging(self.log_level, self.log_path)

    def export_config(self):
        """
        - Exports the post-configuration config parameters to ./config_export.yml
        """
        export_dict = {
            k: getattr(self, k)
            for k, v in self.__dict__.items()
            if k in self.exportable_attrs
        }

        out_path = Path.cwd().joinpath("zenplate_config_export.yml").resolve()
        if self.config_file:
            out_path = self.config_file.resolve()

        if not out_path.exists():
            if not out_path.parent.exists():
                out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.touch(0o777, exist_ok=True)

        with open(out_path, "w") as file:
            yaml.add_representer(pathlib.PosixPath, pathobj_rep)
            yaml.add_representer(pathlib.WindowsPath, pathobj_rep)
            yaml.dump(export_dict, file, sort_keys=False)
