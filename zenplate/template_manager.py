import logging
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from zenplate.config import Config

from zenplate.plugins.plugin_manager import PluginManager
from zenplate.plugins import JinjaFilterPlugin, JinjaTestPlugin
from zenplate.exceptions import ZenplateException


logger = logging.getLogger(__name__)


class ZenplateVariableException(ZenplateException):
    pass


class TemplateManager(object):
    def __init__(self, config: Config):
        self.config = config

        self.template_path = config.template_path
        self.tree_dir = config.tree_directory
        if self.template_path:
            self.template_parent = Path(self.template_path).parent
            self.template_name = Path(self.template_path)
            self.env = Environment(
                loader=FileSystemLoader(self.template_parent),
                autoescape=select_autoescape(),
            )
        elif self.tree_dir:
            self.tree_dir = Path(config.tree_directory)
            self.env = Environment(
                loader=FileSystemLoader(self.tree_dir),
                autoescape=select_autoescape(),
            )
        self.configure_jinja(config.jinja_config)
        self.load_plugins()

    def configure_jinja(self, jinja_conf: dict):
        # Load jinja settings
        for attr in jinja_conf.keys():
            if hasattr(self.env, attr):
                try:
                    setattr(self.env, attr, jinja_conf[attr])
                except Exception as e:
                    logger.error(e)

    def load_plugins(self):
        if self.config.plugin_config:
            try:
                jinja_filter_plugin_manager = PluginManager(JinjaFilterPlugin)
                jinja_filter_plugin_manager.load_plugins(self.config.plugin_config)
                filters = {k: v for k, v in jinja_filter_plugin_manager.plugins.items()}
                self.env.filters.update(filters)
            except Exception as e:
                logger.error(f"Error loading jinja filter plugins: {e}")

            try:
                jinja_test_plugin_manager = PluginManager(JinjaTestPlugin)
                jinja_test_plugin_manager.load_plugins(self.config.plugin_config)

                tests = {k: v for k, v in jinja_test_plugin_manager.plugins.items()}
                self.env.tests.update(tests)

            except Exception as e:
                logger.error(f"Error loading jinja test plugins: {e}")

    def render_tree(self):
        output_path = Path(self.config.output_path)
        if not output_path.exists() or self.config.force_overwrite:
            template_list = self.env.loader.list_templates()
            output_path_list = [
                self.transform_path_name(path) for path in template_list
            ]

            template_dict = {
                name: {"path": path, "content": self.env.get_template(name).render()}
                for name, path in zip(template_list, output_path_list)
            }
            return template_dict
        else:
            logger.warning(
                f"{output_path} already exists. Use --force flag to write to an existing directory."
            )

    def render_template(self):
        template_name = Path(self.template_path).name
        template_dict = {
            template_name: {
                "path": self.config.output_path,
                "content": self.env.get_template(template_name).render(),
            }
        }
        return template_dict

    def transform_path_name(self, name):
        name_path = Path(self.config.output_path).joinpath(name).resolve()
        templated_path = self.env.from_string(str(name_path)).render()
        return Path(str(templated_path))
