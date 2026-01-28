import re
import sys
from packaging.version import Version
import argparse


from .common import (
    run,
    get_current_version,
    pyproject_dot_toml,
    check_package_installed_as_editable,
)


def get_new_version(version: Version, magnitude: str) -> str:
    if magnitude == "dev":
        dev_ver = version.dev + 1 if version.dev else 0
        return f"{version.major}.{version.minor}.{version.micro}.dev{dev_ver}"

    elif magnitude == "patch":
        return f"{version.major}.{version.minor}.{version.micro + 1}"

    elif magnitude == "minor":
        return f"{version.major}.{version.minor + 1}.0"

    elif magnitude == "major":
        return f"{version.major + 1}.0.0"

    else:
        print(f"::error:: Invalid version bump magnitude: {magnitude}")
        sys.exit(1)


def set_new_version(new_version: str):
    content = pyproject_dot_toml.read_text()
    new_content = re.sub(
        r'(^version\s*=\s*["\'])(.+?)(["\'])',
        rf'version = "{new_version}"',
        content,
        flags=re.MULTILINE,
    )
    pyproject_dot_toml.write_text(new_content)


def git_tag(version: str):
    run(f"git add {pyproject_dot_toml}")
    run(f'git commit -m "Release {version}"')
    run(f"git tag v{version}")
    run("git push")
    run(f"git push origin v{version}")


def main(
    dev_release: bool,
    patch_release: bool,
    minor_release: bool,
    major_release: bool,
    manual_version: bool,
    dry_run: bool = False,
) -> None:
    version_bump_magnitude = (
        "dev"
        if dev_release
        else "patch"
        if patch_release
        else "minor"
        if minor_release
        else "major"
        if major_release
        else None
    )

    current_version = get_current_version()

    if version_bump_magnitude is None:
        print(current_version)
        exit(0)

    new_version = current_version
    if not manual_version:
        new_version = get_new_version(current_version, version_bump_magnitude)

    print(f"Bumping version: {current_version} → {new_version}")
    if not dry_run:
        set_new_version(new_version)
        git_tag(new_version)


def cli():
    parser = argparse.ArgumentParser(description="Bump version and create release.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--dev",
        action="store_true",
        help="Bump dev version: Maj.Min.Pat.devDev → Maj.Min.Pat.dev{Dev+1}",
    )
    group.add_argument(
        "--patch",
        action="store_true",
        help="Bump patch version: Maj.Min.Pat → Maj.Min.{Pat+1}",
    )
    group.add_argument(
        "--minor",
        action="store_true",
        help="Bump minor version: Maj.Min.Pat → Maj.{Min+1}.0",
    )
    group.add_argument(
        "--major",
        action="store_true",
        help="Bump major version: Maj.Min.Pat → {Maj+1}.0.0",
    )
    group.add_argument(
        "--manual-version",
        action="store_true",
        help="Don't auto-increment based on release type",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only show log messages, do not modify version in any way",
    )

    args = parser.parse_args()

    check_package_installed_as_editable()

    main(
        dev_release=args.dev,
        patch_release=args.patch,
        minor_release=args.minor,
        major_release=args.major,
        dry_run=args.dry_run,
        manual_version=args.manual_version,
    )


if __name__ == "__main__":
    cli()
