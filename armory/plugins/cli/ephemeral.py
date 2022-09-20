'''

'''
import os
import sys

import platform
import importlib

from pathlib import Path
from inspect import getsourcefile, getmembers, isclass, isfunction


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


class EphemeralCLI(CLI):
    def __init__(self, args):
        self.commands = self.locate_commands()
        self.args     = self.resolve(args)


    def resolve(self, args):
        if (command := args[1]) not in self.commands.keys():
            print(f"ERROR: Unknown command {command}", file=sys.stderr)
            sys.exit(2)
        return args[1:]


    def dispatch(self):
        command = self.args[0]
        data    = self.commands[command]
        module  = self.module_loader(data['module'], data['path'])

        required_hooks = ("usageCLI", "processCLI")

        if all(isfunction(getattr(module, hook, False)) for hook in required_hooks):
            print('processCLI found!!!')
            # module()     # module(self.args.pop())
            # module().processCLI()
            # module().usageCLI()
            # print(module.usage.__doc__)
        else:
            print(f"ERROR: Missing required hooks in {data['path']}", file=sys.stderr)
            print(f"ERROR: Required hooks: {', '.join(required_hooks)}", file=sys.stderr)
            sys.exit(2)
        return 0


    def usage(self):
        # loop commands, get __doc__ and print?
        # import pprint
        # pp = pprint.PrettyPrinter(indent=2)
        # pp.pprint(getmembers(module))
        ...


    def locate_commands(self):
        skip_names = ("__init__.py", "__main__.py", "ephemeral.py")
        commands = { f.stem: {
                "path": f,
                "name": f.name,
                "module": f"{f.stem.capitalize()}CLI",
                "description": "No description available."
            }
            for f in Path(__file__).parent.iterdir() if f.is_file() and f.name not in skip_names
        }
        return commands


    # @debugging.trace
    def module_loader(self, module_name: str, filepath: Path):
        path   = str(filepath.absolute())
        loader = importlib._bootstrap_external.SourceFileLoader(filepath.stem, path)
        spec   = importlib.util.spec_from_file_location(filepath.stem, path, loader=loader)
        try:
            module = getattr(importlib._bootstrap._load(spec), module_name, False)
            if module and isclass(module):
                return module
            else:
                raise Exception(f"Error importing {module_name} module from {filepath}!")
        except:
            raise ImportError(path, sys.exc_info())


def main():
    if version.version_tuple(platform.python_version()) < MIN_PYTHON_VERSION:
        print(f"ERROR: Armory requires Python {'.'.join(map(str, MIN_PYTHON_VERSION))} or higher.")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("ERROR: No command given", file=sys.stderr)
        sys.exit(1)

    return EphemeralCLI(sys.argv).dispatch()
