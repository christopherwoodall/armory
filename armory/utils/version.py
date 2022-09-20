"""
ARMORY Versions use "Semantic Version" scheme where stable releases will have versions
like `0.14.6`.  Armory uses the most recent git tag for versioning. For example if the
most recent git tag is `v0.14.6`, then the version will be `0.14.6`.

If you are a developer, the version will be constructed from the most recent tag plus a
suffix of gHASH where HASH is the short hash of the most recent commit. For example,
if the most recent git tag is v0.14.6 and the most recent commit hash is 1234567 then
the version will be 0.14.6.g1234567. This scheme does differ from the scm strings
which also have a commit count and date in them like 1.0.1.dev2+g0c5ffd9.d20220314181920
which is a bit ungainly.
"""

import os
import re
import sys


from armory.logs import log


def versiontuple(v):
   filled = []
   for point in v.split("."):
      filled.append(point.zfill(8))
   return tuple(filled)


def trim_version(version_str):
    git_tag_regex = re.compile(r"(?P<version>[vV]?\d+(?:\.\d+){0,2})")
    if (tag_match := git_tag_regex.match(version_str)) is not None:
        return tag_match.group("version")
    return False


def get_metadata_version(package: str, version = None) -> str:
    try:
        from importlib.metadata import distribution, version, PackageNotFoundError
    except ModuleNotFoundError:
        from importlib_metadata import distribution, version, PackageNotFoundError

    try:
        if (version := distribution(package).version) is not None:
            return version
        elif (version := version(package)) is not None:
            return version
        else:
            return "0.0.0"
    except PackageNotFoundError:
        log.error(f"Package {package} not installed.")
    raise RuntimeError(f"version.py was unable to find the specified package!")


def get_version():
    try:
        from armory.__about__ import VCS_VERSION
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(5)

    version = trim_version(VCS_VERSION)

    if versiontuple(version) < versiontuple("0.0.0"):
        version = version_trim(get_metadata_version('armory'))

    if versiontuple(version) > versiontuple("0.0.0"):
        return version

    log.error(f"Unable to parse version!")
    raise RuntimeError("Unable to determine version number!")
