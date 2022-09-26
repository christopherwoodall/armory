import os
import sys
import pathlib


def get_project_root(search_from = __file__, indicators = []):
  """Returns project root folder."""
  indicators   = sum( indicators, [".git", "pyproject.toml"])
  project_root = None
  for path in list(pathlib.Path(search_from).parents):
    for file in indicators:
      if list(path.glob(file)):
        project_root = path
        break
  if not project_root:
    raise FileNotFoundError(f"Project root directory not found.")
  return project_root


def set_project_root(search_from = __file__):
  project_root = get_project_root(search_from = search_from)
  path = str(project_root)
  if not os.path.exists(path):
    raise FileNotFoundError(f"Project root path does not exist: {path}")
  os.environ["PROJECT_ROOT"] = path
  sys.path.insert(0, path)
  os.chdir(path)
  return project_root

