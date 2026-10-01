---
title: Branch-ELM compatibility
description: Signatures, parameters, return contracts, and source for branch-elm compatibility.
section: API reference
apiGroup: Compatibility
order: 208
---

## Overview

BranchELM and BranchELMConfig provide the baseline and checkpoint-compatible branched neuron implementation. Inputs use (batch, time, input_channels); the standard two-channel readout contains a spike logit and a soma target coordinate.

Source revision: `856207f6de56`. [Public export index](/api/).

<section class="api-symbol" id="model-branchelmconfig">

## BranchELMConfig

<div class="api-signature">

```python
axosim.model.BranchELMConfig(input_dim: int = 1278, memory_units: int = 30, num_branches: int = 32, hidden_units: int = 64, synapse_decay: float = 0.85, memory_decay: float = 0.9)
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/model.py#L10-L20)

</div>

Dimensions and decay constants for the branched recurrent neuron.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>input_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=1278.</span> Native input-channel count.</dd>
<dt><code>memory_units</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=30.</span> Width of the recurrent memory state.</dd>
<dt><code>num_branches</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=32.</span> Number of branched input features.</dd>
<dt><code>hidden_units</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=64.</span> Width of the hidden feature layer.</dd>
<dt><code>synapse_decay</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.85.</span> Decay coefficient of the synaptic trace.</dd>
<dt><code>memory_decay</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.9.</span> Decay coefficient of recurrent memory.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#model-branchelmconfig-branch-elm-30"><code>BranchELMConfig.branch_elm_30()</code></a></li>
</ul>

<section class="api-method" id="model-branchelmconfig-branch-elm-30">

### BranchELMConfig.branch_elm_30

<div class="api-signature">

```python
@classmethod
axosim.model.BranchELMConfig.branch_elm_30(*, input_dim: int=1278, num_branches: int=32) -> 'BranchELMConfig'
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/model.py#L19-L20)

</div>

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>input_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=1278.</span> Native input-channel count.</dd>
<dt><code>num_branches</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=32.</span> Number of branched input features.</dd>
</dl>

<p class="api-label">Returns</p>

`'BranchELMConfig'`

</section>

</section>

<section class="api-symbol" id="model-branchelm">

## BranchELM

<div class="api-signature">

```python
axosim.model.BranchELM(config: BranchELMConfig)
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/model.py#L23-L74)

</div>

Branch-factorized recurrent surrogate with spike and soma outputs.

Bases: `nn.Module`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>config</code> <span class="api-type">BranchELMConfig</span></dt>
<dd><span class="api-default">required.</span> Model configuration; use the defaults and constraints documented for its configuration class.</dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#model-branchelm-forward"><code>BranchELM.forward()</code></a></li>
<li><a href="#model-branchelm-parameter-count"><code>BranchELM.parameter_count()</code></a></li>
</ul>

<section class="api-method" id="model-branchelm-forward">

### BranchELM.forward

<div class="api-signature">

```python
axosim.model.BranchELM.forward(x: torch.Tensor) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/model.py#L48-L71)

</div>

Predict native spike and soma outputs for the supplied sequence.

x must be (B,T,config.input_dim). Returns (B,T,2), with one spike logit and one soma target coordinate per step. Synaptic and memory states start at zero for each call.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>x</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Input tensor for the full-sequence or streaming operation.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Spike-logit and soma-target channels in the tensor shape specified above.</dd>
</dl>

</section>

<section class="api-method" id="model-branchelm-parameter-count">

### BranchELM.parameter_count

<div class="api-signature">

```python
axosim.model.BranchELM.parameter_count() -> int
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/model.py#L73-L74)

</div>

Return the count of trainable parameters.

<p class="api-label">Returns</p>

`int`

</section>

</section>
