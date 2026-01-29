import re
import site
import subprocess
from pathlib import Path
from sys import exit

from packaging.version import Version

this_directory = Path(__file__).parent
project_root = this_directory.parent.parent
pyproject_dot_toml = project_root / "pyproject.toml"
package_name = "zenplate"


def run(cmd):
    """
    Runs shell commands in the project's root directory

    Args:
        cmd (str):
            The shell command that will be run

    Returns:
        subprocess.CompletedProcess
    """
    print(f"Running: {cmd}")
    return subprocess.run(
        cmd,
        shell=True,
        text=True,
        cwd=project_root,
        capture_output=True,
        check=False,
    )


def check_package_installed_as_editable(package: str = package_name):
    """
    Determines if the current project's Python package was installed with the editable option `pip -e`
    The relative path of the project root, and therefore the path to the tests directory depend on the package being
    installed this way.
    """
    for path in site.getsitepackages() + [site.getusersitepackages()]:
        if not Path(path).exists():
            continue
        editable_pkgs = [p.name for p in Path(path).iterdir() if p.is_file() and p.suffix == ".pth"]
        for pkg in editable_pkgs:
            if package in pkg:
                return

    print(
        "Error: "
        "Ensure the current project's Python package was installed with the editable option `pip -e`. "
        "The relative path of the project root, and therefore the path to the tests directory depend on the "
        "package being installed this way."
    )
    exit(1)


def get_current_branch():
    # This subprocess.run command is distinct from that used in scripts.common.run as this command captures output.
    return run("git rev-parse --abbrev-ref HEAD").stdout.strip()


def check_branch(target_branch: str = "main"):
    current_branch = get_current_branch()
    if current_branch != target_branch:
        print(f"Error: You must be on the main branch to release. Current branch is '{current_branch}'.")
        exit(1)


def get_current_version() -> Version:
    content = pyproject_dot_toml.read_text()
    match = re.search(r'^version\s*=\s*["\'](.+?)["\']', content, re.MULTILINE)
    if not match:
        print("Error: Version not found in pyproject.toml")
        exit(1)
    return Version(match.group(1))
