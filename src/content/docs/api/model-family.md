---
title: Model profiles
description: Signatures, parameters, return contracts, and source for model profiles.
section: API reference
apiGroup: Models
order: 202
---

## Overview

Named profiles provide fixed architecture recipes. Construction returns an untrained model. Mamba profiles use AxoMamba; GRU profiles use AxoTemporalModel with a GRU temporal core. Preserve the backend and saved model kind when loading weights.

Source revision: `306a51ed950b`. [Public export index](/api/).

<section class="api-symbol" id="model-family-axosimmodelprofile">

## AxoSimModelProfile

<div class="api-signature">

```python
axosim.model_family.AxoSimModelProfile(profile_id: str, public_name: str, family: ModelFamily, model_dim: int, state_dim: int, num_layers: int, head_dim: int, mamba_update_normalization: Literal['none', 'fixed_rms'] = 'none')
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/model_family.py#L25-L35)

</div>

Stable recipe for one trained-model capacity point.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>profile_id</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Exact key in AXOSIM_MODEL_PROFILES, such as axosim-gru-small.</dd>
<dt><code>public_name</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Reader-facing name associated with the exact profile ID.</dd>
<dt><code>family</code> <span class="api-type">ModelFamily</span></dt>
<dd><span class="api-default">required.</span> Temporal model family selected by the named profile.</dd>
<dt><code>model_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Temporal hidden-feature width.</dd>
<dt><code>state_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Temporal state width.</dd>
<dt><code>num_layers</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Number of temporal layers.</dd>
<dt><code>head_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Configured head width of the backbone.</dd>
<dt><code>mamba_update_normalization</code> <span class="api-type">Literal[&#x27;none&#x27;, &#x27;fixed_rms&#x27;]</span></dt>
<dd><span class="api-default">default=&#x27;none&#x27;.</span> Normalize residual updates when the supported fixed_rms mode is selected.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="model-family-axosim-model-profiles">

## AXOSIM_MODEL_PROFILES

<div class="api-signature">

```python
axosim.model_family.AXOSIM_MODEL_PROFILES: Mapping[str, AxoSimModelProfile]
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/model_family.py#L86-L88)

</div>

Read-only mapping from exact profile IDs to architecture recipes. Use create_axosim_profile to construct a model from an entry.

</section>

<section class="api-symbol" id="model-family-create-axosim-profile">

## create_axosim_profile

<div class="api-signature">

```python
axosim.model_family.create_axosim_profile(profile_id: str, *, base_config: AxoMambaConfig | None=None, use_pytorch_fallback: bool=False) -> nn.Module
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/model_family.py#L91-L126)

</div>

Build one named GRU or Mamba profile from the common AxoSim shell.

profile_id must exist in AXOSIM_MODEL_PROFILES. A Mamba profile returns an AxoMamba or fallback backbone; a GRU profile returns AxoTemporalModel with a GRU core. Weights are newly initialized, not downloaded.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>profile_id</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Exact key in AXOSIM_MODEL_PROFILES, such as axosim-gru-small.</dd>
<dt><code>base_config</code> <span class="api-type">AxoMambaConfig | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Common backbone configuration whose capacity fields are replaced by the selected profile.</dd>
<dt><code>use_pytorch_fallback</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Construct the CPU/test-compatible backend. Its checkpoint format differs from the fused backend.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>model</code> <span class="api-type">nn.Module</span></dt>
<dd>Newly initialized Mamba backbone or GRU AxoTemporalModel for the requested profile; no weights are downloaded.</dd>
</dl>

<p class="api-label">Examples</p>

Construct an untrained, CPU-compatible GRU profile for an interface check.

```python
from axosim import create_axosim_profile

model = create_axosim_profile(
    'axosim-gru-small', use_pytorch_fallback=True
)
print(type(model).__name__)
```

```text
AxoTemporalModel
```

</section>
