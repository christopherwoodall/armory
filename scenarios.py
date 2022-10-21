#!/usr/bin/env python

from pathlib import Path

scenarios_path = Path('scenarios')

scenarios = [
  { "tactic": "reconnaissance",
    "progression_level": 10,
  },

  { "tactic": "resource-development",
    "progression_level": 20,
  },

  { "tactic": "initial-access",
    "progression_level": 30,
  },

  { "tactic": "model-access",
    "progression_level": 40,
  },

  { "tactic": "execution",
    "progression_level": 50,
  },

  { "tactic": "persistence",
    "progression_level": 60,
  },

  { "tactic": "evasion",
    "progression_level": 70,
  },

  { "tactic": "discovery",
    "progression_level": 80,
  },

  { "tactic": "collection",
    "progression_level": 90,
  },

  { "tactic": "attack-staging",
    "progression_level": 100,
  },

  { "tactic": "exfiltration",
    "progression_level": 110,
  },

  { "tactic": "impact",
    "progression_level": 120,
  },

  { "tactic": "defenses",
    "progression_level": 500,
  },

  { "tactic": "evaluations",
    "progression_level": 1000,
  }
]


for scenario in scenarios:
  scenario_path = Path(scenarios_path / f"{scenario['progression_level']}-{scenario['tactic']}")
  scenario_path.mkdir(parents=True, exist_ok=True)
