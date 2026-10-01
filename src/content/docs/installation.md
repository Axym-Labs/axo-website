---
title: Installation
description: Install AxoSim, select a Mamba backend, and verify the command-line tools.
section: Get started
order: 10
---

## Install AxoSim

Use Python 3.10 or newer. Source installation currently requires access to the private [Axym-Labs/axosim repository](https://github.com/Axym-Labs/axosim). Authenticate the GitHub CLI with an account granted repository access, then install in a virtual environment:

```bash
gh repo clone Axym-Labs/axosim
cd axosim
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

The base installation includes PyTorch, NumPy, and the tools for GRU models, Lite populations, data conversion, and evaluation. CUDA execution requires a compatible GPU and PyTorch installation; a CPU environment is sufficient for the small population examples.

## Install the Mamba backend

Official Mamba checkpoints require the fused `mamba-ssm` and `causal-conv1d` backend. From the source checkout, run:

```bash
python -m pip install -e '.[mamba]'
axosim-setup
axosim list-presets
```

The setup command creates local project directories and installs the package unless you pass `--skip-install`. Large datasets are downloaded only when you request `--download-data`. The preset command prints a JSON object containing the available training and evaluation recipes.

The PyTorch Mamba fallback is useful for tests and smoke runs. Its state-dictionary format differs from the fused backend, so load a checkpoint with its recorded backend rather than substituting the fallback. The [model guide](/models/) explains the available profiles and implementation aliases.

## Inspect data setup before running it

```bash
axosim-setup --dry-run --install-kaggle --download-data --convert-raw
```

This prints the proposed installation, download, and conversion steps. Downloads from Kaggle require credentials configured through Kaggle; keep credentials outside version control. See [datasets](/datasets/) for the separate population and intervention releases.

## Verify the installation

```bash
axosim --help
axosim-setup --help
axosim-evaluate-model --help
```

The [command-line reference](/api/cli/) lists every subcommand and option. For AxoBench core metrics, install the [current AxoBench package](https://github.com/Axym-Labs/axobench) in the same environment before following [evaluation](/evaluation/). Its source repository also currently requires access.

## Next steps

Choose a trained-model workflow in [models](/models/), then run [inference](/inference/). To learn the population interface without downloading a checkpoint, start with the small example in [build populations](/populations/).
