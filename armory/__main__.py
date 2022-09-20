import argparse

from importlib.metadata import distribution


APP_NAME = 'armory'

def main():
    dist = distribution(APP_NAME)
    ep_map = {ep.name: ep for ep in dist.entry_points if ep.group == 'console_scripts'}
    print(ep_map)

    parser = argparse.ArgumentParser(prog=f"python -m {APP_NAME}", add_help=False)
    parser.add_argument('entry_point', choices=list(ep_map) + ['test'])
    args, extra = parser.parse_known_args()


    main = ep_map[args.entry_point].load()

    # main([args.entry_point] + extra)
    main()

if __name__ == '__main__':
    main()
