"""
Enables programmatic accessing of most recent docker images
"""
from armory.docker import ImageMapper
from armory.logs import log, is_progress
from armory.utils import version


# TODO: Not like this...
class ImageMap(ImageMapper):
    repo = "twosixarmory"
    image = "fortress"
    tag = version.to_docker_tag(version.get_version())
    arsenal = ("pytorch", "pytorch-deepspeech", "tf2", "carla-mot", "fortress")


def ensure_image_present(image_name: str) -> str:
    """
    If image_name is available, return it. Otherwise, pull it from dockerhub.
    """
    log.trace(f"ensure_image_present {image_name}")
    image_name=ImageMap().resolve(image_name)

    return image_name
