



class Dispatcher:
  def __init__(self):
    self.commands = {}


print("dispatcher")

import argparse
import sys



if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
    # print(usage())
    # sys.exit(1)
    print('version')
elif sys.argv[1] in ("-v", "--version", "version"):
    print(f"version")
    # sys.exit(0)

parser = argparse.ArgumentParser(prog="armory") #, usage=usage())
parser.add_argument(
    "command",
    metavar="<command>",
    type=str,
    help="armory command",
    # action=Command,
)
args = parser.parse_args(sys.argv[1:2])
