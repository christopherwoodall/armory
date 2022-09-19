"""
ARMORY Versions use "Semantic Version" scheme where stable releases will have versions
like `0.14.6`.  Armory uses `setuptools_scm` which pulls the version from the tags most
recent git tag. For example if the most recent git tag is `v0.14.6`, then the version
will be `0.14.6`.

If you are a developer, the version will be constructed from the most recent tag plus a
suffix of gHASH where HASH is the short hash of the most recent commit. For example,
if the most recent git tag is v0.14.6 and the most recent commit hash is 1234567 then
the version will be 0.14.6.g1234567. This scheme does differ from the scm strings
which also have a commit count and date in them like 1.0.1.dev2+g0c5ffd9.d20220314181920
which is a bit ungainly.
"""

import re
import pathlib

from pathlib import Path

from armory.logs import log


git_tag_regex = re.compile(r"(?P<version>[vV]?\d+(?:\.\d+){0,2})")

def trim_version(version):
    return git_tag_regex.match(version).group('version')


def get_metadata_version(package, version = None):
    try:
        from importlib.metadata import version, PackageNotFoundError
    except ModuleNotFoundError:
        from importlib_metadata import version, PackageNotFoundError
    return version(package)


def get_version():
    version_file = Path(Path(__file__).parent.parent / 'VERSION.txt')
    if version_file.exists():
        version_string = version_file.read_text().strip()
        if (version := trim_version(version_string)):
            return version
        elif (version := version_trim(get_metadata_version('armory'))):
            return version
        else:
            log.error(f"Unable to parse version from {version_file}")
    raise RuntimeError("Unable to determine version number!")


