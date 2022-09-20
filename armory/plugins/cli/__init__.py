import sys

from abc import ABC, abstractmethod

class CLI(ABC):
  # def __init__(self):
  #   self.args = sys.argv[1:]

  def processCLI(self):
    ...

  def usageCLI(self):
    ...