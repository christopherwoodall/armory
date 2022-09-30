import sys
import shutil
import argparse
import subprocess
import setuptools_scm

from pathlib import Path


script_dir = Path(__file__).parent
root_dir = script_dir.parent

armory_frameworks = ["pytorch", "pytorch-deepspeech", "tf2"]

# NOTE: Podman is not officially supported, but this enables
#       use as a drop-in replacement for building.
container_platform = "docker" if shutil.which("docker") else "podman"


def cli_parser(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser("Armory Container Build Script")
    arguments = (
        (("-f", "--framework"), dict(
            choices=armory_frameworks + ["all"],
            help="Framework to build",
            required=True,
        )),
        (("-b", "--base-tag"), dict(
            help="Version tag for twosixarmory/armory-base",
            default="latest",
            required=False,
        )),
        (("-nc", "--no-cache"), dict(
            action="store_true",
            help="Do not use docker cache",
        )),
        (("-np", "--no-pull"), dict(
            action="store_true",
            help="Do not pull latest base",
        )),
        (("-n", "--dry-run"), dict(
            action="store_true",
            help="Do not build, only print commands",
        )),
        (("-p", "--platform"), dict(
            choices=["docker", "podman"],
            help="Print verbose output",
            default=container_platform,
            required=False,
        )),
    )
    for args, kwargs in arguments:
        parser.add_argument(*args, **kwargs)
    parser.set_defaults(func=init)
    return parser.parse_args(argv)


def get_tag_version(git_dir: Path = None) -> str:
    '''Retrieve the version from the most recent git tag'''
    scm_config = {
        'root': git_dir,
        'relative_to': __file__,
        'version_scheme': "post-release",
        'local_scheme': "node-and-date",
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
    scm_version = setuptools_scm.get_version(**scm_config)
    return scm_version.replace("+", ".")


def build_worker(framework, version, platform, base_tag, **kwargs):
    '''Builds armory container for a given framework.'''
    dockerfile = script_dir / f"Dockerfile-{framework}"
    build_command = [
        f"{platform}",
        "build",
        "--force-rm",
        "--tag",
        f"twosixarmory/{framework}:{version}",
        "--build-arg",
        f"base_image_tag={base_tag}",
        "--build-arg",
        f"armory_version={version}",
        "--file",
        f"{dockerfile}",
        f"{Path().cwd()}",
    ]
    if kwargs.get('no_cache'):
        build_command.insert(3, "--no-cache")
    if not kwargs.get('no_pull'):
        build_command.insert(3, "--pull")
    if not dockerfile.exists():
        sys.exit(f"ERROR:\tError building {framework}!\n"
                 f"\tDockerfile not found: {dockerfile}\n")
    print(f"EXEC\tPreparing to run:\n"
          f"\t\t{' '.join(build_command)}")
    if not kwargs.get("dry_run"):
        subprocess.run(build_command)


def init(*args, **kwargs):
    '''Kicks off the build process.'''
    frameworks = [kwargs.get('framework', False)]
    if frameworks == ["all"]:
        frameworks = armory_frameworks
    armory_version = get_tag_version()
    print(f"EXEC:\tRetrieved version {armory_version} from `git` tags.")
    print("EXEC:\tCleaning up...")
    for key in ["framework", "func"]:
        del kwargs[key]
    for framework in frameworks:
        print(f"EXEC:\tBuilding {framework} container.")
        build_worker(framework, armory_version, **kwargs)


if __name__ == "__main__":
    # Ensure correct location
    if not (root_dir / "armory").is_dir():
        sys.exit(f"ERROR:\tEnsure this script is ran from the root of the armory repo.\n"
                 "\tEXAMPLE:\n"
                 f"\t\t$ python3 {script_dir / 'build.py'}")

    # Ensure docker/podman is installed
    if not shutil.which(container_platform):
        sys.exit("ERROR:\tCannot find compatible container on the system.\n"
                 "\tAsk your system administrator to install either `docker` or `podman`.")

    # Parse CLI arguments
    arguments = cli_parser()
    arguments.func(**vars(arguments))
