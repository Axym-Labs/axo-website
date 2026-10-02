---
title: Activity and experimental control
description: Signatures, parameters, return contracts, and source for activity and experimental control.
section: API reference
apiGroup: Populations
order: 216
---

## Overview

Threshold functions convert model-generated spike logits into events using fixed declared thresholds. Patch-phase layout helpers organize native cadence. HomeostaticThresholdController is an experimental optional code feature; it is not required by the lifecycle guides and is not a contribution presented in the technical report.

Source revision: `0f546adfd8fc`. [Public export index](/api/).

<section class="api-symbol" id="activity-stratifiedpatchphaselayout">

## StratifiedPatchPhaseLayout

<div class="api-signature">

```python
axosim.activity.StratifiedPatchPhaseLayout(phase_ids: torch.Tensor, storage_permutation: torch.Tensor, inverse_permutation: torch.Tensor, phase_population_sizes: tuple[int, ...], storage_group_offsets: tuple[int, ...], storage_group_shape: tuple[int, int])
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/activity.py#L12-L32)

</div>

Deterministic patch phases and a phase-major storage permutation.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>phase_ids</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>storage_permutation</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>inverse_permutation</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>phase_population_sizes</code> <span class="api-type">tuple[int, ...]</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>storage_group_offsets</code> <span class="api-type">tuple[int, ...]</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>storage_group_shape</code> <span class="api-type">tuple[int, int]</span></dt>
<dd><span class="api-default">required.</span></dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="activity-stratifiedpatchphaselayout-patch-size"><code>StratifiedPatchPhaseLayout.patch_size: int</code></dt>
<dd>Native timesteps represented by one forecast block. <a href="https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/activity.py#L23-L24">Source</a></dd>
<dt id="activity-stratifiedpatchphaselayout-population-size"><code>StratifiedPatchPhaseLayout.population_size: int</code></dt>
<dd>Number of persistent neurons. <a href="https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/activity.py#L27-L28">Source</a></dd>
<dt id="activity-stratifiedpatchphaselayout-phase-sizes"><code>StratifiedPatchPhaseLayout.phase_sizes: tuple[int, ...]</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/activity.py#L31-L32">Source</a></dd>
</dl>

</section>

<section class="api-symbol" id="activity-fixedactivitythresholds">

## FixedActivityThresholds

<div class="api-signature">

```python
axosim.activity.FixedActivityThresholds(excitatory: tuple[float, ...], inhibitory: tuple[float, ...])
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/activity.py#L36-L67)

</div>

Fixed spike-score thresholds stratified by role and morphology.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>excitatory</code> <span class="api-type">tuple[float, ...]</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>inhibitory</code> <span class="api-type">tuple[float, ...]</span></dt>
<dd><span class="api-default">required.</span></dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="activity-fixedactivitythresholds-morphology-count"><code>FixedActivityThresholds.morphology_count: int</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/activity.py#L54-L55">Source</a></dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#activity-fixedactivitythresholds-as-tensor"><code>FixedActivityThresholds.as_tensor()</code></a></li>
</ul>

<section class="api-method" id="activity-fixedactivitythresholds-as-tensor">

### FixedActivityThresholds.as_tensor

<div class="api-signature">

```python
axosim.activity.FixedActivityThresholds.as_tensor(*, device: torch.device | str, dtype: torch.dtype) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/activity.py#L57-L67)

</div>

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>device</code> <span class="api-type">torch.device | str</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Execution or allocation device.</dd>
<dt><code>dtype</code> <span class="api-type">torch.dtype</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Floating-point execution or allocation dtype.</dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

</section>

<section class="api-symbol" id="activity-fixedblockactivitythresholds">

## FixedBlockActivityThresholds

<div class="api-signature">

```python
axosim.activity.FixedBlockActivityThresholds(forecast_steps: tuple[FixedActivityThresholds, ...])
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/activity.py#L71-L106)

</div>

Fixed role/morphology thresholds for each forecast position.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>forecast_steps</code> <span class="api-type">tuple[FixedActivityThresholds, ...]</span></dt>
<dd><span class="api-default">required.</span></dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="activity-fixedblockactivitythresholds-forecast-step-count"><code>FixedBlockActivityThresholds.forecast_step_count: int</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/activity.py#L88-L89">Source</a></dd>
<dt id="activity-fixedblockactivitythresholds-morphology-count"><code>FixedBlockActivityThresholds.morphology_count: int</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/activity.py#L92-L93">Source</a></dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#activity-fixedblockactivitythresholds-as-tensor"><code>FixedBlockActivityThresholds.as_tensor()</code></a></li>
</ul>

<section class="api-method" id="activity-fixedblockactivitythresholds-as-tensor">

### FixedBlockActivityThresholds.as_tensor

<div class="api-signature">

