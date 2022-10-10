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

# from armory.__main__ import run
from armory.scenarios.main import get as get_scenario


# Marks all tests in this file as `end_to_end`
pytestmark = pytest.mark.end_to_end


# TODO: Turn into a block-list
block_list = [

]
skip = [
    # 'carla_video_tracking.json',
    # "so2sat_eo_masked_pgd.json",
    # "asr_librispeech_entailment.json",
    # "poisoning_gtsrb_dirty_label.json",
    # "carla_multimodal_object_detection.json",
    # "xview_robust_dpatch.json",
    # "asr_librispeech_targeted.json",
    # "poisoning_cifar10_witches_brew.json",
    # "speaker_id_librispeech.json",
    # "ucf101_pretrained_masked_pgd_undefended.json",
    # "ucf101_baseline_pretrained_targeted.json",
    # "ucf101_baseline_finetune.json",
    # "ucf101_pretrained_masked_pgd_defended.json",
    # "ucf101_pretrained_frame_saliency_defended.json",
    # "ucf101_pretrained_flicker_defended.json",
    # "ucf101_pretrained_frame_saliency_undefended.json",
    # "ucf101_pretrained_flicker_undefended.json",
    # "resisc10_poison_dlbd.json",
    # "gtsrb_scenario_clbd_defended.json",
    # "gtsrb_scenario_clbd.json",
    # "gtsrb_scenario_clbd_bullethole.json",
    # "apricot_frcnn.json",
    # "apricot_frcnn_defended.json",
    # "dapricot_frcnn_masked_pgd.json",
    "mnist_baseline.json",
    # "so2sat_sar_masked_pgd_undefended.json",
    # "so2sat_sar_masked_pgd_defended.json",
    # "so2sat_eo_masked_pgd_undefended.json",
    # "so2sat_eo_masked_pgd_defended.json",
    # "librispeech_asr_snr_targeted.json",
    # "librispeech_asr_pgd_undefended.json",
    # "librispeech_asr_pgd_defended.json",
    # "librispeech_asr_pgd_multipath_channel_undefended.json",
    # "librispeech_asr_imperceptible_undefended.json",
    # "librispeech_asr_imperceptible_defended.json",
    # "librispeech_asr_kenansville_undefended.json",
    # "librispeech_asr_snr_undefended.json",
    # "librispeech_asr_kenansville_defended.json",
    # "xview_frcnn_masked_pgd_undefended.json",
    # "xview_frcnn_robust_dpatch_defended.json",
    # "xview_frcnn_targeted.json",
    # "xview_frcnn_sweep_patch_size.json",
    # "xview_frcnn_robust_dpatch_undefended.json",
    # "xview_frcnn_masked_pgd_defended.json",
    "cifar10_baseline.json",
    # "librispeech_baseline_sincnet_snr_pgd.json",
    # "librispeech_baseline_sincnet.json",
    # "librispeech_baseline_sincnet_targeted.json",
    # "resisc45_baseline_densenet121_cascade.json",
    # "resisc45_baseline_densenet121_finetune.json",
    # "resisc45_baseline_densenet121_sweep_eps.json",
    # "resisc45_baseline_densenet121_targeted.json",
    # "resisc45_baseline_densenet121.json",
    # "gtsrb_dlbd_baseline_keras.json",
    # "gtsrb_witches_brew.json",
    # "cifar10_poison_dlbd.json",
    # "cifar10_witches_brew.json",
    # "gtsrb_dlbd_baseline_pytorch.json",
    # "cifar10_dlbd_watermark_spectral_signature_defense.json",
    # "cifar10_dlbd_watermark_perfect_filter.json",
    # "cifar10_dlbd_watermark_undefended.json",
    # "cifar10_dlbd_watermark_random_filter.json",
    # "cifar10_dlbd_watermark_activation_defense.json",
    # "cifar10_witches_brew_activation_defense.json",
    # "cifar10_witches_brew_random_filter.json",
    # "cifar10_witches_brew_undefended.json",
    # "cifar10_witches_brew_perfect_filter.json",
    # "cifar10_witches_brew_spectral_signature_defense.json",
    # "gtsrb_clbd_peace_sign_random_filter.json",
    # "gtsrb_clbd_peace_sign_spectral_signature_defense.json",
    # "gtsrb_clbd_peace_sign_activation_defense.json",
    # "gtsrb_clbd_peace_sign_undefended.json",
    # "gtsrb_clbd_peace_sign_perfect_filter.json",
    # "gtsrb_clbd_bullet_holes_random_filter.json",
    # "gtsrb_clbd_bullet_holes_perfect_filter.json",
    # "gtsrb_clbd_bullet_holes_spectral_signature_defense.json",
    # "gtsrb_clbd_bullet_holes_activation_defense.json",
    # "gtsrb_clbd_bullet_holes_undefended.json",
    # "gtsrb_dlbd_peace_sign_undefended.json",
    # "gtsrb_dlbd_peace_sign_random_filter.json",
    # "gtsrb_dlbd_peace_sign_activation_defense.json",
    # "gtsrb_dlbd_peace_sign_perfect_filter.json",
    # "gtsrb_dlbd_peace_sign_spectral_signature_defense.json",
    # "gtsrb_dlbd_bullet_holes_activation_defense.json",
    # "gtsrb_dlbd_bullet_holes_spectral_signature_defense.json",
    # "gtsrb_dlbd_bullet_holes_perfect_filter.json",
    # "gtsrb_dlbd_bullet_holes_random_filter.json",
    # "gtsrb_dlbd_bullet_holes_undefended.json",
    # "gtsrb_witches_brew_random_filter.json",
    # "gtsrb_witches_brew_activation_defense.json",
    # "gtsrb_witches_brew_spectral_signature_defense.json",
    # "gtsrb_witches_brew_perfect_filter.json",
    # "gtsrb_witches_brew_undefended.json",
    # "carla_obj_det_multimodal_adversarialpatch_undefended.json",
    # "carla_obj_det_multimodal_dpatch_defended.json",
    # "carla_obj_det_multimodal_dpatch_undefended.json",
    # "carla_obj_det_dpatch_undefended.json",
    # "carla_obj_det_dpatch_defended.json",
    # "carla_obj_det_multimodal_adversarialpatch_defended.json",
    # "carla_obj_det_adversarialpatch_undefended.json",
    # "carla_video_tracking_goturn_advtextures_defended.json",
    # "carla_video_tracking_goturn_advtextures_undefended.json",
    # "defended_untargeted_snr_pgd.json",
    # "untargeted_snr_pgd.json",
    # "entailment.json",
    # "defended_targeted_snr_pgd.json",
    # "defended_entailment.json",
    # "targeted_snr_pgd.json",
    "cifar_short.json",
    # # "carla_short.json",
]


