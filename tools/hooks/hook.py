from hatchling.plugin import hookimpl

from .plugin import BuildEnvironment


@hookimpl
def hatch_register_environment():
    return BuildEnvironment
