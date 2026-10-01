---
title: GRU temporal models
description: Signatures, parameters, return contracts, and source for gru temporal models.
section: API reference
apiGroup: Models
order: 204
---

## Overview

AxoTemporalModel wraps the common backbone with a selected temporal core. Named public GRU profiles use this class. Full-sequence forward calls reset temporal state; streaming calls use an explicitly allocated persistent state. Low-level temporal cores and behavior adapters are included below for direct construction.

Source revision: `306a51ed950b`. [Public export index](/api/).

<section class="api-symbol" id="temporal-core-axotemporalstreamingstate">

## AxoTemporalStreamingState

<div class="api-signature">

```python
axosim.temporal_core.AxoTemporalStreamingState(core_state: torch.Tensor | tuple[torch.Tensor, torch.Tensor], local_tcn_histories: list[torch.Tensor], morphology_feature_gains: torch.Tensor | None, patch_sum: torch.Tensor | None = None, patch_correction: torch.Tensor | None = None, patch_position: int = 0)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L16-L24)

</div>

Mutable online state for a replacement temporal core.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>core_state</code> <span class="api-type">torch.Tensor | tuple[torch.Tensor, torch.Tensor]</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>local_tcn_histories</code> <span class="api-type">list[torch.Tensor]</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>morphology_feature_gains</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>patch_sum</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>patch_correction</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>patch_position</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as attributes.

</section>

<section class="api-symbol" id="temporal-core-axotemporalcoreconfig">

## AxoTemporalCoreConfig

<div class="api-signature">

```python
axosim.temporal_core.AxoTemporalCoreConfig(kind: TemporalCoreKind, gru_hidden_units: int | None = None, branch_memory_units: int = 30, branch_hidden_units: int = 64, branch_synapse_decay: float = 0.85, branch_memory_decay: float = 0.9, residual_scale_init: float = 0.1, keep_local_tcn: bool = False, patch_size: int = 1, behavior_adapter_morphology_id: str | None = None, behavior_adapter_rank: int = 0, behavior_adapter_branch_token_offset: bool = False)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L28-L85)

</div>

Configuration for a temporal core behind the shared AxoMamba encoder.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>kind</code> <span class="api-type">TemporalCoreKind</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>gru_hidden_units</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>branch_memory_units</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=30.</span></dd>
<dt><code>branch_hidden_units</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=64.</span></dd>
<dt><code>branch_synapse_decay</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.85.</span></dd>
<dt><code>branch_memory_decay</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.9.</span></dd>
<dt><code>residual_scale_init</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.1.</span> Initial learned multiplier on the residual update.</dd>
<dt><code>keep_local_tcn</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>patch_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=1.</span> Native timesteps represented by one block.</dd>
<dt><code>behavior_adapter_morphology_id</code> <span class="api-type">str | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>behavior_adapter_rank</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
<dt><code>behavior_adapter_branch_token_offset</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="temporal-core-neuronbehavioradapter">

## NeuronBehaviorAdapter

<div class="api-signature">

```python
axosim.temporal_core.NeuronBehaviorAdapter(*, branches: int, width: int, outputs: int, morphology_index: int, rank: int=0, branch_token_offset: bool=False)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L88-L205)

</div>

Neuron-specific response parameters around shared GRU dynamics.

Bases: `nn.Module`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>branches</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Number of routed branch features in the adapter.</dd>
<dt><code>width</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Feature width of the behavior adapter or population recurrence.</dd>
<dt><code>outputs</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Number of readout channels.</dd>
<dt><code>morphology_index</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Index of the morphology row to select.</dd>
<dt><code>rank</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Low-rank adapter factor width.</dd>
<dt><code>branch_token_offset</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Include adaptation offsets for encoded branch tokens.</dd>
</dl>

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="temporal-core-neuronbehavioradapter-parameter-counts"><code>NeuronBehaviorAdapter.parameter_counts: dict[str, int]</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L162-L201">Source</a></dd>
<dt id="temporal-core-neuronbehavioradapter-parameter-count"><code>NeuronBehaviorAdapter.parameter_count: int</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L204-L205">Source</a></dd>
</dl>

</section>

<section class="api-symbol" id="temporal-core-residualgrutemporalcore">

## ResidualGRUTemporalCore

<div class="api-signature">

```python
axosim.temporal_core.ResidualGRUTemporalCore(width: int, *, hidden_units: int | None=None, residual_scale_init: float)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L208-L328)

