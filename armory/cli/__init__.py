



class Command:
  name = None
  # parser = argparse.ArgumentParser()

  def add_arguments(self, parser):
    pass

# def cli_builder(positional=None, flags=None, description=None, func=None):
#     parser = argparse.ArgumentParser(description=description)
#     if positional:
#         subparsers = parser.add_subparsers()
#         for arg in positional:
#             _subparser = subparsers.add_parser(arg)
#             # parser.add_argument(*arg[0], **arg[1])
#     if flags:
#         for arg in flags:
#             parser.add_argument(*arg[0], **arg[1])
#     parser.set_defaults(func=func)
#     return parser


# def cli_parser(argv=sys.argv[1:]):
#     parser    = argparse.ArgumentParser("Armory Container Build Script")
#     arguments = (
#         (("-f", "--framework"), dict(
#             choices  = armory_frameworks + ["all"],
#             help     = "Framework to build",
#             required = True,
#         )),
#         (("-b", "--base-tag"), dict(
#             help     = "Version tag for twosixarmory/armory-base",
#             default  = "latest",
#             required = False,
#         )),
#         (("-nc", "--no-cache"), dict(
#             action = "store_true",
#             help   = "Do not use docker cache",
#         )),
#         (("-np", "--no-pull"), dict(
#             action = "store_true",
#             help   = "Do not pull latest base",
#         )),
#         (("-n", "--dry-run"), dict(
#             action = "store_true",
#             help   = "Do not build, only print commands",
#         )),
#         (("-v", "--verbose"), dict(
#             action = "store_true",
#             help   = "Print verbose output",
#         )),
#         (("-p", "--platform"), dict(
#             choices  = ["docker", "podman"],
#             help     ="Print verbose output",
#             default  = container_platform,
#             required = False,
#         )),
#     )
#     for args, kwargs in arguments:
#         parser.add_argument(*args, **kwargs)
#     parser.set_defaults(func=init)
#     return parser.parse_args(argv)
