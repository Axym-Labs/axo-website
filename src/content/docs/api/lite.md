---
title: Lite neuron and configuration
description: Signatures, parameters, return contracts, and source for lite neuron and configuration.
section: API reference
apiGroup: Models
order: 206
---

## Overview

AxoSimLite aliases AdaptiveSupportP4Surrogate. Route features have shape (morphologies, input_dim, route_feature_dim). The Lite neuron forecasts four native outputs from preceding input blocks; sequence losses should mask the first four causal padding positions. SupportP4Config requires positive dimensions, patch_size=4, output_dim=2, and at least one morphology ID.

Source revision: `306a51ed950b`. [Public export index](/api/).

<section class="api-symbol" id="support-surrogate-supportp4config">

## SupportP4Config

<div class="api-signature">

```python
axosim.support_surrogate.SupportP4Config(input_dim: int = 1278, route_feature_dim: int = 118, token_dim: int = 58, state_dim: int = 16, patch_size: int = 4, output_dim: int = 2, morphology_ids: tuple[str, ...] = (), behavior_adaptation: bool = True)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L13-L38)

</div>

Trainable low-order support recurrence at exact P4 cadence.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>input_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=1278.</span> Native input-channel count.</dd>
<dt><code>route_feature_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=118.</span> Width of aggregated route features.</dd>
<dt><code>token_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=58.</span> Width of each encoded P4 token.</dd>
<dt><code>state_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=16.</span> Temporal state width.</dd>
<dt><code>patch_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=4.</span> Native timesteps represented by one block.</dd>
<dt><code>output_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=2.</span> Readout-channel count; Lite requires two.</dd>
<dt><code>morphology_ids</code> <span class="api-type">tuple[str, ...]</span></dt>
<dd><span class="api-default">default=().</span> Ordered morphology identity vocabulary.</dd>
<dt><code>behavior_adaptation</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=True.</span> Enable the learned behavior adaptation bank.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="support-surrogate-adaptivesupportp4surrogate">

## AdaptiveSupportP4Surrogate

<div class="api-signature">

```python
axosim.support_surrogate.AdaptiveSupportP4Surrogate(config: SupportP4Config, route_features: torch.Tensor)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L41-L535)

</div>

Learned support dynamics with compiled neuron adaptation.

Bases: `nn.Module`.

route_features must match (len(config.morphology_ids),config.input_dim,config.route_feature_dim). They are cloned as a fixed floating-point buffer. Runtime cache width is 2*token_dim+3*state_dim+2*(patch_size*output_dim).

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>config</code> <span class="api-type">SupportP4Config</span></dt>
<dd><span class="api-default">required.</span> Model configuration; use the defaults and constraints documented for its configuration class.</dd>
<dt><code>route_features</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Fixed morphology-conditioned route-feature tensor.</dd>
</dl>

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="support-surrogate-adaptivesupportp4surrogate-patch-size"><code>AdaptiveSupportP4Surrogate.patch_size: int</code></dt>
<dd>Native timesteps represented by one forecast block. <a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L118-L119">Source</a></dd>
<dt id="support-surrogate-adaptivesupportp4surrogate-gate-feature-dim"><code>AdaptiveSupportP4Surrogate.gate_feature_dim: int</code></dt>
<dd>Width of the concatenated token and state gate features. <a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L122-L123">Source</a></dd>
<dt id="support-surrogate-adaptivesupportp4surrogate-runtime-coefficient-slices"><code>AdaptiveSupportP4Surrogate.runtime_coefficient_slices: dict[str, slice]</code></dt>
<dd>Named packed slices of the direct deployed adaptation coefficients. <a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L212-L248">Source</a></dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#support-surrogate-adaptivesupportp4surrogate-reset-parameters"><code>AdaptiveSupportP4Surrogate.reset_parameters()</code></a></li>
<li><a href="#support-surrogate-adaptivesupportp4surrogate-aggregate-inputs"><code>AdaptiveSupportP4Surrogate.aggregate_inputs()</code></a></li>
<li><a href="#support-surrogate-adaptivesupportp4surrogate-compile-adaptation"><code>AdaptiveSupportP4Surrogate.compile_adaptation()</code></a></li>
<li><a href="#support-surrogate-adaptivesupportp4surrogate-initial-state"><code>AdaptiveSupportP4Surrogate.initial_state()</code></a></li>
<li><a href="#support-surrogate-adaptivesupportp4surrogate-step-token"><code>AdaptiveSupportP4Surrogate.step_token()</code></a></li>
<li><a href="#support-surrogate-adaptivesupportp4surrogate-step-p4"><code>AdaptiveSupportP4Surrogate.step_p4()</code></a></li>
<li><a href="#support-surrogate-adaptivesupportp4surrogate-forward-feature-summaries"><code>AdaptiveSupportP4Surrogate.forward_feature_summaries()</code></a></li>
<li><a href="#support-surrogate-adaptivesupportp4surrogate-forward-runtime-coefficients"><code>AdaptiveSupportP4Surrogate.forward_runtime_coefficients()</code></a></li>
<li><a href="#support-surrogate-adaptivesupportp4surrogate-forward-with-gate-features"><code>AdaptiveSupportP4Surrogate.forward_with_gate_features()</code></a></li>
<li><a href="#support-surrogate-adaptivesupportp4surrogate-forward"><code>AdaptiveSupportP4Surrogate.forward()</code></a></li>
</ul>

