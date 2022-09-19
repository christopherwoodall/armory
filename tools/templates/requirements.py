#! /usr/bin/env python3

from pathlib import Path
import yaml

# requirements = Path("requirements.txt").read_text().splitlines()

packages = Path("requirement.yml")
packages = yaml.safe_load(packages.read_text())

print(packages)

# Genreate requirements.txt or environment.yml

