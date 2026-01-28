from os import getenv
from argparse import ArgumentParser

from github import Github

from .common import (
    check_branch,
    check_package_installed_as_editable,
    get_current_version,
)


def create_release(version: str, github_token: str, release_notes: str):
    github_client = Github(github_token)
    github_repo = github_client.get_repo("camratchford/zenplate")

    release = github_repo.create_git_release(
        tag=str(version),
        name=str(version),
        message=release_notes,
        draft=False,
        prerelease=False,
    )
    print(f"Release {release.title} created: {release.html_url}")


def main(release_notes: str):
    check_package_installed_as_editable()
    check_branch()

    version = get_current_version()
    github_token = getenv("GITHUB_TOKEN")
    if not github_token:
        raise RuntimeError("GITHUB_TOKEN environment variable not set")

    create_release(version, github_token, release_notes)


def cli():
    parser = ArgumentParser()
    parser.add_argument(
        "--release-notes",
        type=str,
        default="",
        help="Release notes for the current version",
    )
    args = parser.parse_args()

    check_package_installed_as_editable()
    main(args.release_notes)


if __name__ == "__main__":
    cli()
