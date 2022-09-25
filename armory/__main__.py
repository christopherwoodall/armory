import sys
import argparse

try:
    from importlib.metadata import distribution
except ModuleNotFoundError:
    # Python <= 3.7
    from importlib_metadata import distribution  # type: ignore


app_name = 'armory'


def main():
    dist      = distribution(app_name)
    entry_map = {ep.name: ep for ep in dist.entry_points if ep.group == 'console_scripts'}
    main = entry_map['armory-cli'].load()
    main(sys.argv[1:])


if __name__ == '__main__':
    main()