<section class="api-method" id="support-surrogate-adaptivesupportp4surrogate-reset-parameters">

### AdaptiveSupportP4Surrogate.reset_parameters

<div class="api-signature">

```python
axosim.support_surrogate.AdaptiveSupportP4Surrogate.reset_parameters() -> None
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L135-L149)

</div>

Initialize the model's learned parameters.

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">None</span></dt>
<dd>No return value.</dd>
</dl>

</section>

<section class="api-method" id="support-surrogate-adaptivesupportp4surrogate-aggregate-inputs">

### AdaptiveSupportP4Surrogate.aggregate_inputs

<div class="api-signature">

```python
axosim.support_surrogate.AdaptiveSupportP4Surrogate.aggregate_inputs(inputs: torch.Tensor, *, morphology_indices: torch.Tensor) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L151-L172)

</div>

Project input histories through morphology-conditioned route features.

inputs is (B,T,input_dim), and morphology_indices is integer (B,). Selects each item's route feature bank and returns feature summaries (B,T,route_feature_dim).

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>inputs</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Native input traces or the input tensor supplied to this operation.</dd>
<dt><code>morphology_indices</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Integer class assignments into the model&#x27;s ordered morphology vocabulary; one per batch item or persistent neuron.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>summaries</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Morphology-routed features (batch,time,route_feature_dim).</dd>
</dl>

</section>

<section class="api-method" id="support-surrogate-adaptivesupportp4surrogate-compile-adaptation">

### AdaptiveSupportP4Surrogate.compile_adaptation

<div class="api-signature">

```python
axosim.support_surrogate.AdaptiveSupportP4Surrogate.compile_adaptation(behavior_parameters: torch.Tensor) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L174-L186)

</div>

Project logical behavior rows into deployed runtime coefficients.

behavior_parameters is (B,behavior_parameter_count). Returns compiled coefficients (B,cache_width). Raises ValueError if the configuration disables the adaptation compiler or the width is incompatible.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>behavior_parameters</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Logical behavior coefficients to compile into the model&#x27;s deployed coefficient width.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>coefficients</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Compiled adaptation coefficients (batch,cache_width).</dd>
</dl>

</section>

<section class="api-method" id="support-surrogate-adaptivesupportp4surrogate-initial-state">

### AdaptiveSupportP4Surrogate.initial_state

<div class="api-signature">

```python
axosim.support_surrogate.AdaptiveSupportP4Surrogate.initial_state(batch_size: int, *, device: torch.device, dtype: torch.dtype) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L188-L200)

</div>

Allocate the initial temporal state.

Allocates a zero state with shape (batch_size,state_dim) on the requested device/dtype.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>batch_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Examples processed per batch.</dd>
<dt><code>device</code> <span class="api-type">torch.device</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Execution or allocation device.</dd>
<dt><code>dtype</code> <span class="api-type">torch.dtype</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Floating-point execution or allocation dtype.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>state</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Zero tensor (batch_size,state_dim) on the selected device and dtype.</dd>
</dl>

</section>

<section class="api-method" id="support-surrogate-adaptivesupportp4surrogate-step-token">

### AdaptiveSupportP4Surrogate.step_token

<div class="api-signature">

```python
axosim.support_surrogate.AdaptiveSupportP4Surrogate.step_token(token: torch.Tensor, state: torch.Tensor, *, adaptation_cache: torch.Tensor | None) -> tuple[torch.Tensor, torch.Tensor]
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L250-L312)

</div>

Advance the support recurrence and decode one four-step forecast.

token is (B,token_dim), state is (B,state_dim), and optional adaptation_cache is (B,cache_width). Returns (forecast,next_state) with shapes (B,4,2) and (B,state_dim). This low-level step returns the decoded forecast directly.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>token</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> One encoded P4 token.</dd>
<dt><code>state</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Temporal state returned by the matching initial-state or allocation method.</dd>
<dt><code>adaptation_cache</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Compiled behavior coefficients; use the declared cache width for the neuron model.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>forecast</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Decoded next-block prediction (batch,4,2).</dd>
<dt><code>state</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Updated recurrent state (batch,state_dim).</dd>
</dl>

</section>

<section class="api-method" id="support-surrogate-adaptivesupportp4surrogate-step-p4">

### AdaptiveSupportP4Surrogate.step_p4

<div class="api-signature">

```python
axosim.support_surrogate.AdaptiveSupportP4Surrogate.step_p4(feature_patch: torch.Tensor, state: torch.Tensor, *, behavior_parameters: torch.Tensor | None=None, adaptation_cache: torch.Tensor | None=None) -> tuple[torch.Tensor, torch.Tensor]
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L314-L342)

</div>

Encode a four-step feature patch and advance the support recurrence.

