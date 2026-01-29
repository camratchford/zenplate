import logging
from pathlib import Path
from typing import Annotated, Optional

from byoconfig import Config as BYOConfig

from zenplate.exceptions import ZenplateException
from zenplate.setup_logging import setup_logging

logger = logging.getLogger(__name__)


class ZenplateConfigException(ZenplateException):
    pass


class Config(BYOConfig):
    config_file: Annotated[Path, "excluded"] = None
    template_path: Annotated[Path, "excluded"] = None
    tree_directory: Annotated[Path, "excluded"] = None
    output_path: Annotated[Path, "excluded"] = None

    var_files: Optional[list[Path]] = None
    variables: Optional[list[str]] = []
    plugin_config: dict = {
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

    log_path: Optional[Path] = None
    log_level: str = "ERROR"
    stdout: bool = False
    verbose: bool = False

    def __init__(self, **kwargs):
        self.var_files = []

        self.jinja_env_trim_blocks = False
        self.jinja_env_lstrip_blocks = False
        self.jinja_env_keep_trailing_newline = False

        self.jinja_global_vars: dict = {}
        self.dry_run: bool = False
        self.log_level: str = "ERROR"
        self.log_path: Optional[Path] = None
        self.stdout: bool = False
        self.verbose: bool = False
        self.force_overwrite: bool = False

        setup_logging(log_path=self.log_path, log_level=self.log_level)
        super().__init__(config_assign_attrs=True, **kwargs)
        logger.debug(f"Config initialized with {self.__dict__}")