```python
axosim.activity.FixedBlockActivityThresholds.as_tensor(*, device: torch.device | str, dtype: torch.dtype) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/activity.py#L95-L106)

</div>

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>device</code> <span class="api-type">torch.device | str</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Execution or allocation device.</dd>
<dt><code>dtype</code> <span class="api-type">torch.dtype</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Floating-point execution or allocation dtype.</dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

</section>

<section class="api-symbol" id="activity-homeostaticthresholdcontroller">

## HomeostaticThresholdController

<div class="api-signature">

```python
axosim.activity.HomeostaticThresholdController(*, group_ids: torch.Tensor, target_rates_hz: torch.Tensor, dt_ms: float, update_interval_ms: float, time_constant_ms: float, learning_rate: float, max_abs_offset: float)
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/activity.py#L109-L253)

</div>

Adapt group thresholds to oppose sustained firing-rate errors.

Experimental optional feature. group_ids assigns neurons to declared groups; target_rates_hz supplies each group's target. A causal group-rate estimate drives bounded threshold offsets. This interface does not establish biological timescales or biological realism.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>group_ids</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Integer population vector whose contiguous groups cover the target-rate vector.</dd>
<dt><code>target_rates_hz</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Positive finite firing-rate targets in hertz, one per declared group.</dd>
<dt><code>dt_ms</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Native simulation step in milliseconds.</dd>
<dt><code>update_interval_ms</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Interval between controller updates; an integer multiple of dt_ms.</dd>
<dt><code>time_constant_ms</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Time constant of the controller&#x27;s smoothed rate estimate.</dd>
<dt><code>learning_rate</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Optimizer step size.</dd>
<dt><code>max_abs_offset</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Bound on the absolute threshold correction.</dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#activity-homeostaticthresholdcontroller-observe"><code>HomeostaticThresholdController.observe()</code></a></li>
<li><a href="#activity-homeostaticthresholdcontroller-threshold-offsets-per-neuron"><code>HomeostaticThresholdController.threshold_offsets_per_neuron()</code></a></li>
</ul>

<section class="api-method" id="activity-homeostaticthresholdcontroller-observe">

### HomeostaticThresholdController.observe

<div class="api-signature">

```python
axosim.activity.HomeostaticThresholdController.observe(activity: torch.Tensor) -> bool
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/activity.py#L207-L248)

</div>

Observe one simulation step and update at the window boundary.

Observes one neuron activity vector for a simulation step; returns whether the update interval triggered an offset update. No future activity is used.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>activity</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Boolean neuron activity vector for one simulation step.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>updated</code> <span class="api-type">bool</span></dt>
<dd>True when the update interval triggers a threshold-offset update, otherwise False.</dd>
</dl>

</section>

<section class="api-method" id="activity-homeostaticthresholdcontroller-threshold-offsets-per-neuron">

### HomeostaticThresholdController.threshold_offsets_per_neuron

<div class="api-signature">

```python
axosim.activity.HomeostaticThresholdController.threshold_offsets_per_neuron() -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/activity.py#L250-L253)

</div>

Return the current group offset for every population member.

Returns one current group-derived threshold offset per neuron.

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>offsets</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Current group-derived threshold offsets, one per population member.</dd>
</dl>

</section>

</section>

<section class="api-symbol" id="activity-build-stratified-patch-phase-layout">

## build_stratified_patch_phase_layout

<div class="api-signature">

```python
axosim.activity.build_stratified_patch_phase_layout(morphology_ids: torch.Tensor, inhibitory: torch.Tensor, *, patch_size: int, seed: int, tile_ids: torch.Tensor | None=None) -> StratifiedPatchPhaseLayout
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/activity.py#L256-L376)

</div>

Balance phases independently inside every morphology and E/I group.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>morphology_ids</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Ordered morphology identity vocabulary.</dd>
<dt><code>inhibitory</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>patch_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Native timesteps represented by one block.</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Random seed for the declared operation.</dd>
<dt><code>tile_ids</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
</dl>

<p class="api-label">Returns</p>

`StratifiedPatchPhaseLayout`

</section>

<section class="api-symbol" id="activity-threshold-model-activity">

## threshold_model_activity

<div class="api-signature">

```python
axosim.activity.threshold_model_activity(spike_scores: torch.Tensor, morphology_ids: torch.Tensor, inhibitory: torch.Tensor, thresholds: FixedActivityThresholds) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/activity.py#L379-L414)

</div>

Return variable-cardinality events from fixed model-score crossings.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>spike_scores</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>morphology_ids</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Ordered morphology identity vocabulary.</dd>
<dt><code>inhibitory</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>thresholds</code> <span class="api-type">FixedActivityThresholds</span></dt>
<dd><span class="api-default">required.</span></dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

<section class="api-symbol" id="activity-threshold-block-model-activity">

## threshold_block_model_activity

<div class="api-signature">

```python
axosim.activity.threshold_block_model_activity(spike_scores: torch.Tensor, morphology_ids: torch.Tensor, inhibitory: torch.Tensor, thresholds: FixedBlockActivityThresholds) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/activity.py#L417-L451)

</div>

Threshold an ordered forecast block without fixing event counts.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>spike_scores</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>morphology_ids</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Ordered morphology identity vocabulary.</dd>
<dt><code>inhibitory</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>thresholds</code> <span class="api-type">FixedBlockActivityThresholds</span></dt>
<dd><span class="api-default">required.</span></dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>
