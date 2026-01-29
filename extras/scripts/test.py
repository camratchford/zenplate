from .common import (
    run,
    check_package_installed_as_editable,
)


def cli():
    check_package_installed_as_editable()
    process = run("pytest ./tests")

    if process.returncode == 0:
        print("::info:: Tests passed")


if __name__ == "__main__":
    cli()
