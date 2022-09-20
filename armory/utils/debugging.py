'''
Misc Developer Tools

'''

import os
import sys
import inspect


def module_path(local_func):
  ''' Returns a module's path given a locally defined function.

  Example:
    >>> __module__ = module_path(lambda:0)
  '''
  return os.path.abspath(inspect.getsourcefile(local_func))


def trace(func):
  def wrapper():
    import pdb; pdb.set_trace()
  return wrapper
