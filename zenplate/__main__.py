import logging
import sys

from zenplate.config import Config
from zenplate.template_manager import TemplateManager
from zenplate.template_data import TemplateData
from zenplate.output_handler import OutputHandler
from zenplate.exceptions import ZenplateException


logger = logging.getLogger(__name__)


def main(config: Config):
    templater = TemplateManager(config)
    template_vars = TemplateData(config)

    if config.var_files:
        try:
            logger.debug(f"Loading var files: {config.var_files}")
            template_vars.load_files(config.var_files)
        except ZenplateException as e:
            raise e
        except Exception as e:
            raise e

    if config.variables:
        try:
            logger.debug(f"Loading variables: {config.variables}")
            template_vars.load(config.variables)
        except ZenplateException as e:
            raise e
        except Exception as e:
            raise ZenplateException(f"Error loading variables: {e}")

    try:
        templater.env.globals.update(template_vars.vars)
    except Exception as e:
        raise ZenplateException(f"Error merging template_vars with globals: {e}")

    if config.dry_run:
        logger.debug("Dry run complete, exiting.")
        sys.exit(0)

    # Initialize the file handler
    try:
        logger.debug("Initializing output handler")
        output_handler = OutputHandler(config)
    except ZenplateException as e:
        raise e
    except Exception as e:
        raise ZenplateException(f"Error initializing output handler: {e}")

    if templater.template_path:
        logger.debug(f"Attempting to render template {templater.template_path}")
        template_dict = templater.render_template()
        if not template_dict:
            raise ZenplateException("No template data was rendered")

        if not template_dict.values():
            raise ZenplateException("No template data was rendered")

        properties = list(template_dict.values())[0]
        output_path = properties.get("path")

        try:
            logger.debug(f"Writing template to {config.output_path}")
            output_handler.write_file(template_dict)
        except ZenplateException as e:
            raise e
        except Exception as e:
            raise ZenplateException(f"Error writing template output: {e}")

        if config.stdout:
            logger.debug("Writing template contents to stdout")
            output_handler.write_stdout(output_path)

    elif templater.tree_dir:
        try:
            logger.debug(f"Attempting to render tree {templater.tree_dir}")
            template_dict = templater.render_tree()
        except ZenplateException as e:
            raise e
        except Exception as e:
            raise ZenplateException(f"Error rendering tree templates: {e}")

        try:
            logger.debug(f"Writing templates to {config.output_path}")
            output_handler.write_tree(template_dict)
        except ZenplateException as e:
            raise e
        except Exception as e:
            raise ZenplateException(f"Error writing tree output: {e}")