</div>

Vendor-fused GRU with the same residual contract as AxoMamba blocks.

Bases: `nn.Module`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>width</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Feature width of the behavior adapter or population recurrence.</dd>
<dt><code>hidden_units</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Width of the hidden feature layer.</dd>
<dt><code>residual_scale_init</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Initial learned multiplier on the residual update.</dd>
</dl>

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="temporal-core-residualgrutemporalcore-recurrent-state-elements"><code>ResidualGRUTemporalCore.recurrent_state_elements: int</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L327-L328">Source</a></dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#temporal-core-residualgrutemporalcore-forward"><code>ResidualGRUTemporalCore.forward()</code></a></li>
<li><a href="#temporal-core-residualgrutemporalcore-temporal-correction"><code>ResidualGRUTemporalCore.temporal_correction()</code></a></li>
</ul>

<section class="api-method" id="temporal-core-residualgrutemporalcore-forward">

### ResidualGRUTemporalCore.forward

<div class="api-signature">

```python
axosim.temporal_core.ResidualGRUTemporalCore.forward(hidden: torch.Tensor, *, weight_ih_delta: torch.Tensor | None=None, weight_hh_delta: torch.Tensor | None=None, adapter_mask: torch.Tensor | None=None) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L240-L253)

</div>

Predict native spike and soma outputs for the supplied sequence.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>hidden</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Hidden recurrent state for the selected temporal core.</dd>
<dt><code>weight_ih_delta</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional correction to GRU input-to-hidden weights.</dd>
<dt><code>weight_hh_delta</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional correction to GRU hidden-to-hidden weights.</dd>
<dt><code>adapter_mask</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Mask selecting members that receive the adapter correction.</dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

<section class="api-method" id="temporal-core-residualgrutemporalcore-temporal-correction">

### ResidualGRUTemporalCore.temporal_correction

<div class="api-signature">

```python
axosim.temporal_core.ResidualGRUTemporalCore.temporal_correction(hidden: torch.Tensor, *, weight_ih_delta: torch.Tensor | None=None, weight_hh_delta: torch.Tensor | None=None, adapter_mask: torch.Tensor | None=None) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L255-L286)

</div>

Compute the temporal correction for encoded features.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>hidden</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Hidden recurrent state for the selected temporal core.</dd>
<dt><code>weight_ih_delta</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional correction to GRU input-to-hidden weights.</dd>
<dt><code>weight_hh_delta</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional correction to GRU hidden-to-hidden weights.</dd>
<dt><code>adapter_mask</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Mask selecting members that receive the adapter correction.</dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

</section>

<section class="api-symbol" id="temporal-core-branchelmtemporalcore">

## BranchELMTemporalCore

<div class="api-signature">

```python
axosim.temporal_core.BranchELMTemporalCore(width: int, *, memory_units: int, hidden_units: int, synapse_decay: float, memory_decay: float, residual_scale_init: float)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L331-L393)

</div>

Leaky branch/memory recurrence behind the shared biological encoder.

Bases: `nn.Module`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>width</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Feature width of the behavior adapter or population recurrence.</dd>
<dt><code>memory_units</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Width of the recurrent memory state.</dd>
<dt><code>hidden_units</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Width of the hidden feature layer.</dd>
<dt><code>synapse_decay</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Decay coefficient of the synaptic trace.</dd>
<dt><code>memory_decay</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Decay coefficient of recurrent memory.</dd>
<dt><code>residual_scale_init</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Initial learned multiplier on the residual update.</dd>
</dl>

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="temporal-core-branchelmtemporalcore-recurrent-state-elements"><code>BranchELMTemporalCore.recurrent_state_elements: int</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L392-L393">Source</a></dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#temporal-core-branchelmtemporalcore-forward"><code>BranchELMTemporalCore.forward()</code></a></li>
<li><a href="#temporal-core-branchelmtemporalcore-temporal-correction"><code>BranchELMTemporalCore.temporal_correction()</code></a></li>
</ul>

<section class="api-method" id="temporal-core-branchelmtemporalcore-forward">

### BranchELMTemporalCore.forward

<div class="api-signature">

```python
axosim.temporal_core.BranchELMTemporalCore.forward(hidden: torch.Tensor) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L361-L362)

