from pathlib import Path
from argparse import ArgumentParser
import shutil

import build

import twine.commands.upload
from twine.settings import Settings

from .common import (
    project_root,
    check_package_installed_as_editable,
    check_branch,
)

default_dist_path = project_root / "dist"


def build_python_package(dist_dir: Path):
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir(parents=True, exist_ok=True)

    builder = build.ProjectBuilder(project_root)
    builder.build("wheel", output_directory=str(dist_dir.absolute()))
    builder.build("sdist", output_directory=str(dist_dir.absolute()))

    dist_files = [str(p) for p in dist_dir.iterdir()]

    return dist_files


def publish(dist_files: list[str]):
    settings = Settings(
        verbose=True,
        repository_name="pypi",
    )
    twine.commands.upload.upload(settings, dist_files)


def main(dist_dir: Path, publish_to_pypi: bool):
    dist_files = build_python_package(dist_dir)
    if publish_to_pypi:
        check_branch()
        publish(dist_files)


def cli():
    parser = ArgumentParser()
    parser.add_argument(
        "--dist-dir",
        type=Path,
        default=default_dist_path,
        help="Where to put the dist files",
    )
    parser.add_argument(
        "--publish", action="store_true", help="Publish to PyPi after build"
    )
    args = parser.parse_args()

    check_package_installed_as_editable()
    main(args.dist_dir, publish_to_pypi=args.publish)


if __name__ == "__main__":
    cli()
