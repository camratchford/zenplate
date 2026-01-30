import logging
from enum import Enum
from pathlib import Path
from sys import exit
from typing import List, Optional

import click
import typer
from typing_extensions import Annotated

from zenplate.__main__ import main
from zenplate.config import ZenplateConfig

logger = logging.getLogger(__name__)


cli = typer.Typer()


class LogLevels(str, Enum):
    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    critical = "CRITICAL"
    default = None


@cli.command("", no_args_is_help=True)
def run(
    template: Annotated[
        Optional[Path],
        typer.Argument(
            help="The path to the jinja template / directory that zenplate will render",
            dir_okay=True,
            file_okay=True,
            readable=True,
        ),
    ] = None,
    output: Annotated[
        Optional[Path],
        typer.Argument(
            help="The path to where you'll find the output of zenplate",
            dir_okay=True,
            file_okay=True,
        ),
    ] = None,
    config_file: Annotated[
        Optional[Path],
        typer.Option(
            "--config-file",
            "-c",
            help="The location of the YAML configuration file",
            show_default=True,
            dir_okay=False,
            readable=True,
            envvar="ZENPLATE_CONFIG_FILE",
        ),
    ] = None,
    variables: Annotated[
        Optional[List[str]],
        typer.Option(
            "--var",
            "-v",
            help="A 'varname=value' pair representing a variable. May be used multiple times.",
        ),
    ] = tuple(),
    var_file: Annotated[
        Optional[List[Path]],
        typer.Option(
            "--var-file",
            "-f",
            help="The path to a YAML file containing key: value pairs to be used as variables. "
            "May be used multiple times.",
            dir_okay=False,
            readable=True,
            envvar="ZENPLATE_VAR_FILE",
        ),
    ] = tuple(),
    log_path: Annotated[
        Optional[Path],
        typer.Option(
            "--log-path",
            help="The location of the log file",
            dir_okay=False,
            envvar="ZENPLATE_LOG_PATH",
        ),
    ] = None,
    log_level: Annotated[
        Optional[LogLevels],
        typer.Option(
            "--log-level",
            help="The logging verbosity level",
            show_default=True,
            envvar="ZENPLATE_LOG_LEVEL",
        ),
    ] = "ERROR",
    export_config: Annotated[
        bool,
        typer.Option(
            "--export-config",
            help="When provided, the current set of configuration parameters will be exported "
            "to '--config-file' or './zenplate_config_export.yml' if not provided",
            is_flag=True,
            flag_value=True,
        ),
    ] = False,
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            "-f",
            help="When provided, output will overwrite any file in that path",
            is_flag=True,
        ),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-V",
            help="Enable debug logging",
            is_flag=True,
        ),
    ] = False,
):
    try:
        if (not template and not output) and not export_config:
            raise click.exceptions.BadArgumentUsage(
                "You must provide both 'template' and 'output' arguments "
                "unless the '--help' or '--export-config' flags are provided."
            )
        if (template and not output) or (output and not template):
            raise click.exceptions.BadArgumentUsage("You must provide both 'template' and 'output' arguments.")

    except click.exceptions.BadArgumentUsage as e:
        typer.echo(str(e), err=True)
        exit(1)

    except Exception as e:
        raise e

    config = ZenplateConfig(file_path=config_file)
    if log_path != config.log_path:
        config.set("log_path", log_path)
    if variables != config.variables:
        config.set("variables", variables)
    if var_file != config.var_files:
        var_file_paths = [Path(i) for i in var_file]
        config.set("var_files", var_file_paths)

    if template and template.is_dir():
        config.set("tree_directory", template)
    elif template and template.is_file():
        config.set("template_path", template)
    elif not template:
        typer.echo("No template parameter provided.", err=True)
        exit(1)
    else:
        typer.echo(f"Template path '{template}' is not a file or directory.", err=True)
        exit(1)

    config.set("output_path", Path(output))
    if export_config:
        config.dump_to_file(config.output_path)
        exit(0)
    if force:
        config.set("force_overwrite", force)
    if log_level != config.log_level:
        config.set("log_level", log_level)
    if verbose != config.verbose:
        config.set("verbose", verbose)

    try:
        main(config)
    except Exception as e:
        typer.echo(e, err=True)
        raise e


if __name__ == "__main__":
    cli()
