'''
ARMORY Versions use "Semantic Version" scheme where stable releases will have versions
like `0.14.6`.  Armory uses the most recent git tag for versioning. For example if the
most recent git tag is `v0.14.6`, then the version will be `0.14.6`.

If you are a developer, the version will be constructed from the most recent tag plus a
suffix of gHASH where HASH is the short hash of the most recent commit. For example,
if the most recent git tag is v0.14.6 and the most recent commit hash is 1234567 then
the version will be 0.14.6.g1234567. This scheme does differ from the scm strings
which also have a commit count and date in them like 1.0.1.dev2+g0c5ffd9.d20220314181920
which is a bit ungainly.
'''

import os
import setuptools_scm

from pathlib import Path

try:
    from importlib import metadata
except ModuleNotFoundError:
    # Python <= 3.7
    from importlib_metadata import version, PackageNotFoundError  # noqa

from armory.logs import log


def to_docker_tag(version_str: str) -> str:
    '''Convert version string to docker tag'''
    return version_str.replace('+', '.')


def get_build_hook_version(version_str: str = '') -> str:
    '''Retrieve the version from the build hook'''
    try:
        from armory.__about__ import __version__ as version_str
    except ModuleNotFoundError:
        log.error("ERROR: Unable to extract version from __about__.py")
    return version_str


def get_metadata_version(package: str, version_str: str = '') -> str:
    '''Retrieve the version from the package metadata'''
    try:
        return str(metadata.version(package))
    except metadata.PackageNotFoundError:
        log.error(f"ERROR: Unable to find the specified package! Package {package} not installed.")
    return version_str


def get_tag_version(git_dir: Path = None) -> str:
    '''Retrieve the version from the most recent git tag'''
    scm_config = {
        'root': git_dir,
        'relative_to': __file__,
        'version_scheme': "post-release",
    }
    if git_dir is None:
        for exec_path in (Path(__file__), Path.cwd()):
            if Path(exec_path / ".git").is_dir():
                scm_config['root'] = exec_path
                break
    # Unable to find `.git` directory...
    if scm_config['root'] is None:
        log.error("ERROR: Unable to find `.git` directory!")
        return
    return setuptools_scm.get_version(**scm_config)


def get_version(package_name: str = 'armory-testbed', version_str: str = '') -> str:
    # TODO: "ARMORY_DEV_MODE" environment variable
    # ARMORY_DEV_MODE=1 armory --version
    if os.getenv('ARMORY_DEV_MODE'):
        import re
        import site

        version_str = get_tag_version()
        version_regex = r'(?P<prefix>^Version: )(?P<version>.*)$'
        package_meta = [f for f in metadata.files(package_name) if str(f).endswith('METADATA')][0]

        for site in site.getsitepackages():
            package_data = Path(site / package_meta)
            if package_data.exists():
                break

        package_update = re.sub(version_regex, fr'\g<prefix>{version_str}', package_data.read_text(), flags=re.MULTILINE)
        package_data.write_text(package_update)


        print(f"SCM Version: {version_str}")
        print(f"Metadata Version: {get_metadata_version(package_name)}")

        return version_str
    # version_str = get_metadata_version(package_name)
    # if not bool(version_str):
    #     version_str = get_build_hook_version()
    # if not bool(version_str):
    #     version_str = get_tag_version()
    # return version_str or "0.0.0"
