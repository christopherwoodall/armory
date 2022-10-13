# Needed for double-checked locking
from threading import RLock

import docker

from armory.logs import log, is_progress


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
                break
            elif local_tag == "latest":
                    break
            key = False
        if not key:
            tag = "latest"
            log.info(f"docker pulling from {repo}/{image}:{tag} use '--log=progress' to see status")
            self.rpc.api.pull(f"{repo}/{image}", tag=tag, stream=False)
            log.success(f"pulled {repo}:{tag}")
            key = f"{key}:{tag}"
        return key
