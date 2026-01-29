from argparse import ArgumentParser
from subprocess import CompletedProcess

from .common import check_package_installed_as_editable, run


def main(directories: list[str], test_mode: bool):
    dir_arg = " ".join(directories)
    check_test_arg, format_test_arg = "", ""
    if test_mode:
        check_test_arg = "--exit-non-zero-on-fix"
        format_test_arg = "--check --exit-non-zero-on-fix"
    isort_process: CompletedProcess = run(f"isort --atomic {dir_arg}")
    check_process: CompletedProcess = run(f"ruff check --show-fixes --fix {check_test_arg} {dir_arg}")
    format_process: CompletedProcess = run(f"ruff format {format_test_arg} {dir_arg}")
    return_codes = isort_process.returncode + check_process.returncode + format_process.returncode
    if test_mode and (return_codes != 0):
        isort_errors = isort_process.stderr + isort_process.stdout
        check_errors = check_process.stderr + check_process.stdout
        format_errors = format_process.stderr + format_process.stdout

        print(f"Formater / Linter errors: isort='{isort_errors}' Check='{check_errors}' Format='{format_errors}'")


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
