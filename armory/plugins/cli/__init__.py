import sys
from abc import ABC, abstractmethod


class CLI(ABC):
  def __init__(self):
    args = sys.argv[1:]
    if len(args) == 0:
        print("I'm afraid I can't do that, Dave.")
        return


class Command:
  def __init__(self, name, description, func):
    self.name = name
    self.description = description
    self.func = func


class CommandGroup:
  def __init__(self, name, description):
    self.name = name
    self.description = description
    self.commands = []

  def add_command(self, command):
    self.commands.append(command)

  def get_command(self, name):
    for command in self.commands:
      if command.name == name:
        return command
    return None

  def get_commands(self):
    return self.commands



