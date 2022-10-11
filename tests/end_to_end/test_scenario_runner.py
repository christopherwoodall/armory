#!/usr/bin/env false
# -*- coding: utf-8 -*-

"""End-to-end pytest fixtures for testing scenario configs.

Example:
    $ pip install -e .[developer,engine,math,datasets,pytorch]
    $ pytest --verbose --show-capture=no tests/end_to_end/test_scenario_runner.py
    $ pytest --verbose --show-capture=no tests/end_to_end/test_scenario_runner.py --scenario-path scenario_configs/cifar10_baseline.json
    $ clear; pytest --verbose tests/end_to_end/test_scenario_runner.py --scenario-path scenario_configs/cifar10_baseline.json --github-ci
"""

import re
import json
import pytest
import unittest

from pathlib import Path

from armory import paths

from armory.__main__ import run
from armory.scenarios.main import get as get_scenario


# Marks all tests in this file as `end_to_end`
pytestmark = pytest.mark.end_to_end


# TODO: Turn into a block-list
block_list = [
    "./scenario_configs/eval6/carla_mot/carla_mot_dpatch_defended.json", # waiting on #1655
]



@pytest.mark.usefixtures("pass_parameters")
class TestScenarios(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def capsys(self, capsys):
        self.capsys = capsys


    def test_scenarios(self):
        capsys = self.capsys

        trapped_in_ci = getattr(self, "github_ci", False)
        scenario_path = [Path(self.scenario_path)] if hasattr(self, "scenario_path") else []
        scenario_configs = Path("scenario_configs")
        host_paths = paths.runtime_paths()
        result_path = host_paths.output_dir

        # Setup Armory paths
        paths.set_mode("host")

        with capsys.disabled():

            if not len(scenario_path):
                scenario_path = [Path(f) for f in list(scenario_configs.glob("**/*.json")) if f.name not in block_list]


            for scenario in scenario_path:

                if scenario not in block_list:
                    # scenario_log_path, scenario_log_data = self.run_scenario(scenario)
                    armory_flags = [scenario.as_posix(), "--no-docker", "--check", "--no-gpu"]
                    run(armory_flags, "armory", None)
                    out, err = capsys.readouterr()
                    print(out)
                    print(err)


                # TODO:
                # # Ensure the file exists.
                # assert scenario_log_path.exists(), f"Missing result file: {scenario_log_path}"

                # # Ensure the file is not empty.
                # assert scenario_log_path.stat().st_size > 0, f"Empty result file: {scenario_log_path}"

                # # Check that the results were written.
                # with capsys.disabled():
                #     # Simple object comparison.
                #     assert (ordered(json.loads(Path(scenario_log_path).read_text())) == ordered(scenario_log_data)), "Scenario log data does not match."

                # #     if trapped_in_ci:
                # #         # TODO: Write output to sensible location
                # #         results_path = Path('/tmp/results')
                # #         ci_filename = f"{scenario.stem}-{scenario_log_path.stem}.json"
                # #         results_path.mkdir(parents=True, exist_ok=True)
                # #         Path(results_path / ci_filename).write_text(json.dumps(scenario_log_data))


    def run_scenario(self, scenario_path):
        runner = get_scenario(scenario_path, check_run=True).load()
        runner.evaluate()
        scenario_log_path, scenario_log_data = runner.save()
        return runner.save()


# TODO:
# def test_results(capsys):
#     scores = {}
#     model_results = json.loads(test_data.read_text())
#     result_tolerance = 0.05
#     for result in results_path.glob("**/*.json"):
#         result_json = json.loads(result.read_text())
#         results = result_json['results']
#         filepath = result_json['config']['sysconfig']['filepath']
#         check_used = result_json['config']['sysconfig']['use_gpu']
#         gpu_used = result_json['config']['sysconfig']['use_gpu']
#         adversarial_scores = results['adversarial_mean_categorical_accuracy']
#         benign_scores      = results['benign_mean_categorical_accuracy']
#         adversarial_median = statistics.median(adversarial_scores)
#         benign_median      = statistics.median(benign_scores)
#         with capsys.disabled():
#             print("\n\n")
#             print(math.isclose(adversarial_median, benign_median, abs_tol = result_tolerance))
#             print(all((
#                 math.isclose(bt, at, abs_tol = result_tolerance) for at, bt in
#                     zip(adversarial_scores, benign_scores)
#                     if at != 0.0 and bt != 0.0
#             )))
#         # SETUP
#         scores[filepath] = {
#             'delta': 0,
#             'results': [
#                 {
#                 'tolerance': result_tolerance,
#                 'adversarial_median': adversarial_median,
#                 'benign_median': benign_median,
#                 'check_used': check_used,
#                 'gpu_used': gpu_used
#                 }
#             ]
#         }
#         # /SETUP
#     with capsys.disabled():
#         print(json.dumps(scores, indent=2))
