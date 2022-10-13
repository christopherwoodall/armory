"""
Enables programmatic accessing of most recent docker images
"""
# Needed for double-checked locking
from threading import RLock

import docker
import docker.errors
import requests

import armory
from armory.utils import version
from armory.logs import log, is_progress


class ImageMap:
    repo = "twosixarmory"
    image = "fortress"
    images = ("pytorch", "pytorch-deepspeech", "tf2", "carla-mot", "fortress")
    tag = version.to_docker_tag(armory.__version__)
    query = None
    found = False
    rpc = None

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
        args = list(args) or []

        if len(args) == 1:
            self.query = args.pop(0)

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    def to_srting(self):
        return self.resolve()


    @classmethod
    def resolve(cls, *args, **kwargs):
        instance = getattr(cls, hex(id(cls)), super(ImageMap, cls).__new__(cls))
        found, repo, image, tag = instance.sanitize_image_name(instance.query)
        if found:
            instance.find_image(repo, image, tag)
            print(found)
            print(repo, image, tag)
            log.trace(f"armory.__version__: {instance.tag}")

            instance.repo = repo
            instance.image = image
            instance.tag = tag
        return f"{instance.repo}/{instance.image}:{instance.tag}"


    def sanitize_image_name(self, image_name):
        """
        Return the components of user/repo:tag as (repo, image, tag)
            Return the empty string "" for any that do not exist
        """
        repo, image, tag = self.split_name(image_name)
        # Check that the image is supported
        if image not in self.images:
            raise ValueError("Unsupported Armory Image")
        found = self.found = self.find_image(repo, image, tag)
        return found, repo, image, tag


    def find_image(self, repo, image, tag):
        if not image:
            return

        if int(tag[2:4]) > 16:
           image = self.image

        rpc = self.rpc = self.rpc if self.rpc else docker.from_env(version="auto")
        containers = rpc.images.list()
        tokens = set(tag.split("."))
        best_match = None

        for container in containers:
            repo_tags = container.attrs['RepoTags']

            if len(repo_tags) == 0:
                continue

            for repo_tag in repo_tags:
                local_repo, local_image, local_tag = self.split_name(repo_tag)
                local_tokens = set(local_tag.split("."))

                if not local_image:
                    continue
                if image not in str(local_image):
                    continue

                if local_repo == repo:
                    best_match = container

                if local_tokens == tokens:
                    best_match = container

                if not best_match and len(tokens.intersection(local_tokens)) > len(tokens.intersection((best_match or set()))):
                    best_match = container

                if not best_match and self.text_distance(tag, local_tag) < 0.50:
                    best_match = container

                # if not best_match
                #     # TODO: Search DockerHub
            # TODO: if still no match...
        return best_match


    def split_name(self, image_name):
        """
        Return the components of user/repo:tag as (repo, image, tag)
            Return the empty string "" for any that do not exist
        """
        image, tag = image_name.split(":") if ":" in image_name else (image_name, self.tag)
        repo, image = image.rsplit("/", 1) if "/" in image_name else ("", image_name)
        return repo, image, tag


    def text_distance(self, string1, string2):
        string1, string2 = string1.lower(), string2.lower()
        ascii_lowercase = __import__('string').ascii_lowercase
        total = len(string1) + len(string2)
        error = sum([abs(string1.count(i) - string2.count(i)) for i in ascii_lowercase])
        return (total-error)/total


# def pull_verbose(docker_client, repository, tag=None):
#     """
#     Use low-level docker-py API to show status while pulling docker containers.
#         Attempts to replicate docker command line output if we are showing progress.
#     """
#     if tag is None and ":" in repository:
#         repository, tag = repository.split(":")
#     elif ":" in repository:
#         raise ValueError(
#             f"cannot set tag kwarg and have tag in repository arg {repository}"
#         )
#     elif tag is None:
#         log.info("empty tag is set to latest by API")
#         tag = "latest"

