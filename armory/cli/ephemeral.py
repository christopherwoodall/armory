import sys
import argparse

from pathlib import Path


def locate_commands():
    skip_names = ("__init__.py", "__main__.py", "ephemeral.py", "old_cli.py")
    commands = { f.stem: {
            "path": f,
            "name": f.stem,
            "module": f"{f.stem.capitalize()}CLI",
            "description": "No description available."
        }
        for f in Path(__file__).parent.iterdir() if f.is_file() and f.name not in skip_names
    }
    return commands


# def dispatch(self):
#     command = self.args[0]
#     data    = self.commands[command]
#     module  = self.module_loader(data['module'], data['path'])

#     # TODO: Should the module be loaded in ast for validation? -woodall
#     if all(isfunction(getattr(module, hook, False)) for hook in self.required_hooks):
#         # try:
#         # TODO: Module should inherit args from CLI. -woodall
#         if len(self.args) > 1:
#             module().processCLI(self.args[1:])
#         else:
#             # TODO: Show help for command. -@woodall
#             partial.processCLI()
#         # except Exception as e:
#         #     print(f"ERROR: {e}", file=sys.stderr)
#         #     sys.exit(1)
#     else:
#         print(f"ERROR: Missing required hooks in {data['path']}", file=sys.stderr)
#         print(f"ERROR: Required hooks: {', '.join(required_hooks)}", file=sys.stderr)
#         sys.exit(2)
#     return 0


# def module_loader(self, module_name: str, filepath: Path):
#     path   = str(filepath.absolute())
#     loader = importlib._bootstrap_external.SourceFileLoader(filepath.stem, path)
#     spec   = importlib.util.spec_from_file_location(filepath.stem, path, loader=loader)
#     try:
#         module = getattr(importlib._bootstrap._load(spec), module_name, False)
#         if module and isclass(module):
#             return module
#         else:
#             raise Exception(f"Error importing {module_name} module from {filepath}!")
#     except:
#         raise ImportError(path, sys.exc_info())


# def usage(self):
#     docstring_regex = r'^[\'\"]{3}(?P<docstring>.*?)[\"\']{3}'

#     def parse_docstring(filepath, strict = False):
#         content = filepath.read_text()
#         if (docmatch := re.search(docstring_regex, content, re.DOTALL)) is not None:
#             try:
#                 return toml.loads(docmatch.group('docstring'))
#             except Exception as e:
#                 if strict:
#                     raise e
#         return None

#     lines = [
#         f"{APP_NAME} <command>\n",
#         f"ARMORY Adversarial Robustness Evaluation Test Bed\n",
#         f"https://github.com/twosixlabs/armory\n",
#         f"Commands:\n",
#         # Insert Command Here(index==4)
#         f"    -v, --version - get current armory version\n",
#         f"Run '{APP_NAME} <command> --help' for more information on a command.\n",
#     ]
#     line_index = 4

#     for command, settings in self.commands.items():
#         if (docstring := parse_docstring(settings['path'])) is not None:
#             lines.insert(line_index, f"    {command} - {docstring['plugin']['description']}")
#             line_index += 1

#     return "\n".join(lines)


def main(args=sys.argv[1:]):
    commands = locate_commands()
    print(args)
    if len(args) < 1 or args[0] not in commands:
        # TODO: Print USAGE
        print("Command not found.")
        return

    # TODO: Dispatch command with args


if __name__ == "__main__":
    # # Ensure correct location
    # if not (root_dir / "armory").is_dir():
    #     sys.exit(f"ERROR:\tEnsure this script is ran from the root of the armory repo.\n" \
    #              f"\tEXAMPLE:\n"                                                          \
    #              f"\t\t$ python3 {script_dir / 'build.py'}")

    # # Ensure docker/podman is installed
    # if not shutil.which(container_platform):
    #     sys.exit(f"ERROR:\tCannot find compatible container on the system.\n" \
    #              f"\tAsk your system administrator to install either `docker` or `podman`.")

    main()