</div>

Predict native spike and soma outputs for the supplied sequence.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>hidden</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Hidden recurrent state for the selected temporal core.</dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

<section class="api-method" id="temporal-core-branchelmtemporalcore-temporal-correction">

### BranchELMTemporalCore.temporal_correction

<div class="api-signature">

```python
axosim.temporal_core.BranchELMTemporalCore.temporal_correction(hidden: torch.Tensor) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L364-L389)

</div>

Compute the temporal correction for encoded features.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>hidden</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Hidden recurrent state for the selected temporal core.</dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

</section>

<section class="api-symbol" id="temporal-core-causalpatchedtemporalcore">

## CausalPatchedTemporalCore

<div class="api-signature">

```python
axosim.temporal_core.CausalPatchedTemporalCore(core: nn.Module, *, width: int, patch_size: int)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L396-L455)

</div>

Run a temporal core on causal patch means and delay its correction.

Bases: `nn.Module`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>core</code> <span class="api-type">nn.Module</span></dt>
<dd><span class="api-default">required.</span> Temporal core instance used by the wrapper.</dd>
<dt><code>width</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Feature width of the behavior adapter or population recurrence.</dd>
<dt><code>patch_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Native timesteps represented by one block.</dd>
</dl>

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="temporal-core-causalpatchedtemporalcore-recurrent-state-elements"><code>CausalPatchedTemporalCore.recurrent_state_elements: int</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L451-L455">Source</a></dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#temporal-core-causalpatchedtemporalcore-forward"><code>CausalPatchedTemporalCore.forward()</code></a></li>
</ul>

<section class="api-method" id="temporal-core-causalpatchedtemporalcore-forward">

### CausalPatchedTemporalCore.forward

<div class="api-signature">

```python
axosim.temporal_core.CausalPatchedTemporalCore.forward(hidden: torch.Tensor, **temporal_kwargs) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L413-L448)

</div>

Predict native spike and soma outputs for the supplied sequence.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>hidden</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Hidden recurrent state for the selected temporal core.</dd>
<dt><code>temporal_kwargs</code> <span class="api-type">unannotated</span></dt>
<dd><span class="api-default">variadic.</span> Keyword options forwarded to temporal-core construction.</dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

</section>

<section class="api-symbol" id="temporal-core-axotemporalmodel">

## AxoTemporalModel

<div class="api-signature">

```python
axosim.temporal_core.AxoTemporalModel(source: BranchOfficialMamba, temporal_config: AxoTemporalCoreConfig)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L458-L1163)

</div>

Shared AxoMamba encoder/heads with an interchangeable temporal core.

