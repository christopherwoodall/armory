#!/bin/bash
# -------------------------------------------------------------------
# Export a conda environment's packages with their channel tags.
# -------------------------------------------------------------------
#

## conda install -c conda-forge -n base yaml

conda env export > temp-conda.yml

conda env export --from-history > temp-history.yml

echo -e "dependencies:" > temp-list.yml
conda list | grep -wv "#" | awk '{
    if($4 == "") package = $1;
    else if($4 == "pypi") package = "pip:"$1;
    else package = $4":"$1;
    print "  - ",package,"=",$2;
  }' | sort -d >> temp-list.yml


python - << EOF
import yaml
from pathlib import Path

enviroment = {
  "name": "",
  "channels": [],
  "dependencies": [],
  "prefix": ""
}

conda_env     = yaml.safe_load(open("temp-conda.yml"))
conda_history = yaml.safe_load(open("temp-history.yml"))
conda_list    = yaml.safe_load(open("temp-list.yml"))

lists =  [conda_env, conda_history, conda_list]

enviroment['channels'] = list(set().union(*list(map(lambda f: f.get('channels', []),lists))))

pip_packages = []
for pkg in conda_list["dependencies"]:
  channel, name = pkg.split(":") if ":" in pkg else ("", pkg)
  name, version = name.split("=") if "=" in name else (name, "")

  # if name in history_list:
  if channel == "pip":
    pip_packages.append(f"{name}={version}")
  else:
    pkg_str = f"{channel}:{name}={version}" if channel else f"{name}={version}"
    enviroment["dependencies"].append(pkg_str)
enviroment['dependencies'].append(pip_packages)

Path("pytorch-enviroment.yml").write_text(yaml.dump(enviroment))
EOF

