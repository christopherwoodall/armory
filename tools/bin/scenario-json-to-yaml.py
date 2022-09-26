#! /usr/bin/env python3

import os
import json

from pathlib import Path

from omegaconf import OmegaConf


def convert_scenario_to_yaml(scenario: Path) -> str:
    """Convert a JSON formatted scenario file into a YAML string."""
    scenario_data = OmegaConf.load(scenario)
    scenario_yml  = OmegaConf.to_yaml(scenario_data)
    return scenario_yml


def process_json_scenarios(input_path: Path, output_path: Path, yaml_ext: str = 'yml') -> None:
    """Process all JSON formatted scenario files in a given directory."""
    json_files = [f for f in scenarios_json_path.glob("**/*.json") if f.is_file()]

    for filepath in json_files:
        print(f"Generating {filepath.stem}")
        file_name = filepath.stem
        out_path  = Path(str(filepath.parents[0]).replace(str(input_path), str(output_path)))
        yaml_path = out_path / f"{file_name}.{yaml_ext}"
        yaml_data = convert_scenario_to_yaml(filepath)
        yaml_config = OmegaConf.create(yaml_data)

        if not out_path.exists():
            out_path.mkdir(parents=True)
        OmegaConf.save(yaml_config, yaml_path)


scenarios_json_path = Path("configs/scenarios/json")
scenarios_yml_path  = Path("configs/scenarios/yml")

process_json_scenarios(scenarios_json_path, scenarios_yml_path)