#     if not is_progress():
#         log.info(
#             f"docker pulling from {repository}:{tag} use '--log=progress' to see status"
#         )
#         docker_client.api.pull(repository, tag=tag, stream=False)
#         log.success(f"pulled {repository}:{tag}")
#         return

#     for update in docker_client.api.pull(repository, tag=tag, stream=True, decode=True):
#         tokens = []
#         for key in ("id", "status", "progress"):
#             value = update.get(key)
#             if value is not None:
#                 tokens.append(value)
#         output = ": ".join(tokens)

#         log.info(output)

#     log.success(f"pulled {repository}:{tag}")


def ensure_image_present(image_name: str) -> str:
    """
    If image_name is available, return it. Otherwise, pull it from dockerhub.
    """
    log.trace(f"ensure_image_present {image_name}")
    docker_client = docker.from_env(version="auto")

    print(f"Checking for {image_name}...")
    a=ImageMap(image_name).resolve()
    b=ImageMap(docker_client).resolve(image_name)

    import sys
    sys.exit(0)


#         try:
#             pull_verbose(docker_client, image_name)
#             return image_name
#         except docker.errors.NotFound:
#             log.error(f"Image {image_name} could not be downloaded")
#             raise
#         except requests.exceptions.ConnectionError:
#             log.error("Docker connection refused. Is Docker Daemon running?")
#             raise

#     canon_image_name = get_armory_name(image_name)
#     log.info(f"Retrieved canonical image name for {image_name} as {canon_image_name}")

#     prev_release = last_armory_release(canon_image_name)
#     if canon_image_name != prev_release:  # currently on hashed dev branch
#         if is_image_local(docker_client, canon_image_name):
#             return canon_image_name

#         user, repo, tag = split_name(canon_image_name)
#         tokens = tag.split(".")
#         if len(tokens) == 6:
#             tokens = tokens[:5]
#             tag = ".".join(tokens)
#             clean_canon_image_name = join_name(user, repo, tag)
#             log.info(
#                 f"Current workdir is dirty. Reverting to non-dirty image {clean_canon_image_name}"
#             )
#             if is_image_local(docker_client, clean_canon_image_name):
#                 return clean_canon_image_name

#         log.info(f"reverting to previous release tag image {prev_release}")

#     if is_image_local(docker_client, prev_release):
#         return prev_release

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



# def last_armory_release(image_name: str):
#     """
#     Return the image_name corresponding to the last armory major.minor.patch release
#         If the current image_name is a release, return the current
#     """
#     user, repo, tag = split_name(image_name)
#     if not user or not tag:
#         raise ValueError("Must be a full user/repo:tag docker image_name")
#     tokens = tag.split(".")
#     if len(tokens) == 3:
#         return image_name
#     elif len(tokens) == 4:
#         # remove hash and decrement patch
#         major, minor, patch, _ = tokens
#         patch = int(patch)
#         if patch == 0:
#             raise ValueError(f"Tag {tag}: patch cannot be 0 for SCM with hash appended")
#         patch -= 1
#         patch = str(patch)
#         release_tag = ".".join([major, minor, patch])
#         return join_name(user, repo, release_tag)
#     elif len(tokens) in (5, 6):
#         major, minor, patch, post, ghash = tokens[:5]
#         if len(tokens) == 6:
#             date = tokens[5]
#             if not date.startswith("d20"):
#                 raise ValueError(f"Tag {tag} date must start with 'd20'")
#         if not post.startswith("post"):
#             raise ValueError(f"Tag {tag} post must start with 'post'")
#         if not ghash.startswith("g"):
#             raise ValueError(f"Tag {tag} git hash must start with 'g'")
#         release_tag = ".".join([major, minor, patch])
#         return join_name(user, repo, release_tag)
#     else:
#         raise ValueError(f"Tag {tag} must be in major.minor.patch[.SCM version format]")

