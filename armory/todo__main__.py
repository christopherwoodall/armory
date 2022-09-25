import argparse

from importlib.metadata import distribution
# TODO: ...try/catch for py 3.7 support?
#       e.g. importlib_metadata

# TODO:
#    >>>  import armory.utils.container
#    >>>  if container.where_am_i() == "host":
#    >>>      main()
#    >>>  else:
#    >>>      you're in a container bro

__all__ = ('__version__', 'Config')
__version__ = "WIP"
app_name = 'armory'


def main():
    dist      = distribution(app_name)
    entry_map = {ep.name: ep for ep in dist.entry_points if ep.group == 'console_scripts'}


    import sys
    print(sys.argv)
    print(entry_map)

    # Entry points
    #   - cli (default)
    #   - scenario


    # parser = argparse.ArgumentParser(prog=f"python -m {armory}", add_help=False)
    # TODO: should docker be it's own subcommand?
    # parser.add_argument('entry_point', choices=list(entry_map) + ['run', 'configure', 'docker'])
    # args, extra = parser.parse_known_args()

    # main = entry_map[args.entry_point].load()

    # # main([args.entry_point] + extra)
    # main()


if __name__ == '__main__':
    main()
