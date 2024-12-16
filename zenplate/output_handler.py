import logging

from pathlib import Path

from zenplate.exceptions import ZenplateException

logger = logging.getLogger(__name__)


class OutputHandlerException(ZenplateException):
    pass


class OutputHandler(object):
    def __init__(self, config):
        self.config = config

    def write_tree(self, template_dict: dict):
        if Path(self.config.output_path).exists() and not self.config.force_overwrite:
            raise OutputHandlerException(
                f"Output path '{self.config.output_path}' already exists, use --force to overwrite."
            )

        if not Path(self.config.output_path).exists():
            logger.debug(f"Creating output directory {self.config.output_path}")
            Path(self.config.output_path).mkdir(mode=0o755, parents=True)

        if template_dict:
            for template, properties in template_dict.items():
                name = template
                path = properties.get("path")
                parent_path = path.parent.resolve()
                content = properties.get("content")
                if not parent_path.exists():
                    logger.debug(f"Creating parent directory {parent_path}")
                    parent_path.mkdir(mode=0o755, parents=True)
                try:
                    logger.info(f"Writing {name}")
                    path.touch(exist_ok=True, mode=0o755)
                    path.write_text(content, encoding="utf-8")
                except Exception as e:
                    logger.error(e, f"Could not write {name}")

    def write_file(self, template_dict: dict):
        if template_dict:
            name, properties = template_dict.popitem()
            path = properties.get("path")
            if path.exists() and not self.config.force_overwrite:
                logger.error(
                    f"File '{path.resolve()}' already exists, use --force to overwrite"
                )
                return
            parent_path = path.parent.resolve()
            content = properties.get("content")
            if not parent_path.exists():
                logger.debug(f"Creating parent directory {parent_path}")
                parent_path.mkdir(mode=0o755, parents=True)
            try:
                logger.info(f"Writing {name}")
                path.touch(exist_ok=True, mode=0o755)
                path.write_text(content, encoding="utf-8")
            except Exception as e:
                logger.error(e, f"Could not write {name}")

    def write_stdout(self, output_path: Path):
        print(output_path.read_text())
