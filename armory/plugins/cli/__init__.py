import sys

from abc     import ABC, abstractmethod
from pathlib import Path
from inspect import getsourcefile


# import armory.logs


global __modpath__
__modpath__ = {getsourcefile(lambda:0)}


APP_NAME           = "armory"   # Python 3.7.0# TODO: move to __about__.py or similar. -@woodall
MIN_PYTHON_VERSION = (3, 7, 0)  # Python 3.7.0# TODO: move to __about__.py or similar. -@woodall


class CLI(ABC):
  def __init__(self):
    # self.args = sys.argv[1:]
    self.base_path = Path.cwd()

  def processCLI(self):
    ...

  def usageCLI(self):
    ...