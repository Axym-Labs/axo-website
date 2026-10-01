---
title: Block-forecast models
description: Signatures, parameters, return contracts, and source for block-forecast models.
section: API reference
apiGroup: Models
order: 206
---

## Overview

CausalBlockForecastModel predicts native outputs through causal block forecasting. The top-level AxoSimGRU alias points to this implementation. Its backbone and BlockForecastConfig constructor contract differs from the named GRU-profile factory.

Source revision: `856207f6de56`. [Public export index](/api/).

<section class="api-symbol" id="block-forecast-blockforecastconfig">

## BlockForecastConfig

<div class="api-signature">

```python
axosim.block_forecast.BlockForecastConfig(core_kind: BlockForecastCore, patch_size: int, max_patch_rank: int = 8, max_trajectory_rank: int = 8, keep_local_tcn: bool = False, gru_hidden_units: int | None = None, residual_scale_init: float = 0.1, voltage_anchor_count: int | None = None, event_template: tuple[float, ...] | None = None, event_template_center_init: float = 0.9208316802978516, event_template_temperature: float = 0.25, event_template_hard: bool = False, behavior_adaptation: bool = False)
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/block_forecast.py#L22-L63)

</div>

Configuration for causal next-block trajectory prediction.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>core_kind</code> <span class="api-type">BlockForecastCore</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>patch_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Native timesteps represented by one block.</dd>
<dt><code>max_patch_rank</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=8.</span></dd>
<dt><code>max_trajectory_rank</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=8.</span></dd>
<dt><code>keep_local_tcn</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>gru_hidden_units</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>residual_scale_init</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.1.</span> Initial learned multiplier on the residual update.</dd>
<dt><code>voltage_anchor_count</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>event_template</code> <span class="api-type">tuple[float, ...] | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>event_template_center_init</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.9208316802978516.</span></dd>
<dt><code>event_template_temperature</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.25.</span></dd>
<dt><code>event_template_hard</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>behavior_adaptation</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span> Enable the learned behavior adaptation bank.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="block-forecast-causalblockforecastmodel">

## CausalBlockForecastModel

<div class="api-signature">

```python
axosim.block_forecast.CausalBlockForecastModel(source: nn.Module, forecast_config: BlockForecastConfig)
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/block_forecast.py#L66-L811)

</div>

Predict each native-resolution output block from prior input blocks.

Bases: `nn.Module`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>source</code> <span class="api-type">nn.Module</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>forecast_config</code> <span class="api-type">BlockForecastConfig</span></dt>
<dd><span class="api-default">required.</span> Block forecasting configuration, including core and cadence.</dd>
</dl>

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="block-forecast-causalblockforecastmodel-config"><code>CausalBlockForecastModel.config</code></dt>
<dd>Configuration retained by the model or its shared backbone. <a href="https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/block_forecast.py#L209-L210">Source</a></dd>
<dt id="block-forecast-causalblockforecastmodel-num-input"><code>CausalBlockForecastModel.num_input: int</code></dt>
<dd>Native input-channel count. <a href="https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/block_forecast.py#L213-L214">Source</a></dd>
<dt id="block-forecast-causalblockforecastmodel-num-output"><code>CausalBlockForecastModel.num_output: int</code></dt>
<dd>Readout-channel count. <a href="https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/block_forecast.py#L217-L218">Source</a></dd>
<dt id="block-forecast-causalblockforecastmodel-num-branch"><code>CausalBlockForecastModel.num_branch: int</code></dt>
<dd>Branched input-feature count. <a href="https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/block_forecast.py#L221-L222">Source</a></dd>
<dt id="block-forecast-causalblockforecastmodel-patch-size"><code>CausalBlockForecastModel.patch_size: int</code></dt>
<dd>Native timesteps represented by one forecast block. <a href="https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/block_forecast.py#L225-L226">Source</a></dd>
<dt id="block-forecast-causalblockforecastmodel-sparse-voltage-output"><code>CausalBlockForecastModel.sparse_voltage_output: bool</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/block_forecast.py#L229-L230">Source</a></dd>
<dt id="block-forecast-causalblockforecastmodel-behavior-parameter-count"><code>CausalBlockForecastModel.behavior_parameter_count: int</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/block_forecast.py#L233-L238">Source</a></dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#block-forecast-causalblockforecastmodel-block-state-sequence"><code>CausalBlockForecastModel.block_state_sequence()</code></a></li>
<li><a href="#block-forecast-causalblockforecastmodel-decode-block-state-sequence"><code>CausalBlockForecastModel.decode_block_state_sequence()</code></a></li>
<li><a href="#block-forecast-causalblockforecastmodel-forward"><code>CausalBlockForecastModel.forward()</code></a></li>
<li><a href="#block-forecast-causalblockforecastmodel-component-manifest"><code>CausalBlockForecastModel.component_manifest()</code></a></li>
</ul>

<section class="api-method" id="block-forecast-causalblockforecastmodel-block-state-sequence">

### CausalBlockForecastModel.block_state_sequence

<div class="api-signature">

```python
axosim.block_forecast.CausalBlockForecastModel.block_state_sequence(x: torch.Tensor, *, morphology_indices: torch.Tensor | None=None, behavior_parameters: torch.Tensor | None=None) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/block_forecast.py#L447-L485)

</div>

Encode a native sequence and return each causal macro state.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>x</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Input tensor for the full-sequence or streaming operation.</dd>
<dt><code>morphology_indices</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Integer class assignments into the model&#x27;s ordered morphology vocabulary; one per batch item or persistent neuron.</dd>
<dt><code>behavior_parameters</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Logical behavior coefficients to compile into the model&#x27;s deployed coefficient width.</dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

<section class="api-method" id="block-forecast-causalblockforecastmodel-decode-block-state-sequence">

### CausalBlockForecastModel.decode_block_state_sequence

<div class="api-signature">

```python
axosim.block_forecast.CausalBlockForecastModel.decode_block_state_sequence(block_state: torch.Tensor, *, behavior_parameters: torch.Tensor | None=None) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/block_forecast.py#L487-L509)

</div>

Decode dense native-rate trajectories from causal macro states.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>block_state</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Persistent state of the block-forecast recurrence.</dd>
<dt><code>behavior_parameters</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Logical behavior coefficients to compile into the model&#x27;s deployed coefficient width.</dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

<section class="api-method" id="block-forecast-causalblockforecastmodel-forward">

### CausalBlockForecastModel.forward

<div class="api-signature">

```python
axosim.block_forecast.CausalBlockForecastModel.forward(x: torch.Tensor, *, morphology_indices: torch.Tensor | None=None, behavior_parameters: torch.Tensor | None=None) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/block_forecast.py#L611-L716)

</div>

Predict native spike and soma outputs for the supplied sequence.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>x</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Input tensor for the full-sequence or streaming operation.</dd>
<dt><code>morphology_indices</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Integer class assignments into the model&#x27;s ordered morphology vocabulary; one per batch item or persistent neuron.</dd>
<dt><code>behavior_parameters</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Logical behavior coefficients to compile into the model&#x27;s deployed coefficient width.</dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

<section class="api-method" id="block-forecast-causalblockforecastmodel-component-manifest">

### CausalBlockForecastModel.component_manifest

<div class="api-signature">

```python
axosim.block_forecast.CausalBlockForecastModel.component_manifest() -> dict[str, object]
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/block_forecast.py#L782-L811)

</div>

Describe the model's temporal and readout components.

<p class="api-label">Returns</p>

`dict[str, object]`

</section>

</section>
