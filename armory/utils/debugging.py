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


def trace():
  ''' Prints the current stack trace.

  Example:
    >>> tracer = trace()
    >>> tracer.start()
  '''
  def tracer(frame, event, arg = None):
    code      = frame.f_code
    func_name = code.co_name
    line_no   = frame.f_lineno
    print(f"FUNC:\t{func_name}()\tEVENT: {event}\tLINE: {line_no} ")
    return tracer

  def start():
    sys.settrace(tracer)

  def stop():
    sys.settrace(None)

  return (start, stop)
