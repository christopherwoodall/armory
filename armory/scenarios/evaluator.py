import os

import hydra

from omegaconf import DictConfig, OmegaConf


os.environ["HYDRA_FULL_ERROR"] = '1'


# TODO: Hydra support for relative paths
# def ingest_config_working_relative_path(func):
#   @hydra.main(config_path="../configs", config_name="config", version_base=None)
#   def inner(dict_config):
#     config = hydra.utils.instantiate(dict_config)
#     func(config)
#   return inner


# TODO: Should probably use the compose API?
#       https://hydra.cc/docs/advanced/compose_api/
@hydra.main(version_base=None, config_path=".", config_name="scenario-config")
def main(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    main()


# executor.py
# >>> import armory.scenarios.evaluator
# >>> input_scenario + cli_args => validator(base_config, new_config) => scenario_runner()
#
# python -m armory.scenarios.evaluator --scenario cifar10.yaml +scenario.model.batch_size=64
#
