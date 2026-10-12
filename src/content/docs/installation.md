---
title: Installation
description: Install AxoSim, select a Mamba backend, and verify the command-line tools.
section: Get started
order: 10
---

## Install AxoSim

Use Python 3.10 or newer. Install the [PyPI package](https://pypi.org/project/axosim/) in a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install axosim
```

The base installation includes PyTorch, NumPy, and the tools for GRU models, Lite populations, and data conversion. CUDA execution requires a compatible GPU and PyTorch installation; a CPU environment is sufficient for the small population examples.

## Add the Mamba backend and AxoBench

Two extras add optional dependencies:

```bash
python -m pip install 'axosim[mamba,bench]'
axosim-setup --skip-install
axosim list-presets
```

- `mamba` installs the fused `mamba-ssm` and `causal-conv1d` backend that official Mamba checkpoints require. GRU and Lite work does not need it.
- `bench` installs [AxoBench](/axobench/benchmarking/#install-axobench), which `axosim-evaluate-model` uses to score checkpoints.

`axosim-setup` creates local project directories. Pass `--skip-install` after a PyPI installation; without it, the command installs the project directory in editable mode, which is the step for a source checkout. Large datasets are downloaded only when you request `--download-data`, so this sequence prepares an environment without initiating a multi-gigabyte transfer. `list-presets` prints the training and evaluation recipe names you will pass to later commands.

The PyTorch Mamba fallback is useful for tests and smoke runs. Its state-dictionary format differs from the fused backend, so load a checkpoint with its recorded backend rather than substituting the fallback. The [model guide](/models/) explains the available profiles and implementation aliases.

## Install from source

The source repository, [Axym-Labs/axosim](https://github.com/Axym-Labs/axosim), currently requires access. With an account granted access, authenticate the GitHub CLI and install the checkout in editable mode with the development tools:

```bash
gh repo clone Axym-Labs/axosim
cd axosim
python -m pip install -e '.[dev,mamba,bench]'
axosim-setup
```

In a checkout, `axosim-setup` without `--skip-install` reinstalls the checkout in editable mode.

## Inspect data setup before running it

```bash
axosim-setup --dry-run --install-kaggle --download-data --convert-raw
```

This prints the proposed installation, download, and conversion steps. Downloads from Kaggle require credentials configured through Kaggle; keep credentials outside version control. See [choose a dataset](/datasets/) for the AxoBench single-neuron, population, and intervention releases.

## Verify the installation

```bash
axosim --help
axosim-setup --help
axosim-evaluate-model --help
```

The [command-line reference](/api/cli/) lists every subcommand and option. The `bench` extra requires AxoBench 0.2.0 or newer; the [dataset-relative skill rows](/axobench/skill/) and [error anatomy](/axobench/error-anatomy/) need AxoBench 0.2.1, so upgrade with `python -m pip install -U axobench` before following [evaluation](/evaluation/).

## Next steps

Choose a trained-model workflow in [models](/models/), then run [inference](/inference/). To learn the population interface without downloading a checkpoint, start with the small example in [build populations](/populations/).
