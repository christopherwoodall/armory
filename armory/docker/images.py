"""
Enables programmatic accessing of most recent docker images
"""
# import docker
# import docker.errors
# import requests

import armory
from armory.utils import version
from armory.docker import ImageMapper
from armory.logs import log, is_progress


class ImageMap(ImageMapper):
    repo = "twosixarmory"
    image = "fortress"
    arsenal = ("pytorch", "pytorch-deepspeech", "tf2", "carla-mot", "fortress")
    tag = version.to_docker_tag(armory.__version__)

    @classmethod
    def resolve(cls, image_name):
        instance = getattr(cls, hex(id(cls)), super(ImageMapper, cls).__new__(cls))
        repo, image, tag = instance.sanitize_image_name(image_name)
        return instance.find_image(repo, image, tag)



def ensure_image_present(image_name: str) -> str:
    """
    If image_name is available, return it. Otherwise, pull it from dockerhub.
    """
    log.trace(f"ensure_image_present {image_name}")
    # docker_client = docker.from_env(version="auto")

    print(f"Checking for {image_name}...")
    image_name=ImageMap().resolve(image_name)

    print(image_name)

    import sys
    sys.exit(0)
