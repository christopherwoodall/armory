#! /usr/bin/env python

import json

from pathlib import Path

for scenario in Path("./asr_librispeech").glob("**/*.json"):
  print(scenario)
  # scenario_json = json.loads(scenario.read_text())
  # scenario_json["_description"] += " (eval5)"
  # scenario.write_text(json.dumps(scenario_json, indent=2))