Bases: `nn.Module`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>source</code> <span class="api-type">BranchOfficialMamba</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>temporal_config</code> <span class="api-type">AxoTemporalCoreConfig</span></dt>
<dd><span class="api-default">required.</span> Temporal-core selection and its recurrence/adaptation settings.</dd>
</dl>

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="temporal-core-axotemporalmodel-config"><code>AxoTemporalModel.config</code></dt>
<dd>Configuration retained by the model or its shared backbone. <a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L525-L526">Source</a></dd>
<dt id="temporal-core-axotemporalmodel-num-input"><code>AxoTemporalModel.num_input: int</code></dt>
<dd>Native input-channel count. <a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L529-L530">Source</a></dd>
<dt id="temporal-core-axotemporalmodel-num-output"><code>AxoTemporalModel.num_output: int</code></dt>
<dd>Readout-channel count. <a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L533-L534">Source</a></dd>
<dt id="temporal-core-axotemporalmodel-num-branch"><code>AxoTemporalModel.num_branch: int</code></dt>
<dd>Branched input-feature count. <a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L537-L538">Source</a></dd>
<dt id="temporal-core-axotemporalmodel-base-soma-prediction"><code>AxoTemporalModel.base_soma_prediction: torch.Tensor | None</code></dt>
<dd>Most recently retained base soma prediction, when available. <a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L541-L542">Source</a></dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#temporal-core-axotemporalmodel-forward"><code>AxoTemporalModel.forward()</code></a></li>
<li><a href="#temporal-core-axotemporalmodel-allocate-streaming-state"><code>AxoTemporalModel.allocate_streaming_state()</code></a></li>
<li><a href="#temporal-core-axotemporalmodel-streaming-step"><code>AxoTemporalModel.streaming_step()</code></a></li>
<li><a href="#temporal-core-axotemporalmodel-streaming-step-events"><code>AxoTemporalModel.streaming_step_events()</code></a></li>
<li><a href="#temporal-core-axotemporalmodel-recurrent-state-bytes"><code>AxoTemporalModel.recurrent_state_bytes()</code></a></li>
<li><a href="#temporal-core-axotemporalmodel-component-manifest"><code>AxoTemporalModel.component_manifest()</code></a></li>
</ul>

<section class="api-method" id="temporal-core-axotemporalmodel-forward">

### AxoTemporalModel.forward

<div class="api-signature">

```python
axosim.temporal_core.AxoTemporalModel.forward(x: torch.Tensor, *, morphology_indices: torch.Tensor | None=None) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L544-L652)

</div>

Predict native spike and soma outputs for the supplied sequence.

x is (B,T,num_input), with integer morphology_indices (B,) when morphology conditioning or behavior adaptation is configured. Returns (B,T,num_output). Each sequence forward initializes the core state.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>x</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Input tensor for the full-sequence or streaming operation.</dd>
<dt><code>morphology_indices</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Integer class assignments into the model&#x27;s ordered morphology vocabulary; one per batch item or persistent neuron.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Spike-logit and soma-target channels in the tensor shape specified above.</dd>
</dl>

</section>

<section class="api-method" id="temporal-core-axotemporalmodel-allocate-streaming-state">

### AxoTemporalModel.allocate_streaming_state

<div class="api-signature">

```python
axosim.temporal_core.AxoTemporalModel.allocate_streaming_state(batch_size: int, *, device: torch.device | str | None=None, dtype: torch.dtype | None=None) -> AxoTemporalStreamingState
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L654-L729)

</div>

Allocate exact online state without retaining native-rate history.

Allocates an AxoTemporalStreamingState for batch_size on the requested device and dtype; the state contains temporal-core values and causal local-filter histories.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>batch_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Examples processed per batch.</dd>
<dt><code>device</code> <span class="api-type">torch.device | str | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Execution or allocation device.</dd>
<dt><code>dtype</code> <span class="api-type">torch.dtype | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Floating-point execution or allocation dtype.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>state</code> <span class="api-type">AxoTemporalStreamingState</span></dt>
<dd>Fresh temporal-core buffers and local-filter histories for the selected batch, device, and dtype.</dd>
</dl>

</section>

<section class="api-method" id="temporal-core-axotemporalmodel-streaming-step">

### AxoTemporalModel.streaming_step

<div class="api-signature">

