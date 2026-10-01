---
title: Choose a model
description: Choose a neuron model for sequence prediction or connected population simulation.
section: Get started
order: 20
---

For single-neuron traces, choose GRU or Mamba and load a trained checkpoint. Both predict spike logits and somatic voltage from the same native input channels. For connected populations, choose Lite, whose compact state supports recurrent routing and inference-time adaptation across many neurons.

## Model catalog

<div class="model-catalog">
  <section class="model-card">
    <a class="model-art gru" href="/api/temporal-core/" aria-label="Explore AxoSim-GRU"><span>GRU</span></a>
    <h3><a href="/api/temporal-core/">AxoSim–GRU</a></h3>
    <p>Recurrent neuron models for spike and voltage prediction. Choose Small for a compact model or Medium for the report's strongest spike Mean F1.</p>
    <dl>
      <div><dt>Profiles</dt><dd><code>axosim-gru-small</code><br /><code>axosim-gru-medium</code></dd></div>
      <div><dt>Create</dt><dd><a href="/api/model-family/#model-family-create-axosim-profile"><code>create_axosim_profile</code></a></dd></div>
      <div><dt>Predict</dt><dd><code>(batch, time, 2)</code><br />Spike logit and soma voltage</dd></div>
      <div><dt>Use it</dt><dd><a href="/inference/">Load and run a checkpoint →</a></dd></div>
    </dl>
  </section>
  <section class="model-card">
    <a class="model-art mamba" href="/api/mamba/" aria-label="Explore AxoSim-Mamba"><span>Mamba</span></a>
    <h3><a href="/api/mamba/">AxoSim–Mamba</a></h3>
    <p>Selective state-space neuron models with a shared dendritic front end. Choose among three capacities and use the checkpoint's temporal backend.</p>
    <dl>
      <div><dt>Profiles</dt><dd><code>axosim-mamba-small</code><br /><code>axosim-mamba-medium</code><br /><code>axosim-mamba-large</code></dd></div>
      <div><dt>Create</dt><dd><a href="/api/model-family/#model-family-create-axosim-profile"><code>create_axosim_profile</code></a></dd></div>
      <div><dt>Predict</dt><dd><code>(batch, time, 2)</code><br />Spike logit and soma voltage</dd></div>
      <div><dt>Use it</dt><dd><a href="/training/">Train a named model →</a></dd></div>
    </dl>
  </section>
  <section class="model-card">
    <a class="model-art lite" href="/api/lite/" aria-label="Explore AxoSim-Lite"><span>Lite</span></a>
    <h3><a href="/api/lite/">AxoSim–Lite</a></h3>
    <p>Compact neuron dynamics for connected populations. Adapt behavior, morphology, and contact efficacies while retaining the temporal gradient.</p>
    <dl>
      <div><dt>Neuron</dt><dd><a href="/api/lite/"><code>AxoSimLite</code></a><br /><a href="/api/lite/#support-surrogate-supportp4config"><code>SupportP4Config</code></a></dd></div>
      <div><dt>Connect</dt><dd><a href="/api/interfaces/#interfaces-axosimpopulation"><code>AxoSimPopulation</code></a></dd></div>
      <div><dt>Predict</dt><dd>Four causal forecast steps<br />Explicit recurrent state</dd></div>
      <div><dt>Use it</dt><dd><a href="/populations/">Build a connected population →</a></dd></div>
    </dl>
  </section>
</div>

## Choose a capacity and backend

A model profile selects architecture parameters; a checkpoint supplies fitted weights. Compare candidate checkpoints using the [AxoBench metrics](/evaluation/) relevant to your application: spike Mean F1, Voltage SERA, and Dynamics SERA. The [technical report](/report/main.pdf) compares fidelity and inference cost across the trained models.

<details class="recipe-details">
<summary>Architecture recipes</summary>

| Profile ID | `model_dim` | `state_dim` | `num_layers` | `head_dim` |
| --- | ---: | ---: | ---: | ---: |
| `axosim-gru-small` | 32 | 8 | 2 | 32 |
| `axosim-gru-medium` | 128 | 32 | 2 | 128 |
| `axosim-mamba-small` | 32 | 8 | 2 | 32 |
| `axosim-mamba-medium` | 176 | 44 | 4 | 88 |
| `axosim-mamba-large` | 488 | 124 | 8 | 124 |

These are the exact fields in the [profile registry](/api/model-family/). For GRU, the recurrent hidden width equals `model_dim`; `state_dim` describes the common backbone configuration rather than the GRU hidden state.

</details>

Use the profile factory when starting a new training run. This example selects the compact GRU architecture and a PyTorch fallback backend so you can inspect it on a machine without fused CUDA kernels:

```python
from axosim import AXOSIM_MODEL_PROFILES, create_axosim_profile

profile = AXOSIM_MODEL_PROFILES["axosim-gru-small"]
model = create_axosim_profile(
    profile.profile_id,
    use_pytorch_fallback=True,
)
print(profile.public_name)
print(type(model).__name__)
```

```text
AxoSim-GRU Small
AxoTemporalModel
```

The factory returns the named GRU implementation, `AxoTemporalModel`. Its weights are initialized for training; to make trained predictions, [load a checkpoint](/inference/). Preserve the backend choice when saving and restoring a model, and use the fused backend for checkpoints trained with it.

## Load trained weights

For inference, restore the checkpoint's configuration instead of reconstructing a model from its display name:

```python
from axosim.checkpoint import load_checkpoint

model, metadata = load_checkpoint("runs/axosim-mamba.pt", map_location="cpu")
model.eval()
print(type(model).__name__)
```

Use a trusted checkpoint from your training run or a verified release. `load_checkpoint` restores the saved model class, weights, and configuration, including supported historical formats. The [checkpoint reference](/api/checkpoint/) describes the persistence contract; [inference](/inference/) demonstrates input construction, morphology IDs, output conversion, and streaming.

The top-level `AxoSimGRU` export names the compatible block-forecast class `CausalBlockForecastModel`. Use `create_axosim_profile` for the named GRU profiles above, or consult [block-forecast models](/api/block-forecast/) when constructing that class directly.

## Next steps

Run [single-neuron inference](/inference/), [train a model](/training/), or construct a [Lite population](/populations/). For a connected application, the [fly-connectome article](https://axym.org/work/axosim-fly-geometry/) follows population activity from visual input to low-dimensional motion representations.