feature_patch is (B,4,route_feature_dim) and state is (B,state_dim). Supply either logical behavior_parameters or compiled adaptation_cache. Returns (forecast,next_state) with shapes (B,4,2) and (B,state_dim).

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>feature_patch</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Four native timesteps of routed features to encode as one token.</dd>
<dt><code>state</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Temporal state returned by the matching initial-state or allocation method.</dd>
<dt><code>behavior_parameters</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Logical behavior coefficients to compile into the model&#x27;s deployed coefficient width.</dd>
<dt><code>adaptation_cache</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Compiled behavior coefficients; use the declared cache width for the neuron model.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>forecast</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Decoded next-block prediction (batch,4,2).</dd>
<dt><code>state</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Updated recurrent state (batch,state_dim).</dd>
</dl>

</section>

<section class="api-method" id="support-surrogate-adaptivesupportp4surrogate-forward-feature-summaries">

### AdaptiveSupportP4Surrogate.forward_feature_summaries

<div class="api-signature">

```python
axosim.support_surrogate.AdaptiveSupportP4Surrogate.forward_feature_summaries(summaries: torch.Tensor, *, morphology_indices: torch.Tensor | None=None, behavior_parameters: torch.Tensor | None=None) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L453-L469)

</div>

summaries is (B,T,route_feature_dim), with T>0. Select logical adaptation by morphology_indices or supply behavior_parameters when configured. Returns (B,T,2) with four initial causal padding positions.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>summaries</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Morphology-routed input-feature summaries.</dd>
<dt><code>morphology_indices</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Integer class assignments into the model&#x27;s ordered morphology vocabulary; one per batch item or persistent neuron.</dd>
<dt><code>behavior_parameters</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Logical behavior coefficients to compile into the model&#x27;s deployed coefficient width.</dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

<section class="api-method" id="support-surrogate-adaptivesupportp4surrogate-forward-runtime-coefficients">

### AdaptiveSupportP4Surrogate.forward_runtime_coefficients

<div class="api-signature">

```python
axosim.support_surrogate.AdaptiveSupportP4Surrogate.forward_runtime_coefficients(summaries: torch.Tensor, *, runtime_coefficients: torch.Tensor) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L471-L489)

</div>

Run with direct deployed coefficients instead of a compiler.

summaries is (B,T,route_feature_dim), and runtime_coefficients must be (B,cache_width). Bypasses the logical adaptation compiler and returns (B,T,2) with the same causal padding as the summary sequence path.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>summaries</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Morphology-routed input-feature summaries.</dd>
<dt><code>runtime_coefficients</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Direct deployed adaptation coefficients, with shape (batch, cache_width).</dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

<section class="api-method" id="support-surrogate-adaptivesupportp4surrogate-forward-with-gate-features">

### AdaptiveSupportP4Surrogate.forward_with_gate_features

<div class="api-signature">

```python
axosim.support_surrogate.AdaptiveSupportP4Surrogate.forward_with_gate_features(inputs: torch.Tensor, *, morphology_indices: torch.Tensor | None=None, behavior_parameters: torch.Tensor | None=None) -> tuple[torch.Tensor, torch.Tensor]
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L491-L516)

</div>

Return predictions and their existing causal token/state values.

inputs is (B,T,input_dim); morphology_indices is required. Returns (predictions,gate_features) with shapes (B,T,2) and (B,floor(T/4),token_dim+state_dim). Gate features are shifted causally by one block, and their first block is zero.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>inputs</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Native input traces or the input tensor supplied to this operation.</dd>
<dt><code>morphology_indices</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Integer class assignments into the model&#x27;s ordered morphology vocabulary; one per batch item or persistent neuron.</dd>
<dt><code>behavior_parameters</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Logical behavior coefficients to compile into the model&#x27;s deployed coefficient width.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Native output trace (batch,time,2).</dd>
<dt><code>gate_features</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Causally shifted token/state features (batch,floor(time/4),token_dim+state_dim), with a zero first block.</dd>
</dl>

</section>

<section class="api-method" id="support-surrogate-adaptivesupportp4surrogate-forward">

### AdaptiveSupportP4Surrogate.forward

<div class="api-signature">

```python
axosim.support_surrogate.AdaptiveSupportP4Surrogate.forward(inputs: torch.Tensor, *, morphology_indices: torch.Tensor | None=None, behavior_parameters: torch.Tensor | None=None) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L518-L535)

</div>

Predict native spike and soma outputs for the supplied sequence.

inputs is (batch,native_steps,input_dim), with one morphology index per batch item where required. Return shape is (batch,native_steps,2). Mask the first four causal padding positions.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>inputs</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Native input traces or the input tensor supplied to this operation.</dd>
<dt><code>morphology_indices</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Integer class assignments into the model&#x27;s ordered morphology vocabulary; one per batch item or persistent neuron.</dd>
<dt><code>behavior_parameters</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Logical behavior coefficients to compile into the model&#x27;s deployed coefficient width.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Spike-logit and soma-target channels in the tensor shape specified above.</dd>
</dl>

</section>

</section>
