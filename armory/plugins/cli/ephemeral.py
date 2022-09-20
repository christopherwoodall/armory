'''

'''
import os
import re
import sys
import platform
import importlib

from pathlib import Path
from inspect import getmembers, isclass, isfunction

try:
    import tomllib  # Python 3.11
except ImportError:
    import toml     # Python 3.10

try:
    import armory
except Exception as e:
    raise Exception(f"Error importing Armory module from {__file__}!")

from armory.plugins.cli import CLI

from armory.utils import (
    debugging,
    version
)


APP_NAME           = "armory"   # TODO: move to __about__.py or similar. -@woodall
MIN_PYTHON_VERSION = (3, 7, 0)  # TODO: move to __about__.py or similar. -@woodall
BASE_PATH          = Path.cwd() # TODO: Import from CLI module -@woodall


class EphemeralCLI(CLI):
    # TODO: inherited from CLI, but not used. -@woodall
    required_hooks = ("usageCLI", "processCLI")

    def __init__(self, args):
        self.commands = self.locate_commands()
        self.args     = self.resolve(args)


    @classmethod
    def locate_commands(self):
        skip_names = ("__init__.py", "__main__.py", "ephemeral.py")
        commands = { f.stem: {
                "path": f,
                "name": f.stem,
                "module": f"{f.stem.capitalize()}CLI",
                "description": "No description available."
            }
            for f in Path(__file__).parent.iterdir() if f.is_file() and f.name not in skip_names
        }
        return commands


    def resolve(self, args):
        if (command := args[1]) in ("-h", "--help", "help"):
            print(self.usage())
            sys.exit(0)
        elif command not in self.commands.keys():
            print(f"ERROR: Unknown command {command}", file=sys.stderr)
            sys.exit(2)

        return args[1:]


    def dispatch(self):
        command = self.args[0]
        data    = self.commands[command]
        module  = self.module_loader(data['module'], data['path'])

        # TODO: Should the module be loaded in ast for validation? -woodall
        if all(isfunction(getattr(module, hook, False)) for hook in self.required_hooks):
            # try:
            # TODO: Module should inherit args from CLI. -woodall
            if len(self.args) > 1:
                module().processCLI(self.args[1:])
            else:
                # TODO: Show help for command. -@woodall
                partial.processCLI()
            # except Exception as e:
            #     print(f"ERROR: {e}", file=sys.stderr)
            #     sys.exit(1)
        else:
            print(f"ERROR: Missing required hooks in {data['path']}", file=sys.stderr)
            print(f"ERROR: Required hooks: {', '.join(required_hooks)}", file=sys.stderr)
            sys.exit(2)
        return 0


    def usage(self):
        docstring_regex = r'^[\'\"]{3}(?P<docstring>.*?)[\"\']{3}'

        def parse_docstring(filepath, strict = False):
            content = filepath.read_text()
            if (docmatch := re.search(docstring_regex, content, re.DOTALL)) is not None:
                try:
                    return toml.loads(docmatch.group('docstring'))
                except Exception as e:
                    if strict:
                        raise e
            return None

        lines = [
            f"{APP_NAME} <command>\n",
            f"ARMORY Adversarial Robustness Evaluation Test Bed\n",
            f"https://github.com/twosixlabs/armory\n",
            f"Commands:\n",
            # Insert Command Here(index==4)
            f"    -v, --version - get current armory version\n",
            f"Run '{APP_NAME} <command> --help' for more information on a command.\n",
        ]
        line_index = 4

        for command, settings in self.commands.items():
            if (docstring := parse_docstring(settings['path'])) is not None:
                lines.insert(line_index, f"    {command} - {docstring['plugin']['description']}")
                line_index += 1

        return "\n".join(lines)


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


def main() -> int:
    # TODO the run method now returns a status code instead of sys.exit directly
    # the rest of the COMMANDS should conform
    if version.version_tuple(platform.python_version()) < MIN_PYTHON_VERSION:
        print(f"ERROR: Armory requires Python {'.'.join(map(str, MIN_PYTHON_VERSION))} or higher.")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("ERROR: No command given", file=sys.stderr)
        sys.exit(1)

    elif sys.argv[1] in ("-v", "--version", "version"):
        print(f"{armory.__version__}")
        sys.exit(0)

    ephemeral = EphemeralCLI(sys.argv)
    return ephemeral.dispatch()


if __name__ == "__main__":
    sys.exit(main())