```python
axosim.temporal_core.AxoTemporalModel.streaming_step(x: torch.Tensor, state: AxoTemporalStreamingState, *, morphology_indices: torch.Tensor | None=None) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L731-L769)

</div>

Advance one dense native-rate timestep.

Advances one native input step using persistent state. The guide supplies x as (B,num_input) and morphology_indices as (B,) when required. Returns (B,1,num_output).

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>x</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Input tensor for the full-sequence or streaming operation.</dd>
<dt><code>state</code> <span class="api-type">AxoTemporalStreamingState</span></dt>
<dd><span class="api-default">required.</span> Temporal state returned by the matching initial-state or allocation method.</dd>
<dt><code>morphology_indices</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Integer class assignments into the model&#x27;s ordered morphology vocabulary; one per batch item or persistent neuron.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">torch.Tensor</span></dt>
<dd>One native output step (batch,1,num_output); the supplied state is updated in place.</dd>
</dl>

</section>

<section class="api-method" id="temporal-core-axotemporalmodel-streaming-step-events">

### AxoTemporalModel.streaming_step_events

<div class="api-signature">

```python
axosim.temporal_core.AxoTemporalModel.streaming_step_events(event_indices: torch.Tensor, event_values: torch.Tensor, state: AxoTemporalStreamingState, *, morphology_indices: torch.Tensor | None=None, chunk_size: int | None=None, output_buffer: torch.Tensor | None=None, retain_base_soma_prediction: bool=True) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L771-L921)

</div>

Advance one timestep from padded sparse channel/value rows.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>event_indices</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>event_values</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Signed floating-point event amplitudes, one per paired address.</dd>
<dt><code>state</code> <span class="api-type">AxoTemporalStreamingState</span></dt>
<dd><span class="api-default">required.</span> Temporal state returned by the matching initial-state or allocation method.</dd>
<dt><code>morphology_indices</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Integer class assignments into the model&#x27;s ordered morphology vocabulary; one per batch item or persistent neuron.</dd>
<dt><code>chunk_size</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Chunk length for the supported Mamba or streaming execution path.</dd>
<dt><code>output_buffer</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional preallocated output tensor for the operation.</dd>
<dt><code>retain_base_soma_prediction</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=True.</span> Keep the base soma readout available for inspection.</dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

<section class="api-method" id="temporal-core-axotemporalmodel-recurrent-state-bytes">

### AxoTemporalModel.recurrent_state_bytes

<div class="api-signature">

```python
axosim.temporal_core.AxoTemporalModel.recurrent_state_bytes(*, dtype: torch.dtype) -> int
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L1127-L1135)

</div>

Report the declared recurrent-state storage in bytes.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>dtype</code> <span class="api-type">torch.dtype</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Floating-point execution or allocation dtype.</dd>
</dl>

<p class="api-label">Returns</p>

`int`

</section>

<section class="api-method" id="temporal-core-axotemporalmodel-component-manifest">

### AxoTemporalModel.component_manifest

<div class="api-signature">

```python
axosim.temporal_core.AxoTemporalModel.component_manifest() -> dict[str, object]
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L1137-L1163)

</div>

Describe the model's temporal and readout components.

<p class="api-label">Returns</p>

`dict[str, object]`

</section>

</section>

<section class="api-symbol" id="temporal-core-create-temporal-model">

## create_temporal_model

<div class="api-signature">

```python
axosim.temporal_core.create_temporal_model(source: BranchOfficialMamba, temporal_config: AxoTemporalCoreConfig) -> BranchOfficialMamba | AxoTemporalModel
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L1166-L1174)

</div>

Compose a selected AxoMamba front end with one temporal core.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>source</code> <span class="api-type">BranchOfficialMamba</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>temporal_config</code> <span class="api-type">AxoTemporalCoreConfig</span></dt>
<dd><span class="api-default">required.</span> Temporal-core selection and its recurrence/adaptation settings.</dd>
</dl>

<p class="api-label">Returns</p>

`BranchOfficialMamba \| AxoTemporalModel`

</section>

<section class="api-symbol" id="temporal-core-migrate-legacy-gru-state-dict">

## migrate_legacy_gru_state_dict

<div class="api-signature">

```python
axosim.temporal_core.migrate_legacy_gru_state_dict(state_dict: dict[str, torch.Tensor]) -> dict[str, torch.Tensor]
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L1177-L1195)

</div>

Map the internal I108 GRU wrapper into the unified checkpoint schema.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>state_dict</code> <span class="api-type">dict[str, torch.Tensor]</span></dt>
<dd><span class="api-default">required.</span> Stored parameter and buffer mapping to load.</dd>
</dl>

<p class="api-label">Returns</p>

`dict[str, torch.Tensor]`

</section>
