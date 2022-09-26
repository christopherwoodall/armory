
from armory.cli import Command


class RunCLI(Command):
  name = "run"

  def __init__(self):
    print("RunCLI")