@pytest.mark.usefixtures("pass_parameters")
class TestScenarios(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def capsys(self, capsys):
        self.capsys = capsys


    def test_scenarios(self):
        trapped_in_ci = getattr(self, "github_ci", False)
        scenario_path = [Path(self.scenario_path)] if hasattr(self, "scenario_path") else []
        scenario_configs = Path("scenario_configs")
        host_paths = paths.runtime_paths()
        result_path = host_paths.output_dir

        # Setup Armory paths
        paths.set_mode("host")

        with self.capsys.disabled():

            if not len(scenario_path):
                scenario_path = [Path(f) for f in list(scenario_configs.glob("**/*.json")) if f.name in skip]

            for scenario in scenario_path:
                scenario_log_path, scenario_log_data = self.run_scenario(scenario)

                # TODO:
                # # Ensure the file exists.
                # assert scenario_log_path.exists(), f"Missing result file: {scenario_log_path}"

                # # Ensure the file is not empty.
                # assert scenario_log_path.stat().st_size > 0, f"Empty result file: {scenario_log_path}"

                # # Check that the results were written.
                # with capsys.disabled():
                #     # Simple object comparison.
                #     assert (ordered(json.loads(Path(scenario_log_path).read_text())) == ordered(scenario_log_data)), "Scenario log data does not match."

                if trapped_in_ci:
                    # TODO: Write output to sensible location
                    results_path = Path('/tmp/results')
                    ci_filename = f"{scenario.stem}-{scenario_log_path.stem}.json"
                    results_path.mkdir(parents=True, exist_ok=True)
                    Path(results_path / ci_filename).write_text(json.dumps(scenario_log_data))


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
