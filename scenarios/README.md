# Scenario Configurations

## Organization

The directory structure is modeled after [MITRE | ATLAS](https://atlas.mitre.org/); also see [AdvML Threat Matrix](https://github.com/mitre/advmlthreatmatrix/).


```
┌─ ...
│
├─ scenarios
│   │
│   ├─ 10-reconnaissance
│   │
│   ├─ 20-resource-development
│   │
│   ├─ 30-initial-access
│   │
│   ├─ 40-model-access
│   │
│   ├─ 50-execution
│   │
│   ├─ 60-persistence
│   │
│   ├─ 70-evasion
│   │
│   ├─ 80-discovery
│   │
│   ├─ 90-collection
│   │
│   ├─ 100-attack-staging
│   │
│   ├─ 110-exfiltration
│   │
│   ├─ 120-impact
│   │
│   ├─ 500-defenses
│   │
│   └─ 1000-evaluations
│
└── ...

```


## Setup

```bash
mkdir -p ./scenarios && pushd ./scenarios

SCENARIO_DIRS=(10-reconnaissance 20-resource-development 30-initial-access 40-model-access 50-execution 60-persistence 70-evasion 80-discovery 90-collection 100-attack-staging 110-exfiltration 120-impact 500-defenses 1000-evaluations)

for DIR in "${SCENARIO_DIRS[@]}"; do
    mkdir -p "${DIR}"
    touch "${DIR}/.gitkeep"
done

popd
```
