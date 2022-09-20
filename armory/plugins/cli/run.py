'''

'''
try:
    from armory.plugins.cli import CLI
except Exception as e:
    raise Exception(f"Error importing CLI module from {__file__}!")

from armory.utils import debugging


class RunCLI(CLI):

  def __init__(self):
    print("run imported")


  def processCLI(self):
    print("run processCLI")


  def usageCsLI(self):
    '''
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
    '''
    # print(self.usage.__doc__)
    # from docopt import docopt
    # docopt(self.usage.__doc__, version='armory 0.16.0')
    print("usageCLI")