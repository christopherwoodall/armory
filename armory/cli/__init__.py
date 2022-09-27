# import os
import sys
import argparse
import importlib

from abc import ABC, abstractmethod
from inspect import getmembers, isclass, isfunction
from pathlib import Path

try:
  # https://github.com/kislyuk/argcomplete
  import argcomplete
  HAS_ARGCOMPLETE = True
except ImportError:
  HAS_ARGCOMPLETE = False


try:
    import armory
except Exception as e:
    raise Exception(f"Error importing Armory module from {__file__}!")


# if sys.version_info < (3, 7):
#     raise SystemExit(
#         'ERROR: Armory requires Python 3.7 or newer. '
#         'Current version: %s' % ''.join(sys.version.splitlines())
#     )


class CLI(ABC):
  name        = None
  description = None
  version     = armory.__version__

  def __init__(self, args, callback=None):
    if not args:
      raise ValueError('A non-empty list for args is required')

    if len(args) <= 1:
      print(f"{self.usage()}")
      sys.exit(0)

    if len(args) >= 1:
      if args[1] in ('-h', '--help'):
        print(f"{self.usage()}")
      if args[1] in ('-v', '--version'):
         print(f"{self.version}")
      sys.exit(0)

    self.cmd_path = Path.cwd()
    self.args     = args
    self.parser   = None
    self.callback = callback


  @classmethod
  def init(cls, args=None, exit_code=0):
    if args is None:
      args = sys.argv
    try:
      cli   = cls(args)
      setup = cli.setup()
      exit_code = cli.run()
    except KeyboardInterrupt:
      # log.warn("Execution interrupted(KeyboardInterrupt)")
      exit_code = 1
    except Exception as e:
      # log.error(e)
      # TODO: Show stacktrace(in debug mode), start `pdb`, and enter post mortem.
      exit_code = 1
    sys.exit(exit_code)


  @abstractmethod
  def setup():
    raise NotImplementedError("Method not implemented!")


  @abstractmethod
  def run():
    raise NotImplementedError("Method not implemented!")


  @abstractmethod
  def usage():
    raise NotImplementedError("Method not implemented!")


  def config(self, positional=None, flags=None, func=None):
    parser = self.parser = argparse.ArgumentParser(prog=self.name, description=self.description)
    if func:
      parser.set_defaults(func=init)
    if positional:
      for position in positional:
        subparsers = parser.add_subparsers(**position)
    if flags:
      for args, kwargs in flags:
        parser.add_argument(*args, **kwargs)
    if HAS_ARGCOMPLETE:
      argcomplete.autocomplete(self.parser)
    self.args = self.parser.parse_args(self.args)


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

