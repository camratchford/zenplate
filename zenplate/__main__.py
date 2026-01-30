import logging
import sys

from zenplate.config import ZenplateConfig
from zenplate.output_handler import OutputHandler
from zenplate.template_data import TemplateData
from zenplate.template_manager import TemplateManager

logger = logging.getLogger(__name__)


def main(config: ZenplateConfig):
    templater = TemplateManager(config)
    template_vars = TemplateData(config)

    if config.var_files:
        try:
            logger.debug(f"Loading var files: {config.var_files}")
            template_vars.load_files(config.var_files)
        except Exception as e:
            raise e

    if config.variables:
        try:
            logger.debug(f"Loading variables: {config.variables}")
            template_vars.load(config.variables)

        except Exception as e:
            raise ValueError(f"Error loading variables: {e}")

    try:
        templater.env.globals.update(template_vars.vars)
    except Exception as e:
        raise ValueError(f"Error merging template_vars with globals: {e}")

    if config.dry_run:
        logger.debug("Dry run complete, exiting.")
        sys.exit(0)

    # Initialize the file handler
    try:
        logger.debug("Initializing output handler")
        output_handler = OutputHandler(config)
    except Exception as e:
        raise ValueError(f"Error initializing output handler: {e}")

    if templater.template_path:
        logger.debug(f"Attempting to render template {templater.template_path}")
        template_dict = templater.render_single_template()
        if not template_dict:
            raise ValueError("No template data was rendered")

        if not template_dict.values():
            raise ValueError("No template data was rendered")

        properties = list(template_dict.values())[0]
        output_path = properties.get("path")

        try:
            logger.debug(f"Writing template to {config.output_path}")
            output_handler.write_file(template_dict)
        except Exception as e:
            raise IOError(f"Error writing template output: {e}")

    elif templater.tree_dir:
        try:
            logger.debug(f"Attempting to render tree {templater.tree_dir}")
            template_dict = templater.render_tree_template()
        except Exception as e:
            raise e

        try:
            logger.debug(f"Writing templates to {config.output_path}")
            output_handler.write_tree(template_dict)
        except Exception as e:
            raise IOError(f"Error writing tree output: {e}") from e
