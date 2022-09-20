from importlib.metadata import distribution


def main():
    dist = distribution('armory')
    ep_map = {_short_name(ep.name): ep for ep in dist.entry_points if ep.group == 'console_scripts'}
    print(ep_map)


if __name__ == '__main__':
    main()
