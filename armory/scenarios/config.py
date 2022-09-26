from dataclasses import dataclass

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class Config:
  main: Main
  db: DataBase
  neptune: Neptune
  experiment: Experiment = MISSING


cs = ConfigStore.instance()
# Registering the Config class with the name 'config'.
cs.store(name="config", node=Config)


# class Scenario:
#   name:        str
#   version:     str
#   description: str
#   # model:
#   #  batch_size:

#   # train:
#   #  hparams:
#   #  ckpt_path:

#   # eval:

#   # attack:
#   #   name: str
#   #   module: str
#   #   kwargs: dict

#   # defense:
#   #   name: str
#   #   module: str
#   #   kwargs: dict

#   # metrics:
#   #   name: str
#   #   module: str
#   #   kwargs: dict

