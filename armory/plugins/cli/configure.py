'''
[plugin]
name        = "configure"
description = "Set up armory and dataset paths."
'''

import argparse

try:
    import armory
except Exception as e:
    raise Exception(f"Error importing CLI module from {__file__}!")

from armory.plugins.cli import CLI


class ConfigureCLI(CLI):
  def processCLI(self, args):
    print("run processCLI")
    print(args)
    if args[1] == "--help":
      ...






# def configure(command_args, prog, description):
#     parser = argparse.ArgumentParser(prog=prog, description=description)
#     _debug(parser)

#     parser.add_argument(
#         "--use-defaults", default=False, action="store_true", help="Use Defaults"
#     )

#     args = parser.parse_args(command_args)
#     armory.logs.update_filters(args.log_level, args.debug)

#     default_host_paths = paths.HostDefaultPaths()

#     config = None

#     if args.use_defaults:
#         config = {
#             "dataset_dir": default_host_paths.dataset_dir,
#             "local_git_dir": default_host_paths.local_git_dir,
#             "saved_model_dir": default_host_paths.saved_model_dir,
#             "tmp_dir": default_host_paths.tmp_dir,
#             "output_dir": default_host_paths.output_dir,
#             "verify_ssl": True,
#         }
#         print("Saving configuration...")
#         save_config(config, default_host_paths.armory_dir)
#         print("Configure successful")
#         print("Configure complete")
#         return

#     elif os.path.exists(default_host_paths.armory_config):
#         response = None
#         while response is None:
#             prompt = f"Existing configuration found: {default_host_paths.armory_config}"
#             print(prompt)

#             response = input("Load existing configuration? [Y/n]")
#             if response in ("Y", "y", ""):
#                 print("Loading configuration...")
#                 config = load_global_config(
#                     default_host_paths.armory_config, validate=False
#                 )
#                 print("Load successful")
#             elif response in ("N", "n"):
#                 print("Configuration not loaded")
#             else:
#                 print(f"Invalid selection: {response}")
#                 response = None
#             print()

#     instructions = "\n".join(
#         [
#             "Configuring paths for armory usage",
#             f'    This configuration will be stored at "{default_host_paths.armory_config}"',
#             "",
#             "Please enter desired target directory for the following paths.",
#             "    If left empty, the default path will be used.",
#             "    Absolute paths (which include '~' user paths) are required.",
#             "",
#         ]
#     )
#     print(instructions)

#     default_dataset_dir = (
#         config["dataset_dir"]
#         if config is not None and "dataset_dir" in config.keys()
#         else default_host_paths.dataset_dir
#     )
#     default_local_dir = (
#         config["local_git_dir"]
#         if config is not None and "local_git_dir" in config.keys()
#         else default_host_paths.local_git_dir
#     )
#     default_saved_model_dir = (
#         config["saved_model_dir"]
#         if config is not None and "saved_model_dir" in config.keys()
#         else default_host_paths.saved_model_dir
#     )
#     default_tmp_dir = (
#         config["tmp_dir"]
#         if config is not None and "tmp_dir" in config.keys()
#         else default_host_paths.tmp_dir
#     )
#     default_output_dir = (
#         config["output_dir"]
#         if config is not None and "output_dir" in config.keys()
#         else default_host_paths.output_dir
#     )

#     config = {
#         "dataset_dir": _get_path("dataset_dir", default_dataset_dir),
#         "local_git_dir": _get_path("local_git_dir", default_local_dir),
#         "saved_model_dir": _get_path("saved_model_dir", default_saved_model_dir),
#         "tmp_dir": _get_path("tmp_dir", default_tmp_dir),
#         "output_dir": _get_path("output_dir", default_output_dir),
#         "verify_ssl": _get_verify_ssl(),
#     }
#     resolved = "\n".join(
#         [
#             "Resolved paths:",
#             f"    dataset_dir:     {config['dataset_dir']}",
#             f"    local_git_dir:   {config['local_git_dir']}",
#             f"    saved_model_dir: {config['saved_model_dir']}",
#             f"    tmp_dir:         {config['tmp_dir']}",
#             f"    output_dir:      {config['output_dir']}",
#             "Download options:",
#             f"    verify_ssl:      {config['verify_ssl']}",
#             "",
#         ]
#     )
#     print(resolved)
#     save = None
#     while save is None:

#         if os.path.isfile(default_host_paths.armory_config):
#             print("WARNING: this will overwrite existing configuration.")
#             print("    Press Ctrl-C to abort.")
#         answer = input("Save this configuration? [Y/n] ")
#         if answer in ("Y", "y", ""):
#             print("Saving configuration...")
#             save_config(config, default_host_paths.armory_dir)
#             print("Configure successful")
#             save = True
#         elif answer in ("N", "n"):
#             print("Configuration not saved")
#             save = False
#         else:
#             print(f"Invalid selection: {answer}")
#         print()
#     print("Configure complete")