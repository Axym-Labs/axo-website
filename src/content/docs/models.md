---
title: Choose a model
description: Select a GRU, Mamba, or Lite workflow and load the correct implementation.
section: Choose a model
order: 20
---

## Model families

AxoSim provides full single-neuron sequence models and a compact population neuron. Use a trained full model to predict spikes and somatic voltage from native input traces. Use AxoSim-Lite when constructing a differentiable population with separate behavior, morphology, and synaptic parameters.

| Family | Intended workflow | Public implementation |
| --- | --- | --- |
| AxoSim-Mamba | Full sequence prediction with a selective state-space temporal core | `axosim.axomamba.AxoMamba` |
| Named AxoSim-GRU profiles | Full sequence prediction with a GRU temporal core | `axosim.temporal_core.AxoTemporalModel`, created by `create_axosim_profile` |
| AxoSim-Lite | Causal four-step forecasts for differentiable populations | `axosim.support_surrogate.AdaptiveSupportP4Surrogate` |

The top-level `AxoSimGRU` import currently aliases `CausalBlockForecastModel`, a related block-forecast class whose constructor takes a backbone and forecast configuration. The named GRU factory returns `AxoTemporalModel`; use that factory for the profiles below. This distinction matters when constructing models directly. Loading a saved model with `load_checkpoint` reconstructs the actual saved class.

## Named full-model profiles

The [profile registry](/api/model-family/) contains these architecture recipes:

| Profile ID | `model_dim` | `state_dim` | `num_layers` | `head_dim` |
| --- | ---: | ---: | ---: | ---: |
| `axosim-gru-small` | 32 | 8 | 2 | 32 |
| `axosim-gru-medium` | 128 | 32 | 2 | 128 |
| `axosim-mamba-small` | 32 | 8 | 2 | 32 |
| `axosim-mamba-medium` | 176 | 44 | 4 | 88 |
| `axosim-mamba-large` | 488 | 124 | 8 | 124 |

The columns list exact profile configuration fields. For GRU profiles, the GRU hidden width equals `model_dim`; `state_dim` is the common backbone configuration field rather than the GRU state width. These recipes construct untrained models. A profile ID selects architecture parameters, while a checkpoint contains fitted weights and the precise configuration used to train them.

```python
from axosim import AXOSIM_MODEL_PROFILES, create_axosim_profile

profile = AXOSIM_MODEL_PROFILES["axosim-gru-small"]
model = create_axosim_profile(
    profile.profile_id,
    use_pytorch_fallback=True,
)
print(profile.public_name)
```

```text
AxoSim-GRU Small
```

The fallback flag selects a test-compatible backbone implementation. Preserve this choice in checkpoints; use the fused backend for a checkpoint trained with it.

## Load trained weights

Use a trusted checkpoint produced by your training run or distributed with a verified release. The documentation uses local paths such as `runs/axosim-mamba.pt`; these are example output paths, not download URLs.

```python
from axosim.checkpoint import load_checkpoint

model, metadata = load_checkpoint("runs/axosim-mamba.pt")
print(type(model).__name__)
print(metadata.get("model_kind"))
```

The loader supports current public model kinds and historical checkpoint formats. It reads the architecture configuration from the checkpoint rather than inferring it from a public model name. See [checkpoint reference](/api/checkpoint/) for the supported kinds, persistence format, and loading behavior.

## Compare models on your workload

Select the model using the metrics and runtime conditions you need. Spike Mean F1, Voltage SERA, and Dynamics SERA measure different aspects of fidelity; input shape, precision, batch size, and horizon affect throughput. The technical report compares the measured model family, while [evaluation](/evaluation/) shows how to make a paired comparison on your own data.

## Next steps

Run [single-neuron inference](/inference/), [train a model](/training/), or construct a [Lite population](/populations/).
