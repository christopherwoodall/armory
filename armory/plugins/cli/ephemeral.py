'''

'''
import os
import sys

import platform
import importlib

from pathlib import Path
from inspect import getsourcefile, getmembers, isclass


try:
    from armory.plugins.cli import CLI
except Exception as e:
    raise Exception(f"Error importing CLI module from {__file__}!")

from armory.utils import (
    debugging,
    version
)


global __modpath__
__modpath__ = {getsourcefile(lambda:0)}


MIN_PYTHON_VERSION = (3, 7, 0)
BASE_PATH          = Path.cwd()


def get_commands():
    skip_names = ("__init__.py", "__main__.py", "ephemeral.py")
    commands      = { }
    command_files = [f for f in Path(__file__).parent.iterdir() if f.is_file() and f.name not in skip_names]
    for command in command_files:
        commands[command.stem] = {
            "path":   command,
            "module": f"{command.stem.title()}CLI",
            "description": "TODO",
        }
    return commands


# @debugging.trace
def module_loader(module_name: str, filepath: Path) -> class:
    path      = str(filepath.absolute())
    filename  = filepath.name
    name, ext = (filepath.stem, filepath.suffix)

    loader = importlib._bootstrap_external.SourceFileLoader(name, path)
    spec = importlib.util.spec_from_file_location(name, path, loader=loader)

    try:
        module = getattr(importlib._bootstrap._load(spec), module_name, False)
        if module:
            print(type(module))
            return module
        else:
            raise Exception(f"Error importing {module_name} module from {filename}!")
    except:
        raise ImportError(path, sys.exc_info())



def main():
    # Grab a list of commands
    command_list = get_commands()

    # Check python version
    if version.version_tuple(platform.python_version()) < MIN_PYTHON_VERSION:
        print(f"ERROR: Armory requires Python {'.'.join(map(str, MIN_PYTHON_VERSION))} or higher.")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("ERROR: No command given", file=sys.stderr)
        sys.exit(1)

    if (command := sys.argv[1]) not in command_list.keys():
        print(f"ERROR: Unknown command {command}", file=sys.stderr)
        sys.exit(2)


    # TODO:
    command_data   = command_list[command]
    command_module = module_loader(command_data['module'], command_data['path'])
    command_module()

