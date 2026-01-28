from argparse import ArgumentParser
from subprocess import CompletedProcess

from .common import (
    run,
    check_package_installed_as_editable,
)


def main(directories: list[str], test_mode: bool):
    dir_arg = " ".join(directories)
    check_test_arg, format_test_arg = "", ""
    if test_mode:
        check_test_arg = "--exit-non-zero-on-fix"
        format_test_arg = "--check --exit-non-zero-on-fix"

    check_process: CompletedProcess = run(
        f"ruff check --show-fixes --fix {check_test_arg} {dir_arg}"
    )
    format_process: CompletedProcess = run(f"ruff format {format_test_arg} {dir_arg}")

    if test_mode and (check_process.returncode != 0 or format_process.returncode != 0):
        check_errors = check_process.stderr | check_process.stdout
        format_errors = format_process.stderr | format_process.stdout

        print(
            f"Formater / Linter errors: Check='{check_errors}' Format='{format_errors}'"
        )


def cli():
    parser = ArgumentParser()
    parser.add_argument(
        "--test",
        action="store_true",
        help="Exits with error if ruff needs to make changes",
    )
    parser.add_argument(
        "--directories",
        nargs="+",
        help="List of directories to format and lint",
        default=["."],
    )
    args = parser.parse_args()

    check_package_installed_as_editable()
    main(directories=args.directories, test_mode=args.test)


if __name__ == "__main__":
    cli()
