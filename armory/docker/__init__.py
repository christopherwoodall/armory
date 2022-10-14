# Needed for double-checked locking
from threading import RLock

import docker
import requests

from armory.logs import log, is_progress


# TODO: Not like this...
class ImageMapper:
  def __new__(cls, *args, **kwargs):
      instance_id = hex(id(cls))
      # getattr will dip into base classes, so __dict__ must be used
      instance = cls.__dict__.get(instance_id, None)
      if instance is None:
          rlock = RLock()
          with rlock:
              instance = object.__new__(cls)
              setattr(cls, instance_id, instance)
          instance.init(*args, **kwargs)
      return instance


  def init(self, *args, **kwargs):
      self.rpc = rpc = docker.from_env(version="auto")
      containers = [c for c in rpc.images.list() if len(c.attrs['RepoTags'])]
      self.images = { c.attrs['RepoTags'][i]: c for c in rpc.images.list() for i in range(len(c.attrs['RepoTags'])) }


  @classmethod
  def resolve(cls, image_name):
      instance = getattr(cls, hex(id(cls)), super(ImageMapper, cls).__new__(cls))
      repo, image, tag = instance.sanitize_image_name(image_name)
      docker_image = instance.find_image(repo, image, tag)
      log.info(f"Launching image: {docker_image}")
      return docker_image


  def sanitize_image_name(self, image_name):
      """
      Return the components of user/repo:tag as (repo, image, tag)
          Return the empty string "" for any that do not exist
      """
      image, tag = image_name.split(":") if ":" in image_name else (image_name, self.tag)
      repo, image = image.rsplit("/", 1) if "/" in image_name else ("", image_name)
          # Check that the image is supported
      if image not in self.arsenal:
          raise ValueError("Unsupported Armory Image")
      return repo, image, tag


  def find_image(self, repo, image, tag):
    # TODO: Token/Tag resolution could be better...
    if int(tag[2:4]) > 16:
        image = self.image
    tokens = tag.split(".")
    keys = [key for key in self.images.keys() if self.repo in key and image in key]
    if not keys:
      raise ValueError("Image not found")
    for key in keys:
      local_tag = key.split(":")[1]
      local_tokens = local_tag.split(".")
      if tokens == local_tokens:
        print("Found Exact match")
        break
      elif tokens[:2] == local_tokens[:2]:
        print("Found release version")
        break
      elif [tokens[0], int(tokens[1]) - 1, tokens[2]] == local_tokens:
        print("found older version")
        # log.info(f"reverting to previous release tag image {prev_release}")
        break
      elif local_tag == "latest":
        break
      key = False
    if not key:
        key = self.pull_image(f"{repo}/{image}:latest")
    return key


  def pull_image(self, image):
    image, tag = image.split(":") if ":" in image else (image, "latest")
    log.info(f"docker pulling {image}:{tag} use '--log=progress' to see status")
    try:
      self.rpc.api.pull(f"{image}:{tag}", tag=tag, stream=False)
      log.success(f"pulled {repo}:{tag}")
      return image
    except docker.errors.NotFound:
      log.error(f"Image {image} could not be downloaded")
      raise
    except requests.exceptions.ConnectionError:
      log.error("Docker connection refused. Is Docker Daemon running?")
      raise


#     log.info(f"image {prev_release} not found. downloading...")
#     try:
#         pull_verbose(docker_client, prev_release)
#         return prev_release
#     except docker.errors.NotFound:
#         log.error(f"Image {prev_release} could not be downloaded")
#         raise ValueError(
#             "You are attempting to pull an unpublished armory docker image.\n"
#             "This is likely because you're running armory from a dev branch. "
#             "If you want a stable release with "
#             "published docker images try pip installing 'armory-testbed' "
#             "or using out one of the release branches on the git repository. "
#             "If you'd like to continue working on the developer image please "
#             "build it from source on your machine as described here:\n"
#             "https://armory.readthedocs.io/en/latest/contributing/#development-docker-containers\n"
#             "python docker/build.py --help"
#         )
#     except requests.exceptions.ConnectionError:
#         log.error("Docker connection refused. Is Docker Daemon running?")
#         raise

