import logging
from pathlib import Path
from typing import Union

from jinja2 import Environment, FileSystemLoader, select_autoescape

from zenplate.config import ZenplateConfig
from zenplate.plugins import JinjaFilterPlugin, JinjaTestPlugin
from zenplate.plugins.plugin_manager import PluginManager

logger = logging.getLogger(__name__)


class TemplateManager(object):
    def __init__(self, config: ZenplateConfig):
        self.config = config

        self.template_path = config.template_path
        self.tree_dir = config.tree_directory
        if self.template_path:
            self.template_parent = Path(self.template_path).parent
            self.template_name = Path(self.template_path)
            self.env = Environment(
                loader=FileSystemLoader(self.template_parent),
                autoescape=select_autoescape(),
                **config.get_by_prefix(prefix="jinja_env", trim_prefix=True),
            )
        elif self.tree_dir:
            self.tree_dir = Path(config.tree_directory)
            self.env = Environment(
                loader=FileSystemLoader(self.tree_dir),
                autoescape=select_autoescape(),
            )
        self.load_plugins()

    def load_plugins(self):
        if self.config.plugin_config:
            try:
                jinja_filter_plugin_manager = PluginManager(JinjaFilterPlugin)
                jinja_filter_plugin_manager.load_plugins(self.config.plugin_config)
                filters = {k: v for k, v in jinja_filter_plugin_manager.plugins.items()}
                self.env.filters.update(filters)
            except Exception as e:
                logger.error(f"An unhandled exception occurred while loading Jinja2 filter plugins: {e}")
                logger.error(f"Error loading jinja filter plugins: {e}")

            try:
                jinja_test_plugin_manager = PluginManager(JinjaTestPlugin)
                jinja_test_plugin_manager.load_plugins(self.config.plugin_config)

                tests = {k: v for k, v in jinja_test_plugin_manager.plugins.items()}
                self.env.tests.update(tests)

            except Exception as e:
                logger.error(f"An unhandled exception occurred while loading Jinja2 test plugins: {e}")
                raise e

    def _render_template(self, template_name: str, output_path: Path) -> dict[str, dict[str, Union[str, Path]]]:
        try:
            template_content = self.env.get_template(template_name).render()
        except Exception as e:
            logger.error(f"An unhandled exception occurred while rendering template: {e}")
            raise e

        template_dict = {
            template_name: {
                "path": output_path,
                "content": template_content,
            }
        }
        return template_dict

    def render_tree_template(self) -> dict[str, dict[str, Union[str, Path]]]:
        dir_output_path = Path(self.config.output_path)
        if not dir_output_path.exists() or self.config.force_overwrite:
            template_list = self.env.loader.list_templates()
            output_path_list = [self.transform_path_name(path) for path in template_list]

            template_dict = {}
            for template_name, output_path in zip(template_list, output_path_list):
                template_dict.update(self._render_template(template_name, output_path))

            return template_dict

        else:
            logger.error(f"{dir_output_path} already exists. Use --force flag to write to an existing directory.")
            return {}

    def render_single_template(self) -> dict[str, dict[str, Union[str, Path]]]:
        template_name = Path(self.template_path).name
        return self._render_template(template_name, self.config.output_path)

    def transform_path_name(self, name: str) -> Path:
        name_path = Path(self.config.output_path).joinpath(name).resolve()
        templated_path = self.env.from_string(str(name_path)).render()
        return Path(str(templated_path))
