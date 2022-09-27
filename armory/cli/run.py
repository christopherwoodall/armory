'''
[plugin]
name        = "run"
description = "Run armory from config file"
'''
# [plugin|command]
# name
# description


from armory.cli import Command


class RunCLI(Command):
  name = "run"

  def __init__(self):
    print("RunCLI")

