import logging
import sys

from zenplate.config import Config
from zenplate.template_manager import TemplateManager
from zenplate.template_data import TemplateData
from zenplate.output_handler import OutputHandler


logger = logging.getLogger(__name__)


def main(config: Config):
    # Create the Jinja environment

    templater = TemplateManager(config)

    # Load the TemplateVars object with the app config
    template_vars = TemplateData(config)

    # Load template_vars object in order of least to most precedence
    if config.var_files:
        template_vars.load_files(config.var_files)
    if config.variables:
        template_vars.load(config.variables)

    # Load the template_vars variable dictionary into the templates environment
    templater.env.globals.update(template_vars.vars)

    if config.dry_run:
        sys.exit(0)

    # Initialize the file handler
    output_handler = OutputHandler(config)

    if templater.template_path:
        template_dict = templater.render_template()
        if not template_dict:
            logger.error("No template data was rendered")
            sys.exit(1)
        properties = list(template_dict.values())[0]
        output_path = properties.get("path")

        output_handler.write_file(template_dict)
        if config.stdout:
            output_handler.write_stdout(output_path)

    elif templater.tree_dir:
        template_dict = templater.render_tree()
        output_handler.write_tree(template_dict)
