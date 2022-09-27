import re
import sys
import argparse

from pathlib import Path




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




try:
    import tomllib  # Python 3.11
except ImportError:
    import toml     # Python 3.10

from armory.cli import CLI


class EmphemeralCLI(CLI):
    name = "armory"
    description = "ARMORY Adversarial Robustness Evaluation Test Bed"

    def setup(self):
        self.commands = self.locate_commands()

        # self.config(
        #     flags = [
        #         (["-v", "--version"], {
        #             "action":  "version",
        #             "help":    "Show the version and exit.",
        #             "version": self.version
        #         }),
        #         # (["-h", "--help"], {
        #         #     "help":    "Show help message.",
        #         #     "action":  "help",
        #         #     "default": argparse.SUPPRESS,
        #         #     "dest":    "help"
        #         # }),
        #     ],
        #     # positional=[
        #     #     {
        #     #         'title': cmd,
        #     #         'description':values['description']
        #     #     }
        #     #     for cmd, values in self.commands.items()
        #     # ],
        #     # actions=[]
        #     # func=main
        # )



    def run(self):
        # super(EmphemeralCLI, self).<METHOD>()
        ...


    def usage(self):

        docstring_regex = r'^[\'\"]{3}(?P<docstring>.*?)[\"\']{3}'
        commands = self.locate_commands()

        def parse_docstring(filepath, strict = False):
            content  = filepath.read_text()
            docmatch = re.search(docstring_regex, content, re.DOTALL)
            if docmatch is not None:
                try:
                    return toml.loads(docmatch.group('docstring'))
                except Exception as e:
                    if strict:
                        raise e
            return None

        lines = [
            f"armory <command>\n",
            f"ARMORY Adversarial Robustness Evaluation Test Bed\n",
            f"https://github.com/twosixlabs/armory\n",
            f"Commands:\n",
            # Insert Command Here(index==4)
            f"    -v, --version - get current armory version\n",
            f"Run 'armory <command> --help' for more information on a command.\n",
        ]
        line_index = 4

        for command, settings in commands.items():
            docstring = parse_docstring(settings['path'])
            if docstring is not None:
                lines.insert(line_index, f"    {command} - {docstring['plugin']['description']}")
                line_index += 1

        return "\n".join(lines)




    def locate_commands(self):
        skip_names = ("__init__.py", "__main__.py", "ephemeral.py", "old_cli.py")
        commands   = { f.stem: {
                "path": f,
                "name": f.stem,
                "module": f"{f.stem.capitalize()}CLI",
                "description": "No description available."
            }
            for f in Path(__file__).parent.iterdir() if f.is_file() and f.name not in skip_names
        }
        return commands









def main(args=sys.argv[1:]):
    # EmphemeralCLI()
    EmphemeralCLI.init()
    # .launch()
    # .enter()
    # .trigger()
    # .setup()
    # .run()
    # .initiate()



if __name__ == "__main__":
    # # Ensure docker/podman is installed
    # if not shutil.which(container_platform):
    #     sys.exit(f"ERROR:\tCannot find compatible container on the system.\n" \
    #              f"\tAsk your system administrator to install either `docker` or `podman`.")

    main()
