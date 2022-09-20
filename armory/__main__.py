from importlib.metadata import distribution


APP_NAME = 'armory'

def main():
    dist = distribution(APP_NAME)
    ep_map = {ep.name: ep for ep in dist.entry_points if ep.group == 'console_scripts'}
    print(ep_map)


if __name__ == '__main__':
    main()
