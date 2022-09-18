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

# TODO: See pandas library: https://github.com/pandas-dev/pandas/blob/main/pandas/_version.py

import re
import pathlib
import subprocess
import pkg_resources


from armory.logs import log


_VERSION = None

def get_version():
    global _VERSION
    if _VERSION is None:
        _VERSION = generate_version()
    return _VERSION


def get_metadata_version(package, version = None):
    try:
        from importlib.metadata import version, PackageNotFoundError
    except ModuleNotFoundError:
        from importlib_metadata import version, PackageNotFoundError
    return version(package)
    # import pkg_resources
    # version = pkg_resources.get_distribution(package).version


def get_pyproject_version():
    """
    Produce version number found in the pyproject.toml.
      - https://peps.python.org/pep-0621/

    Return None if not found.
    """
    try:
        import tomllib as toml  # Python 3.10+
    except ModuleNotFoundError:
        import toml

    pyproject = pathlib.Path(__file__).parent.parent / "pyproject.toml"

    if pyproject.exists():
        pyproject = toml.load(pyproject)
        # Check if the project was packaged with poetry.
        if (poetry := pyproject.get('tool', {}).get('poetry', {})) != {}:
            return poetry.get('version', None)
        # TODO: setuptools, et. al.
    return None


def get_setuptools_version():
    """
    Produce the version dynamically from setup.py if available.
    Return None if setup.py is not available
    """
    armory_repo_root = pathlib.Path(__file__).parent.parent
    setup = armory_repo_root / "setup.py"
    if not setup.is_file():
        return None

    completed = subprocess.run(
        ["python", str(setup), "--version"],
        cwd=str(armory_repo_root),
        capture_output=True,
        text=True,
    )
    try:
        completed.check_returncode()
    except subprocess.CalledProcessError:
        log.critical("setup.py exists but 'python setup.py --version' failed.")
        raise
    _version = completed.stdout.strip()
    return _version


def trim_version(version):
    if type(version) == str:
        return re.sub(r"dev\d+\+(g[0-9a-f]+)(\.d\d+)?$", r"\1", version)
    else:
        print(version.__module__)
        return get_metadata_version('armory')
    # return version


def generate_version():
    if (version := get_pyproject_version()) is not None:
        return trim_version(version)
    elif (version := get_metadata_version('armory')) is not None:
        return trim_version(version)
    elif (version := get_setuptools_version()) is not None:
        return trim_version(version)
    else:
        raise RuntimeError("Unable to determine version number!")
    return None