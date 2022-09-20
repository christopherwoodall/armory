#! /usr/bin/env python
# -*- coding: utf-8 -*-
import shutil
from pathlib import Path


class Runtime:
  """
  Detect the execution environment.

  Documentation:
    - https://docs.kernel.org/filesystems/proc.html
    - https://github.com/containers

  Example:
    runtime = Runtime()

  TODO:
    - Turn into functions instead of class.
  """
  supported_runtimes = ('docker', 'podman')
  init_systems = ("systemd", "init")
  docker_oui = "02:42:ac"

  def __init__(self):
    self.runtime = self.execution_enviroment()
    print(self.runtime)


  def execution_enviroment(self):
    """
    TODO: Expand detection to include `--init` flags; e.g.
          `--init /usr/bin/tini`.
    """
    enviroment = {
      "runtime": "host" if self.detect_init_system() else "container"
    }
    self.detect_docker_container()
    if enviroment["runtime"] == "host":
      return {
        **enviroment,
        **self.detect_host_capabilities()
      }
    else:
      return {
        **enviroment,
        **self.detect_container_runtime()
      }
    return enviroment


  def detect_host_capabilities(self):
    # Detect host runtimes and cgroup support.
    #   - https://wiki.archlinux.org/title/cgroups#Documentation
    runtimes = list(filter(lambda cmd: shutil.which(cmd) is not None, self.supported_runtimes))
    cgroup_type = 2 if Path('/sys/fs/cgroup/cgroup.controllers').exists() else 1
    return { "runtimes": runtimes, "cgroup": cgroup_type }


  def detect_init_system(self):
    initsched  = r"/proc/1/sched"
    initcomm   = r"/proc/1/comm"
    initstatus = r"/proc/1/status"

    has_init_system = lambda proc: proc.split(' ')[0] not in self.init_systems

    if not all(list(map(has_init_system, (initsched, initcomm)))):
      return False
    return True


  def detect_container_runtime(self):
    # Docker runtime detection.
    runtime = "docker" if self.detect_docker_container() else "unknown"
    runtime = "podman" if self.detect_podman_container() else runtime
    return { "engine": runtime }


  def detect_docker_container(self):
    # Documentation:
    #   - https://www.kernel.org/doc/Documentation/ABI/testing/sysfs-class-net
    if Path('/.dockerenv').is_file():
      return True
    # Check 2: Check if network interface matches docker OUI.
    is_docker_oui = lambda iface: iface.startswith(self.docker_oui)
    return any([is_docker_oui(Path(iface / "address").read_text()) for iface in Path("/sys/class/net/").iterdir()])


    def detect_podman_container():
      # Documentation:
      #  - https://github.com/containers/podman/blob/main/pkg/env/env.go#L15
      if Path("/run/.containerenv").is_file():
        return True
      # Check 2: Podman enviromental variables
      if "container" in Path("/proc/self/environ").read_text():
        return True

