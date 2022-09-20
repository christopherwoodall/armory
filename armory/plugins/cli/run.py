

class RunCLI:
  """run
  --something
  """
  def __init__(self):
    print("run imported")



  def usage(self):
    """
    Usage:
    armory [options]
    armory ( -h | --help )
    armory ( --version )
    Options:
        -a, --all             An optional flaag.
        -b                    Another optional flag.
        -f=FOO, --foo=FOO     An option with an argument.
        -h, --help            Show this help message and exits.
        -V, --version         Print version and copyright information.
    """
    # print(self.usage.__doc__)
    # from docopt import docopt
    # docopt(self.usage.__doc__, version='armory 0.16.0')
    ...
